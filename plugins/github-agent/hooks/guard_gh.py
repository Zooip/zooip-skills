#!/usr/bin/env python3
"""PreToolUse guard: keep agents on the GitHub App identity.

A tripwire for the usual mistakes, not a security boundary: a command built at
run time (eval, a script, a variable) escapes it.

Two guards, applied to every `gh` found in a shell command:
- secrets: commands that print or reroute credentials are always refused,
  also inside `gh app-auth exec` and with the identity escape;
- identity: a plain `gh` aimed at a repository a gh-app-auth route covers is
  refused, unless the segment sets GITHUB_AGENT_AS_DEVELOPER=1.
Nothing is refused until a route is configured; then GitHub MCP tools are refused too.
Reads the hook payload on stdin; prints a deny decision or nothing.
"""

import fnmatch
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

ESCAPE = "GITHUB_AGENT_AS_DEVELOPER"
SEPARATORS = {";", "&&", "||", "|", "&", "(", ")", "|&", ";;"}
WRAPPERS = {"command", "env", "exec", "nohup", "sudo", "time", "xargs", "builtin"}
SHELLS = {"sh", "bash", "zsh", "dash"}
ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
APP_AUTH_ALLOWED = {"list", "ls", "test", "exec", "scope", "setup", "remove", "migrate", "help", "completion"}
APP_AUTH_DENIED = {
    "token": "it prints a token",
    "gitconfig": "it routes Git pushes through the App",
    "config": "it prints the configuration file; read the routes with `gh app-auth list`",
}
GH_AUTH_DENIED = "it prints or changes the developer's credentials; the developer runs it themselves"
SKILL = "Follow the github-agent skill."


class Unreadable(Exception):
    pass


# --- gh-app-auth configuration ------------------------------------------------

