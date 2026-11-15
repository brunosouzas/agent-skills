# Delivery model rules

How to change this file: CONTRIBUTING.md. A rule keeps its ID for life; a rule that no longer applies is retired, not deleted.

## DLM: in every model

- **DLM-1** A pull request runs the build, the checks and, where the model has one, a preview. It never deploys to production; production deploys only from a tag (in model 1, the release on `main`).
  Why: a branch run that reaches production skips every gate the merge has.
  Check: no pipeline job that deploys production runs on a pull request or branch trigger.
- **DLM-2** A `vX.Y.Z` tag ([SemVer](https://semver.org/)) is created only by the pipeline or release tool. A tag pushed by hand (a retry, a release that never got its tag) is a level 2 action, and only where the repository's release documentation allows it.
  Why: a hand-made tag can point at a commit no release process built.
- **DLM-3** Merge a short branch with a squash (`gh pr merge --squash --delete-branch`), and a `release/`, `hotfix/` or back-merge pull request with a merge commit (`gh pr merge --merge`).
  Why: a squash keeps the history one commit per change; a merge commit keeps `main` and `develop` sharing history in GitFlow.
- **DLM-4** Moving a repository to a model is a change of its own at level 2: the pipeline and the branch protection first, the `Model:` line last.
  Why: the rules must never switch before what backs them exists.
- **DLM-5** A repository that has not migrated keeps its own branch rules and pipeline until its migration; its `AGENTS.md` wins over these branch names.
  Why: half-applied branch rules break a pipeline that still expects the old names.
- **DLM-6** In model 3, when the verification right after a production deploy fails, rolling back to the previous release is level 1: do it, then tell the approver at once.
  Why: every minute of a broken production costs more than a rollback that turns out unneeded.
- **DLM-7** A pipeline change is tested by running it on the branch; a pipeline that would deploy production from a branch run is fixed first (DLM-1).
  Why: a pipeline cannot be reviewed into working.

## REL: releases, hotfixes and consumers

- **REL-1** A release is always its own pull request at level 2. In models 2 and 3 it is the release pull request the release tool keeps open: the agent never edits it (the tool rewrites it on every merge); when asked for a release, say it is ready in one line with its link and what it carries.
  Why: the release pull request is generated; an edit is lost or, worse, released by hand.
- **REL-2** In model 1, a `release/x.y.z` or `hotfix/x.y.z` pull request into `main` is walked like any change. A `release/` one carries no new code (`S2 Review: not needed: release`); a `hotfix/` one carries the fix, which gets the review.
  Why: the hotfix is code nobody has reviewed yet; the release branch is code already reviewed.
- **REL-3** In model 1, a hotfix is `hotfix/x.y.z` from `main`. If `main`'s `pom.xml` does not already carry `x.y.z-SNAPSHOT`, its first commit sets it with `mvn versions:set -DnewVersion=x.y.z-SNAPSHOT -DgenerateBackupPoms=false`, the one version change made outside the pipeline.
  Why: `release:prepare` releases the version in the POM, and the hotfix needs its own.
- **REL-4** In model 1, after a release, merge the back-merge pull request `main → develop` (merge commit) when it has no conflicts; with conflicts (usually the version), resolve them on a `chore/back-merge-x.y.z` branch cut from `main`, never squashed, keeping `develop`'s `-SNAPSHOT`.
  Why: a squashed back-merge loses the merge, and `main` and `develop` drift apart again.
- **REL-5** An urgent fix in model 2 or 3 is a `bugfix/` into `main`, then the release pull request. When `main` already holds other unreleased changes, ask the approver whether they go out together or whether to cut `release/x.y` from the last tag and cherry-pick the fix once it is on `main` (upstream first).
  Why: an urgent fix should not ship changes nobody chose to release yet.
- **REL-6** After a release merges, watch the release pipeline: when it stops at an environment approval, tell the approver in one line with the run's link and wait. Then verify production (the published version, the URL, the smoke check) and post the after-merge report; a release still waiting for approval is reported as `production pending approval`, and a later `Production verified: <check -> result>` comment closes it.
  Why: a release is done when production runs it, not when its pull request merges.
- **REL-7** Once a package release is published, open one follow-up pull request per consumer that only bumps the version (`S2 Review: not needed: version bump`), merged at the consumer's own gate. Using the new feature there is a change of its own. Release a consumer that is itself a package only when asked.
  Why: a release nobody consumes fixes nothing.
