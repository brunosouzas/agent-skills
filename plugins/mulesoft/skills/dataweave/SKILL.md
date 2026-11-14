---
name: dataweave
description: "Rules for DataWeave 2: scripts, modules, functions, types, null handling, pattern matching, dates and numbers, performance and tests. Use when writing, changing, reviewing or explaining a DataWeave transform, a .dwl script or module, a DataWeave library (dw-library) or an isolated DataWeave snippet; recognise it by .dwl files, %dw 2.0 headers or ee:transform elements. Triggers: DataWeave, DataWeave 2, DWL, .dwl, Transform Message script. Not for the Mule flow around a transform, its connectors or error handling (mulesoft skill), MUnit suite structure (munit skill), or publishing a DataWeave library as an asset (mule-sdk skill)."
license: Apache-2.0
metadata:
  version: "1.0.0" # x-release-please-version
  aliases: "dataweave 2, dwl"
---

# DataWeave

What is particular to DataWeave 2 work, inside a Mule application or on its own. When the transform sits in a flow, the flow itself follows `mulesoft`, if installed.

## When

- Use for transforms, `.dwl` scripts and modules, DataWeave libraries and their tests, and a snippet asked about out of context.
- Not for the flow, its connectors or its MUnit structure (`mulesoft` and `munit`, if installed). Not for the API contract (`api-spec`, if installed).

## How to work

1. **Know the inputs and the output.** Read the input's MIME type and shape (an example, the spec's type, the connector's metadata) and the output the contract asks for. With no example, write a minimal synthetic one (DWTEST-2).
2. **Write small, pure functions** (DW-5), typed when they are public (DW-6), in a module when they are reused (DW-1).
3. **Handle absence on purpose:** every optional field gets `default` or a null-safe selector (DW-2), every `match` an `else` (DW-7).
4. **Test** each function and each transform with its edge cases: missing field, empty array, null, a wrong type (DWTEST-1).
5. **Report** what you ran. An isolated snippet you could not run against the real input is reported as not verified, with what would prove it.

## Rules

Read [rules.md](rules.md) and follow every rule. Cite a rule by its ID and this skill's version when you apply or break it, for example "breaks DW-7 (dataweave 1.0.0)".
