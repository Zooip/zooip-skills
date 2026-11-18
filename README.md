# zooip-skills

Agent skills for Claude Code, Codex and any tool [rulesync](https://github.com/dyoshikawa/rulesync) generates for, split into plugins you install separately:

| Plugin | Skills | Needs |
| -- | -- | -- |
| [`pre-project`](#pre-project) | `setup-pre-project`, `pre-project`, `preliminary-study`, `exploration`, `architecture`, `breakdown` | `visual-grilling`, mattpocock-skills |
| [`visual-grilling`](#visual-grilling) | `visual-grilling` | mattpocock-skills (`grilling`) |
| [`github-agent`](#github-agent) | `setup-github-agent`, `github-agent` | `gh`, gh-app-auth |

Each plugin lives in `plugins/<plugin>/`, with its skills in `plugins/<plugin>/skills/`.

## Pre-project

Take a project from a loose need to tickets an agent can grab, in four phases. Each phase leaves a document the next one starts from, so a phase can run in a fresh session or be picked up by someone else.

| Skill | Role |
| -- | -- |
| [`/setup-pre-project`](plugins/pre-project/skills/setup-pre-project/SKILL.md) | Run once per repo: what a project is in your tools, where phase documents live, their language, the triage labels |
| [`/pre-project <project>`](plugins/pre-project/skills/pre-project/SKILL.md) | Entry point: finds the current phase of a project and names the next skill |
| [`/preliminary-study`](plugins/pre-project/skills/preliminary-study/SKILL.md) | Phase 1: what the code does today, blockers, traps, the questions the spec leaves open |
| [`/exploration`](plugins/pre-project/skills/exploration/SKILL.md) | Phase 2: widen the field of solutions, then converge through a visual grilling session |
| [`/architecture`](plugins/pre-project/skills/architecture/SKILL.md) | Phase 3: modules, interfaces, stable technical names, blast radius, for peer review |
| [`/breakdown`](plugins/pre-project/skills/breakdown/SKILL.md) | Phase 4: tracer-bullet tickets, with open questions carried as provisional rules |

An open question never stalls the pre-project unless its answer would change the direction (a **pivot**). Any other question (a **setting**) proceeds on a working hypothesis, recorded with who answers it and where the answer will land.

Works with any tracker and documentation system: Linear, Jira with Confluence, GitHub Issues with docs in the repo, local markdown, or one you describe.

### Requirements

- The `visual-grilling` plugin: `/exploration` runs its convergence through it.
- The [mattpocock-skills](https://github.com/mattpocock/skills): the phases build on `grilling`, `codebase-design` and `to-tickets`, and on the configuration `/setup-matt-pocock-skills` writes (issue tracker, glossary).
- Access to your tracker and documentation system from the agent (an MCP server or a CLI such as `gh`).

Install all the pre-project skills together: the phase skills read shared conventions from `plugins/pre-project/skills/pre-project/references/`. Neither rulesync nor the plugins resolve dependencies for you: every skill checks they are there before it starts, and names the line that installs them if one is missing.

### Then

1. Run `/setup-matt-pocock-skills` if the repo has no `docs/agents/issue-tracker.md`.
2. Run `/setup-pre-project`.
3. Run `/pre-project <your project>` and follow the phase it names.

## Visual grilling

[`visual-grilling`](plugins/visual-grilling/skills/visual-grilling/SKILL.md) runs a grilling session with a board page: one diagram per option on structural questions, and answers on the page when the agent can publish Claude Artifacts. Usable on its own, on any design whose choices shape the architecture. It runs the rounds through `grilling` from the mattpocock-skills.

## GitHub Agent

[`/setup-github-agent`](plugins/github-agent/skills/setup-github-agent/SKILL.md) sets up, checks or repairs the GitHub App coding agents use as their bot identity to open and maintain PRs. It diagnoses an existing setup first, configures [gh-app-auth](https://github.com/AmadeusITGroup/gh-app-auth) and verifies each installation. SSH pushes and commit identity stay untouched.

[`github-agent`](plugins/github-agent/skills/github-agent/SKILL.md) is the skill agents reach for on their own before any `gh` command or GitHub API call: it checks the repository is covered, runs every `gh` command through `gh app-auth exec`, and reports what the bot is refused instead of falling back to your account.

In Claude Code and Codex, the plugin also ships a `PreToolUse` hook that refuses a plain `gh` command on a repository a gh-app-auth route covers, `gh app-auth token` and `gitconfig`, and GitHub MCP tools while a route is configured. Codex asks you to trust the hook the first time. rulesync installs only the skills, without the hook.

## Install

### Claude Code plugins

```
/plugin marketplace add Zooip/zooip-skills
/plugin install pre-project@zooip
/plugin install visual-grilling@zooip
/plugin install github-agent@zooip
```

Install only the plugins you need, and the mattpocock-skills plugin the same way if you don't have it.

### Codex plugins

```bash
codex plugin marketplace add Zooip/zooip-skills
codex plugin add pre-project
codex plugin add visual-grilling
codex plugin add github-agent
```

The mattpocock-skills have no Codex plugin manifest (each skill carries its own `agents/openai.yaml`): install them through rulesync, or copy their folders next to these skills.

### rulesync

rulesync has no plugins: add one source per plugin you want to `rulesync.jsonc`, then run `rulesync install && rulesync generate`. For the pre-project and its dependencies:

```jsonc
{
  "sources": [
    { "source": "Zooip/zooip-skills", "path": "plugins/pre-project/skills" },
    { "source": "Zooip/zooip-skills", "path": "plugins/visual-grilling/skills" },
    { "source": "mattpocock/skills", "path": "skills/engineering", "skills": ["codebase-design", "to-tickets", "setup-matt-pocock-skills"] },
    { "source": "mattpocock/skills", "path": "skills/productivity", "skills": ["grilling"] }
  ]
}
```

For the GitHub Agent plugin alone:

```jsonc
{
  "sources": [
    { "source": "Zooip/zooip-skills", "path": "plugins/github-agent/skills" }
  ]
}
```

## License

MIT
