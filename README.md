# agent-skills

Specialty skills for AI coding agents, in the open [Agent Skills](https://agentskills.io) format, packaged as plugins for **Claude Code** and **Codex**. A specialty skill knows one technology: its rules (each with a stable ID, a reason and a check), the scripts that check what has one right answer, and when it applies. A specialty does not tell you how your team works. The separate `delivery` plugin is an optional process (change flow, merge gates, delivery models) that reads your repository's `AGENTS.md`; use it, or bring your own.

## Plugins

| Plugin | Skills | For |
|---|---|---|
| [mulesoft](plugins/mulesoft/README.md) | `mulesoft`, `dataweave`, `munit`, `mule-sdk` | Mule 4 applications, DataWeave, MUnit, Mule SDK connectors and shared assets |
| [api](plugins/api/README.md) | `api-spec` | REST API specifications in RAML and OpenAPI |
| [languages](plugins/languages/README.md) | `java`, `python`, `shell` | Standalone Java, Python, and Bash or sh scripts |
| [devops](plugins/devops/README.md) | `azure-devops`, `github-actions`, `jenkins` | CI/CD pipelines in Azure Pipelines, GitHub Actions and Jenkins |
| [web](plugins/web/README.md) | `astro`, `cloudflare` | Astro static sites, Cloudflare Workers and Pages |
| [delivery](plugins/delivery/README.md) | `change-flow`, `merge-gates`, `delivery-models` | The process: plan, review, merge gates and delivery of a change (not a technology) |

## Install

Claude Code:

```bash
claude plugin marketplace add brunosouzas/agent-skills
claude plugin install mulesoft@brunosouzas-agent-skills   # or api, languages, devops, web, delivery
```

From a local clone, pass its path to `claude plugin marketplace add` instead.

Codex (skills only):

```bash
codex plugin marketplace add brunosouzas/agent-skills
codex plugin add mulesoft@brunosouzas-agent-skills   # or api, languages, devops, web, delivery
```

Other tools that read Agent Skills: copy or link `plugins/<plugin>/skills/<skill>/` into the tool's skills folder.

## How a skill is chosen

Each skill's `description` says what it does, when to use it, the words that trigger it and when not to use it, so a tool loads only the skill a request needs: "fix this DataWeave function" loads `dataweave`, a Mule flow loads `mulesoft`. A repository can also name its technologies on a `Stack:` line of its `AGENTS.md` ([docs/agents-md.md](docs/agents-md.md)).

## Versions

Every skill has its own semantic version (`metadata.version` in `SKILL.md`) and `CHANGELOG.md`; a review can cite exactly the rule it applied: "breaks DW-4 (dataweave 1.0.0)". How versions are raised: [CONTRIBUTING.md](CONTRIBUTING.md#versions) and [docs/releasing.md](docs/releasing.md).

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md): the writing rules, the rule format, versions, commit titles and evals.

## License

[Apache-2.0](LICENSE).
