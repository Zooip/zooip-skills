#!/usr/bin/env python3
"""Build and check the plugins of this repo. Standard library only.

  python3 scripts/plugins.py build            regenerate every manifest from the *.meta.json sources
  python3 scripts/plugins.py check [--base R] run every check; R is the ref versions are compared to
                                              (default: the merge-base with origin/main)
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ROOT / "plugins"

FRONTMATTER_KEYS = {"name", "description", "disable-model-invocation", "argument-hint", "allowed-tools", "license", "metadata"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
FENCE_RE = re.compile(r"^(```|~~~).*?^\1", re.S | re.M)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def dumps(data):
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


# ---------------------------------------------------------------- build


def manifests():
    """Every generated file, as {path: content}, computed from the meta sources."""
    meta = load(ROOT / "marketplace.meta.json")
    author = meta["owner"]
    out = {}
    claude_entries, codex_entries = [], []
    for name in meta["plugins"]:
        p = load(PLUGINS / name / "plugin.meta.json")
        base = {
            "name": name,
            "version": p["version"],
            "description": p["description"],
            "author": author,
            "repository": meta["repository"],
            "license": meta["license"],
            "keywords": p["keywords"],
        }
        out[PLUGINS / name / ".claude-plugin" / "plugin.json"] = dumps(base)
        out[PLUGINS / name / ".codex-plugin" / "plugin.json"] = dumps({
            **base,
            "skills": "./skills/",
            "interface": {
                "displayName": p["displayName"],
                "shortDescription": p["shortDescription"],
                "developerName": author["name"],
                "category": meta["category"]["codex"],
            },
        })
        claude_entries.append({
            "name": name,
            "source": f"./plugins/{name}",
            "description": p["description"],
            "category": meta["category"]["claude"],
        })
        codex_entries.append({
            "name": name,
            "source": {"source": "local", "path": f"./plugins/{name}"},
            "policy": {"installation": "AVAILABLE"},
            "category": meta["category"]["codex"],
        })
    out[ROOT / ".claude-plugin" / "marketplace.json"] = dumps({
        "name": meta["name"],
        "owner": author,
        "description": meta["description"],
        "plugins": claude_entries,
    })
    out[ROOT / ".agents" / "plugins" / "marketplace.json"] = dumps({
        "name": meta["name"],
        "interface": {"displayName": meta["displayName"]},
        "plugins": codex_entries,
    })
    return out


def build():
    for path, content in manifests().items():
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            path.write_text(content, encoding="utf-8")
            print(f"wrote {path.relative_to(ROOT)}")
    print("manifests up to date")


# ---------------------------------------------------------------- check


class Report:
    def __init__(self):
        self.errors = []

    def error(self, path, message):
        where = path.relative_to(ROOT) if isinstance(path, Path) else path
        self.errors.append(f"{where}: {message}")


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def frontmatter(text):
    """Parse the flat `key: value` frontmatter a SKILL.md carries. None if absent."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        m = re.match(r"^([a-z-]+):\s*(.*)$", line)
        if not m:
            fields.setdefault("__invalid__", []).append(line)
            continue
        fields[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return fields


def openai_yaml(text):
    """Read the three fields this repo uses from agents/openai.yaml."""
    fields = {}
    section = None
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" "):
            section = line.rstrip(":").strip()
            continue
        m = re.match(r"^\s+([a-z_]+):\s*(.*)$", line)
        if m:
            fields[f"{section}.{m.group(1)}"] = m.group(2).strip().strip('"').strip("'")
    return fields


def check_generated(r):
    for path, content in manifests().items():
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            r.error(path, "out of date; run `python3 scripts/plugins.py build`")


def check_plugins(r):
    meta = load(ROOT / "marketplace.meta.json")
    listed = meta["plugins"]
    on_disk = sorted(d.name for d in PLUGINS.iterdir() if d.is_dir())
    for name in sorted(set(on_disk) - set(listed)):
        r.error(PLUGINS / name, "plugin folder missing from `plugins` in marketplace.meta.json")
    for name in sorted(set(listed) - set(on_disk)):
        r.error(ROOT / "marketplace.meta.json", f"lists `{name}`, which has no plugins/{name}/ folder")
    for name in listed:
        d = PLUGINS / name
        if not NAME_RE.match(name):
            r.error(d, "plugin names are kebab-case")
        meta_path = d / "plugin.meta.json"
        if not meta_path.exists():
            r.error(meta_path, "missing")
            continue
        p = load(meta_path)
        for key in ("version", "description", "keywords", "displayName", "shortDescription"):
            if key not in p:
                r.error(meta_path, f"missing `{key}`")
        if not SEMVER_RE.match(str(p.get("version", ""))):
            r.error(meta_path, "`version` must be MAJOR.MINOR.PATCH")
        if not (d / "skills").is_dir() or not any((d / "skills").glob("*/SKILL.md")):
            r.error(d, "a plugin ships at least one skill in skills/<skill>/SKILL.md")


