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
| Mule SDK, Mule extension, Mule connector, mule-plugin, dw-library | `mule-sdk` |

The other plugins:

| Name on the line | Skill |
|---|---|
| RAML, OpenAPI, OAS, Swagger | `api-spec` |
| Java, JDK, JUnit, Gradle, Maven, Spring Boot | `java` |
| Python, Python 3, pytest | `python` |
| Shell, Bash, sh, zsh, POSIX sh | `shell` |
| Azure DevOps, Azure Pipelines, ADO | `azure-devops` |
| GitHub Actions, GitHub workflows, GHA | `github-actions` |
| Jenkins, Jenkinsfile, Groovy | `jenkins` |
| Astro | `astro` |
| Cloudflare, Cloudflare Workers, Cloudflare Pages, Wrangler | `cloudflare` |

Without a `Stack:` line, each skill's `description` still routes the request by what the files look like (a `pom.xml` with `mule-application` packaging, a `.dwl` file).
