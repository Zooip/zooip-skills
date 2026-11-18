---
name: setup-github-agent
description: Set up, check or repair the GitHub App identity coding agents use through gh-app-auth. Diagnoses an existing setup first and runs only the steps that fail.
disable-model-invocation: true
---

Guide the developer through creating or reusing a GitHub App and configuring [gh-app-auth](https://github.com/AmadeusITGroup/gh-app-auth). Keep the workflow independent of any app, developer or organization.

The skill ends at a verified setup; how agents then act lives in the `github-agent` skill. Git keeps the developer's SSH pushes and commit identity throughout (step 6, item 6).

## 1. Diagnose

Run `gh extension list`. When it lists gh-app-auth and `gh app-auth list` shows at least one app, run every check in [references/verify.md](references/verify.md) and report its result table. Run them in the context agents will act from, such as their sandbox or container, and settle any key reported `Not found` with the cross-check in that file before treating it as missing.

- **All checks pass:** confirm the routes cover every account and repository the developer wants agents on. If they do, give the hand-off summary of step 7 and stop.
- **Some checks fail, or a target is missing:** run only the steps the failures name, reusing the app ID, key and routes already configured. Ask in step 2 only for what the configuration cannot tell. Then go to step 7.
- **No app configured:** start at step 2.

## 2. Collect information

Reuse known answers and inspect non-secret existing configuration before asking. Collect missing information in a short batch:

- **App name and description:** distinguish the shared bot identity from the individual agent tools, such as Claude Code and Codex.
- **App owner:** personal account or organization that will own the app, with its exact GitHub login.
- **Installation targets:** exact user/organization logins and repositories to authorize. Distinguish all repositories of an owner from a selected list. Collect one accessible test repository per route: one per owner whose repositories are all authorized, and each selected repository tests itself.
- **Existing app:** whether to reuse it; collect the App ID or Client ID and local PEM path when available.
- **Local environment:** OS, availability of `gh`, and whether local commands can be executed. Explain that hosted cloud environments need separate validation and are outside this setup.

Never ask for private key contents or tokens in chat. Do not hardcode information from a previous developer's setup.

Check `gh --version` and `gh extension list`. If installed, read `gh app-auth setup --help` and `gh app-auth exec --help`. Use `gh auth status` to identify the authenticated account when useful, without assuming it is the intended owner. Do not print stored tokens or full secret-bearing configuration files.

## 3. Generate the prefilled form

For an existing app, skip creation and verify its settings instead.

Choose the base URL from the collected owner:

| Owner | Base URL |
| -- | -- |
| Personal account | `https://github.com/settings/apps/new` |
| Organization | `https://github.com/organizations/OWNER/settings/apps/new` |

Ensure the browser is signed in to the intended personal owner. Generate a clickable URL with the actual collected values, encoded with `urllib.parse.urlencode` or `URLSearchParams`. Do not interpolate untrusted input into shell code or give only a placeholder URL.

Use these parameters for an agent that maintains PRs, debugs CI, reads reviews and handles dependency updates:

| Parameter | Value |
| -- | -- |
| `name`, `description` | Collected values |
| `url` | Full GitHub profile or organization URL of the owner |
| `public` | `false` if every installation target is the owner; `true` otherwise |
| `webhook_active` | `false` |
| `request_oauth_on_install` | `false` |
| `contents` | `write` |
| `pull_requests` | `write` |
| `checks` | `read` |
| `statuses` | `read` |
| `actions` | `write` |
| `workflows` | `write` |
| `vulnerability_alerts` | `read` |

Explain the proposed access: Contents and Pull requests allow code/PR changes, reviews and comments; Checks and Commit statuses expose CI results; Actions exposes logs and reruns; Workflows allows workflow-file updates; Dependabot alerts exposes vulnerability reports. Contents permits writes even though this workflow keeps local pushes authenticated with the developer's SSH key. Remove permissions outside the collected needs. Leave Issues, administration, secrets and organization permissions unset unless specifically needed; Metadata read access is implicit. Do not grant bypass rights.

Explain that **Any account** permits installation on multiple accounts without making repositories public or sharing access between installations. **Only on this account** cannot cover both personal repositories and a different organization. A Marketplace listing is unnecessary.

Have the user review the form, leave callback/setup URLs empty, keep OAuth user authorization, device flow and webhooks off, and create the app. Record its App ID or Client ID and actual slug/settings URL. Never guess the slug from its name.

## 4. Generate and store the PEM

Guide the user through the app owner's **Settings → Developer settings → GitHub Apps → Edit**. Current interfaces use **Credentials → Key pairs → New key**; older ones show **Private keys → Generate a private key**. Follow the labels actually visible.

Have the user download the PEM and provide its local path only. Recommend a directory outside repositories, such as `~/.config/github-apps/APP_SLUG/private-key.pem`. On Linux/macOS, use directory mode `700` and key mode `600`. Safely quote paths, expand `~` before passing it to tools, and do not overwrite an existing key when moving the download.

Reuse an existing valid PEM instead of rotating it unnecessarily. Never display it, commit it, put its contents in command arguments or distribute this developer's key to teammates. Explain that tokens expire but private keys remain valid until revoked. Provision each developer's intended app/key explicitly.

## 5. Install on the target accounts

From the app settings, open **Install App**. Install separately on every collected user/organization account, preferably with **Only select repositories** and the collected repository list. Select all repositories only when requested. If organization approval is needed, report the outstanding request rather than claiming completion.

For existing installations, verify repository selection and accept requested permission changes. Distinguish app IDs from installation IDs: an app has one installation per target account. Let gh-app-auth discover installations; collect an explicit installation ID only if auto-detection fails or routing is ambiguous.

## 6. Configure gh-app-auth

When a command cannot run locally, give the user the exact command and mark that step unverified.

1. Install `gh` using supported OS instructions if missing. If initial authentication is needed, have the user complete `gh auth login` themselves. Do not log out, replace or expose existing credentials.
2. Install the extension only if absent:

   ```bash
   gh extension install AmadeusITGroup/gh-app-auth
   ```

3. Check installed CLI help. Build comma-separated routes from the collected targets: `github.com/OWNER/*` for all of an owner's repositories, or `github.com/OWNER/REPO` for selected repositories. Avoid `github.com/*/*`. Routing chooses credentials; GitHub's installation permissions enforce access.
4. Run this shape with actual values, passed as safely quoted arguments:

   ```bash
   gh app-auth setup \
     --app-id APP_ID \
     --key-file /absolute/path/to/private-key.pem \
     --patterns "github.com/PERSONAL_OWNER/*,github.com/ORG/REPO" \
     --name "APP_DISPLAY_NAME"
   ```

   Substitute `--client-id CLIENT_ID` for `--app-id` when using a supported Client ID; do not pass both. Prefer the default OS keyring. Preserve unrelated app/PAT entries; resolve existing overlapping routes before rerunning setup.
5. Read the keyring outcome from the cross-check in [references/verify.md](references/verify.md):

   - **Key missing:** it fails in both contexts. Store the PEM with step 4, then rerun setup.
   - **Keyring out of reach:** it passes in a fresh local terminal and fails in the agents' context. Keep the key: request host keyring access through the environment's own permission mechanism, then run the setup and its verification under that same access. A setup that succeeds with host access, followed by a sandboxed check that fails, means the check lacked access, not that storage failed.
   - **File storage:** `--use-filesystem` stores the key in a file instead of the keyring. Present it with its consequences, a key file readable by any process running as the developer, and use it only on the developer's explicit choice.

6. Do not run `gh app-auth gitconfig --sync` or `gh auth setup-git`. Leave Git remotes, SSH authentication and `user.name`/`user.email` intact.

## 7. Verify and hand off

Run every check in [references/verify.md](references/verify.md), on the test repository of each route. Repeat the steps a failure names until every check passes, or report what stays outstanding, such as a pending organization approval. Do not create PRs, comments, commits or pushes just to test setup.

Summarize the app owner/name, account/repository routes, PEM path or keyring storage, the check results and the context they ran in. When the key is reachable only with host keyring access, say so: agents in a sandbox without it will fail. Give `gh app-auth exec --repo github.com/OWNER/REPO -- gh pr list` as a read-only example. Explain that it supplies a short-lived token only to that command; SSH pushes and commit identity remain unchanged. Stop here.

## References

Use installed CLI help to resolve version differences. Consult these primary sources when needed:

- [Prefilled app forms](https://docs.github.com/en/apps/sharing-github-apps/registering-a-github-app-using-url-parameters)
- [Register a GitHub App](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/registering-a-github-app)
- [Manage private keys](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/managing-private-keys-for-github-apps)
- [gh-app-auth setup and usage](https://github.com/AmadeusITGroup/gh-app-auth)
