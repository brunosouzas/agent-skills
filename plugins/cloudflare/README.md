# cloudflare plugin

```bash
claude plugin marketplace add brunosouzas/agent-skills
claude plugin install cloudflare@brunosouzas-agent-skills
```

Codex: `codex plugin marketplace add brunosouzas/agent-skills`, then `codex plugin add cloudflare@brunosouzas-agent-skills`.

One skill, loaded from its `description` when a request needs it.

| Skill | For | Rules |
|---|---|---|
| [cloudflare](skills/cloudflare/SKILL.md) | Cloudflare Workers and Pages deploys | CFL, CFW, CFD, CFB, CFR |

The skill's version is in its `SKILL.md` (`metadata.version`) and its history in its `CHANGELOG.md`. The routing evals are in [evals/](evals/).
