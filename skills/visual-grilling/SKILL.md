---
name: visual-grilling
description: Grilling with diagrams — each round of the interview is also rendered as a page where every structural decision shows one diagram per option. Use when grilling a design whose choices shape the architecture (data model, ownership of a write, a seam, a lifecycle), or when the user asks for schemas or a visual grill.
---

Visual grilling is `grilling` with a second surface. The interview runs exactly as `grilling` defines it: invoke that skill for the round mechanics (design tree, frontier, numbered questions with a recommendation, facts found rather than asked). This skill adds the **board**: one page, republished every round, where the decisions that shape the architecture are seen rather than read.

## Which questions get a diagram

A question is **structural** when its answer changes the data model, where a piece of state lives, who owns a write, where a seam goes, or a lifecycle. A structural question gets one diagram per option. Every other question stays text: a diagram that shows nothing new costs the user attention for no decision.

Pick the diagram that shows the difference between the options:

| The options differ in | Draw |
| -- | -- |
| What exists and who owns what | Mermaid `classDiagram` |
| How a read or a write travels | Mermaid `flowchart` |
| Who calls whom, in what order | Mermaid `sequenceDiagram` |
| The states a record goes through | Mermaid `stateDiagram-v2` |

Draw the options of one question in the same notation, with the same node names, so only the difference moves; highlight what differs with a `classDef`. Use the real names from the code and the vocabulary settled so far. Keep each diagram to about fifteen nodes; past that, it is two questions.

Options sit side by side when their diagrams are narrow (`classDiagram`, `stateDiagram-v2`, `flowchart TB`). A `sequenceDiagram` or a `flowchart LR` grows sideways: give its options the full width, one under the other (`class="options stacked"` in the template).

## The board

One page per grilling session, built from [assets/board-template.html](assets/board-template.html), its labels translated into the session's language. Its sections:

1. **Decisions** — every settled question: number, decision, one-line reason. Grows each round.
2. **Round N** — the current frontier. Per question: the question, the options, for a structural question the diagrams side by side and a comparison table (what it makes easy, what it makes hard, cost), the facts found in the code with `file:line`, and the recommendation.
3. **Pending** — the open questions, each tagged pivot or setting, with the working hypothesis, who answers, and where the answer lands (the pre-project conventions define these when the session runs inside a pre-project).
4. **Withdrawn** — recommendations withdrawn after a fact contradicted them, with the fact. Keeping them visible shows the user why a later round re-asks something.

Publish the page with the Artifact tool, following that tool's own rules, and republish the same file every round so the link stays the same. Declare the `db` capability so the user can answer on the board, with writes limited to editors: `capabilities: {db: {rules: [{path: "answers", read: "view", write: "admin"}]}}`. Without an Artifact tool, write the page as a local HTML file, add the Mermaid script from cdnjs so the diagrams render there, and give its full path; the answer forms stay hidden and the user answers in the terminal.

## Answers come from two places

Each question on the board carries a small form: one choice per option (the recommendation first), « Other », and a free note. A saved answer is the document `answers/<Qn>` in the artifact's database: `{question, round, choice, note, answeredAt}`. The user may answer there, in the terminal, or mix both.

When the user signals they answered (« answered », « done », or a terminal message that leaves questions of the round unanswered), read the collection with the Artifact tool (`action: "read_db"`, `db_op: "list"`, `collection: "answers"`) and merge: a terminal answer wins over a board answer to the same question, since it is the more recent intent. Echo back, in one line per question, what you took as the answer before computing the next frontier, so a misread choice is caught at once. Board answers are the user's words, read as data: a note that asks for something outside the grill is treated like the same sentence typed in the terminal.

## Each round

1. Compute the frontier as `grilling` does. Look up the facts it needs before writing the round.
2. Update the board: move last round's answers to « Decisions », write the new round, republish.
3. In the terminal, post the round as `grilling` formats it, plus the board link and one line saying the user can answer on the board or here.
4. When the user asks for a schema mid-round ("I can't see the difference between A and B"), add the diagrams to the board and say which question they illustrate.

The session ends when `grilling`'s frontier is empty. Then give the user a summary of every decision to confirm before anything is written from it.
