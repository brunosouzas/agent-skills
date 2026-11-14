# DataWeave: rules

Rules for DataWeave 2, from MuleSoft's DataWeave documentation and common practice. In an existing project, follow the conventions it already uses and report a difference instead of renaming; these rules decide new scripts and files. A rule marked `(locked)` protects secrets, personal data or sensitive logs: a project's own convention never overrides it.

How to change this file (see CONTRIBUTING.md of this repository):
- **Add a rule:** copy an item, give it the next number in its group, write the rule, why it exists and how to check it. A new rule is a MINOR version.
- **Change a rule:** edit it in place and keep its ID, so old reviews still point at the right rule. A rule that now says the opposite is a MAJOR version; clearer wording is a PATCH.
- **Retire a rule:** keep its ID and heading, replace the text with `(retired in <version>: <reason>)`, and never reuse the number. A retired rule is a MAJOR version.

## Scripts (DW)

- **DW-1** Move transformations longer than a few lines into `.dwl` files under `src/main/resources/dwl/`, in one folder per domain (`dwl/customer/`, `dwl/error/`, `dwl/common/`), and reuse functions through modules.
  Why: inline scripts cannot be tested or reused, and one flat folder of dozens of scripts hides what belongs together.
  Check: new long transforms reference a `.dwl` resource in a domain folder.

- **DW-2** Declare the output MIME type and handle null and missing fields explicitly (`default`, `?`).
  Why: a null in the input becomes a runtime error or a silent wrong value.
  Check: optional fields use `default` or a null-safe selector.

- **DW-3** Name DataWeave files by role: a script that builds a payload starts with `p-`, one that builds a variable with `v-` (kebab-case, `p-customer-response.dwl`); other scripts are kebab-case without a prefix; a reusable function module is TitleCase (`common/ValueUtils.dwl`).
  Why: the prefix says what a script feeds without opening it; modules read like the types they import as.
  Check: new `.dwl` files follow the prefixes.

- **DW-4** Every script starts with `%dw 2.0` and an `output` directive; a script that does not read the Mule message (a module function's test input, a standalone script) also declares its `input` with its MIME type.
  Why: the default output and the guessed input type change with the runtime and the caller; the header makes the script say what it reads and writes.
  Check: each new `.dwl` has the header; standalone scripts declare `input`.

- **DW-5** Functions are pure: their result depends only on their parameters. Read `vars`, `attributes` and `p(...)` in the top-level script and pass the values in.
  Why: a function that reads the message can only be tested inside a flow and changes meaning when the flow changes.
  Check: no `vars.`, `attributes.` or `p(` inside a `fun` body of a module.

- **DW-6** A module's public functions declare their parameter and return types (`fun toCustomer(row: Object): Customer`), with the types defined in the module or imported.
  Why: a typed signature fails at compile time where an untyped one fails on the first odd input in production.
  Check: every `fun` a module exports has typed parameters and a return type.

- **DW-7** Branch on the shape or value of data with `match` and patterns, and give every `match` an `else` that either maps the unexpected case or fails with a message naming it (`fail("Unknown status: $(s)")`).
  Why: nested `if` chains hide a missing case, and a `match` with no `else` throws a generic error at runtime.
  Check: each `match` has an `else` case.

- **DW-8** Parse and format dates, times and numbers with an explicit `format` (and a time zone for date-times); never rely on the default format or the runtime's zone. Money is never built by string concatenation.
  Why: defaults differ between runtimes, locales and servers; a date that moves a day or an amount that loses a digit is a silent defect.
  Check: every `as Date`, `as DateTime`, `as String` of a number or date, and every `as Number` from a string has `{format: ...}`.

- **DW-9** Index or join large collections once (`groupBy` or `indexOf` into an object, then look up by key) instead of searching inside a `map`.
  Why: `filter` or `firstWith` inside `map` makes the transform quadratic, which is invisible in tests and slow in production.
  Check: no `filter`, `find` or `firstWith` over the same collection inside a `map` body.

## Tests (DWTEST)

- **DWTEST-1** Each function of a module and each transform has a test with its edge cases: in a Mule application an MUnit test with the input in a file (`src/test/resources/`), in a DataWeave library the DataWeave testing framework run by its Maven plugin.
  Why: DataWeave fails on the shape of data, and a happy-path test does not exercise the shape.
  Check: tests cover at least one missing field, one empty collection and one wrong type for each changed function.

- **DWTEST-2** (locked) Test and example inputs are synthetic and minimal: never a real payload, production data or personal data, also not in an isolated snippet sent to an assistant.
  Why: a test file is committed and read widely, and a pasted payload leaves the organisation that owns it.
  Check: no real names, document numbers, emails or account identifiers in test inputs or examples.
