# github-actions plugin

```bash
claude plugin marketplace add brunosouzas/agent-skills
claude plugin install github-actions@brunosouzas-agent-skills
```

Codex: `codex plugin marketplace add brunosouzas/agent-skills`, then `codex plugin add github-actions@brunosouzas-agent-skills`.

One skill, loaded from its `description` when a request needs it.

| Skill | For | Rules |
|---|---|---|
| [github-actions](skills/github-actions/SKILL.md) | GitHub Actions workflows, reusable workflows and composite actions | GHAS, GHA, GHAD |

The skill's version is in its `SKILL.md` (`metadata.version`) and its history in its `CHANGELOG.md`. The routing evals are in [evals/](evals/).
