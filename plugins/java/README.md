# java plugin

```bash
claude plugin marketplace add brunosouzas/agent-skills
claude plugin install java@brunosouzas-agent-skills
```

Codex: `codex plugin marketplace add brunosouzas/agent-skills`, then `codex plugin add java@brunosouzas-agent-skills`.

One skill, loaded from its `description` when a request needs it.

| Skill | For | Rules |
|---|---|---|
| [java](skills/java/SKILL.md) | Standalone Java applications, libraries and CLIs, and their JUnit tests | JBLD, JAVA, JTST |

The skill's version is in its `SKILL.md` (`metadata.version`) and its history in its `CHANGELOG.md`. The routing evals are in [evals/](evals/).
