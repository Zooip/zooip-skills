---
name: ux-design
description: Phase 3 of a pre-project — design the interface around the end users' tasks: job stories, friction budget, low-fidelity options, a clickable prototype, a heuristic review and a test with a real end user, distilled into the UX design document.
disable-model-invocation: true
---

The UX design turns the exploration's decisions into an interface the **end users** (the people the product serves, named in `docs/agents/ux.md`) can use without friction. The agent does the design work; the user who runs this skill makes three moves: **choose** between options, **run the test** with an end user, **validate** the distillation.

Read [../pre-project/references/conventions.md](../pre-project/references/conventions.md) first, and check the configuration it lists, `ux.md` included.

A **gesture** is one unit of end-user effort: a click or tap, a field filled, a screen or tab change, a value looked up elsewhere, a decision the screen asks for. Count gestures the same way in today's tool and in every design, so the counts compare.

## Process

1. **Load the ground.** Read the exploration and preliminary study documents, the project, and `docs/agents/ux.md`. If the exploration records the interface as « not applicable », stop and point the user to `/architecture`. Done when you can name every exploration decision that changes what an end user sees or does.

2. **Write the job stories.** One per task the feature serves: « When [situation], I want to [action], so that [outcome] », in the end users' words, from the need, its feedback and the vocabulary source. Each cites its source (a quote, a ticket, who said it); a story with no source is marked as an assumption for the test to confirm. Done when every exploration decision from step 1 is covered by a story, and the user agrees the list is complete.

3. **Measure the friction.** For each job story, walk the journey in the end users' current tool (the friction baseline of `ux.md`) step by step and count its gestures. Set the **friction budget**: at most the baseline count, unless the user accepts a larger one for a stated gain (a check the old tool skipped, a value it lost). Done when every story has a baseline journey, its count, and a budget.

4. **Sketch the options.** Draft 2 or 3 options, **structurally different**: different layout, information hierarchy or primary affordance, never variations of colour or copy. Draw them low-fidelity (greyscale boxes, real labels, no styling) side by side on one page; for each, the journey and gesture count of every story against its budget, what it makes easy and hard, and how it meets each success criterion of `ux.md`. Publish the page as an Artifact where you have the tool, a local HTML file otherwise, and give the link. The user chooses one, or combines parts. Done when the choice is made and each rejected option has its reason.

5. **Build the clickable prototype** of the chosen option. Pick the medium by what the test must check:
   - **Artifact** (a local HTML page without the tool) when the question is the journey: gestures, order, wording. It is shared by a link and runs on a phone. Reuse what `ux.md` says the artifact can reproduce (tokens, a stylesheet), meet its usage contexts (pointer or touch, target sizes, screen widths), and list on the page what it does not imitate.
   - **In the app**, through the `prototype` skill (its UI branch), when the question depends on the real components, density or data. Call the Skill tool with `prototype`; if it is missing, give the install line of the conventions, or fall back to an artifact with the user's agreement.

   Start from the default medium `ux.md` gives, and say why when you depart from it. Fill the prototype with plausible sample data (never real personal data), mark it as a prototype, and keep its state in memory. Done when every job story can be completed end to end in the prototype, and its gesture count matches the chosen option.

6. **Review by heuristics.** Check the prototype against each heuristic of the grid `ux.md` names (Nielsen's ten usability heuristics by default), and call the interface review skills it lists. Each finding: heuristic, where, severity (Nielsen's 0 to 4 scale), fix. Fix every finding of severity 3 or 4 before the test, or tell the user why it stays. Done when every heuristic has been checked and every finding has a severity and an outcome.

7. **Hand over the test protocol.** Write a sheet the user can run without you, following the testing rules of `ux.md` (who organises, how long, where, on which device):
   - 3 or 4 real tasks drawn from the job stories, each phrased as a goal in the end users' words, never naming a screen or a button;
   - the instruction to give the participant: think aloud, there is no wrong answer, the prototype is under test, not them;
   - the observer's rules: stay silent, answer a question with a question, let a hesitation run; when the participant is stuck for a minute, note it and move to the next task;
   - per task, what to note: completed or not, hesitations and where, gestures that went astray, the participant's words;
   - three debrief questions: what was easy, what was surprising, what they would do in their current tool.

   Give the sheet and the prototype link, then wait for the notes. Done when the notes cover every task.

8. **Distill.** Turn each observation into a finding: what happened, its likely cause, and what is done about it (a change to the design, an accepted cost, a setting). A finding that contradicts an exploration decision goes back to the user as a pivot. Apply the changes to the prototype; when they alter a journey, offer a second test round. Then write the **acceptance criteria**: per job story, checkable statements an implementer can test, the friction budget among them (« Recording X takes at most N gestures from Y »). Done when every observation has an outcome and every job story has its criteria.

9. **Write the document**, after the summary/go-ahead step of the conventions:

   | Section | Content |
   | -- | -- |
   | Introduction | What was designed, links to the exploration and to the prototype |
   | Job stories | Numbered (J1, J2…): the story, its source or « assumption » |
   | Friction | Per story: today's journey and gesture count, the budget, the prototype's count |
   | Options compared | The low-fidelity options side by side (link or images), their trade-offs, the choice and its reason |
   | Prototype | Link, medium and why, what it does not imitate |
   | Heuristic review | Findings: heuristic, where, severity, outcome |
   | User test | Who, when, on what device; per task, what was observed; per finding, what is done |
   | Interface decisions | Numbered (U1, U2…): decision, short reason, the job story or finding behind it |
   | Acceptance criteria | Numbered (A1, A2…), grouped by job story; the architecture and the breakdown carry them |
   | Open questions | Each setting: working hypothesis, who answers, where it lands |
   | Agent notes | Prototype location (branch, file, artifact), sample data, design system parts used |

   Store the options page and the prototype where `ux.md` says mockups live, and link them from the document.

Completion: every job story has a budget met by the prototype or an accepted overrun, the test notes are distilled, and every story has acceptance criteria. Then point the user to `/architecture`.
