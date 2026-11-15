# delivery plugin

```bash
claude plugin marketplace add brunosouzas/agent-skills
claude plugin install delivery@brunosouzas-agent-skills
```

Codex: `codex plugin marketplace add brunosouzas/agent-skills`, then `codex plugin add delivery@brunosouzas-agent-skills`.

A process for agents that change code, in three skills. Where the specialty plugins say what is particular to a technology, this one says how a change travels: planned, reviewed, merged by the right person, delivered and verified. It reads a few lines of the repository's `AGENTS.md` ([docs/agents-md.md](../../docs/agents-md.md)) and never names a person, a board or an account: those come from the repository or from your own agent instructions.

| Skill | For | Rules |
|---|---|---|
| [change-flow](skills/change-flow/SKILL.md) | The path of one change: entry checklist and plan, small or spec, branch and draft pull request, independent review, exit checklists, the tracker | CHG, REV, TRK |
| [merge-gates](skills/merge-gates/SKILL.md) | Who merges, approves or releases, by risk: levels 0 to 2, reserved items, approval on the head commit, delegation | GATE |
| [delivery-models](skills/delivery-models/SKILL.md) | What a merge does: GitFlow, release pull request, continuous delivery with staging, local install, reference; destinations; releases, hotfixes, rollback | DLM, REL |

## Making it yours

The plugin fills a missing line in this order: the repository's `AGENTS.md`, then your own instructions (a user-level `CLAUDE.md` or `AGENTS.md`), then the strictest reading. So a personal layer only sets values, for example:

```markdown
In my repositories (github.com/<you>/...):
- Approver: <your login>
- Tracker: GitHub Issues <you>/<repository>
- The agent writes on GitHub as <bot account>; my login is for reads.
```

A process of your own that goes further (more models, risk classes, notes after a merge) loads these skills and adds to them; it never needs to copy them.

Each skill's version is in its `SKILL.md` (`metadata.version`) and its history in its `CHANGELOG.md`. The routing evals are in [evals/](evals/).
