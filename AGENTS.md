# zooip-skills

Agent skills shipped as plugins for Claude Code and Codex, and as plain skill folders for rulesync. A **plugin** is the unit someone installs: group skills into one only when they are always wanted together.

## Layout

- `plugins/<plugin>/skills/<skill>/SKILL.md`: one folder per skill, inside the plugin that ships it.
- `plugins/<plugin>/plugin.meta.json` and `marketplace.meta.json`: the **sources** of every manifest. Edit these, then run `python3 scripts/plugins.py build`.
- `plugins/<plugin>/.claude-plugin/`, `plugins/<plugin>/.codex-plugin/`, `.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`: **generated**. A hand edit is overwritten by the next build and fails the check.
- A new plugin: create its folder with a `plugin.meta.json`, add its name to `plugins` in `marketplace.meta.json`, build.

## Checks

`python3 scripts/plugins.py check` runs everything below; the pre-commit hook and the GitHub Action run it too. Enable the hook once per clone: `git config core.hooksPath .githooks`. The script is the source of truth for the rules it enforces; this file keeps the reasons.

- **Version bump.** Claude Code and Codex offer an update only when a plugin's `version` changes, so any change under `plugins/<plugin>/` since `origin/main` needs a bump in its `plugin.meta.json`. Bump once per push, by semver: patch for wording, minor for a new skill or behaviour, major for a removed or renamed skill.
- **Links stay inside their plugin.** An installed plugin is its own folder and nothing else: a relative link into another plugin resolves in this repo and breaks once installed. Reach another plugin's skill by name (see Dependencies).
- **Skill names are unique across plugins.** rulesync flattens every source into one skills folder.
- **The README links every skill** to its `SKILL.md`, and names every plugin.
- **Tests.** Code a plugin ships, such as a hook, gets contract tests in `tests/` (outside the plugin, so they are not installed with it); the check runs them.

## Skills

Every skill is **user-invoked** or **model-invoked**, in both harnesses at once:

- User-invoked (reachable only by the human typing its name): `disable-model-invocation: true` in the frontmatter, and `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. Its `description` is a one-line summary for a person browsing commands.
- Model-invoked (the default): neither flag. Its `description` carries the trigger phrasing ("Use when …") that makes the agent reach for it.

Each skill has `agents/openai.yaml` beside its `SKILL.md`, with `interface.display_name` and `interface.short_description` for the Codex picker. Write skills in English; the agent answers in the user's language.

Before writing or editing a skill or this file, call the Skill tool with `writing-for-agents`.

## Dependencies

- Inside a plugin, skills share reference files by relative link (the pre-project phases read `../pre-project/references/conventions.md`).
- Across plugins or repos, a step that runs another skill says "Call the Skill tool with `<skill>`". That only reaches model-invoked skills: for a user-invoked one, tell the user to run `/<skill>`.
- A skill that depends on another plugin checks it is installed before it starts, and names the install line for Claude Code, Codex and rulesync when it is missing. Record the dependency in the README's plugin table.

## Commits

Conventional prefixes (`feat:`, `fix:`, `refactor:`, `docs:`, `chore:`), the subject in the imperative with a capital letter, the body saying why.
