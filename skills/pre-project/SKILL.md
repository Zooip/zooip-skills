---
name: pre-project
description: Run the pre-project of a project, from first study to tickets: tells you which phase comes next and which skill runs it.
disable-model-invocation: true
---

A **pre-project** turns a project (a need, a feedback, a loose spec) into tickets an agent can grab, through four **phases**. Each of the first three phases ends on a document, and the last on tickets, so the next phase — often a fresh session, sometimes another person — starts from what was written, not from a conversation.

| Phase | Skill | Leaves behind |
| -- | -- | -- |
| 1. Preliminary study | `/preliminary-study` | the preliminary study document |
| 2. Exploration | `/exploration` | the exploration document |
| 3. Architecture | `/architecture` | the architecture document |
| 4. Breakdown | `/breakdown` | the tickets themselves (no document) |

Every phase follows the shared rules in [references/conventions.md](references/conventions.md): the configuration it needs, the open-question policy, the reality check, the document conventions. Read it first, and check the configuration before anything else.

## Process

1. **Locate the project.** Take it from the argument, in the form `docs/agents/project-docs.md` describes, or ask for it. Read the need (description, comments, linked tickets and feedback) and list the phase documents that exist.
2. **Find the current phase.** The first phase whose document is missing is the current one; once the architecture document exists, the breakdown is done when the project has its tickets. A document that ends on unanswered **pivots** (see the conventions) means its phase is not finished: say which pivots, and who is meant to answer them.
3. **Report the state** in a few lines: what each existing document settled, the **settings** still waiting for an answer and the working hypothesis standing in for each, and the next phase.
4. **Hand over.** Tell the user which skill to run next, with the project as its argument. If answers to open questions arrived since the last phase, say which documents and tickets they update (the conventions describe how) before moving on.

A phase can be replayed: running a phase skill on a project that already has its document updates that document rather than creating a second one.
