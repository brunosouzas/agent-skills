# python plugin

```bash
claude plugin marketplace add brunosouzas/agent-skills
claude plugin install python@brunosouzas-agent-skills
```

Codex: `codex plugin marketplace add brunosouzas/agent-skills`, then `codex plugin add python@brunosouzas-agent-skills`.

One skill, loaded from its `description` when a request needs it.

| Skill | For | Rules |
|---|---|---|
| [python](skills/python/SKILL.md) | Python applications, CLIs and scripts with logic, and their tests | PENV, PY, PTST |

The skill's version is in its `SKILL.md` (`metadata.version`) and its history in its `CHANGELOG.md`. The routing evals are in [evals/](evals/).
