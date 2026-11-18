---
name: github-agent
description: Act on GitHub as the agents' bot identity through gh-app-auth. Use before any `gh` command or GitHub API call, such as opening, updating or commenting on a PR, reading reviews, checks or CI logs, or rerunning a workflow.
---

Every GitHub action you take runs under the **bot identity**: the GitHub App the developer set up with `/setup-github-agent`, reached through [gh-app-auth](https://github.com/AmadeusITGroup/gh-app-auth). The developer's own account stays theirs: what the bot cannot do is reported, never redone under the developer's account.

## 1. Resolve the repository

Take the repository from `git remote get-url origin` (or the remote the work targets) and write it as `github.com/OWNER/NAME`. The repository is **covered** when one of the routes in `gh app-auth list` matches it (`github.com/OWNER/*` or `github.com/OWNER/NAME`).

## 2. Preflight

Once per repository per session, run checks 3 and 4 of [the setup checks](../setup-github-agent/references/verify.md) on it: `gh app-auth test` passes and the viewer login ends in `[bot]`.

When the repository is not covered, gh-app-auth is missing, or a check fails: stop the GitHub part of the task, tell the user what failed, and ask them to run `/setup-github-agent`. Local work (code, commits, tests) carries on.

## 3. Run gh as the bot

Prefix every `gh` command with the route:

```bash
gh app-auth exec --repo github.com/OWNER/NAME -- gh pr view 42 --json title,state
```

- One `gh` command per `exec`. Pipes and filters go outside it: `gh app-auth exec --repo … -- gh api … | jq …`.
- Pass `--repo` every time, also inside the repository: worktrees and other remotes then resolve to the same route.
- A GitHub MCP server or other tool holding the developer's token acts as the developer: reach GitHub through `gh` here instead.
- Keep tokens out of sight: authenticate only through `exec`, never through `gh app-auth token`, `gh auth` or a token in the environment.

## 4. Keep Git as it is

Commit and push with plain `git`: pushes go through the developer's SSH key and commits keep the configured author. Leave remotes, credential helpers and `user.name`/`user.email` unchanged. Push the branch before `gh pr create` so the bot finds it on GitHub.

## 5. When the bot is refused

`Resource not accessible by integration` (HTTP 403) means the App lacks a permission or the installation does not reach the repository; `Bad credentials` on a command without `exec` means it bypassed the bot. Report the command and the error, then ask the user to choose: extend the App with `/setup-github-agent`, do it themselves, or have you run it under their own account this once. Act on their account only after that explicit answer: prefix that one command with `GITHUB_AGENT_AS_DEVELOPER=1` so the plugin's hook lets it through, and say in the result which identity acted.