def config_path():
    base = os.environ.get("GH_CONFIG_DIR") or os.path.join(
        os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config"), "gh")
    return Path(base) / "extensions" / "gh-app-auth" / "config.yml"


def parse_patterns(text):
    """Route patterns of github_apps, without needing PyYAML."""
    try:
        import yaml
    except ImportError:
        yaml = None
    if yaml:
        try:
            data = yaml.safe_load(text) or {}
        except yaml.YAMLError as e:
            raise Unreadable(str(e))
        if not isinstance(data, dict):
            raise Unreadable("not a mapping")
        apps = data.get("github_apps") or []
        return [str(p).lower() for app in apps if isinstance(app, dict) for p in (app.get("patterns") or [])]
    found, section, in_patterns, keys = [], None, False, 0
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line[0].isspace():
            section, in_patterns = line.split(":", 1)[0].strip(), False
            continue
        if section != "github_apps":
            continue
        inline = re.match(r"\s*(?:-\s*)?patterns:\s*\[(.*)\]\s*$", line)
        if inline:
            keys += 1
            found += [p.strip().strip("\"'").lower() for p in inline.group(1).split(",") if p.strip()]
            in_patterns = False
        elif re.match(r"\s*(?:-\s*)?patterns:\s*$", line):
            keys, in_patterns = keys + 1, True
        elif in_patterns and re.match(r"\s*-\s*\S", line):
            found.append(line.split("-", 1)[1].strip().strip("\"'").lower())
        elif re.match(r"\s*(?:-\s*)?\w+:", line):
            in_patterns = False
    if keys and not found:
        raise Unreadable("patterns not recognised")
    return found


def routes():
    path = config_path()
    try:
        text = path.read_text()
    except FileNotFoundError:
        return []
    except OSError as e:
        raise Unreadable(str(e))
    return parse_patterns(text)


# --- repositories ---------------------------------------------------------------

def normalize(repo):
    """github.com/OWNER/NAME from OWNER/NAME, a URL or a git remote."""
    repo = re.sub(r"\.git$", "", repo.strip())
    repo = re.sub(r"^(https?://|ssh://)?(git@)?", "", repo, flags=re.I)
    repo = re.sub(r"^github\.com[:/]", "github.com/", repo, flags=re.I)
    parts = [p for p in repo.split("/") if p]
    if parts and parts[0].lower() == "github.com":
        parts = parts[1:]
    return "github.com/" + "/".join(parts[:2]) if len(parts) >= 2 else None


def cwd_repo(cwd):
    try:
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        url = subprocess.run(["git", "-C", cwd or ".", "remote", "get-url", "origin"],
                             capture_output=True, text=True, timeout=2, env=env).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    return normalize(url) if url.strip() else None


def target(args, env, cwd):
    """Repository a gh command acts on, resolved the way gh does, best effort."""
    for i, a in enumerate(args):
        if a in ("-R", "--repo") and i + 1 < len(args):
            return normalize(args[i + 1])
        if a.startswith("--repo=") or (a.startswith("-R") and len(a) > 2):
            return normalize(a.split("=", 1)[1] if "=" in a else a[2:])
    for a in args:
        m = re.match(r"^https?://github\.com/([^/\s]+)/([^/\s#?]+)", a, re.I)
        if m:
            return normalize(f"{m.group(1)}/{m.group(2)}")
    if args and args[0] == "api":
        for a in args[1:]:
            m = re.match(r"^/?repos/([^/\s]+)/([^/\s?]+)", a)
            if m:
                return normalize(f"{m.group(1)}/{m.group(2)}")
    gh_repo = env.get("GH_REPO") or os.environ.get("GH_REPO")
    if gh_repo:
        return normalize(gh_repo)
    return cwd_repo(cwd)


def covered(repo, patterns):
    return bool(repo) and any(fnmatch.fnmatchcase(repo.lower(), p) for p in patterns)


# --- shell parsing --------------------------------------------------------------

def segments(command):
    """(env, words) of each simple command, descending into `sh -c '…'`."""
    text = command.replace("`", " ; ").replace("\n", " ; ")
    lexer = shlex.shlex(text, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    current = []
    for tok in list(lexer) + [";"]:
        if tok in SEPARATORS:
            if current:
                yield from expand(current)
            current = []
        else:
            current.append(tok)


def expand(words):
    """Strip assignments and wrappers (`env X=1 sudo gh …`) down to the real command."""
    env, wrapped = {}, False
    while words:
        if ASSIGNMENT.match(words[0]):
            key, value = words[0].split("=", 1)
            env[key] = value
        elif os.path.basename(words[0]) in WRAPPERS or (wrapped and words[0].startswith("-")):
            wrapped = True
        else:
            break
        words = words[1:]
    if words and os.path.basename(words[0]) in SHELLS:
        flag = next((i for i, w in enumerate(words[1:], 1) if re.match(r"^-[a-zA-Z]*c[a-zA-Z]*$", w)), None)
        if flag is not None and flag + 1 < len(words):
            for inner_env, inner in segments(words[flag + 1]):
                yield {**env, **inner_env}, inner
            return
    if words:
        yield env, words


def parse(command):
    try:
        return list(segments(command))
    except ValueError:
        return [({}, command.split())]


# --- decisions ------------------------------------------------------------------

def secret_reason(args):
    """Why a gh command is refused whatever the identity, or None."""
    if args[:1] == ["auth"]:
        sub = args[1] if len(args) > 1 else ""
        if sub == "status" and not {"-t", "--show-token"} & set(args):
            return None
        return f"`gh auth {sub}` is off limits to agents: {GH_AUTH_DENIED}."
    if args[:1] == ["app-auth"]:
        sub = next((a for a in args[1:] if not a.startswith("-")), "help")
        if sub in APP_AUTH_DENIED:
            return f"`gh app-auth {sub}` is off limits to agents: {APP_AUTH_DENIED[sub]}."
        if sub not in APP_AUTH_ALLOWED:
            return f"`gh app-auth {sub}` is not a command agents run. {SKILL}"
        if sub == "exec" and "--" in args:
            inner = args[args.index("--") + 1:]
            for _, words in expand(inner):
                if os.path.basename(words[0]) == "gh":
                    reason = secret_reason(words[1:])
                    if reason:
                        return reason
    return None


def is_local(args):
    """Plain gh commands that never act on GitHub as anyone."""
    if not args or {"--help", "-h"} & set(args):
        return True
    if args[0] in ("--version", "version", "help", "completion"):
        return True
    if args[:2] == ["auth", "status"]:
        return True
    return args[0] == "extension" and len(args) > 1 and args[1] in ("list", "ls", "install", "upgrade", "remove")


def gh_reason(env, args, cwd, patterns):
    reason = secret_reason(args)
    if reason:
        return reason
    if args[:1] == ["app-auth"] or is_local(args) or env.get(ESCAPE) == "1":
        return None
    repo = target(args, env, cwd)
    if not covered(repo, patterns):
        return None
    shown = " ".join(args[:2])
    return (f"Plain `gh` acts as the developer, and {repo} is covered by the agents' GitHub App. "
            f"Run it as the bot: `gh app-auth exec --repo {repo} -- gh {shown} …`. {SKILL}")


def decide(payload, load_routes=routes):
    tool = str(payload.get("tool_name") or "")
    command = (payload.get("tool_input") or {}).get("command")
    is_mcp = bool(re.match(r"^mcp__.*github", tool, re.I))
    if isinstance(command, list):
        command = " ".join(shlex.quote(str(c)) for c in command)
    has_gh = isinstance(command, str) and re.search(r"(^|[^\w.-])gh($|\s)", command)
    if not is_mcp and not has_gh:
        return None
    try:
        patterns = load_routes()
    except Unreadable as e:
        return (f"The gh-app-auth configuration ({config_path()}) cannot be read ({e}), so the agents' "
                "identity cannot be checked. Ask the user to run /setup-github-agent.")
    if not patterns:
        return None
    if is_mcp:
        return ("This GitHub MCP tool acts under an identity this plugin cannot check. Use the matching "
                f"`gh` command through `gh app-auth exec` instead. {SKILL}")
    cwd = payload.get("cwd")
    for env, words in parse(command):
        if words[0] == "cd":
            dest = os.path.expanduser(words[1]) if len(words) > 1 else os.path.expanduser("~")
            cwd = os.path.normpath(os.path.join(cwd or os.getcwd(), dest))
            continue
        if os.path.basename(words[0]) != "gh":
            continue
        args = words[1:]
        reason = gh_reason(env, args, cwd, patterns)
        if reason:
            return reason
    return None


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return
    reason = decide(payload)
    if reason:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }}))


if __name__ == "__main__":
    main()
