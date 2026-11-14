# MuleSoft: rules

Rules for Mule 4 applications, from MuleSoft's published best practices (Catalyst *Mule Development Standards*), the platform's documented behaviour and practice in reference projects. In an existing project, follow the conventions it already uses and report a difference instead of renaming; these rules decide new projects and new files. A rule marked `(locked)` protects secrets, personal data or sensitive logs: a project's own convention never overrides it.

Rules for the other parts of a Mule project live in their own skills, with their own IDs: DataWeave (`DW`, `DWTEST`) in `dataweave`, MUnit (`MUNIT`) in `munit`, shared assets (`ASSET`) in `mule-sdk`.

How to change this file (see CONTRIBUTING.md of this repository):
- **Add a rule:** copy an item, give it the next number in its group, write the rule, why it exists and how to check it. A new rule is a MINOR version.
- **Change a rule:** edit it in place and keep its ID, so old reviews still point at the right rule. A rule that now says the opposite is a MAJOR version; clearer wording is a PATCH.
- **Retire a rule:** keep its ID and heading, replace the text with `(retired in <version>: <reason>)`, and never reuse the number. A retired rule is a MAJOR version.

## Flows (FLOW)

- **FLOW-1** Keep the API layer thin: the APIkit flows route and validate; business logic lives in private flows or subflows named after what they do.
  Why: the generated flows mirror the spec; logic inside them gets duplicated across operations and is hard to find and test.
  Check: APIkit flows contain only a flow reference (and maybe a transform).

- **FLOW-2** Every processor and scope has an explicit `doc:name` that says what it does; never a missing name, never the palette default (`Transform Message`, `Set Variable`, `Logger`, `Try`, `Choice`, `Scatter-Gather`). Patterns per type: FLOW-5.
  Why: the Studio canvas, logs and Anypoint Monitoring show these names; a flow of unnamed `Set Variable` and `Choice` boxes can only be read by opening each one. A missing `doc:name` is as bad as a default one: Studio shows the component type.
  Check: in `src/main/mule/**/*.xml`, every child of `flow`, `sub-flow`, `try`, `when`, `otherwise`, `foreach`, `route`, `on-error-*` and `until-successful` has `doc:name`, except value elements (`ee:message`, `ee:variables`, `http:headers`, `http:body` and similar), and none equals its palette default. `scripts/check-docnames.py` checks this.

- **FLOW-3** Global elements (listeners, requesters, connectors) are defined once in the global configuration file (LAYOUT-2) and referenced by name; their display name is `<Purpose> <Type> Config` (`Main Http Listener Config`, `Secure Properties Config`).
  Why: duplicated configs drift apart and multiply connection pools.
  Check: new global elements live in the global configuration file and their `doc:name` ends in `Config`.

