# agent-skills

Specialty skills for AI coding agents, in the open [Agent Skills](https://agentskills.io) format, packaged as plugins for **Claude Code** and **Codex**. A specialty skill knows one technology: its rules (each with a stable ID, a reason and a check), the scripts that check what has one right answer, and when it applies. A specialty does not tell you how your team works. The separate `delivery` plugin is an optional process (change flow, merge gates, delivery models) that reads your repository's `AGENTS.md`; use it, or bring your own.

## Plugins

| Plugin | Skills | For |
|---|---|---|
| [java](plugins/java/README.md) | `java` | Standalone Java applications, libraries and CLIs, and their JUnit tests |
| [python](plugins/python/README.md) | `python` | Python applications, CLIs and scripts with logic, and their tests |
| [shell](plugins/shell/README.md) | `shell` | Bash and POSIX sh scripts, git hooks and pipeline steps |
| [azure-devops](plugins/azure-devops/README.md) | `azure-devops` | Azure Pipelines YAML, templates, variable groups and environments |
| [github-actions](plugins/github-actions/README.md) | `github-actions` | GitHub Actions workflows, reusable workflows and composite actions |
| [jenkins](plugins/jenkins/README.md) | `jenkins` | Jenkinsfiles and Groovy shared libraries |
| [astro](plugins/astro/README.md) | `astro` | Astro static sites |
| [cloudflare](plugins/cloudflare/README.md) | `cloudflare` | Cloudflare Workers and Pages |
| [delivery](plugins/delivery/README.md) | `change-flow`, `merge-gates`, `delivery-models` | The process: plan, review, merge gates and delivery of a change (not a technology) |

Each plugin is what you install together: one technology, one plugin, most holding the skill of the same name (`java:java`, `astro:astro`), and `delivery` holds the three process skills. The MuleSoft and API skills (the former `mulesoft` and `api` plugins) moved to [devFoundry](https://github.com/brunosouzas/devfoundry-plugins), with the same rule IDs. Install only the ones your repositories use.

## Install

Claude Code:

```bash
claude plugin marketplace add brunosouzas/agent-skills
claude plugin install java@brunosouzas-agent-skills   # or python, shell, azure-devops, github-actions, jenkins, astro, cloudflare, delivery
```

From a local clone, pass its path to `claude plugin marketplace add` instead.

Codex (skills only):

```bash
codex plugin marketplace add brunosouzas/agent-skills
codex plugin add java@brunosouzas-agent-skills   # or python, shell, azure-devops, github-actions, jenkins, astro, cloudflare, delivery
```

Other tools that read Agent Skills: copy or link `plugins/<plugin>/skills/<skill>/` into the tool's skills folder.

## How a skill is chosen

Each skill's `description` says what it does, when to use it, the words that trigger it and when not to use it, so a tool loads only the skill a request needs: "fix this Bash script" loads `shell`, a Gradle build loads `java`. A repository can also name its technologies on a `Stack:` line of its `AGENTS.md` ([docs/agents-md.md](docs/agents-md.md)).

## Versions

Every skill has its own semantic version (`metadata.version` in `SKILL.md`) and `CHANGELOG.md`; a review can cite exactly the rule it applied: "breaks JBLD-1 (java 1.0.0)". How versions are raised: [CONTRIBUTING.md](CONTRIBUTING.md#versions) and [docs/releasing.md](docs/releasing.md).

## Related open-source projects

- [brunosouzas-design-system](https://github.com/brunosouzas/brunosouzas-design-system): design tokens and Remotion motion components for a personal site's visual identity.
- [stackledger](https://github.com/brunosouzas/stackledger): a CLI that governs a software stack and its licences from a Git catalogue; the agent skill is in its repository.
- [hermes-daily-reading](https://github.com/brunosouzas/hermes-daily-reading): a plugin for the Hermes agent that builds a daily reading digest from RSS and Atom feeds, ranked by your themes and read aloud.
- [hermes-day-panel](https://github.com/brunosouzas/hermes-day-panel): a plugin for the Hermes agent that adds a Today page to Hermes Desktop from pluggable, read-only sources.
- [hermes-kokoro-tts](https://github.com/brunosouzas/hermes-kokoro-tts): a plugin for the Hermes agent with local Kokoro text-to-speech on Apple Silicon, in nine languages.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md): the writing rules, the rule format, versions, commit titles and evals.

## License

[Apache-2.0](LICENSE).
