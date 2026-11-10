---
name: architecture
description: Phase 3 of a pre-project — turn the exploration's decisions into modules, interfaces and stable technical names, checked against the code, and write the architecture document for peer review.
disable-model-invocation: true
---

The architecture makes the decisions concrete enough for other developers to review and for agents to implement: which modules exist, what each one's interface is, what it hides, and what every concept is called in code.

Read [../pre-project/references/conventions.md](../pre-project/references/conventions.md) first, and check the configuration it lists.

## Process

1. **Load the decisions.** Read the exploration document. Invoke the `codebase-design` skill: its vocabulary (module, interface, seam, adapter, depth, leverage, locality) is the language of this phase and of its document.
2. **Read the code the design lands in.** The models, services, entry points and readers the decisions touch, so every interface is drawn against real signatures. Done when each module you propose can name the existing code it wraps or replaces, with `file:line`.
3. **Draft the modules.** For each one: its interface (signature, invariants, error modes), what it hides, the deletion test, and whether its seam is real (two adapters) or hypothetical (one). Settle the technical names here; they stay fixed from now on.
4. **Map the blast radius.** Find every reader and writer of the concepts the design changes (search the code, database views and raw queries included), and assign each to the module or entry point it must go through. Readers that must move first become **prefactoring**: a change that leaves behaviour identical and makes the feature an easy change.
5. **Place the open questions.** Put each setting from the exploration in the one module where its answer will land. A setting that fits no single place is a pivot: raise it before going on.
6. **Review in conversation.** Present the design, then iterate with the user on each point they challenge. Run the reality check of the conventions on every claim. Offer an HTML page of the design for reading.
7. **Write the document**:

   | Section | Content |
   | -- | -- |
   | Introduction | What the design covers, links to the earlier documents |
   | Overview | One Mermaid diagram: modules, transports, the main data paths |
   | Modules | Per module: interface (code block), what it hides, deletion test, seam |
   | Data | Which source each column or field is read from, as a table |
   | Sequences | The main write path as a Mermaid `sequenceDiagram` |
   | Readers | The blast-radius map: reader, entry point it goes through, what it reads |
   | Decisions taken during design | What this phase settled beyond the exploration |
   | Open questions | Each setting and the module where it lands; becomes « Decisions » once answered |
   | Tests | What is tested through which interface; which existing tests prove the seam by passing unchanged |
   | Agent notes | Files read, conventions to follow (the repo's rules on migrations, docs, errors, front-end patterns) |

Completion: every decision of the exploration is realised by a module, every reader of a changed concept is mapped, every open question has a single landing place. Then share the document with the peers who review it, and point the user to `/breakdown`.
