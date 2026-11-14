# mulesoft plugin

```bash
/plugin install mulesoft --marketplace brunosouzas/agent-skills
```

Skills for Mule 4 work. Each one loads on its own, from its `description`, so a DataWeave question loads only `dataweave`.

| Skill | For | Rules |
|---|---|---|
| [mulesoft](skills/mulesoft/SKILL.md) | Mule 4 applications: flows, layout, configuration, errors, logging, platform, build | FLOW, LAYOUT, CFG, MERR, MLOG, PLAT, BUILD |
| [dataweave](skills/dataweave/SKILL.md) | DataWeave 2 scripts, modules, libraries and their tests | DW, DWTEST |
| [munit](skills/munit/SKILL.md) | MUnit tests of Mule 4 applications | MUNIT |
| [mule-sdk](skills/mule-sdk/SKILL.md) | Connectors (Mule SDK), shared Mule plugins and DataWeave libraries as published assets | ASSET |

Each skill's version is in its `SKILL.md` (`metadata.version`) and its history in its `CHANGELOG.md`. The routing evals are in [evals/](evals/).
