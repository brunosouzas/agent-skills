# MUnit: rules

Rules for MUnit tests of Mule 4 applications, from MuleSoft's MUnit documentation and practice in reference projects. In an existing project, follow the conventions it already uses and report a difference instead of renaming; these rules decide new suites and tests.

How to change this file (see CONTRIBUTING.md of this repository):
- **Add a rule:** copy an item, give it the next number in its group, write the rule, why it exists and how to check it. A new rule is a MINOR version.
- **Change a rule:** edit it in place and keep its ID, so old reviews still point at the right rule. A rule that now says the opposite is a MAJOR version; clearer wording is a PATCH.
- **Retire a rule:** keep its ID and heading, replace the text with `(retired in <version>: <reason>)`, and never reuse the number. A retired rule is a MAJOR version.

## MUnit (MUNIT)

- **MUNIT-1** Every flow change has an MUnit test that asserts the payload and the status the scenario specifies, with external calls mocked.
  Why: a test that only checks that the flow ran proves nothing.
  Check: each test has `assert-that` on the payload or variables, and `mock-when` for each outbound call.

- **MUNIT-2** Test the error paths: each mapped error type has a test that triggers it.
  Why: error handling is the part nobody exercises by hand.
  Check: tests use `mock-when` with an error to trigger each handler.

- **MUNIT-3** Keep the coverage gate in `pom.xml` and never lower it to pass a build.
  Why: lowering the gate hides untested code.
  Check: the diff does not change the coverage settings.

- **MUNIT-4** In an MUnit suite that calls an APIkit router, list the implementation flows in `enable-flow-sources` along with the listener flow.
  Why: without them the router answers `NOT_IMPLEMENTED`, and the test fails for a reason that is not in the code under test.
  Check: each suite that calls the router has `munit:enable-flow-source` for every flow the scenario reaches.

