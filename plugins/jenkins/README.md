# jenkins plugin

```bash
claude plugin marketplace add brunosouzas/agent-skills
claude plugin install jenkins@brunosouzas-agent-skills
```

Codex: `codex plugin marketplace add brunosouzas/agent-skills`, then `codex plugin add jenkins@brunosouzas-agent-skills`.

One skill, loaded from its `description` when a request needs it.

| Skill | For | Rules |
|---|---|---|
| [jenkins](skills/jenkins/SKILL.md) | Jenkinsfiles and Groovy shared libraries | JNK, JNKS |

The skill's version is in its `SKILL.md` (`metadata.version`) and its history in its `CHANGELOG.md`. The routing evals are in [evals/](evals/).
