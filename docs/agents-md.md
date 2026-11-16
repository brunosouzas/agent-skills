# The AGENTS.md lines these skills read

A skill in this repository works in any repository. It reads a few lines of that repository's `AGENTS.md` (or `CLAUDE.md`) when they are there, and works without them when they are not. This page lists every line any skill reads; a skill that starts reading a new line adds it here in the same pull request. The specialty skills read only `Stack:`; the `delivery` plugin reads the [process lines](#the-process-lines-delivery-plugin).

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

The other plugins, one per technology (each holds the skill of the same name, except `api`, which holds `api-spec`):

| Name on the line | Plugin and skill |
|---|---|
| RAML, OpenAPI, OAS, Swagger | `api`: `api-spec` |
| Java, JDK, JUnit, Gradle, Maven, Spring Boot | `java`: `java` |
| Python, Python 3, pytest | `python`: `python` |
| Shell, Bash, sh, zsh, POSIX sh | `shell`: `shell` |
| Azure DevOps, Azure Pipelines, ADO | `azure-devops`: `azure-devops` |
| GitHub Actions, GitHub workflows, GHA | `github-actions`: `github-actions` |
| Jenkins, Jenkinsfile, Groovy | `jenkins`: `jenkins` |
| Astro | `astro`: `astro` |
| Cloudflare, Cloudflare Workers, Cloudflare Pages, Wrangler | `cloudflare`: `cloudflare` |

Without a `Stack:` line, each skill's `description` still routes the request by what the files look like (a `pom.xml` with `mule-application` packaging, a `.dwl` file).

## The process lines (`delivery` plugin)

The skills of the `delivery` plugin read these lines. A missing line is filled in this order: the repository's `AGENTS.md`, then the user's own instructions (a user-level `CLAUDE.md` or `AGENTS.md`), then the strictest reading, named in the session plan. A line the agent adds or changes counts only once its pull request is merged (merge-gates GATE-7).

```markdown
## Technology

Stack: Python, GitHub Actions
Spec: OpenSpec
Delivery: D local
Model: 4 install locally
Integration branch: `main`
Data: `feeds.yaml`
Tracker: GitHub Issues acme/tool
Approver: @acme/maintainers
- Deliver and verify: `pipx install --force .`; verify with `tool --version`
```

| Line | Values | Read by | Gate line |
|---|---|---|---|
| `Spec:` | the spec tool (`OpenSpec`), or `none` (every change takes the small path) | `change-flow` (SIZE, SPEC), `merge-gates` | yes |
| `Delivery:` | `A live`, `B package`, `C environments`, `D local`, `E reference`: where a merged change goes while the repository has no `Model:` line | `delivery-models`, `merge-gates` | yes |
| `Model:` | `1 GitFlow release`, `2 release PR`, `3 continuous delivery with staging`, `4 install locally`, `reference`; another value is read from the repository's delivery documentation | `delivery-models`, `merge-gates` | yes |
| `Integration branch:` | the branch changes start from and merge into (`develop` in model 1, otherwise `main`) | `change-flow` (CHG-1), `merge-gates` | yes |
| `Data:` | paths that are data lists, changed without an independent review (never skills, prompts or configuration), or `none` | `change-flow` (REV-4), `merge-gates` | yes |
| `Tracker:` | `Azure Boards <organisation>/<project>, area <area>`, `GitHub Issues <owner>/<repository>`, `Jira <site>, project <KEY>`, or `none` | `change-flow` (TRK) | no |
| `Approver:` | the person or team who approves level 2 actions, as the forge names them (`login` or `@login`, `@org/team`) | `merge-gates` (GATE-1) | yes |
| `Deliver and verify:` | what runs after a merge and the check that it worked | `delivery-models`, `change-flow` (S6) | no |

A gate line decides which merge gate applies, so changing it is always a level 2 change (merge-gates GATE-3). The checks (`Build:`, `Test:`) are the commands the repository lists; `change-flow` runs them in S1.
