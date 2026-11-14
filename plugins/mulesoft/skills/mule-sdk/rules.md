# Mule SDK and shared assets: rules

Rules for Mule 4 connectors, shared Mule plugins and DataWeave libraries, from the Mule SDK documentation and semantic versioning. In an existing asset, follow the conventions it already uses and report a difference instead of renaming.

How to change this file (see CONTRIBUTING.md of this repository):
- **Add a rule:** copy an item, give it the next number in its group, write the rule, why it exists and how to check it. A new rule is a MINOR version.
- **Change a rule:** edit it in place and keep its ID, so old reviews still point at the right rule. A rule that now says the opposite is a MAJOR version; clearer wording is a PATCH.
- **Retire a rule:** keep its ID and heading, replace the text with `(retired in <version>: <reason>)`, and never reuse the number. A retired rule is a MAJOR version.

## Shared assets (ASSET)

- **ASSET-1** Treat exported operations, functions and their parameters as a public contract: a breaking change bumps the major version.
  Why: every application that depends on the asset breaks on upgrade.
  Check: changed signatures come with a version bump in `pom.xml`.

- **ASSET-2** A connector built with the Mule SDK keeps connection management in its connection provider and exposes only the operations it needs.
  Why: connection handling in operations leaks connections and cannot be pooled.
  Check: operations receive the connection as a parameter.
