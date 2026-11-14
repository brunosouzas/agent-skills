# devops plugin

```bash
claude plugin marketplace add brunosouzas/agent-skills
claude plugin install devops@brunosouzas-agent-skills
```

Codex: `codex plugin marketplace add brunosouzas/agent-skills`, then `codex plugin add devops@brunosouzas-agent-skills`.

Skills for CI/CD pipelines. Each one loads on its own, from its `description`, so a request loads only the skill it needs.

| Skill | For | Rules |
|---|---|---|
| [azure-devops](skills/azure-devops/SKILL.md) | Azure Pipelines YAML, templates, variable groups, environments and checks | ADON, ADO, ADOS, ADOD |
| [github-actions](skills/github-actions/SKILL.md) | GitHub Actions workflows, reusable workflows and composite actions | GHAS, GHA, GHAD |
| [jenkins](skills/jenkins/SKILL.md) | Jenkinsfiles and Groovy shared libraries | JNK, JNKS |

Each skill's version is in its `SKILL.md` (`metadata.version`) and its history in its `CHANGELOG.md`. The routing evals are in [evals/](evals/).
