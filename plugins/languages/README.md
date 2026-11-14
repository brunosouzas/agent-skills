# languages plugin

```bash
claude plugin marketplace add brunosouzas/agent-skills
claude plugin install languages@brunosouzas-agent-skills
```

Codex: `codex plugin marketplace add brunosouzas/agent-skills`, then `codex plugin add languages@brunosouzas-agent-skills`.

Skills for general-purpose languages. Each one loads on its own, from its `description`, so a request loads only the skill it needs.

| Skill | For | Rules |
|---|---|---|
| [java](skills/java/SKILL.md) | Standalone Java applications, libraries and CLIs, and their JUnit tests | JBLD, JAVA, JTST |
| [python](skills/python/SKILL.md) | Python applications, CLIs and scripts with logic, and their tests | PENV, PY, PTST |
| [shell](skills/shell/SKILL.md) | Bash and POSIX sh scripts, git hooks, installers and pipeline steps | SH, SHP, SHI |

Each skill's version is in its `SKILL.md` (`metadata.version`) and its history in its `CHANGELOG.md`. The routing evals are in [evals/](evals/).
