# The AGENTS.md lines these skills read

A skill in this repository works in any repository. It reads a few lines of that repository's `AGENTS.md` (or `CLAUDE.md`) when they are there, and works without them when they are not. This page lists every line any skill reads; a skill that starts reading a new line adds it here in the same pull request.

## `Stack:`

The technologies the repository is made of, by their usual names, comma-separated:

```markdown
## Technology

Stack: Mule 4, MUnit, DataWeave, Azure Pipelines
```

An agent loads the skill whose `name` or one of whose `metadata.aliases` matches each name, ignoring case. For the `mulesoft` plugin:

| Name on the line | Skill |
|---|---|
| MuleSoft, Mule, Mule 4, Anypoint, APIkit, CloudHub | `mulesoft` |
| DataWeave, DataWeave 2, DWL | `dataweave` |
| MUnit, MUnit 3, MUnit Tools | `munit` |
| Mule SDK, Mule extension, Mule connector, Mule plugin, dw-library | `mule-sdk` |

Without a `Stack:` line, each skill's `description` still routes the request by what the files look like (a `pom.xml` with `mule-application` packaging, a `.dwl` file).
