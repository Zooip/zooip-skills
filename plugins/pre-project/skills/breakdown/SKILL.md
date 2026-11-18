---
name: breakdown
description: Phase 4 of a pre-project — slice the architecture document into tracer-bullet tickets on the issue tracker, with open questions carried as provisional rules.
disable-model-invocation: true
---

The breakdown turns the architecture into tickets. The slicing itself is the `to-tickets` process (tracer bullets, blocking edges, quiz the user, publish); this skill adds what a pre-project needs on top.

Read [../pre-project/references/conventions.md](../pre-project/references/conventions.md) first, and check the configuration it lists.

## Process

1. **Load the architecture.** Read the architecture and exploration documents.
2. **Slice in this order**, with tracer bullets and blocking edges as `to-tickets` defines them:
   - **Prefactoring** first: the moves the architecture's blast-radius map requires, behaviour unchanged.
   - **The tracer bullet**: the narrowest path through every layer that a user can see working.
   - **Extensions**, each blocked by the tracer, parallel to each other where nothing else gates them.
   - **One ticket per group of settings** still open, blocked by the ticket that holds their provisional rule, with the `needs-info` role. It lists what must be answered and by whom.
   - **One investigation ticket** per item of the exploration's « To check ».
3. **Carry the hypotheses.** Where a ticket implements a working hypothesis, the ticket says so in a section marked provisional, and names the ticket that will replace it. A rule already decided is written as decided.
4. **Quiz and publish.** Present the breakdown as `to-tickets` does (title, blocked by, what it delivers), iterate until the user approves, then publish to the tracker `issue-tracker.md` describes: native blocking links where the tracker has them, attached to the project, linking the architecture document. Fully specified tickets take the `ready-for-agent` role, the others `needs-info`, through the labels in `triage-labels.md`. If the user invokes `/to-tickets` for this step, the rules above still apply to its slicing.
5. **Report** the published tickets to the user as a table (identifier, title, blocked by, state), and which ones can start now. The tickets are the record of this phase; no document is written.

When answers to the parked settings arrive, apply the propagation rule of the conventions: rewrite the provisional sections, move the `needs-info` tickets to `ready-for-agent` once fully specified, and turn the open questions of the architecture document into decisions.
