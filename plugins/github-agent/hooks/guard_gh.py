#!/usr/bin/env python3
"""PreToolUse guard: keep agents on the GitHub App identity.

Denies a plain `gh` command aimed at a repository a gh-app-auth route covers,
and GitHub MCP tools while any route is configured. Everything else passes.
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
# Plain gh commands that never act on GitHub as anyone.
LOCAL = {("--version",), ("version",), ("help",), ("extension",), ("auth", "status"), ("completion",)}
APP_AUTH_DENIED = {"token": "it prints a token", "gitconfig": "it routes Git pushes through the App"}


def routes():
    """Patterns of the github_apps entries in the gh-app-auth config."""
    base = os.environ.get("GH_CONFIG_DIR") or os.path.join(
        os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config"), "gh")
    path = Path(base) / "extensions" / "gh-app-auth" / "config.yml"
    try:
        lines = path.read_text().splitlines()
    except OSError:
        return []
    found, section = [], None
    for line in lines:
        if line and not line[0].isspace():
            section = line.split(":", 1)[0].strip()
            continue
        m = re.match(r"\s*-\s*[\"']?(github\.com/[^\"'\s]+)", line)
        if section == "github_apps" and m:
            found.append(m.group(1).lower())
    return found


def normalize(repo):
    """github.com/OWNER/NAME from a --repo value, a URL or a git remote."""
    repo = re.sub(r"\.git$", "", repo.strip())
    repo = re.sub(r"^(https?://|ssh://)?(git@)?", "", repo, flags=re.I)
    repo = re.sub(r"^github\.com[:/]", "github.com/", repo, flags=re.I)
    parts = [p for p in repo.split("/") if p]
    if parts and parts[0].lower() == "github.com":
        parts = parts[1:]
    return "github.com/" + "/".join(parts[:2]) if len(parts) >= 2 else None


def cwd_repo(cwd):
    try:
        url = subprocess.run(["git", "-C", cwd or ".", "remote", "get-url", "origin"],
                             capture_output=True, text=True, timeout=2).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    return normalize(url) if url.strip() else None


def segments(command):
    """Simple commands of a shell line, descending into `sh -c '…'`."""
    text = command.replace("`", " ; ").replace("\n", " ; ")
    lexer = shlex.shlex(text, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    tokens = list(lexer)
    current = []
    for tok in tokens + [";"]:
        if tok in SEPARATORS:
            if current:
                yield from expand(current)
            current = []
        else:
            current.append(tok)


ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")


def expand(words):
    """Strip assignments and wrappers (`env X=1 sudo gh …`) down to the real command."""
    env = {}
    while words:
        if ASSIGNMENT.match(words[0]):
            key, value = words[0].split("=", 1)
            env[key] = value
        elif os.path.basename(words[0]) in WRAPPERS or (words[0].startswith("-") and env.get("_wrapped")):
            env["_wrapped"] = True
        else:
            break
        words = words[1:]
    if words and os.path.basename(words[0]) in SHELLS:
        flag = next((i for i, w in enumerate(words[1:], 1)
                     if re.match(r"^-[a-zA-Z]*c[a-zA-Z]*$", w)), None)
        if flag is not None and flag + 1 < len(words):
            yield from segments(words[flag + 1])
            return
    if words:
        yield env, words


def target(args, cwd):
    for i, a in enumerate(args):
        if a in ("-R", "--repo") and i + 1 < len(args):
            return normalize(args[i + 1])
        if a.startswith("--repo="):
            return normalize(a.split("=", 1)[1])
    if args and args[0] == "api":
        for a in args[1:]:
            m = re.match(r"^/?repos/([^/\s]+)/([^/\s?]+)", a)
            if m:
                return normalize(f"{m.group(1)}/{m.group(2)}")
    return cwd_repo(cwd)


def covered(repo, patterns):
    return bool(repo) and any(fnmatch.fnmatchcase(repo.lower(), p) for p in patterns)


def check_gh(env, args, cwd, patterns):
    """Deny reason for one `gh` invocation, or None."""
    if env.get(ESCAPE) == "1":
        return None
    if args and args[0] == "app-auth":
        sub = next((a for a in args[1:] if not a.startswith("-")), "")
        if sub in APP_AUTH_DENIED:
            return f"`gh app-auth {sub}` is off limits to agents: {APP_AUTH_DENIED[sub]}."
        return None
    if any(tuple(args[:len(k)]) == k for k in LOCAL):
        return None
    repo = target(args, cwd)
    if not covered(repo, patterns):
        return None
    return (f"Plain `gh` acts as the developer, and {repo} is covered by the agents' GitHub App. "
            f"Run it as the bot: `gh app-auth exec --repo {repo} -- gh {' '.join(args[:2])} …`. "
            "Follow the github-agent skill.")


def decide(payload, patterns):
    tool = str(payload.get("tool_name") or "")
    if re.match(r"^mcp__.*github", tool, re.I):
        return ("This GitHub MCP tool acts with the developer's token. Use `gh` through "
                "`gh app-auth exec` instead, as the github-agent skill describes.")
    command = (payload.get("tool_input") or {}).get("command")
    if isinstance(command, list):
        command = " ".join(shlex.quote(str(c)) for c in command)
    if not isinstance(command, str) or not re.search(r"(^|[^\w.-])gh($|\s)", command):
        return None
    cwd = payload.get("cwd")
    try:
        parsed = list(segments(command))
    except ValueError:
        parsed = [({}, command.split())]
    for env, words in parsed:
        if os.path.basename(words[0]) == "gh":
            reason = check_gh(env, words[1:], cwd, patterns)
            if reason:
                return reason
    return None


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return
    patterns = routes()
    if not patterns:
        return
    reason = decide(payload, patterns)
    if reason:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }}))


if __name__ == "__main__":
    main()
