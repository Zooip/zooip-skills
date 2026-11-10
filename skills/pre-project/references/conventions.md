# Pre-project conventions

Shared by every phase skill: `preliminary-study`, `exploration`, `architecture`, `breakdown`. Each one points here; nothing below is repeated in them.

## Configuration

The repo's configuration should have been provided to you, in `docs/agents/` (summarised in the `## Agent skills` block of `CLAUDE.md` or `AGENTS.md`):

- `project-docs.md`: what a project is here, where its documents live, their language and titles, how diagrams and agent notes are written;
- `issue-tracker.md` and `triage-labels.md`: where tickets live and which labels carry the triage roles;
- `domain.md`: where the glossary and the ADRs live.

If `project-docs.md` or `triage-labels.md` is missing, tell the user to run `/setup-pre-project`. If `issue-tracker.md` or `domain.md` is missing, tell the user to run `/setup-matt-pocock-skills`. Stop there: a phase run without them writes documents nobody will find.

## Open questions never stall the pre-project

The pre-project moves faster than peers can read and answer. An unanswered question blocks only when its answer would change the direction. Classify every open question as one of two kinds:

- A **pivot**: a different answer would change which modules exist, the shape of the data model, or where a seam goes. A pivot blocks the phase that builds on it. Say so plainly, name who must answer, and stop that phase there.
- A **setting**: a different answer would land in one place (a policy rule, a guard, a default, a label) and leave the structure alone. A setting never blocks. Record it with three things:
  - the **working hypothesis** the work proceeds on;
  - **who** answers it (a role: product owner, lead developer, support, the people who define access rights);
  - **where** the answer will land (the module, the guard, the ticket).

The architecture phase is the test of a setting: if its answer cannot be placed in a single module, it is a pivot that was misfiled — raise it.

When answers arrive later, propagate them everywhere the question appears: in **every** document that lists it (an exploration's open question left as is contradicts the architecture's decision), the row becomes a decision, with who answered and when (a decision with no source reads as unconfirmed); the provisional part of a ticket is rewritten; a ticket waiting for information (`needs-info`) moves to `ready-for-agent`. An answer often raises a smaller follow-up question (a conflict the hypothesis hid); classify it the same way.

## Facts are found, decisions are asked

Finding a fact in the code, the tracker or the docs is the agent's job; asking the user for something it could look up wastes their time. Decisions are the user's: put each one to them with a recommendation, and wait.

**Reality check.** A recommendation that rests on how the code behaves is checked in the code before it is made. When a fact found later contradicts a recommendation already accepted, withdraw it explicitly, say what changed, and re-ask the decisions downstream of it. Cite `file:line` for every fact the documents rely on.

## Phase documents

- One document per phase, where `project-docs.md` says, under the titles it gives for the preliminary study, the exploration and the architecture. The breakdown leaves tickets, not a document. Replaying a phase updates its document.
- Documents are written in the language `project-docs.md` sets, for people first: short sentences, one term per concept throughout, tables for comparisons, diagrams wherever a structure or a flow is the point. The phase skills name sections in English; translate them when writing.
- Diagrams are Mermaid, unless `project-docs.md` gives a fallback for a system that cannot render them.
- Detail aimed at agents (file lists, code facts with `file:line`, conventions to follow) goes in a collapsible « Agent notes » section at the end, in the syntax `project-docs.md` gives, so the human part stays readable.
- Each document opens with one paragraph saying what it covers and the date of the survey, and links the documents before it.
- Before writing a document, give the user a summary of what it will state (decisions, hypotheses, edge cases) and get their go-ahead. The document is written from that confirmed summary.
- When a document is long and diagram-heavy, offer an HTML page alongside it for reading (an Artifact where the agent has one); the documentation system stays the source of truth.

## Vocabulary

Use the project's domain vocabulary, from the glossary `domain.md` points to (or the vocabulary source `project-docs.md` names), in documents and tickets. A new term settled during the pre-project is recorded in the document that settles it, with the terms considered and rejected, and goes into the glossary in the first implementation change.
