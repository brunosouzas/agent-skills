# web plugin

```bash
claude plugin marketplace add brunosouzas/agent-skills
claude plugin install web@brunosouzas-agent-skills
```

Codex: `codex plugin marketplace add brunosouzas/agent-skills`, then `codex plugin add web@brunosouzas-agent-skills`.

Skills for websites and the edge that serves them. Each one loads on its own, from its `description`, so a request loads only the skill it needs.

| Skill | For | Rules |
|---|---|---|
| [astro](skills/astro/SKILL.md) | Astro static sites: pages, layouts, components, content, build | AST, ASB, ASD |
| [cloudflare](skills/cloudflare/SKILL.md) | Cloudflare Workers and Pages deploys | CFL, CFW, CFD, CFB, CFR |

Each skill's version is in its `SKILL.md` (`metadata.version`) and its history in its `CHANGELOG.md`. The routing evals are in [evals/](evals/).
