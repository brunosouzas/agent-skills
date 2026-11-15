---
name: delivery-models
description: "How a merged change becomes a release and reaches production, by the delivery model on the Model line of a repository's AGENTS.md (1 GitFlow release, 2 release pull request, 3 continuous delivery with staging, 4 install locally, reference) or, without one, its destination on the Delivery line (live, package, environments, local, reference): long branches, what a merge does, release pull requests and tags, production approval, rollback, hotfixes, the after-merge verification and follow-up bumps in consumers. Use when a change is merged and must be delivered and verified, when cutting or merging a release, tagging, rolling back, shipping a hotfix, or choosing or migrating a repository's delivery model. Triggers: release, release-please, tag, deploy, rollback, hotfix, staging, production, GitFlow, back-merge, Model line, Delivery line, Deliver and verify. Not for who may merge or approve (merge-gates), the steps of the change before its merge (change-flow), or writing the pipeline itself (its pipeline skill)."
license: Apache-2.0
metadata:
  version: "1.0.0" # x-release-please-version
---

# Delivery models

The `Model:` line names how a repository delivers. The model decides the long branches, what a merge does, who releases and how production goes back; the language only picks the tool that makes the version (the Maven release plugin for Maven, release-please for the rest). A repository follows its model once the `Model:` line is merged; until then its `Delivery:` destination applies.

| Model | For | Long branches | A merge into the base | Release | Production | Back out |
|---|---|---|---|---|---|---|
| **1. GitFlow release** | Maven projects that release with the release plugin | `main`, `develop` | Into `develop`: the pipeline publishes the `-SNAPSHOT` and deploys to the test environment | A pull request from `release/x.y.z` (from `develop`) or `hotfix/x.y.z` (from `main`) into `main`, merge commit; the pipeline runs `release:prepare release:perform`: tag `vX.Y.Z`, the artifact, a back-merge pull request `main → develop` | The same artifact, after the approver approves the environment | Deploy the previous artifact with the same pipeline |
| **2. Release PR** | Libraries and packages | `main` | Nothing is published | release-please keeps a release pull request (version and changelog); the approver merges it; the workflow tags `vX.Y.Z` | The publish job waits for the approver's approval of its environment | A new patch release; deprecate the bad version |
| **3. Continuous delivery with staging** | Sites, workers, internal services | `main` | The pipeline deploys `main` to staging | A release-please release pull request, merged by the approver after looking at staging | The tag deploys after the approver approves the environment | Roll back or redeploy the previous tag (DLM-6) |
| **4. Install locally** | Tools, dotfiles, local services | `main` | `Deliver and verify:` runs | none | none | Revert and reinstall |
| **Reference** | Examples and labs others cite | `main` | Nothing | none; a citation gets a tag of its own (not `v*`) | — | Revert |

A `Model:` value this skill does not define (a number or name of the repository's own process) is read from that repository's delivery documentation; when it has none, ask before the first merge.

## Destinations (no `Model:` line)

| `Delivery:` | Before the merge | Deliver | Verify |
|---|---|---|---|
| **A. Live** | A preview: build locally and attach screenshots of each changed page, or the pipeline's preview URL | The pipeline that runs on the merge | The run is green and the changed URL answers with the change |
| **B. Package** | For a visual change, rendered stills of each changed piece | A release is its own pull request that bumps the version; the release workflow publishes after the approver's approval | The version is published; follow-up pull requests open in consumers |
| **C. Environments** | — | The repository's pipeline, environment by environment, with its approvals | A smoke check in each environment the change reached |
| **D. Local** | — | What `Deliver and verify:` says (an install, a reinstall, a fast-forward of the checkout a tool reads) | The check on the same line |
| **E. Reference** | — | Nothing | Links, paths and endpoints others cite still work |

## How to work

1. Read `Model:`, `Delivery:`, `Integration branch:` and `Deliver and verify:`. A missing `Deliver and verify:` is inferred from the pipelines and README, named in the plan, and added in the change.
2. After the merge, run or watch exactly what the model or destination says, then the verification, and report it in S6 (`change-flow`).
3. A failed delivery or verification is reported at once with what failed and the way back; the fix is a new change.

## Rules

Read [rules.md](rules.md) (DLM, REL) and follow every rule. Cite a rule by its ID when you apply or break it.
