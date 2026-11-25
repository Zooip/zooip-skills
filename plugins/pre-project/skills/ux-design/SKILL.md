---
name: ux-design
description: Phase 3 of a pre-project — design the interface around the end users' tasks: job stories, friction budget, low-fidelity options, a clickable prototype, an independent review and a test with a real end user, distilled into the UX design document.
disable-model-invocation: true
---

The UX design turns the exploration's decisions into an interface the **end users** (the people the product serves, named in `docs/agents/ux.md`) can use without friction. The agent does the design work; the user who runs this skill makes three moves: **choose** between options, **run the test** with an end user, **validate** the distillation.

Read [../pre-project/references/conventions.md](../pre-project/references/conventions.md) first, and check the configuration it lists, `ux.md` included. Every method below is described, with its source, in [references/methods.md](references/methods.md); the steps name the section to read.

## Two paths

The exploration records the interface as one of three levels:

- **not applicable**: the phase does not run;
- **light**: the feature reuses an existing screen pattern, named in the exploration, with no new journey. Steps 1, 2, 3, 5, 6, 8 and 9: no options compared, no user test. A finding of severity 3 or 4 in step 6 moves the project to the full path, from step 4;
- **full**: every step.

An exploration written before the levels existed has none: ask the user which one applies, with a recommendation.

## Process

1. **Load the ground.** Read the exploration and preliminary study documents, the project, and `docs/agents/ux.md`. Take the interface level from the exploration: « not applicable » sends the user to `/architecture`. Done when you can name every exploration decision that changes what an end user sees or does.

2. **Write the job stories.** One per task the feature serves: « When [situation], I want to [action], so that [outcome] », in the end users' words, from the need, its feedback and the vocabulary source. Each cites its source (a quote, a ticket, who said it); a story with no source is marked as an assumption for the test to confirm. Done when every exploration decision from step 1 is covered by a story, and the user agrees the list is complete.

3. **Measure the friction**, as a simplified Keystroke-Level Model (methods: « Counting operations »). For each job story, walk the journey in the end users' current tool (the friction baseline of `ux.md`) and count its **physical** and **mental operations** in two columns, each count marked **estimated** or **observed**. Set the **friction budget**: per column, at most the baseline count, unless the user accepts more for a stated gain (a check the old tool skipped, a value it lost). Done when every story has a baseline journey, both counts with their status, and a budget.

4. **Sketch the options.** Draft 2 or 3 options, **structurally different**: different layout, information hierarchy or primary affordance, never variations of colour or copy. Draw them low-fidelity (greyscale boxes, real labels, no styling) side by side on one page; for each, the journey and operation counts of every story against its budget, what it makes easy and hard, and how it meets each success criterion of `ux.md`. Publish the page as an Artifact where you have the tool, a local HTML file otherwise, and give the link. The user chooses one, or combines parts. Done when the choice is made and each rejected option has its reason.

5. **Build the clickable prototype** of the chosen option (on the light path, of the existing pattern extended). Pick the medium by what the test must check:
   - **Artifact** (a local HTML page without the tool) when the question is the journey: operations, order, wording. It is shared by a link and runs on a phone. Reuse what `ux.md` says the artifact can reproduce (tokens, a stylesheet), meet its usage contexts (pointer or touch, target sizes, screen widths), and list on the page what it does not imitate.
   - **In the app**, through the `prototype` skill (its UI branch), when the question depends on the real components, density or data. Call the Skill tool with `prototype`; if it is missing, give the install line of the conventions, or fall back to an artifact with the user's agreement.

   Start from the default medium `ux.md` gives, and say why when you depart from it. Fill the prototype with plausible sample data (never real personal data), mark it as a prototype, and keep its state in memory. Done when every job story can be completed end to end in the prototype, and its counts match the chosen option.

