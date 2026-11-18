# Verify a GitHub Agent setup

Every check is read-only: it writes nothing to GitHub, Git or the gh-app-auth configuration, and prints no token or key. Run them in order: a failure makes the checks below it unreliable. **Fix** names the step of [the setup skill](../SKILL.md) that repairs a failure.

Read the configuration first:

```bash
gh app-auth list --format json
```

Each entry of `github_apps` gives an `app_id`, an installation ID and its `patterns` (the **routes**); entries of `pats` are personal access tokens with their own patterns. Pick one **test repository** per route: the route's repository itself, or for `github.com/OWNER/*` a repository of that owner the developer named. `REPO` below is `OWNER/NAME`.

Run every check in the context agents will act from: a sandbox, container or remote session can read the gh-app-auth configuration yet not reach the host keyring that holds the key. A visible app whose key shows `Not found` is therefore unproven, not missing. Before treating it as missing, have the developer run in a fresh local terminal:

```bash
gh app-auth list --verify-keys
gh app-auth exec --repo github.com/REPO -- gh pr list
```

- **Fails in both contexts:** the key is missing or invalid.
- **Passes locally, fails for the agent:** the agents' context lacks keyring access; the key is fine.
- **Passes in both:** the setup is valid.

| # | Check | Command | Pass | Fix |
| -- | -- | -- | -- | -- |
| 1 | Tools | `gh --version` and `gh extension list` | `gh` runs and lists `AmadeusITGroup/gh-app-auth` | 6 |
| 2 | Key and routing | `gh app-auth list --verify-keys` and the JSON above | every app shows its key as accessible in the agents' context, and no PAT pattern matches a test repository | key missing in both contexts: 4, then 6; key reachable only locally: keyring access (6), keeping the key; PAT: narrow or remove it with the developer (6) |
| 3 | Route and token | `gh app-auth test --repo github.com/REPO` | all tests pass | route missing: 6; installation missing: 5 |
| 4 | Bot identity | `gh app-auth exec --repo github.com/REPO -- gh api graphql -f query='{ viewer { login } }' --jq .data.viewer.login`, then `gh app-auth exec --repo github.com/REPO -- gh api /apps/SLUG --jq .id` | the login is `SLUG[bot]`, and the second command prints the route's `app_id` | 6 |
| 5 | App permissions | `gh app-auth exec --repo github.com/REPO -- gh api /apps/SLUG --jq '{owner: .owner.login, permissions}'` | nothing beyond the table in step 3 of the setup; a permission from that table may be missing only if the developer chose to drop it | app settings (3), then accept the change on each installation (5) |
| 6 | Installation reach | `gh app-auth exec --repo github.com/REPO -- gh api /installation/repositories --paginate --jq '.repositories[].full_name'` | every repository the developer wants agents on under this route is listed | 5 |
| 7 | Git untouched | `git config --show-origin --get-regexp '^credential\.'` | no helper that calls `gh app-auth` (no output and exit code 1 pass) | ask before removing it (see step 6) |

`SLUG` is the login from check 4 without `[bot]`. Run checks 3 to 6 once per route.

`gh app-auth test` ends by suggesting `gh app-auth gitconfig --sync`: leave it unrun, since pushes stay on the developer's SSH key.

A blocked GraphQL call leaves check 4 **incomplete**, not passed: repository access alone does not prove which identity acts.

Report one line per check and route, pass or fail, with the failing output and its fix.
