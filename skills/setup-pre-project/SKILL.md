---
name: setup-pre-project
description: Configure this repo for the pre-project skills: what a project is, where its phase documents live, their language, and the triage labels the breakdown needs. Run once before the first /pre-project.
disable-model-invocation: true
---

Scaffold the per-repo configuration the pre-project skills assume, next to the one `setup-matt-pocock-skills` writes:

- **Project docs** (`docs/agents/project-docs.md`): what a project is in this team's tools, where the phase documents live, their language and titles, how diagrams and collapsible agent notes are written there;
- **Triage labels** (`docs/agents/triage-labels.md`): the labels for the canonical triage roles, which the breakdown applies to its tickets.

The issue tracker and the glossary stay with `setup-matt-pocock-skills`. This is a prompt-driven skill: explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

Read whatever exists; don't assume:

- `docs/agents/`: `issue-tracker.md`, `triage-labels.md`, `domain.md`, a previous `project-docs.md`;
- the `## Agent skills` block in `CLAUDE.md` or `AGENTS.md`;
- the connectors and CLIs available to you: an MCP server or CLI for Linear, Jira, Confluence, GitHub (`gh`);
- folders that already hold specs or design docs (`docs/`, `docs/projects/`, `doc/`, `specs/`);
- a vocabulary file other than `GLOSSARY.md` (a rule file, a wiki page) that the team already maintains.

If `issue-tracker.md` or `domain.md` is missing, tell the user to run `/setup-matt-pocock-skills` first, and stop: the project-docs choice depends on the tracker.

### 2. Present findings and ask

One section, one answer, then the next. Lead each with the recommended answer so the user can accept it in a word.

**Section A: Project container and documentation system.** Recommend the pairing that matches the tracker:

| Tracker | Project container | Phase documents | Seed |
| -- | -- | -- | -- |
| Linear | Linear project | Documents attached to the project | [project-docs-linear.md](project-docs-linear.md) |
| Jira | Epic | Confluence pages linked from the epic | [project-docs-confluence.md](project-docs-confluence.md) |
| GitHub | Milestone or GitHub Project | Markdown files in the repo | [project-docs-repo.md](project-docs-repo.md) |
| Local markdown | Folder under `.scratch/` | Markdown files in the repo | [project-docs-repo.md](project-docs-repo.md) |

A team may keep documents somewhere else than its tracker suggests (Linear tickets with Confluence pages); ask only when exploration hints at it. For any other system, have the user describe it in a paragraph and write the file from that description, covering the same fields as the seeds.

**Section B: Language.** Recommend the language the user writes to you in. It applies to phase documents and ticket descriptions; ticket titles follow `issue-tracker.md` if it sets a convention.

**Section C: Vocabulary source.** Skip it when `domain.md` points to a glossary that exists. Otherwise, if exploration found a vocabulary file the team maintains, propose it as the vocabulary source.

**Section D: Triage labels.** Skip it when `triage-labels.md` exists. Otherwise ask one question: keep the default labels? The defaults are the five canonical roles, each label equal to its name: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. On no, collect the tracker's existing names (a status may carry a role, as Linear's `Triage` status does for `needs-triage`).

### 3. Confirm and write

Show the drafts, let the user edit, then write:

- `docs/agents/project-docs.md`, from the seed of Section A filled with the answers;
- `docs/agents/triage-labels.md`, only if Section D ran;
- a `### Project docs` sub-block in the `## Agent skills` block, same shape as its siblings: one line on where phase documents live, then « See `docs/agents/project-docs.md`. »

When labels were collected on GitHub or GitLab and the tracker lacks some, create them (`gh label create`, `glab label create`).

### 4. Done

Tell the user the pre-project skills can now run, starting with `/pre-project <project>`. They can edit `docs/agents/project-docs.md` directly later.
