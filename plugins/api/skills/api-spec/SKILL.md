---
name: api-spec
description: "Rules for REST API specifications in RAML 1.0 or OpenAPI 3: resources and methods, data types, error responses, examples, versioning and security schemes. Use when writing, changing or reviewing an API contract from its requirements: a *.raml file, an openapi.yaml or openapi.json, their types, examples, traits and shared fragments, or an exchange.json with a rest-api classifier. Triggers: RAML, OpenAPI, OAS, Swagger, API spec, API contract, API design. Not for deciding what the API must do (the requirements come first), implementing it in a Mule flow (mulesoft skill), or the DataWeave that maps its payloads (dataweave skill)."
license: Apache-2.0
metadata:
  version: "1.1.0" # x-release-please-version
  aliases: "raml, openapi, oas, swagger"
---

> **Deprecated:** this skill moved to devFoundry as `api-contracts:api-contract` (the `devfoundry` marketplace; see this plugin's README), with the same rule IDs. It still works, gets no new rules, and will be removed.

# API spec

What is particular to writing a REST API contract. The requirements (what the API must do, its scenarios) come before the spec; this skill turns them into it. The implementation follows `mulesoft` or the language's skill, if installed.

## When

- Use for RAML 1.0 and OpenAPI 3 specifications, their data types, examples, traits and shared fragments.
- Not for deciding what the API should do. Not for implementing it: a Mule implementation follows `mulesoft` with this skill, if installed.

## How to work

1. Start from the requirements or their scenarios; each operation in the spec answers one of them.
2. Reuse what exists: shared data types, traits, security schemes and error responses from the project or its published fragments.
3. Write examples for every request and response, including the errors (CON-3).
4. Verify: the spec parses and validates with the project's tool (Anypoint API Designer, `raml-cop`, `@redocly/cli lint`, or the Maven plugin the project uses), and the examples validate against their types.

## Rules

Read [rules.md](rules.md) and follow every rule. Cite a rule by its ID and this skill's version when you apply or break it, for example "breaks CON-2 (api-spec 1.0.0)".
