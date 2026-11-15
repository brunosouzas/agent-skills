# Change flow rules

How to change this file: CONTRIBUTING.md. A rule keeps its ID for life; a rule that no longer applies is retired, not deleted.

## CHG: branches and pull requests

- **CHG-1** One change, one branch, one pull request; nothing is committed straight on a long branch. Branch from the up-to-date integration branch (`Integration branch:`, else `main`) with `git switch -c <branch> origin/<base> --no-track`.
  Why: without an upstream a bare `git push` cannot land on the base by mistake.
  Check: `git rev-parse --abbrev-ref @{upstream}` fails before the first push.
- **CHG-2** Name the branch by intent: `feature/<card>-<slug>` for new or changed behaviour, `bugfix/<card>-<slug>` for a correction, `chore/<card>-<slug>` for maintenance with no behaviour change; drop `<card>-` without a card. A delivery model may add its own long-branch names (`delivery-models`).
  Why: the name tells a reader the kind of change before they open it.
- **CHG-3** Never switch branches in a checkout a tool or a person reads; work in a worktree.
  Why: tools load skills, plugins and configuration from their checkout, and a person may have work in progress there.
- **CHG-4** Draft means "the agent is working", ready means "done, can be merged". Open every pull request as a draft; mark it ready only when S1 to S5 are answered and the latest review has no open `high` or `medium` finding. Work resumed on a ready pull request puts it back to draft first (`gh pr ready --undo`).
  Why: the approver reads ready pull requests only, and a push to a ready one changes what they are reading.
- **CHG-5** The pull request title is a Conventional Commit (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`, `ci:`, `build:`, `perf:`, `revert:`, `style:`; `!` for a breaking change), and the description starts with the plan block.
  Why: a squash merge makes the title the commit a release tool reads, and an after-merge routine can find the pull requests of this flow by the plan block.
- **CHG-6** A request that spans repositories is one change per repository, walked in order: the producer, its release, then each consumer. Put the card's closing keyword on the last pull request only, so the first merge does not close the card.
  Why: a consumer cannot take a version that is not released yet.
- **CHG-7** A missing step is a step to do, not a reason to stop: no spec when one is needed, write it; no `Stack:` or `Delivery:` line, infer it and add it in this change.
  Why: stopping hands the gap back to the user, who asked for the change, not for a list of what is missing.
- **CHG-8** When a draft stops moving (an open finding after the last review round, a blocker, the session ending before OUT1), tell the user in one line with its link and what blocks it.
  Why: a silent draft looks like work in progress for weeks.

## REV: the independent review

- **REV-1** Review with a clean context: a separate reviewer (the `reviewer` agent, if installed, or a new session) given only the base ref, the branch, the spec change if any, the lens and the repository's `AGENTS.md`; never the author's reasoning. Spec review asks whether an implementer with no other context could build exactly the intended behaviour from the artifacts alone.
  Why: a reviewer who knows what the author meant reads that instead of what is on disk.
  Check: the pull request names the reviewer and the reviewed commit; a review in the same context is reported as "independent review not done".
- **REV-2** Fix every right `high` and `medium` finding. A rejected finding gets one line in the pull request saying why; a finding that needs the approver goes to the description's Questions.
  Why: a finding dropped without a line cannot be told apart from one never read.
- **REV-3** At most two review rounds, each with a new reviewer; a second round only when the first had a `high` or `medium` finding. A finding still open after the second stays open: the pull request stays a draft and the user is told (CHG-8).
  Why: a third round means the contract is unclear, and more rounds will not make it clear.
- **REV-4** Skills, agents, prompts, pipelines and `AGENTS.md` are code and always get the review. The only exemptions: a version bump, a back-merge, a path on the `Data:` line, a typo in prose no tool reads.
  Why: an instruction file changes what every later agent does.
- **REV-5** Code and spec never disagree: when implementing shows the spec gives a worse result, change the spec text and its scenario in the same commit as the code.
  Why: the spec is the next change's acceptance criteria; a stale one misleads it.

## TRK: the tracker

- **TRK-1** A card is required for a spec-sized change, for work planned before the session, and for work over more than one session. A small change done in one session needs none: its pull request is the record. The `Tracker:` line names the system, project and area; `Tracker: none` means no cards.
  Why: the card is the plan; git and the pull request are the history.
- **TRK-2** The card shows only the state (to do, doing, done). Move it to doing when the branch starts and to done after the merge, unless the merge closes it; a pull request with a card ends with the tracker's closing line ([trackers](references/trackers.md)).
  Why: the truth is the branch and the pull request; a card that carries detail drifts from them.
- **TRK-3** Never create a card, branch prefix or note on the tracker of another owner: a repository whose `AGENTS.md` names no tracker and whose owner the user's instructions do not cover gets no card.
  Why: a card on the wrong board leaks work into someone else's plan.
