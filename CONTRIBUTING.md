# Contributing

This repository is a marketplace of plugins; each plugin holds specialty skills for one technology family (`mulesoft`, `api`, `languages`, `devops`, `web`). A specialty skill says what is particular to a technology: its rules, how to check them, and when to use it. It never says how a team works: processes, reviews and delivery belong to whoever installs the skills.

## Writing rules

1. **No process, no person.** A specialty never cites a process (a playbook, a team's workflow) or a person. It may cite another skill, always as "if it is installed": the reader may have installed only this one.
2. **The `description` routes the request.** It says what the skill does, when to use it (`Use when ...`), the words that trigger it (`Triggers: ...`) and when not to use it (`Not for ...`, naming the skill that covers that case). It is the only text a tool reads before deciding to load the skill, so it is written for that decision, at most 1024 characters.
3. **Short files.** `SKILL.md` has about 100 lines at most: when to use the skill, how to work in a few steps, and where the rules are. A `rules.md` over about 150 lines is split into `references/<subject>.md`, and `SKILL.md` says when to read each one.
4. **What has a right answer becomes a script.** A check that a program can decide (a missing attribute, a forbidden default, a file layout) is a script in the skill's `scripts/`, with a test in `tests/`, and the rule's `Check:` line names it. Scripts use the Python standard library only and start with a header saying what they do, why, how to run them and what can go wrong.
5. **No personal or environment facts.** No machine, user name, home path, `JAVA_HOME` value, board card, notes vault or company. A fact true only on one machine belongs in that user's own agent instructions, not in a shared skill. `scripts/check_repo.py` refuses the common ones.
6. **Rule IDs are stable.** A rule keeps its ID for life (`DW-4`), also when it moves to another skill of the repository. A rule that no longer applies is retired, not deleted: keep its ID and heading and replace its text with `(retired in <version>: <reason>)`. A number is never reused. CI refuses a pull request that removes an ID.
7. **Every skill has evals.** Each skill has at least one routing case that must load it and one that must not (see [Evals](#evals)).
8. **Every skill has a version.** `metadata.version` in the frontmatter, starting at `1.0.0`, on the line marked `# x-release-please-version`; release-please raises it (see [Versions](#versions)).

## A skill's files

```
plugins/<plugin>/skills/<skill>/
├── SKILL.md        frontmatter + when + how to work + where the rules are
├── rules.md        the rules (or references/<subject>.md when it grows)
├── scripts/        checks with one right answer
├── CHANGELOG.md    written by release-please
└── package.json    version record for release-please (private, never published)
```

Frontmatter (the [Agent Skills](https://agentskills.io/specification) format; `metadata` values are strings):

```yaml
---
name: dataweave
description: "Rules for DataWeave 2: ... Use when ... Triggers: ... Not for ..."
license: Apache-2.0
metadata:
  version: "1.0.0" # x-release-please-version
  aliases: "dataweave 2, dwl"
---
```

`metadata.aliases` lists, comma-separated, the other names of the technology as people write them on the `Stack:` line of a repository's `AGENTS.md` ([docs/agents-md.md](docs/agents-md.md)). Names and aliases are unique across the repository.

A rule:

```markdown
- **DW-7** Give every `match` an `else` that maps the unexpected case or fails with a message naming it.
  Why: a `match` with no `else` throws a generic error at runtime.
  Check: each `match` has an `else` case.
```

A rule marked `(locked)` protects secrets, personal data or sensitive logs: a project's own convention never overrides it.

## Versions

Each skill and each plugin is a release-please package ([docs/releasing.md](docs/releasing.md)). The version of a skill follows what its users can rely on:

| Bump | When |
|---|---|
| **MAJOR** | A rule is retired or now says the opposite; the description covers fewer cases than before |
| **MINOR** | A new rule, reference or script; the description covers more cases |
| **PATCH** | Wording, a clearer `Why:` or `Check:`, a fixed link or typo |

A reviewer cites the rule and the version it read: "breaks DW-4 (dataweave 1.3.0)".

## Commits and pull requests

- One change per pull request, squash-merged. The pull request title becomes the commit, so it is a [Conventional Commit](https://www.conventionalcommits.org/): `feat` (MINOR), `fix` (PATCH), `feat!` or a `BREAKING CHANGE:` footer (MAJOR); `docs`, `chore`, `ci`, `test`, `refactor` release nothing.
- **The scope names every skill the change touches**, comma-separated: `feat(dataweave): add DW-10 for streaming`, `fix(dataweave,munit): ...`. CI refuses a title without it (`scripts/check_commit_scope.py`). release-please assigns the commit to each skill by the paths it changes and writes the title into that skill's `CHANGELOG.md`.
- A rule that moves between skills keeps its ID: it is a MINOR in the skill that receives it and a MAJOR in the one that loses it.

## Evals

Routing cases live in `plugins/<plugin>/evals/<case>/case.yaml`, in the format of `claude plugin eval`. Each case is a prompt and graders on the `Skill` tool: a grader named `loads-<skill>` asserts the skill is loaded, one named `does-not-load-<skill>` (with `min: 0`, `max: 0`) asserts it is not. Write prompts the way people ask, in more than one language when the users do.

```bash
claude plugin eval ./plugins/mulesoft --ablation none --runs 3
```

`--ablation none` makes the routing graders part of the score. Run the evals of a plugin before a pull request that changes a `description`; paste the summary in the pull request.

## Checks

```bash
python3 scripts/check_repo.py
python3 -m unittest discover -s tests -v
claude plugin validate ./plugins/mulesoft
```

CI runs the first two on every pull request, plus the title check.