- **FLOW-4** Every flow and sub-flow has a one-sentence description in `doc:description` (Studio's Notes tab): what it does and when it is called.
  Why: the name says what, the note says why and from where; it is the first thing a maintainer reads.
  Check: no `flow` or `sub-flow` without `doc:description`; `scripts/check-docnames.py` checks this.

- **FLOW-5** Display names start with a fixed word per type: Set Variable `SET v<Name>` (variables are `v` + camelCase: `SET vCustomerId`), Logger `<LEVEL>: Log …` (`DEBUG: Log CRM Query`), Flow Reference `Refer to <flow-name>`, Raise Error `Raise <Type> Error - <reason>`, Try `Try …`, error handlers `On Error Propagate (<case>)`. Everything else is verb + object (`Build CRM Request`, `Query CRM Accounts`, `For Each Order Line`, `Validate Customer Exists`). APIkit-generated names stay as generated.
  Why: one shape per type makes names predictable to write and to search; the type is visible on the box, so the name adds the purpose.
  Check: Set Variable, Logger, Flow Reference, Raise Error, Try and error-handler names start with their fixed word.

- **FLOW-6** Flow names are kebab-case and say what the flow does: the main flow is `<api-name>-main`, sub-flows start with `sf-`, flows shared across the application start with `common-`, other flows are plain kebab-case; APIkit-generated flows keep their generated names.
  Why: the prefix groups flows in Studio's lists and autocomplete and shows at once whether a flow is an entry point, private or shared; renaming an APIkit flow breaks routing.
  Check: hand-written `sub-flow` names start with `sf-` or `common-`; all flow names are kebab-case.

## Layout (LAYOUT)

- **LAYOUT-1** For a Mule application: one application per project, created from Anypoint Studio or Code Builder (or an official template). Test helpers that are applications of their own are separate projects, never nested inside another application's folder.
  Why: Studio imports one project per folder, and a Mule developer expects to open the application directly; an aggregator or a nested application needs manual setup.
  Check: the application folder has `pom.xml` with `mule-application` packaging and `mule-artifact.json`, and no other Mule project below it.

- **LAYOUT-2** `src/main/mule/` holds `<api-name>-main.xml` (listener or APIkit router), `common/` (`global-config.xml`, `common-error.xml` and shared `common-*.xml` flows) and `impl/` (one `<resource>-impl.xml` per API resource or use case).
  Why: a maintainer finds the entry point, the shared configuration and each use case without searching.
  Check: new flow files go into these folders; no flow files loose next to `<api-name>-main.xml`.

## Configuration (CFG)

- **CFG-1** Every environment-specific value (host, port, path, timeout, client id) is a property, read from a per-environment file or from runtime properties; nothing environment-specific is hard-coded in XML.
  Why: the same artifact must run in every environment.
  Check: search the XML for hosts, ports and URLs.

- **CFG-2** (locked) Secrets live in secure properties (encrypted) or the secret store, read with `secure::`; never in plain property files or in git. List in `secureProperties` in `mule-artifact.json` the decryption-key property and every secret supplied as a Runtime Manager property, so Runtime Manager shows them masked.
  Why: property files are packaged inside the artifact; Runtime Manager shows unlisted properties in clear text.
  Check: secret keys are referenced with `secure::`; no plain secret values in `src/main/resources`; `secureProperties` contains the decryption-key property name.

- **CFG-3** Properties live in `src/main/resources/properties/`: `config.yaml` holds what is common to all environments; keys are hierarchical camelCase (`crm.retry.maxCount`). What differs per environment comes either from `config-<env>.yaml` and `secure-<env>.yaml`, one pair per environment, or from runtime properties that the deploy sets; the project's delivery decides which, and never both for one key.
  Why: one predictable place per value; a key set in a file and again at deploy has two owners, and nobody knows which one won.
  Check: with per-environment files, they exist for each target environment; with runtime properties, no `config-<env>.yaml` exists and each such key is named in the deploy's configuration.

## Errors (MERR)

- **MERR-1** Handle errors with a global error handler, plus local `on-error-continue`/`on-error-propagate` only where the flow needs a specific response.
  Why: one place defines the error contract; scattered handlers return inconsistent errors.
  Check: the application references a global error handler.

- **MERR-2** Map each error type to the HTTP status and body the API spec defines; never return a raw Mule error message to the caller.
  Why: internal messages leak implementation detail and break the contract.
  Check: the error responses match the spec's error types.

## Logging (MLOG)

- **MLOG-1** Log through a structured logger (JSON Logger published to your Exchange, the shared logger the project already uses, or a JSON layout in the application's own `src/main/resources/log4j2.xml`); log the correlation id at the start and end of each inbound flow, and on every error.
  Why: the correlation id is the only way to follow one call across APIs, and structured entries can be searched by it in the log platform.
  Check: the listener flows log `correlationId` at entry, exit and in the error handler; no core `<logger>` in new flows unless `log4j2.xml` gives it a JSON layout.

- **MLOG-2** (locked) Never log full payloads or personal data at INFO; log identifiers.
  Why: logs are retained and read widely.
  Check: no `#[payload]` in INFO loggers.

## Platform (PLAT)

- **PLAT-1** No organisation ID, business group ID, environment ID or API instance ID in the repository: the `groupId` is the canonical one the project chose, and every platform ID arrives at deploy time (`api.id` for autodiscovery included).
  Why: an Exchange `groupId` must equal the organisation ID, which changes when an account is recreated; a literal ID turns that into a code change and binds the artifact to one organisation.
  Check: no UUID in `pom.xml`, `src/main/resources` or `mule-artifact.json`; autodiscovery reads `${api.id}`.

- **PLAT-2** A spec the application implements is a Maven dependency (classifier `raml` or `oas`, type `zip`) and the APIkit configuration names it as `resource::<groupId>:<assetId>:<version>:<classifier>:zip:<file>`; the spec's `assetId` differs from the application's `artifactId`.
  Why: the router reads the spec as an artifact by its coordinates, so the application builds against one versioned contract, whether the build installs it from the source tree or downloads it from Exchange; equal coordinates make the spec and the application overwrite each other on Exchange.
  Check: `apikit:config` uses `resource::`; the spec's `exchange.json` `assetId` is not the POM's `artifactId`.

- **PLAT-3** An application deployed to CloudHub 2.0 answers `GET /health` with 200 outside the API spec and the APIkit router, without calling any backend, and no policy limits that path.
  Why: the deploy's verification calls it; a health check behind the router depends on the spec, one that calls a backend fails when the backend does, and a rate limit on it makes a verification fail under load.
  Check: a flow with its own listener path `/health`; the API's policy pointcut, if any, excludes it.

- **PLAT-4** An API Manager policy is applied only in a version that has a Mule 4 implementation (the asset holds a `mule-policy` jar, or an `<asset>-mule` version depends on it); Flex Gateway-only versions are refused.
  Why: on a Mule 4 runtime a Flex-only policy does not load, the gatekeeper keeps blocking the API, and the deploy's verification times out with no error that names the policy (`rate-limiting` 1.4.2 and 1.5.x are Flex-only; 1.4.1 has `rate-limiting-mule`).
  Check: every policy version in the project's policy file has a Mule 4 implementation on Exchange.

- **PLAT-5** The application receives only the properties listed in the `cloudhub2Deployment` configuration of the Mule Maven Plugin (`properties` and `secureProperties`); a property the code reads must be listed there or in the property files.
  Why: CloudHub 2.0 passes nothing else, so an unlisted property is silently empty at runtime.
  Check: every `${...}` the XML reads that is not in a property file is listed in `cloudhub2Deployment`.

## Build (BUILD)

- **BUILD-1** Build with Maven 3.9.x, the JDK the runtime supports (17 for Mule 4.6 and later) and a pinned LTS runtime version; never Maven 3.10 with the Mule plugins.
  Why: Maven 3.10 breaks `mule-extensions-maven-plugin` with `NoSuchMethodError`, and a wrong JDK fails with errors that do not mention Java.
  Check: the pipeline and the wrapper pin Maven 3.9.x and Java 17; the runtime version is explicit.

- **BUILD-2** The POM has a `<name>`, and the dependencies outside test scope have no known vulnerability: upgrade the library that brings one (APIkit 1.13.4 or later instead of 1.11.x, which brings old jackson, guava and rhino), or pin the fixed version in `dependencyManagement`; never drop the scan.
  Why: publishing to Exchange fails after the whole test run on a missing `name` ("Property name is required"); a vulnerable transitive dependency ships with the application.
  Check: `<name>` present; the dependency scan of the pipeline passes without exclusions.

