---
name: github-agent
description: Act on GitHub as the agents' bot identity through gh-app-auth. Use before any `gh` command or API call that reads or writes GitHub, such as a PR, a review, checks and CI logs, or a workflow run.
---

GitHub actions run under the **bot identity** by default: the GitHub App the developer set up with `/setup-github-agent`, reached through [gh-app-auth](https://github.com/AmadeusITGroup/gh-app-auth). The developer's own account acts only after their explicit answer (step 5).

Local `gh` commands touch no account and run plain: `gh --version`, `--help`, `gh auth status`, `gh extension list`, and `gh app-auth list` or `test`.

## 1. Resolve the repository

Take the repository from `git remote get-url origin` (or the remote the work targets) and write it as `github.com/OWNER/NAME`. It is **covered** when one of the app routes in `gh app-auth list` matches it (`github.com/OWNER/*` or `github.com/OWNER/NAME`).

## 2. Preflight

Once per repository per session, and again after any change to the gh-app-auth configuration, run checks 2 to 4 of [the setup checks](../setup-github-agent/references/verify.md) on it. It passes when the key is accessible, no PAT shares the route, `gh app-auth test` passes, and the viewer login is the configured App's `SLUG[bot]`.

When the repository is not covered or a check fails, hold the GitHub part of the task and offer the user the choices of step 5. Local work (code, commits, tests) carries on.

## 3. Run gh as the bot

Prefix every `gh` command that reaches GitHub with the route:

```bash
gh app-auth exec --repo github.com/OWNER/NAME -- gh pr view 42 --json title,state
```

- One `gh` command per `exec`. Pipes and filters go outside it: `gh app-auth exec --repo … -- gh api … | jq …`.
- Pass `--repo` every time, also inside the repository: worktrees and other remotes then resolve to the same route.
- Reach GitHub through this `gh`, also where a GitHub MCP tool would do: this plugin cannot tell which identity an MCP server acts under.
- Authenticate through `exec` alone: the token stays inside the child process.
- A keyring error inside a sandbox (`secret not found`, key `Not found`) means the sandbox cannot reach the host keyring, not that the key is gone: rerun that `exec` outside the sandbox through your environment's escalation, and keep running `gh app-auth` there for the session.

## 4. Keep Git as it is

Commit and push with plain `git`: pushes go through the developer's SSH key and commits keep the configured author. Push the branch before `gh pr create` so the bot finds it on GitHub.

## 5. When the bot cannot act

A preflight failure, `Resource not accessible by integration` (HTTP 403: the App lacks a permission or its installation misses the repository), or the plugin's hook refusing a command: report the command and the error, then ask the user to choose:

- extend or repair the App with `/setup-github-agent`;
- do it themselves;
- have you run that one command under their account.

On the third answer, prefix that command with `GITHUB_AGENT_AS_DEVELOPER=1` so the hook lets it through, and say in the result which identity acted. The prefix lifts the identity check only: commands that print or reroute credentials stay refused.
