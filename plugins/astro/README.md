# astro plugin

```bash
claude plugin marketplace add brunosouzas/agent-skills
claude plugin install astro@brunosouzas-agent-skills
```

Codex: `codex plugin marketplace add brunosouzas/agent-skills`, then `codex plugin add astro@brunosouzas-agent-skills`.

One skill, loaded from its `description` when a request needs it.

| Skill | For | Rules |
|---|---|---|
| [astro](skills/astro/SKILL.md) | Astro static sites: pages, layouts, components, content, build | AST, ASB, ASD |

The skill's version is in its `SKILL.md` (`metadata.version`) and its history in its `CHANGELOG.md`. The routing evals are in [evals/](evals/).
