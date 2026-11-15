# Trackers

The `Tracker:` line of `AGENTS.md` names the system, then what locates a card in it. These commands are enough for TRK-1 and TRK-2; replace the placeholders with the line's values.

| `Tracker:` line | Find | Create | Move | Closing line |
|---|---|---|---|---|
| `Azure Boards <organisation>/<project>, area <area>` | `az boards query --org https://dev.azure.com/<organisation> --project <project> --wiql "SELECT [System.Id], [System.Title], [System.State] FROM workitems WHERE [System.Title] CONTAINS '<words>'" -o table` | `az boards work-item create --org https://dev.azure.com/<organisation> --project <project> --type <the project's work item type> --title "<title>" --area '<project>\<area>'` | `az boards work-item update --org https://dev.azure.com/<organisation> --id <id> --state <its in-progress state>` | `Fixes AB#<id>` |
| `GitHub Issues <owner>/<repository>` | `gh issue list -R <owner>/<repository> --search "<words> in:title"` | `gh issue create -R <owner>/<repository> --title "<title>" --body "<one line>"` | a label or project column, if the repository uses one; otherwise nothing until the merge | `Fixes #<number>` |
| `Jira <site>, project <KEY>` | the Jira search for `project = <KEY> AND summary ~ "<words>"` | a new issue in `<KEY>` | the workflow's "In Progress" transition | `<KEY>-<number>` in the title or description (the Jira integration links it) |
| `none` | — | — | — | — |

The branch name carries the card as the tracker writes it, in lower case without symbols: `ab42`, `gh17`, `key-42`.

A system not in this table: use its own command-line tool or web interface for the same four operations, and say so in the plan.
