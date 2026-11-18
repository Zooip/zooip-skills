---
name: preliminary-study
description: Phase 1 of a pre-project — survey what the code does today, the obvious blockers, and the questions the spec leaves open, then write the preliminary study document.
disable-model-invocation: true
---

The preliminary study answers one question: **what stands between today's code and this need?** It decides nothing. It maps the ground, so the exploration can choose a direction knowing where the traps are.

Read [../pre-project/references/conventions.md](../pre-project/references/conventions.md) first, and check the configuration it lists.

## Process

1. **Read the need.** The project from the argument: its description, comments, linked tickets and feedback. Restate the need in one paragraph, in the user's terms. Done when the user agrees with the restatement.
2. **Trace today's paths.** For each actor the need involves (the one who acts today, the one who will act), follow the code path end to end: entry point, authorization, service, model, background jobs, readers of the result. Use a sub-agent for sweeps across many files. Done when every path the need touches has a sequence you could draw from memory, with `file:line` for each step.
3. **Classify what you found.** Each finding gets one tag:
   - **Blocker**: the need cannot be met without changing it;
   - **Trap**: it will silently produce a wrong result if ignored;
   - **Existing**: something already built that the solution can reuse;
   - **Sound**: a worry that turns out unfounded, with the reason.

   Each finding carries the code excerpt that proves it.
4. **Find the spec axes.** List the big questions a solution must answer, and the gaps in the initial spec (cases it never mentions, actors it forgets, words it leaves vague). Give each question a concrete **scenario** that shows why it matters, and classify it as pivot or setting. Where the approaches are already visible, compare them in a table as working hypotheses, never as decisions. Stay out of the solution: scope, ticket breakdown and estimates belong to later phases.
5. **List the files.** For each file a solution will likely touch: its role today and what would change. This is the map later agents start from.
6. **Write the document**, after the summary/go-ahead step of the conventions, with these sections:

   | Section | Content |
   | -- | -- |
   | Introduction | What the document covers, the survey date, the fact that choices stay open |
   | Key points | 3 to 6 bullets, each starting with its tag |
   | Data model | A Mermaid `classDiagram` of the models involved, simplified, with what is left out named below it |
   | Sequences | One Mermaid `sequenceDiagram` per actor path today, plus one for the target as a hypothesis |
   | Traps in the code | One subsection per finding: tag and title, the consequence in plain words, the code excerpt with its path |
   | Approaches (if any) | The comparison table from step 4 and a provisional recommendation |
   | Files to change | File, role today, what changes |
   | Questions to settle | Each spec question with its scenario, type, working hypothesis, who answers, where it lands |
   | Agent notes | Files read, code facts with `file:line` |

Completion: every blocker and trap cites code, every question has a scenario, every file the sequences cross is in the files table. Then point the user to `/exploration`.
