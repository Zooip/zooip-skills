# Verify a GitHub Agent setup

Every check is read-only: it writes nothing to GitHub, Git or the gh-app-auth configuration, and prints no token or key. Run them in order: a failure makes the checks below it unreliable. **Fix** names the step of [the setup skill](../SKILL.md) that repairs a failure.

Read the configuration first:

```bash
gh app-auth list --format json
```

Each entry of `github_apps` gives an app ID, an installation ID and its `patterns` (the **routes**). Pick one **test repository** per route: the route's repository itself, or for `github.com/OWNER/*` a repository of that owner the user names or that `/installation/repositories` (check 6) lists. `REPO` below is `OWNER/NAME`.

| # | Check | Command | Pass | Fix |
| -- | -- | -- | -- | -- |
| 1 | Tools | `gh --version` and `gh extension list` | `gh` runs and lists `AmadeusITGroup/gh-app-auth` | 6 |
| 2 | Key | `gh app-auth list --verify-keys` | every app shows its key as accessible | 4, then 6 |
| 3 | Route and token | `gh app-auth test --repo github.com/REPO` | all tests pass | route missing: 6; installation missing: 5 |
| 4 | Bot identity | `gh app-auth exec --repo github.com/REPO -- gh api graphql -f query='{ viewer { login } }' --jq .data.viewer.login` | `SLUG[bot]`, never the developer's login | 6 |
| 5 | App permissions | `gh app-auth exec --repo github.com/REPO -- gh api /apps/SLUG --jq '{owner: .owner.login, permissions}'` | permissions match the table in step 3 of the setup, nothing more | app settings (3), then accept the change on each installation (5) |
| 6 | Installation reach | `gh app-auth exec --repo github.com/REPO -- gh api /installation/repositories --paginate --jq '.repositories[].full_name'` | every repository the route should cover is listed | 5 |
| 7 | Git untouched | `git config --show-origin --get-regexp '^credential\.'` | no helper that calls `gh app-auth` (no output and exit code 1 pass) | ask before removing it (see step 6) |

`SLUG` is the login from check 4 without `[bot]`. Run checks 3 to 6 once per route.

`gh app-auth test` ends by suggesting `gh app-auth gitconfig --sync`: leave it unrun, since pushes stay on the developer's SSH key.

A blocked GraphQL call leaves check 4 **incomplete**, not passed: repository access alone does not prove which identity acts.

Report one line per check and route, pass or fail, with the failing output and its fix.
