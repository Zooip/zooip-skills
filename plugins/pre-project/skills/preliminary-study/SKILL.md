---
name: preliminary-study
description: Phase 1 of a pre-project — survey what the code does today, the prior art outside it, the obvious blockers, and the questions the spec leaves open, then write the preliminary study document.
disable-model-invocation: true
---

The preliminary study answers two questions: **what stands between today's code and this need, and what is already known and built around it?** It decides nothing. It maps the ground, so the exploration can choose a direction knowing where the traps are and which approaches exist.

Read [../pre-project/references/conventions.md](../pre-project/references/conventions.md) first, and check the configuration it lists.

## Process

1. **Read the need.** The project from the argument: its description, comments, linked tickets and feedback. Restate the need in one paragraph, in the user's terms. Done when the user agrees with the restatement.
2. **Survey the prior art.** Search the web for what is already known and built around this need. It comes in two halves, each with its kinds:
   - **Knowledge**, what the field knows about the problem itself:
     - **Norms**: rules a solution must or should respect: laws and regulations, industry standards, professional rules (accounting standards for a ledger, accessibility rules for a form);
     - **Theory**: established design patterns, reference models, research papers and reference works on the problem.
   - **Solutions**, how the need is already met:
     - **Companies**: how large companies or well-known products solve this problem (engineering blogs, public docs, talks);
     - **Ready-made solutions**: products or services, open-source or commercial, that cover the need whole or in part;
     - **Libraries**, when the need is technical: packages in the project's ecosystem that attack the problem.

   Run one sub-agent per kind, in parallel, so each search stays free of what you already assume. Run every kind: a kind that finds nothing reports its empty searches, and that note is the answer. Split a kind into several sub-agents when the need spans several domains or jurisdictions. Brief each with the problem stated as the job to be done (who wants what outcome), the project's domain and ecosystem, and its hard constraints (jurisdiction, hosting, licence, budget). Keep the brief to the problem: the spec's proposed solution, your own hypotheses and the project's internal vocabulary stay out of it. Ask each sub-agent to phrase the problem several ways, including in other fields' vocabulary, and to return, for each entry, its source link and:
   - for knowledge: what it states, whether it is **binding** (a rule the solution must follow) or **guidance**, and what it means for this need;
   - for a solution: what it is, the approach it takes (its shape, in a sentence), what adopting it would demand (licence, cost, lock-in, maintenance).

   Merge the results yourself: drop the entries that miss the domain, the ecosystem or the constraints, then give a verdict on the solutions: the problem is **solved** elsewhere, **partly solved**, or **open**. A binding norm constrains every solution: carry it into the spec axes. The prior art is reference for the exploration to learn from: describe each approach on its own terms and leave the choice to the exploration. Without web access, say so and mark the section as from memory, unverified. Done when each kind has entries with sources, or a note naming the searches tried and found empty, every norm is marked binding or guidance, and the verdict is given.
3. **Trace today's paths.** For each actor the need involves (the one who acts today, the one who will act), follow the code path end to end: entry point, authorization, service, model, background jobs, readers of the result. Use a sub-agent for sweeps across many files. Done when every path the need touches has a sequence you could draw from memory, with `file:line` for each step.
4. **Classify what you found.** Each finding gets one tag:
   - **Blocker**: the need cannot be met without changing it;
   - **Trap**: it will silently produce a wrong result if ignored;
   - **Existing**: something already built that the solution can reuse;
   - **Sound**: a worry that turns out unfounded, with the reason.

   Each finding carries the code excerpt that proves it.
5. **Find the spec axes.** List the big questions a solution must answer, and the gaps in the initial spec (cases it never mentions, actors it forgets, words it leaves vague). Give each question a concrete **scenario** that shows why it matters, and classify it as pivot or setting. Where the approaches are already visible, compare them in a table as working hypotheses, never as decisions; the prior art often reveals cases the spec never mentions, and a binding norm the spec ignores is a gap. Stay out of the solution: scope, ticket breakdown and estimates belong to later phases.
6. **List the files.** For each file a solution will likely touch: its role today and what would change. This is the map later agents start from.
7. **Write the document**, after the summary/go-ahead step of the conventions, with these sections:

   | Section | Content |
   | -- | -- |
   | Introduction | What the document covers, the survey date, the fact that choices stay open |
   | Key points | 3 to 6 bullets, each starting with its tag |
   | State of the art | **Knowledge**: one table per kind from step 2: name, what it states, binding or guidance, what it means here, source link. **Solutions**: the verdict (solved, partly solved, open), then one table per kind: name, approach, what it demands, source link |
   | Data model | A Mermaid `classDiagram` of the models involved, simplified, with what is left out named below it |
   | Sequences | One Mermaid `sequenceDiagram` per actor path today, plus one for the target as a hypothesis |
   | Traps in the code | One subsection per finding: tag and title, the consequence in plain words, the code excerpt with its path |
   | Approaches (if any) | The comparison table from step 5 and a provisional recommendation |
   | Files to change | File, role today, what changes |
   | Questions to settle | Each spec question with its scenario, type, working hypothesis, who answers, where it lands |
   | Agent notes | Files read, code facts with `file:line` |

Completion: every blocker and trap cites code, every prior-art entry links its source, every question has a scenario, every file the sequences cross is in the files table. Then point the user to `/exploration`.
