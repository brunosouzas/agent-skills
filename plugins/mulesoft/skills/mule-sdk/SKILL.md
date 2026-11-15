---
name: mule-sdk
description: "Rules for shared Mule 4 assets that other applications depend on: connectors built with the Mule SDK (Java SDK), shared Mule plugins (mule-plugin packaging) and DataWeave libraries published to Exchange or a Maven repository. Covers the public contract of exported operations and functions, semantic versioning of the asset, and connection management in connectors. Use when writing, changing or reviewing such an asset; recognise it by a pom.xml with mule-extension, mule-plugin or dw-library packaging, or @Extension and @Operations classes. Triggers: Mule SDK, Mule extension, Mule connector, custom connector, shared Mule plugin, mule-plugin packaging, dw-library. Not for a Mule application or the Mule Maven Plugin's deployment configuration (mulesoft skill), the DataWeave code inside a library (dataweave skill) or a standalone Java library with no Mule packaging (java skill)."
license: Apache-2.0
metadata:
  version: "1.0.1" # x-release-please-version
  aliases: "mule sdk, mule extension, mule connector, mule-plugin, dw-library"
---

# Mule SDK and shared assets

What is particular to Mule 4 assets that applications depend on: connectors (Mule SDK), shared Mule plugins and DataWeave libraries. What makes them different from an application is that their exported surface is a contract: every consumer breaks when it changes. The DataWeave code of a library follows `dataweave`, and the build toolchain follows `mulesoft` BUILD-1, if they are installed.

## When

- Use for a `pom.xml` with `<packaging>mule-extension</packaging>` (a connector), `mule-plugin` (a shared plugin of flows or configuration) or `dw-library` (a DataWeave library built with the `data-weave-maven-plugin`).
- Not for a Mule application (`mulesoft`), and not for a plain Java library (`java`), if installed.

## How to work

1. **Know the asset and its consumers.** Read the packaging and the current version in `pom.xml`, and find which applications depend on it before changing an exported operation, function or parameter.
2. **Decide the version first** (ASSET-1): a removed or changed exported signature is a new major version; a new operation or function is a minor one.
3. **Keep connections in the provider** (ASSET-2): an operation receives the connection as a parameter and never opens one.
4. **Build with the toolchain the Mule plugins support:** Maven 3.9.x and the JDK of the target runtime. Maven 3.10 breaks `mule-extensions-maven-plugin` with `NoSuchMethodError`.
5. **Verify:** `mvn clean verify` on the asset, then build one consumer against the new version before publishing.

## Rules

Read [rules.md](rules.md) and follow every rule. Cite a rule by its ID and this skill's version when you apply or break it, for example "breaks ASSET-1 (mule-sdk 1.0.0)".