6. **Have it reviewed by an independent evaluator.** Dispatch a fresh sub-agent with the prototype, the job stories, `ux.md` (grid, success criteria, usage contexts, accessibility target) and [references/methods.md](references/methods.md); keep out the design reasoning and the rejected options. Dispatch two in parallel when you can, then consolidate their findings (cluster duplicates, severity = the mean of their ratings). Without sub-agents, run the review in a separate session and say so in the document. Each evaluator, on every job story:
   - a **cognitive walkthrough** of each step (methods: « Cognitive walkthrough »);
   - the **heuristics** of the grid `ux.md` names, Nielsen's ten by default, and each **success criterion** of `ux.md` as one more heuristic, checked as `ux.md` says (methods: « Heuristic evaluation »);
   - the **accessibility check** at the level `ux.md` sets, WCAG 2.2 AA by default (methods: « Accessibility check »);
   - the interface review skills `ux.md` lists.

   Each finding: method, where, severity 0 to 4, suggested fix. Fix every finding of severity 3 or 4 before the test, or tell the user why it stays; on the light path, such a finding moves the project to the full path. Done when every job story has been walked, every heuristic and success criterion checked, every accessibility criterion of the table judged, and every finding has a severity and an outcome.

7. **Hand over the test protocol.** Write a sheet the user can run without you, following the testing rules of `ux.md` (who organises, participants, how long, where, on which device) and the measures of methods « User test measures »:
   - 3 or 4 real tasks drawn from the job stories, each phrased as a goal in the end users' words, never naming a screen or a button;
   - the instruction to give the participant: think aloud, there is no wrong answer, the prototype is under test, not them;
   - the observer's rules: stay silent, answer a question with a question, let a hesitation run; when the participant is stuck for a minute, note it and move to the next task;
   - per task, what to note: success, partial success or failure; the Single Ease Question score, and why when it is under 5; hesitations and where; operations that went astray; the participant's words;
   - the debrief: what was easy, what was surprising, and « show me how you do it today » for each task whose baseline is estimated, noting the observed counts;
   - the number of participants per round from `ux.md`, and the SUS after the test only when it declares several.

   Give the sheet and the prototype link, then wait for the notes. Done when the notes cover every task.

8. **Distill.** Turn each observation and each open review finding into a finding: what happened, its likely cause, the success criterion it touches if any, and what is done about it (a change to the design, an accepted cost, a setting). A failed task or a Single Ease score under 5 is always a finding; an unmet success criterion is a finding of severity 3 at least, or a pivot when meeting it would contradict an exploration decision. Update the baseline with the observed counts. Apply the changes to the prototype; when they alter a journey, offer a second test round. Then write the **acceptance criteria** as Given / When / Then scenarios (methods: « Acceptance criteria »), per job story, the friction budget among them. Done when every observation has an outcome and every job story has its criteria.

9. **Write the document**, after the summary/go-ahead step of the conventions:

   | Section | Content |
   | -- | -- |
   | Introduction | What was designed, the path (light or full) and why, links to the exploration and to the prototype |
   | Job stories | Numbered (J1, J2…): the story, its source or « assumption » |
   | Friction | Per story: physical and mental operations today (estimated or observed), the budget, the prototype's counts |
   | Options compared | The low-fidelity options side by side (link or images), their trade-offs, the choice and its reason; « light path » otherwise |
   | Prototype | Link, medium and why, what it does not imitate |
   | Review | Who reviewed (sub-agents, how many), then per method the findings: where, severity, outcome; one row per success criterion; the accessibility criteria judged |
   | User test | Who, when, on what device; per task: success, Single Ease score, what was observed; per finding, what is done; « light path » otherwise |
   | Interface decisions | Numbered (U1, U2…): decision, short reason, the job story or finding behind it |
   | Acceptance criteria | Numbered (A1, A2…), grouped by job story, in Given / When / Then; the architecture and the breakdown carry them |
   | Open questions | Each setting: working hypothesis, who answers, where it lands |
   | Agent notes | Prototype location (branch, file, artifact), sample data, design system parts used |

   Store the options page and the prototype where `ux.md` says mockups live, and link them from the document.

Completion: every job story has a budget met by the prototype or an accepted overrun, every review finding of severity 3 or 4 is fixed or accepted, the test notes are distilled (full path), and every story has acceptance criteria. Then point the user to `/architecture`.
