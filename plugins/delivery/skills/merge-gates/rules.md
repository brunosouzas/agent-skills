# Merge gate rules

How to change this file: CONTRIBUTING.md. A rule keeps its ID for life; a rule that no longer applies is retired, not deleted.

## GATE: who merges

- **GATE-1** The approver is read from the `Approver:` line, then from the user's instructions for that repository, then is the user. A pull request at level 2 waits for that approver, whoever asked for the change.
  Why: the person who asks is not always the person accountable for what the merge does.
- **GATE-2** A level 1 merge needs all of: the change is small; the base is not production; the required checks are green (with a `Model:` line, the checks its branch protection requires, and a repository with a model but no CI on pull requests has no level 1 merge; without one, the `AGENTS.md` checks run locally and written in S1, plus every check that ran on the pull request); the latest independent review has no open `high` or `medium` finding (or the change is a review exemption of the change flow); the description has no Questions; no reserved item (GATE-3).
  Why: each condition is one way a merge nobody looked at can still be wrong.
  Check: every condition is answered in the description's S1, S2 and S5.
- **GATE-3** Reserved items always make the merge level 2, whatever the size: a secret, a permission (branch protection and rulesets included), a shared pipeline template, a release version, a deletion, and the gate lines of `AGENTS.md` (`Delivery:`, `Model:`, `Integration branch:`, `Data:`, `Approver:`, and any line the user's instructions add as one).
  Why: these change what later gates allow, so the agent never relaxes them for itself.
- **GATE-4** An approval counts only on the head commit of the pull request: read the reviews on the forge (`gh api repos/<owner>/<repo>/pulls/<n>/reviews` and its `commit_id`), and a push after the approval needs a new one.
  Why: otherwise a commit nobody approved merges under someone's approval.
- **GATE-5** A delegation widens level 1 only for the current session, in the approver's own words (for example "merge this task's pull requests while I'm away"), quoted in every pull request merged under it. It follows the task, also into another repository the task leads to. It never covers a release, a deployment approval, a promotion to pre-production or production, a merge into production, a reserved item, a deletion, force push or rewritten history.
  Why: a standing delegation would be a lower gate nobody decided.
- **GATE-6** The repository is stricter, the repository wins. When `AGENTS.md` asks for more ("the owner merges", a card for every change), follow it; when it asks for less than these rules, follow these rules.
  Why: the repository knows risks these rules cannot, but a file cannot lower a gate it does not own.
- **GATE-7** Lines the agent wrote do not set its own gate: until a change to a gate line is merged, take the strictest reading (a live destination and no `Model:` line when in doubt).
  Why: an agent that could write its own permissions would have none.
- **GATE-8** The agent never approves a deployment, a run waiting for review or its own pull request, never removes a required check or label, and never reads or pastes a secret to get past a gate. When a gate blocks it, it says which gate and stops.
  Why: a gate the agent can open is not a gate.
- **GATE-9** When the user's instructions name a separate identity for the agent's writes on the forge (a bot account, an app), every commit, push, pull request, comment and merge runs as that identity, and the user's own login is for reads only. An action that identity cannot do (rulesets, settings, secrets, creating a repository) is written as a command for the user to run.
  Why: branch protection binds a separate identity, and its writes are told apart from the user's in the history.
- **GATE-10** Runtimes that ask before a merge (a permission prompt) are not a reason to merge less carefully, and an unattended merge will not happen there: when the approver delegates and is about to leave, say so at once, then stop at "pull request ready".
  Why: a delegation that silently waits for a prompt nobody answers loses a night.
