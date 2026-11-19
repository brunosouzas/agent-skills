# api plugin

> **Deprecated.** These skills moved to [devFoundry](https://github.com/brunosouzas/devfoundry-plugins) (marketplace `devfoundry`), which keeps their rule IDs and adds verified Mule examples, a project profile and API-first implementation. Install it instead: `claude plugin marketplace add brunosouzas/devfoundry-plugins`, then `claude plugin install api-contracts@devfoundry`. This plugin gets no new rules and will be removed from this marketplace.

Where each skill went: `api-spec` → `api-contracts:api-contract`, with the same RES, CON and APISEC rules.

```bash
claude plugin marketplace add brunosouzas/agent-skills
claude plugin install api@brunosouzas-agent-skills
```

Codex: `codex plugin marketplace add brunosouzas/agent-skills`, then `codex plugin add api@brunosouzas-agent-skills`.

Skills for API contracts. Each one loads on its own, from its `description`, so a request loads only the skill it needs.

| Skill | For | Rules |
|---|---|---|
| [api-spec](skills/api-spec/SKILL.md) | REST API specifications in RAML 1.0 and OpenAPI 3 | RES, CON, APISEC |

Each skill's version is in its `SKILL.md` (`metadata.version`) and its history in its `CHANGELOG.md`. The routing evals are in [evals/](evals/).
