# mulesoft plugin

> **Deprecated.** These skills moved to [devFoundry](https://github.com/brunosouzas/devfoundry-plugins) (marketplace `devfoundry`), which keeps their rule IDs and adds verified Mule examples, a project profile and API-first implementation. Install it instead: `claude plugin marketplace add brunosouzas/devfoundry-plugins`, then `claude plugin install mule-engineering@devfoundry`. This plugin gets no new rules and will be removed from this marketplace.

Where each skill went: `mulesoft` → `mule-engineering:mule-app` (and `apikit`); `dataweave` → `mule-engineering:dataweave`; `munit` → `mule-engineering:munit`; `mule-sdk` → `mule-engineering:mule-sdk`. The naming rules FLOW-5, FLOW-6 and DW-3 and the deploy rules PLAT-1, PLAT-3 to PLAT-5 are not in devFoundry: they belong to a project's or a company's own conventions and delivery.

```bash
claude plugin marketplace add brunosouzas/agent-skills
claude plugin install mulesoft@brunosouzas-agent-skills
```

Codex: `codex plugin marketplace add brunosouzas/agent-skills`, then `codex plugin add mulesoft@brunosouzas-agent-skills`.

Skills for Mule 4 work. Each one loads on its own, from its `description`, so a DataWeave question loads only `dataweave`.

| Skill | For | Rules |
|---|---|---|
| [mulesoft](skills/mulesoft/SKILL.md) | Mule 4 applications: flows, layout, configuration, errors, logging, platform, build, and the integration patterns applied in them | FLOW, LAYOUT, CFG, MERR, MLOG, PLAT, BUILD, EIP patterns (references/eip.md) |
| [dataweave](skills/dataweave/SKILL.md) | DataWeave 2 scripts, modules, libraries and their tests | DW, DWTEST |
| [munit](skills/munit/SKILL.md) | MUnit tests of Mule 4 applications | MUNIT |
| [mule-sdk](skills/mule-sdk/SKILL.md) | Connectors (Mule SDK), shared Mule plugins and DataWeave libraries as published assets | ASSET |

Each skill's version is in its `SKILL.md` (`metadata.version`) and its history in its `CHANGELOG.md`. The routing evals are in [evals/](evals/).

## Patterns in Mule 4: articles and example

The EIP rules of the `mulesoft` skill (`references/eip.md`) say what each pattern solves and how to build and test it in Mule 4. The article explains the same pattern at length, with a runnable example; the examples repository holds the flows and the MUnit tests.

- Catalog of the patterns and the Mule component of each: https://brunosouzas.com/wiki/eip-catalog-in-mulesoft/
- Dead Letter Channel: https://brunosouzas.com/wiki/dead-letter-channel-in-mulesoft/
- Idempotent Receiver: https://brunosouzas.com/wiki/idempotent-receiver-in-mulesoft/
- Correlation Identifier: https://brunosouzas.com/wiki/correlation-identifier-in-mulesoft/
- Publish-Subscribe Channel: https://brunosouzas.com/wiki/publish-subscribe-in-mulesoft/
- Circuit Breaker: https://brunosouzas.com/blog/circuit-breaker-in-mulesoft/
- Examples: https://github.com/brunosouzas/mulesoft-patterns-examples
