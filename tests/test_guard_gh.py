"""Contract tests for plugins/github-agent/hooks/guard_gh.py: the shell forms it promises to catch."""

import importlib.util
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "plugins/github-agent/hooks/guard_gh.py"
spec = importlib.util.spec_from_file_location("guard_gh", HOOK)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)

ROUTES = ["github.com/acme/*"]


# A pre-commit hook exports GIT_DIR and friends: without this, git would act on this repo.
CLEAN_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def repo_dir(root, name, remote):
    path = Path(root) / name
    path.mkdir()
    subprocess.run(["git", "init", "-q", str(path)], check=True, env=CLEAN_ENV)
    subprocess.run(["git", "-C", str(path), "remote", "add", "origin", remote], check=True, env=CLEAN_ENV)
    return str(path)


class Guard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.covered = repo_dir(cls.tmp.name, "covered", "git@github.com:acme/app.git")
        cls.other = repo_dir(cls.tmp.name, "other", "https://github.com/someone/lib.git")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def decide(self, command, cwd=None, tool="Bash", routes=ROUTES):
        payload = {"tool_name": tool, "tool_input": {"command": command}, "cwd": cwd or self.covered}
        return guard.decide(payload, load_routes=lambda: routes)

    def assertDenied(self, command, **kw):
        self.assertIsNotNone(self.decide(command, **kw), command)

    def assertAllowed(self, command, **kw):
        self.assertIsNone(self.decide(command, **kw), command)

    def test_plain_gh_on_covered_repo(self):
        for c in ["gh pr list", "git push && gh pr create --fill", "echo $(gh pr view 1)",
                  "bash -c 'gh issue list'", "env FOO=1 gh pr list", "gh pr list | jq .",
                  ["bash", "-lc", "gh pr list"], "gh extension exec foo"]:
            self.assertDenied(c)

    def test_target_resolution(self):
        self.assertDenied("gh pr list --repo acme/app", cwd=self.other)
        self.assertDenied("gh pr list -Racme/app", cwd=self.other)
        self.assertDenied("GH_REPO=acme/app gh pr list", cwd=self.other)
        self.assertDenied("gh pr view https://github.com/acme/app/pull/3", cwd=self.other)
        self.assertDenied("gh api repos/acme/app/issues", cwd=self.other)
        self.assertDenied(f"cd {self.covered} && gh pr list", cwd=self.other)
        self.assertAllowed("gh pr view https://github.com/someone/lib/pull/3")
        self.assertAllowed("gh pr list --repo someone/lib")
        self.assertAllowed("gh pr list", cwd=self.other)
        self.assertAllowed(f"cd {self.other} && gh pr list")

    def test_bot_and_local_commands(self):
        for c in ["gh app-auth exec --repo github.com/acme/app -- gh pr list",
                  "gh app-auth exec -- gh pr list | jq .", "gh app-auth test --repo github.com/acme/app",
                  "gh app-auth list --verify-keys", "gh --version", "gh auth status", "gh pr list --help",
                  "gh extension list", "echo 'gh pr list'", "git log --grep gh"]:
            self.assertAllowed(c)

    def test_secrets_always_refused(self):
        for c in ["gh auth status --show-token", "gh auth token", "gh auth setup-git", "gh auth login",
                  "gh app-auth token --app-id 1 --repo github.com/acme/app", "gh app-auth gitconfig --sync",
                  "gh app-auth config", "gh app-auth exec --repo github.com/acme/app -- gh auth token",
                  "GITHUB_AGENT_AS_DEVELOPER=1 gh auth token", "gh app-auth frobnicate"]:
            self.assertDenied(c)

    def test_escape_lifts_identity_only(self):
        self.assertAllowed("GITHUB_AGENT_AS_DEVELOPER=1 gh pr comment 1 -b hi")

    def test_mcp(self):
        self.assertDenied("", tool="mcp__github__create_pull_request")
        self.assertAllowed("", tool="mcp__claude_ai_Linear__list_issues")

    def test_inactive_without_routes(self):
        self.assertAllowed("gh pr list", routes=[])
        self.assertAllowed("gh auth token", routes=[])
        self.assertAllowed("", tool="mcp__github__create_pull_request", routes=[])

    def test_unreadable_config_is_refused(self):
        def broken():
            raise guard.Unreadable("boom")
        payload = {"tool_name": "Bash", "tool_input": {"command": "gh pr list"}, "cwd": self.covered}
        self.assertIn("cannot be read", guard.decide(payload, load_routes=broken))


class Config(unittest.TestCase):
    def test_block_and_inline_lists(self):
        block = "version: '1.0'\ngithub_apps:\n  - name: A\n    patterns:\n      - github.com/Acme/*\n    priority: 5\npats: null\n"
        inline = 'github_apps:\n  - name: A\n    patterns: ["github.com/acme/app", "github.com/beta/*"]\n'
        self.assertEqual(guard.parse_patterns(block), ["github.com/acme/*"])
        self.assertEqual(guard.parse_patterns(inline), ["github.com/acme/app", "github.com/beta/*"])

    def test_pat_patterns_are_not_routes(self):
        text = "github_apps: []\npats:\n  - name: P\n    patterns:\n      - github.com/acme/*\n"
        self.assertEqual(guard.parse_patterns(text), [])


if __name__ == "__main__":
    unittest.main()
