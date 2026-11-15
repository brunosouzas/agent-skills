---
name: merge-gates
description: "Who may merge, approve or release a change, by the risk of its effect: what the agent does without asking, which merges it may do and report, and what waits for the approver the repository's Approver line names; the reserved items that always need the approver, approval on the head commit, a delegation for one session, and a repository stricter than these rules. Use when deciding whether to merge a pull request, whether a change needs someone's approval, whether a delegation covers a merge, or what the agent may do on its own in a repository. Triggers: can I merge, who approves, merge this PR, approval, delegation, auto-merge, level 1, level 2, reserved item, Approver line. Not for the steps of the change itself (change-flow), what a merge releases or deploys (delivery-models), or a repository's branch protection settings (its pipeline skill)."
license: Apache-2.0
metadata:
  version: "1.0.0" # x-release-please-version
---

# Merge gates

The gate follows the risk of the effect, not the git command. A pushed branch changes nothing; a merge, a release or a promotion does. The approver is the person or team on the `Approver:` line of the repository's `AGENTS.md`; without one, the person the user's instructions name for the repository; without either, the user.

| Level | Who | What |
|---|---|---|
| **0. The agent, no asking** | the agent | Read, run checks, branch, commit and push to the change branch, open a draft pull request, mark it ready or back to draft, move the card, update the repository's docs in the pull request |
| **1. The agent merges, then reports** | the agent; the approver sees it in the pull request and can revert | The merge of a **small** change into a base that is **not production**, when GATE-2 holds |
| **2. The approver** | the approver approves on the forge, then the agent completes the merge; or the approver merges | Accepting a proposal (G1); the merge of a spec-sized change; **every release**; approving a production deployment; a promotion to a pre-production or production environment; any merge with a reserved item (GATE-3); a deletion of a repository, data or a branch with unmerged work; force push or rewritten history |

**Bases that are not production** follow the repository's model (`delivery-models`): the integration branch of a GitFlow model, `main` in a release-pull-request, continuous-delivery or local-install model, and `main` of a reference repository; without a `Model:` line, the base of a local or reference destination. A live destination is production.

## How to work

1. Read `Approver:`, `Model:`, `Delivery:` and `Data:` from `AGENTS.md`, and any stricter merge rule there (GATE-6).
2. Check the pull request against GATE-2 and GATE-3. Anything not plainly level 1 is level 2.
3. Level 1: merge (`gh pr merge --squash --delete-branch`; a model's long-branch merges as `delivery-models` says) and report in one line. Level 2: tell the approver it is ready, in one line with its link, and stop.
4. After the approver approves, check the approval is on the head commit (GATE-4), then complete the merge.

## Rules

Read [rules.md](rules.md) (GATE) and follow every rule. Cite a rule by its ID when you apply or break it.
