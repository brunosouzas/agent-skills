---
name: munit
description: "Rules for MUnit 3 tests of Mule 4 applications: what a test asserts, mocking outbound calls, error-path tests, the coverage gate and APIkit router suites. Use when writing, changing, reviewing or fixing an MUnit test or suite under src/test/munit/, or when an MUnit run fails; recognise it by munit:test, munit-tools:mock-when or the munit-maven-plugin in a pom.xml. Triggers: MUnit, MUnit test, MUnit suite, mock-when, assert-that, Mule test coverage. Not for the flow under test itself (mulesoft skill), the DataWeave inside it (dataweave skill), or tests of a standalone DataWeave library run by the DataWeave testing framework (dataweave skill)."
license: Apache-2.0
metadata:
  version: "1.1.0" # x-release-please-version
  aliases: "munit 3, munit tools"
---

> **Deprecated:** this skill moved to devFoundry as `mule-engineering:munit` (the `devfoundry` marketplace; see this plugin's README), with the same rule IDs. It still works, gets no new rules, and will be removed.

# MUnit

What is particular to testing Mule 4 applications with MUnit. The flow under test follows `mulesoft`, and the DataWeave in its inputs and assertions follows `dataweave`, if they are installed.

## When

- Use for MUnit suites (`src/test/munit/*.xml`), their test resources (`src/test/resources/`), the `munit-maven-plugin` configuration and a failing MUnit run.
- Not for the flow's own code, and not for the DataWeave testing framework of a standalone DataWeave library.

## How to work

1. **Start from the scenario.** Each test proves one scenario of the change: name it after the scenario, and decide first which payload, variables and status prove it (MUNIT-1).
2. **Mock every outbound call** with `munit-tools:mock-when`, matched by the processor's `doc:name` or its attributes; a test never reaches a real system.
3. **Keep inputs in files** under `src/test/resources/`, synthetic and minimal, never a real payload.
4. **Cover the error paths:** one test per mapped error type, triggered by a mock that raises it (MUNIT-2).
5. **For an APIkit API**, call the router through the listener flow and enable every flow the scenario reaches (MUNIT-4).
6. **Verify:** `mvn clean verify` runs the suites and the coverage gate (MUNIT-3). Read a failure's cause in `target/` before changing the test: a test changed to pass hides the defect it found.

## Rules

Read [rules.md](rules.md) and follow every rule. Cite a rule by its ID and this skill's version when you apply or break it, for example "breaks MUNIT-2 (munit 1.0.0)".
