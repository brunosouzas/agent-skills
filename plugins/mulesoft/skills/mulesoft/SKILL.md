---
name: mulesoft
description: "Rules and checks for Mule 4 applications: flows, layout, configuration and properties, error handling, logging, Anypoint and CloudHub 2.0 deployment config, API Manager policies and the Maven build. Use when writing, changing or reviewing a Mule 4 application, a flow XML file under src/main/mule/, its global configuration or its properties; recognise it by a pom.xml with mule-application packaging or a mule-artifact.json. Also the integration patterns a flow needs (dead letter, idempotent receiver, correlation identifier, publish-subscribe, circuit breaker), applied when they fit. Triggers: Mule, Mule 4, MuleSoft, Mule flow, APIkit, Anypoint, CloudHub, integration pattern, dead letter, idempotent, circuit breaker. Not for DataWeave scripts on their own (dataweave skill), MUnit tests (munit skill), Mule SDK connectors, shared plugins or DataWeave libraries as assets (mule-sdk skill), the RAML or OpenAPI spec (api-spec skill), or the CI/CD pipeline (azure-devops, github-actions or jenkins skill)."
license: Apache-2.0
metadata:
  version: "1.1.0" # x-release-please-version
  aliases: "mule, mule 4, anypoint, apikit, cloudhub"
---

# MuleSoft

What is particular to Mule 4 application work: flows, layout, configuration, errors, logging, the platform and the build. Other parts of a Mule project have their own skills in this plugin; use them when they are installed:

- DataWeave transforms and `.dwl` files: `dataweave`.
- MUnit suites: `munit`.
- Connectors (Mule SDK), shared Mule plugins and DataWeave libraries as published assets: `mule-sdk`.

## When

- Use for a Mule application (`<packaging>mule-application</packaging>`): new or changed flows, sub-flows, global elements, property files, error handlers, loggers, `mule-artifact.json`, the Mule Maven Plugin's deployment configuration, API Manager policies.
- Not for the API specification itself (RAML, OpenAPI: `api-spec`), the pipeline YAML (`azure-devops`, `github-actions` or `jenkins`), if installed, or the delivery process (releases, promotions, rollbacks), which follows the repository's own process.

## How to work

1. **Know the artifact** from `pom.xml`: `mule-application` (this skill), `mule-plugin`, `mule-extension` or `dw-library` (with `mule-sdk`). Read the Mule runtime and MUnit versions there too.
2. **Build with the toolchain the runtime supports** (BUILD-1): Maven 3.9.x and Java 17 for Mule 4.6 and later, Java 8 or 11 before that. A wrong JDK fails with errors that do not mention Java, so check `java -version` and `mvn -version` first. When the repository says the build runs only in its pipeline (the credentials of a private repository stay there), the pull request's run is the build.
3. **Read before adding.** Read the existing flows, global configuration and property files first. In an existing project, follow its layout and naming and report a difference instead of renaming; in a new one, start from an Anypoint Studio or Code Builder project and use LAYOUT-1, LAYOUT-2, CFG-3 and FLOW-6, and the DataWeave layout of `dataweave` (DW-1, DW-3), if installed.
4. **Apply the integration patterns.** Before writing a flow, list its integration decisions (where a message goes, how a repeat is handled, what happens after a failure, how a reply is matched to its request, how a failing service is avoided). For each one, apply the pattern in [references/eip.md](references/eip.md) only when the flow has the problem it solves and none of its "not when" applies; apply it without the developer asking. Name the pattern in the flow's description (FLOW-4). If the developer names a pattern, apply it under EIP-8.
5. **Name and describe as you build**, not at the end: every processor gets a display name (FLOW-2, FLOW-5) and every flow a description (FLOW-4).
6. **Test every flow change** with an MUnit test (with `munit`, if installed) and every DataWeave function with a test of its own (with `dataweave`, if installed).
7. **Verify:** `mvn clean verify` (runs MUnit and its coverage gate), then run the name check on the changed files:

   ```bash
   python3 <this skill's folder>/scripts/check-docnames.py src/main/mule
   ```

   It lists every processor without `doc:name` or with a palette default name (FLOW-2) and every flow or sub-flow without `doc:description` (FLOW-4), and exits 1 when it finds one. A deploy is never part of verification.

## Rules

Read [rules.md](rules.md) and [references/eip.md](references/eip.md), and follow every rule. Cite a rule by its ID and this skill's version when you apply or break it, for example "breaks MERR-2 (mulesoft 1.0.0)".
