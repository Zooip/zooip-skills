# UX design methods

The methods the `ux-design` steps apply, each with its source, so a reader can check where a rule comes from. A rule marked **(this skill)** is an adaptation the sources do not state.

## Counting operations: a simplified Keystroke-Level Model

The friction budget counts operations the way the **Keystroke-Level Model** (KLM) does: Card, Moran & Newell, « The Keystroke-Level Model for User Performance Time with Interactive Systems », *Communications of the ACM* 23(7), 1980, pp. 396–410 ([doi:10.1145/358886.358895](https://doi.org/10.1145/358886.358895); operators and values summarised on [Wikipedia](https://en.wikipedia.org/wiki/Keystroke-level_model)).

The KLM splits a task into physical operators (K keystroke, P pointing, H homing between devices, D drawing) and one mental operator, **M**: the time « for thinking or decision making ». Its standard values: M = 1.35 s, P = 1.1 s, H = 0.4 s, K from 0.08 s (expert typist) to 1.2 s (unfamiliar with the keyboard), 0.2 s for an average skilled typist.

This skill keeps **counts in two columns, not times** (this skill):

| Column | Counts one for each | KLM operators |
| -- | -- | -- |
| Physical | click or tap, field filled, screen or tab change, switch between keyboard and pointer | K, P, H |
| Mental | decision the screen asks for, value looked up elsewhere (another file, paper, memory), calculation in the head, check that something worked | M |

- A field counts as **one** physical operation whatever its widget (free text, list, date picker, checkbox) and its length; choosing the value, when the screen asks for a decision, is a mental operation counted apart (this skill). Counting a list as two operations (open, pick) against one for free text would push the budget towards free text, which yields dirty data.
- A mental operation costs about as much as pointing and clicking (1.35 s against 1.1 s plus a button press), and several keystrokes: never treat it as free. A design that removes two clicks and adds a decision has not reduced friction.
- Each count is **estimated** (read from a file, screenshots, a description) or **observed** (watched while the end user does it). An estimated baseline is confirmed during the test (« show me how you do it today »).
- The full KLM time calculation, with its rules for placing M, is out of scope: the counts only need to compare today's tool and each option the same way.

## Heuristic evaluation

- **Heuristics**: Jakob Nielsen's ten usability heuristics (with Rolf Molich, 1990; refined 1994), [nngroup.com/articles/ten-usability-heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/): visibility of system status; match between the system and the real world; user control and freedom; consistency and standards; error prevention; recognition rather than recall; flexibility and efficiency of use; aesthetic and minimalist design; help users recognize, diagnose, and recover from errors; help and documentation.
- **Evaluators**: « Ideally, three to five people should independently evaluate the same interface », since each one misses some issues; they do not see each other's findings until their own evaluation is complete, then consolidate them by clustering similar issues ([how to conduct a heuristic evaluation](https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/)).
- **Independent of the design**: the evaluators are fresh sub-agents that never see the design reasoning or the rejected options. See « Two looks, the blind one first » for what each one receives.
- **Severity** ([how to rate the severity](https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/)), judged on frequency, impact and persistence (plus market impact):

  | Rating | Meaning |
  | -- | -- |
  | 0 | Not a usability problem at all |
  | 1 | Cosmetic problem only: fix if extra time is available |
  | 2 | Minor usability problem: low priority |
  | 3 | Major usability problem: important to fix, high priority |
  | 4 | Usability catastrophe: imperative to fix before release |

  Each evaluator rates independently. The **mean** of several evaluators' ratings is « satisfactory for many practical purposes »; a single evaluator's ratings are « too unreliable to be trusted ». With one evaluator, say so next to the ratings.
- **Success criteria as heuristics (this skill)**: each success criterion of `ux.md` is checked like one more heuristic, with the check `ux.md` gives for it.

## Two looks, the blind one first

A heuristic evaluation and a cognitive walkthrough need opposite inputs (this skill, from the two methods below):

- the **blind evaluator** gets no action sequence. It runs the heuristics, the success criteria, the accessibility check, and a free attempt at each job story, as a newcomer would;
- the **sequence evaluator** gets the action sequence of each job story (the steps and the expected actions, without the reasons for them) and runs the cognitive walkthrough, which is defined on that sequence.

An evaluator who knows the expected path stops seeing what a newcomer sees, and an answer once known cannot be forgotten. So with a single sub-agent, the order is fixed: the blind look first, its findings handed back, then the sequence for the walkthrough. Neither evaluator ever gets the design reasoning or the rejected options.

A blind agent still is no end user: it reads the whole page source, closed menus and off-screen labels included, so its success proves little about how easy the interface is to learn. That proof is the user test, where the participant never gets the sequence.

## Cognitive walkthrough

An inspection of learnability without users, along the correct path of each task (Wharton, Rieman, Lewis & Polson, « The Cognitive Walkthrough Method: A Practitioner's Guide », in Nielsen & Mack (eds.), *Usability Inspection Methods*, Wiley, 1994; [nngroup.com/articles/cognitive-walkthroughs](https://www.nngroup.com/articles/cognitive-walkthroughs/)). Its inputs, as Spencer restates Wharton et al.: the users, sample tasks, « action sequences for completing the tasks », and the interface. At each step of the sequence, the evaluator tries to tell a credible story for each of four questions:

1. Will users try to achieve the right result?
2. Will users notice that the correct action is available?
3. Will users associate the correct action with the result they're trying to achieve?
4. After the action is performed, will users see that progress is made toward the goal?

Where no plausible story can be told, Wharton et al. record that it could not, and Spencer records « the failure and the knowledge that the user will need ». Spencer's streamlined version (R. Spencer, « The Streamlined Cognitive Walkthrough Method, Working Around Social Constraints Encountered in a Software Development Company », CHI 2000, pp. 353–359, [doi:10.1145/332040.332456](https://doi.org/10.1145/332040.332456)) collapses questions 1 to 3 into « Will the user know what to do at this step? »; this skill keeps the four, which point at the cause of a problem. It keeps Spencer's ground rules, written against design defensiveness: no designing, no defending a design, no debating cognitive theory. A design idea is noted in one line and the walkthrough moves on.

**Evidence for every yes (this skill)**: the story behind a « yes » names what is visible at that step: a label, a position, a state, the feedback shown. A « yes » with no visible evidence is a finding. An evaluator that knows the task answers yes too easily; tying the story to the screen is the guard.

A failed step is a finding, rated on the severity scale. This skill runs the walkthrough on every job story before the user test, so the end user meets a prototype without the obvious blocks.

## Accessibility check

The target is **WCAG 2.2, level AA** unless `ux.md` sets another ([w3.org/TR/WCAG22](https://www.w3.org/TR/WCAG22/), [quick reference](https://www.w3.org/WAI/WCAG22/quickref/), [new in 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)). Level AA includes the level A criteria. A prototype can be judged on these; the rest is checked in the real app:

| Criterion | What to check |
| -- | -- |
| 1.4.1 Use of Color | Colour is never the only way information is conveyed |
| 1.4.3 Contrast (Minimum) | Text contrast at least 4.5:1 |
| 1.4.11 Non-text Contrast | Controls and meaningful graphics at least 3:1 against adjacent colours |
| 2.1.1 Keyboard | Every function works from the keyboard |
| 2.4.3 Focus Order | Focus moves in an order that preserves meaning |
| 2.4.7 Focus Visible | The keyboard focus is visible |
| 2.4.11 Focus Not Obscured (Minimum) | The focused control is never entirely hidden by other content |
| 2.5.8 Target Size (Minimum) | Targets at least 24 × 24 CSS pixels, or spaced as the criterion allows |
| 3.3.1 Error Identification | An input error is identified and described in text |
| 3.3.2 Labels or Instructions | Every field has a label or instructions |
| 3.3.3 Error Suggestion | When a fix is known, the error message suggests it |

Usage contexts in `ux.md` may set larger targets (touch use often does); the larger value wins.

Each criterion ends with one of three outcomes: **met**, **finding** (with a severity), or **not judged on this prototype**, with the reason. A criterion not judged is carried into the acceptance criteria or the architecture's agent notes, to be checked in the app. An empty verdict is better than a guessed one (this skill).

**Contrast is computed, never estimated by eye**, from the colour values in the tokens or the prototype's CSS. WCAG defines the [contrast ratio](https://www.w3.org/TR/WCAG22/#dfn-contrast-ratio) as (L1 + 0.05) / (L2 + 0.05), L1 being the lighter colour's [relative luminance](https://www.w3.org/TR/WCAG22/#dfn-relative-luminance): L = 0.2126 R + 0.7152 G + 0.0722 B, where each channel is c / 255, linearised as c / 12.92 when it is at most 0.04045, ((c + 0.055) / 1.055) ^ 2.4 otherwise.

## How the evaluator sees the prototype

What an evaluator can judge depends on its tools; the review says which it had (this skill):

- **With a browser tool** (the agent's own, Playwright, Chrome DevTools…): open the prototype, take screenshots at each width of the usage contexts in `ux.md`, a phone's included, go through each journey with the keyboard alone, and measure the rendered targets.
- **Without one**: read the HTML and the CSS, judge what follows from them (labels, colours, declared sizes, source order), and mark the rest « not judged on this prototype »: focus visibility and occlusion, keyboard order as rendered, rendered target sizes.

## User test measures

The test follows Steve Krug's lightweight protocol (*Rocket Surgery Made Easy*, 2010) with thinking aloud: participants use the system « while continuously thinking out loud », and the facilitator lets them talk, since prompts « can very easily change user behavior » ([thinking aloud](https://www.nngroup.com/articles/thinking-aloud-the-1-usability-tool/)). It records three light measures, in line with the effectiveness, efficiency and satisfaction of ISO 9241-11:2018 (*Ergonomics of human-system interaction — Usability: Definitions and concepts*):

- **Task success**, per task, as a word label, never a number to average: **success**, **partial success** (completed with an issue: a detour, a wrong value fixed, a hint), **failure** ([success rate](https://www.nngroup.com/articles/success-rate-the-simplest-usability-metric/), Nielsen & Budiu).
- **Single Ease Question** (SEQ), asked right after each task: « Overall, how difficult or easy was the task to complete? », from 1 (very difficult) to 7 (very easy). Averages sit around 5.3 to 5.6; under 5, ask the participant briefly why ([10 things to know about the SEQ](https://measuringu.com/seq10/), Jeff Sauro). With one or two participants, read each score as a signal on its task, not as a statistic.
- **Task time** is optional: thinking aloud « contaminates task time measures » (success rate article above).

The **System Usability Scale** (SUS; ten items, after the whole test) measures perceived ease of the whole system and « was not intended to diagnose usability problems » ([measuringu.com/sus](https://measuringu.com/sus/)). It is left out by default; use it to compare rounds when `ux.md` declares several participants per round.

**Participants**: « testing no more than 5 users and running as many small tests as you can afford », for comparable users; with distinct user groups, three or four per group ([why you only need to test with 5 users](https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/), Nielsen, 2000). Krug sets the rhythm rather than the size: « A morning a month, that's all we ask » (chapter 3). When the product has only one or two end users, test with them and run more short rounds.

## Acceptance criteria: Given / When / Then

Each acceptance criterion is a **Given / When / Then** scenario: Given describes « the initial context of the system », When « an event, or an action », Then « an expected outcome », on an observable output ([Gherkin reference](https://cucumber.io/docs/gherkin/reference/)); And and But continue a Given or a Then. The form comes from Dan North and Chris Matts's Behaviour-Driven Development: « A story's behaviour is simply its acceptance criteria », and the scenarios become « proper end-to-end functional tests » ([Introducing BDD](https://dannorth.net/introducing-bdd/); [Martin Fowler, GivenWhenThen](https://martinfowler.com/bliki/GivenWhenThen.html)).

- Write them in the documents' language, with the end users' words; Gherkin's keywords exist in over 70 languages (French: Étant donné / Soit, Quand, Alors, Et, Mais).
- The friction budget is a criterion like the others: « Given …, When the user records X from Y, Then it takes at most N physical and M mental operations ».
- This is the format, not a tool: no Cucumber required. Each criterion usually maps to one acceptance test (system or end to end) of the ticket that delivers it.

## Proportional effort

Discount usability (« simple user testing with 5 participants, paper prototyping, and heuristic evaluation ») gives « a cheap, fast, and early focus on usability », and « bad user testing beats no user testing » ([discount usability: 20 years](https://www.nngroup.com/articles/discount-usability-20-years/), Nielsen, 2009). The light path of this skill applies the same idea to small interfaces: fewer steps rather than a skipped phase.
