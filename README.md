# zooip-skills

Agent skills for Claude Code, Codex and any tool [rulesync](https://github.com/dyoshikawa/rulesync) generates for.

## Pre-project

Take a project from a loose need to tickets an agent can grab, in four phases. Each phase leaves a document the next one starts from, so a phase can run in a fresh session or be picked up by someone else.

| Skill | Role |
| -- | -- |
| `/setup-pre-project` | Run once per repo: what a project is in your tools, where phase documents live, their language, the triage labels |
| `/pre-project <project>` | Entry point: finds the current phase of a project and names the next skill |
| `/preliminary-study` | Phase 1: what the code does today, blockers, traps, the questions the spec leaves open |
| `/exploration` | Phase 2: widen the field of solutions, then converge through a visual grilling session |
| `/architecture` | Phase 3: modules, interfaces, stable technical names, blast radius, for peer review |
| `/breakdown` | Phase 4: tracer-bullet tickets, with open questions carried as provisional rules |
| `visual-grilling` | A grilling session with a board page: one diagram per option on structural questions, and answers on the page when the agent can publish Claude Artifacts |

An open question never stalls the pre-project unless its answer would change the direction (a **pivot**). Any other question (a **setting**) proceeds on a working hypothesis, recorded with who answers it and where the answer will land.

Works with any tracker and documentation system: Linear, Jira with Confluence, GitHub Issues with docs in the repo, local markdown, or one you describe.

### Requirements

- The [mattpocock-skills](https://github.com/mattpocock/skills): the phases build on `grilling`, `codebase-design` and `to-tickets`, and on the configuration `/setup-matt-pocock-skills` writes (issue tracker, glossary).
- Access to your tracker and documentation system from the agent (an MCP server or a CLI such as `gh`).

Install all the skills together: the phase skills read shared conventions from `skills/pre-project/references/`.

## Install

### Claude Code plugin

```
/plugin marketplace add Zooip/zooip-skills
/plugin install pre-project@zooip
```

Install the mattpocock-skills plugin the same way if you don't have it.

### Codex plugin

```bash
codex plugin marketplace add Zooip/zooip-skills
codex plugin add pre-project
```

The mattpocock-skills ship no Codex manifest: install them through rulesync, or copy them into your skills folder.

### rulesync

Add the sources to `rulesync.jsonc`, then run `rulesync install && rulesync generate`:

```jsonc
{
  "sources": [
    { "source": "Zooip/zooip-skills", "path": "skills" },
    { "source": "mattpocock/skills", "path": "skills/engineering", "skills": ["codebase-design", "to-tickets", "setup-matt-pocock-skills"] },
    { "source": "mattpocock/skills", "path": "skills/productivity", "skills": ["grilling"] }
  ]
}
```

## Then

1. Run `/setup-matt-pocock-skills` if the repo has no `docs/agents/issue-tracker.md`.
2. Run `/setup-pre-project`.
3. Run `/pre-project <your project>` and follow the phase it names.

## License

MIT
