---
name: exploration
description: Phase 2 of a pre-project — widen the field of solutions, converge through a visual grilling session, then write the exploration document.
disable-model-invocation: true
---

The exploration turns the questions of the preliminary study into decisions. It **diverges** first, so the obvious solution is not the only one considered, then **converges** through a grilling session until every branch is decided or parked.

Read [../pre-project/references/conventions.md](../pre-project/references/conventions.md) first, and check the configuration it lists.

## Process

1. **Load the ground.** Read the preliminary study and the project. Its questions to settle seed the design tree. Ask the user for any framing they want to add (a direction to challenge, a constraint from a discussion with peers); record it as context, not as a decision.
2. **Diverge.** Before any question about details, name the **solution families**: distinct shapes the solution could take, including at least one that breaks the spec's own framing (the spec says "edit X"; a family that never edits X counts). For each family: one diagram of its structure, what it makes easy, what it makes hard. Let the user discard families; keep the survivors as branches of the tree. Done when the user agrees the families on the table cover the plausible field.
3. **Converge.** Invoke the `visual-grilling` skill and run it on the tree, round after round, until its frontier is empty. Run the reality check of the conventions on every recommendation that rests on code. Classify every question the user cannot answer now as a pivot or a setting.
4. **Summarize.** Give the user the list of decisions, the vocabulary settled, the accepted edge cases and the open questions, and get their confirmation. A pivot still open ends the phase here: the document is written, marked as waiting on it.
5. **Write the document**:

   | Section | Content |
   | -- | -- |
   | Introduction | What was explored, link to the preliminary study |
   | Vocabulary | Each concept: the term kept, its other-language and technical names, the terms rejected and why |
   | Decisions | Numbered table (Q1, Q2…): question, decision, short reason |
   | Findings in the code | The facts that drove decisions, with the diagrams that show them |
   | Options compared | For each structural decision, the diagrams of the options side by side and the comparison that settled it |
   | Accepted edge cases | Each edge case the design accepts knowingly, with its consequence |
   | Open questions | Each setting: working hypothesis, who answers, where it lands |
   | Out of scope | What was set aside but must stay possible later, and why the design does not close it off |
   | To check | Doubts about current code found on the way, to become investigation tickets |
   | Agent notes | Files read, code facts with `file:line` |

Completion: every branch of the tree is a decision, a parked setting, or a pivot named as blocking. Then point the user to `/architecture`.
