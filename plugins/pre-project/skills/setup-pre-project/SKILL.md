---
name: setup-pre-project
description: Configure this repo for the pre-project skills: what a project is, where its phase documents live, their language, the triage labels the breakdown needs, and the UX setup the UX design phase needs. Run once before the first /pre-project.
disable-model-invocation: true
---

Scaffold the per-repo configuration the pre-project skills assume, next to the one `setup-matt-pocock-skills` writes:

- **Project docs** (`docs/agents/project-docs.md`): what a project is in this team's tools, where the phase documents live, their language and titles, how diagrams and collapsible agent notes are written there;
- **Triage labels** (`docs/agents/triage-labels.md`): the labels for the canonical triage roles, which the breakdown applies to its tickets;
- **UX** (`docs/agents/ux.md`): who the end users are and how to test with them, the success criteria, the friction baseline, the design system, how prototypes are built, where mockups live. The UX design phase reads it, and so can any interface review.

The issue tracker and the glossary stay with `setup-matt-pocock-skills`. This is a prompt-driven skill: explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

First check the dependencies listed in [../pre-project/references/conventions.md](../pre-project/references/conventions.md) (section « Dependencies »), and stop there if one is missing.

Then read whatever exists; don't assume:

- `docs/agents/`: `issue-tracker.md`, `triage-labels.md`, `domain.md`, a previous `project-docs.md` or `ux.md`;
- the `## Agent skills` block in `CLAUDE.md` or `AGENTS.md`;
- the connectors and CLIs available to you: an MCP server or CLI for Linear, Jira, Confluence, GitHub (`gh`);
- folders that already hold specs or design docs (`docs/`, `docs/projects/`, `doc/`, `specs/`);
- a vocabulary file other than `GLOSSARY.md` (a rule file, a wiki page) that the team already maintains;
- the interface stack: the component library (from the dependency files), a tokens or theme file, a component catalogue (Storybook, Lookbook), interface review skills among your available skills, and the product's principles or success criteria if a doc states them.

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

**Section E: UX.** Skip it when the repo has no end-user interface (a library, an API alone), and say so: the UX design phase will then always be « not applicable ». When `ux.md` exists, review it with the user instead. Otherwise fill the seed [ux.md](ux.md) one part at a time, proposing what exploration found and asking only for what it could not:

- **End users and testing**: who they are, and how a test is run (who organises it, who can take part and how many per round, how long, where, on which device). Recommend about five participants per round when the population allows; with one or two end users, all of them, in more short rounds.
- **Success criteria**: what makes the product succeed for them, beyond each feature's spec, each with how a design is checked against it. Propose the ones a doc already states; otherwise ask for two or three.
- **Friction baseline**: the tools they use today for the tasks the product covers, and where the agent can see them (a sample file, screenshots, a person to watch).
- **Design system**: components, tokens, interface review skills, the heuristic grid (recommend Nielsen's ten), the accessibility target (recommend WCAG 2.2 AA) and what checks it in the app, the usage contexts (pointer or touch, target sizes, screen widths).
- **Prototypes**: the default medium. Recommend an artifact when the agent can publish one and the design system can be approximated by tokens or a stylesheet; in the app when its components cannot be imitated. Note what an artifact can reproduce.
- **Where mockups live**: recommend storing the options page and the prototype next to the UX design document, linked from it.

### 3. Confirm and write

Show the drafts, let the user edit, then write:

- `docs/agents/project-docs.md`, from the seed of Section A filled with the answers; when it already exists, keep it and add what it lacks against the seed (a title for the UX design, written before that phase existed);
- `docs/agents/triage-labels.md`, only if Section D ran;
- `docs/agents/ux.md`, from the seed filled with Section E, only if it ran;
- a `### Project docs` sub-block in the `## Agent skills` block, same shape as its siblings: one line on where phase documents live, then « See `docs/agents/project-docs.md`. »; and, when `ux.md` was written, a `### UX` sub-block: one line naming the end users and the design system, then « See `docs/agents/ux.md`. »

When labels were collected on GitHub or GitLab and the tracker lacks some, create them (`gh label create`, `glab label create`).

### 4. Done

Tell the user the pre-project skills can now run, starting with `/pre-project <project>`. They can edit `docs/agents/project-docs.md` and `docs/agents/ux.md` directly later.
