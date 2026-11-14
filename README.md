# agent-skills

Specialty skills for AI coding agents, in the open [Agent Skills](https://agentskills.io) format, packaged as plugins for **Claude Code** and **Codex**. A specialty skill knows one technology: its rules (each with a stable ID, a reason and a check), the scripts that check what has one right answer, and when it applies. It does not tell you how your team works; bring your own process.

## Plugins

| Plugin | Skills | For |
|---|---|---|
| [mulesoft](plugins/mulesoft/README.md) | `mulesoft`, `dataweave`, `munit`, `mule-sdk` | Mule 4 applications, DataWeave, MUnit, Mule SDK connectors and shared assets |

## Install

Claude Code:

```bash
claude plugin marketplace add brunosouzas/agent-skills
claude plugin install mulesoft@agent-skills
```

From a local clone, pass its path to `claude plugin marketplace add` instead.

Codex: add the marketplace in `.agents/plugins/marketplace.json` of this repository (`codex plugin marketplace add brunosouzas/agent-skills`, or the local path), then install `mulesoft` from it. Codex gets the skills only.

Other tools that read Agent Skills: copy or link `plugins/<plugin>/skills/<skill>/` into the tool's skills folder.

## How a skill is chosen

Each skill's `description` says what it does, when to use it, the words that trigger it and when not to use it, so a tool loads only the skill a request needs: "fix this DataWeave function" loads `dataweave`, a Mule flow loads `mulesoft`. A repository can also name its technologies on a `Stack:` line of its `AGENTS.md` ([docs/agents-md.md](docs/agents-md.md)).

## Versions

Every skill has its own semantic version (`metadata.version` in `SKILL.md`) and `CHANGELOG.md`; a review can cite exactly the rule it applied: "breaks DW-4 (dataweave 1.0.0)". How versions are raised: [CONTRIBUTING.md](CONTRIBUTING.md#versions) and [docs/releasing.md](docs/releasing.md).

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md): the writing rules, the rule format, versions, commit titles and evals.

## License

[Apache-2.0](LICENSE).
