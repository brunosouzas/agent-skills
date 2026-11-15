# Report templates

Each checklist item of the change flow has its line here, so what was checked is written where the approver and any after-merge routine can see it.

## The plan (PLAN; the start of the pull request description)

```
Plan
E1 Repository: <path or name>
E2 Stack: <...> | Spec: <tool | none> | Delivery: <destination> | Model: <model | none yet> | Base: <branch> | Tracker: <system | none> | Approver: <who> | Checks: <commands> | Deliver and verify: <what runs, the check> | Lines to add: <none | which>
E3 Size: <small | spec>: <why, one line>
E4 Card: <id> | none: <why>
E5 Consumers: <repositories> | none
E6 Merge: level <0-2> | delegation: "<the user's words>" | Agent access: write | missing: <asked>
E7 Skills: <names>
E8 Questions: <asked in ASK> | none
```

## The pull request description (OUT1)

```
<the plan block>

What changed: <behaviour, plain words>
Spec: <change name, scenarios covered> | no spec: <why>
S1 Checks: <command -> result>; not run: <which, why>
S2 Review: <rounds, fixed, rejected and why> | not done: <why> | not needed: <release | version bump | back-merge | data list | prose typo>
S3 Docs: <files> | none: <why>
S4 Preview: <URL, screenshots or stills> | n/a: <why>
S5 Merge: level <0-2> | delegation: "<the user's words>" | approver
Decisions taken: <choices made without the approver>
Questions: <only what needs the approver> | none

<the tracker's closing line, when there is a card>
```

## After the merge (OUT2; a comment on the merged pull request)

```
After merge
S6 Delivery: <what ran -> result>; verified: <check -> result>
S7 Records: <notes updated> | nothing to change: <why>; card: done | no card
S8 Consumers: <pull requests opened> | none
S9 Cleanup: <branches and worktrees removed>
S10 Process: <what the flow missed or got wrong> | none
```

The session that merges posts it at once.

## Picking up merged work (the start of IN)

Work merged after its session ended is picked up by the next session, before new work. List:

1. the merged pull requests of this flow (description starting with `Plan`) with no "After merge" comment;
2. the release pull requests merged in the last week (a `release-please--` head branch, whoever opened it) with no "After merge" comment: verify their production as REL-6 says;
3. the merged release pull requests whose "After merge" comment says `production pending approval`: once the run is approved and production checks out, comment `Production verified: <check -> result>`.

Finish one or two; with more, list them for the user and ask before going on, so a new request is not buried under old work. An after-merge routine the user's instructions name may own the recent ones.
