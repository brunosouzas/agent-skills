# shell plugin

```bash
claude plugin marketplace add brunosouzas/agent-skills
claude plugin install shell@brunosouzas-agent-skills
```

Codex: `codex plugin marketplace add brunosouzas/agent-skills`, then `codex plugin add shell@brunosouzas-agent-skills`.

One skill, loaded from its `description` when a request needs it.

| Skill | For | Rules |
|---|---|---|
| [shell](skills/shell/SKILL.md) | Bash and POSIX sh scripts, git hooks, installers and pipeline steps | SH, SHP, SHI |

The skill's version is in its `SKILL.md` (`metadata.version`) and its history in its `CHANGELOG.md`. The routing evals are in [evals/](evals/).
