# azure-devops plugin

```bash
claude plugin marketplace add brunosouzas/agent-skills
claude plugin install azure-devops@brunosouzas-agent-skills
```

Codex: `codex plugin marketplace add brunosouzas/agent-skills`, then `codex plugin add azure-devops@brunosouzas-agent-skills`.

One skill, loaded from its `description` when a request needs it.

| Skill | For | Rules |
|---|---|---|
| [azure-devops](skills/azure-devops/SKILL.md) | Azure Pipelines YAML, templates, variable groups, environments and checks | ADON, ADO, ADOS, ADOD |

The skill's version is in its `SKILL.md` (`metadata.version`) and its history in its `CHANGELOG.md`. The routing evals are in [evals/](evals/).