def check_skills(r):
    seen = {}
    for skill_md in sorted(PLUGINS.glob("*/skills/*/SKILL.md")):
        d = skill_md.parent
        fm = frontmatter(skill_md.read_text(encoding="utf-8"))
        if fm is None:
            r.error(skill_md, "no `---` frontmatter")
            continue
        for line in fm.pop("__invalid__", []):
            r.error(skill_md, f"frontmatter line is not `key: value` on one line: {line!r}")
        for key in sorted(set(fm) - FRONTMATTER_KEYS):
            r.error(skill_md, f"unknown frontmatter key `{key}`")
        if fm.get("name") != d.name:
            r.error(skill_md, f"`name` must equal the folder name `{d.name}`")
        if not NAME_RE.match(d.name) or len(d.name) > 64:
            r.error(d, "skill names are kebab-case, 64 characters at most")
        description = fm.get("description", "")
        if not description:
            r.error(skill_md, "missing `description`")
        elif len(description) > 1024:
            r.error(skill_md, f"`description` is {len(description)} characters, 1024 at most")
        if d.name in seen:
            r.error(skill_md, f"skill name already used by {seen[d.name].relative_to(ROOT)}")
        seen[d.name] = skill_md

        user_invoked = fm.get("disable-model-invocation") == "true"
        yaml_path = d / "agents" / "openai.yaml"
        if not yaml_path.exists():
            r.error(yaml_path, "missing (Codex display name, and the invocation policy)")
            continue
        y = openai_yaml(yaml_path.read_text(encoding="utf-8"))
        for key in ("interface.display_name", "interface.short_description"):
            if not y.get(key):
                r.error(yaml_path, f"missing `{key}`")
        implicit = y.get("policy.allow_implicit_invocation", "true")
        if user_invoked and implicit != "false":
            r.error(yaml_path, "user-invoked skill: set `policy.allow_implicit_invocation: false`")
        if not user_invoked and implicit == "false":
            r.error(yaml_path, "model-invoked skill: drop the `policy` block, or set `disable-model-invocation: true`")


def check_links(r):
    files = [ROOT / f for f in git("ls-files", "--cached", "--others", "--exclude-standard", "*.md").stdout.split()]
    for md in files:
        if not md.exists():
            continue
        text = FENCE_RE.sub("", md.read_text(encoding="utf-8"))
        text = re.sub(r"`[^`\n]*`", "", text)
        rel = md.relative_to(ROOT)
        boundary = ROOT / rel.parts[0] / rel.parts[1] if rel.parts[0] == "plugins" else ROOT
        for target in LINK_RE.findall(text):
            if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
                continue
            path = (md.parent / target.split("#")[0]).resolve()
            if not path.exists():
                r.error(md, f"broken link `{target}`")
            elif boundary != ROOT and not path.is_relative_to(boundary):
                r.error(md, f"link `{target}` leaves its plugin: an installed plugin only has its own folder")


def check_readme(r):
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for name in load(ROOT / "marketplace.meta.json")["plugins"]:
        if f"`{name}`" not in readme:
            r.error(ROOT / "README.md", f"plugin `{name}` is not mentioned")
        for skill_md in sorted((PLUGINS / name / "skills").glob("*/SKILL.md")):
            link = skill_md.relative_to(ROOT).as_posix()
            if f"]({link})" not in readme:
                r.error(ROOT / "README.md", f"no link to {link}")


def plugin_changed(base, name):
    folder = f"plugins/{name}"
    if git("diff", "--quiet", base, "--", folder).returncode != 0:
        return True
    return bool(git("ls-files", "--others", "--exclude-standard", folder).stdout.strip())


def base_version(base, name):
    shown = git("show", f"{base}:plugins/{name}/plugin.meta.json")
    if shown.returncode != 0:
        return None
    return json.loads(shown.stdout).get("version")


def check_versions(r, base_ref):
    if base_ref is None:
        upstream = git("rev-parse", "--verify", "--quiet", "origin/main")
        if upstream.returncode != 0:
            print("versions: no origin/main, skipped")
            return
        base = git("merge-base", "origin/main", "HEAD").stdout.strip()
    else:
        resolved = git("rev-parse", "--verify", "--quiet", f"{base_ref}^{{commit}}")
        if resolved.returncode != 0:
            print(f"versions: base `{base_ref}` not found, skipped")
            return
        base = git("merge-base", resolved.stdout.strip(), "HEAD").stdout.strip()
    for name in load(ROOT / "marketplace.meta.json")["plugins"]:
        meta_path = PLUGINS / name / "plugin.meta.json"
        if not meta_path.exists():
            continue
        old = base_version(base, name)
        if old is None or not plugin_changed(base, name):
            continue
        new = load(meta_path).get("version")
        if new == old:
            r.error(meta_path, f"plugins/{name}/ changed since {base[:7]} but `version` is still {old}: bump it")


def check_claude_validate(r):
    if shutil.which("claude") is None:
        print("claude plugin validate: `claude` not on PATH, skipped")
        return
    for target in [ROOT, *[PLUGINS / n for n in load(ROOT / "marketplace.meta.json")["plugins"]]]:
        res = subprocess.run(["claude", "plugin", "validate", str(target)], cwd=ROOT, capture_output=True, text=True)
        if res.returncode != 0:
            r.error(target, "`claude plugin validate` failed:\n" + (res.stdout + res.stderr).strip())


def check(base_ref):
    r = Report()
    check_generated(r)
    check_plugins(r)
    check_skills(r)
    check_links(r)
    check_readme(r)
    check_versions(r, base_ref)
    check_claude_validate(r)
    for e in r.errors:
        print(f"✘ {e}", file=sys.stderr)
    if r.errors:
        print(f"{len(r.errors)} problem(s)", file=sys.stderr)
        return 1
    print("✔ all checks passed")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build")
    c = sub.add_parser("check")
    c.add_argument("--base", help="ref plugin versions are compared to (default: merge-base with origin/main)")
    args = parser.parse_args()
    if args.command == "build":
        build()
        return 0
    return check(args.base)


if __name__ == "__main__":
    sys.exit(main())
