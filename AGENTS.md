# agent-skills: project context

A marketplace of agent skills for software engineering, one plugin per technology, installable in Claude Code and Codex. Read [README.md](README.md) for what is here and [CONTRIBUTING.md](CONTRIBUTING.md) for the rules every skill follows.

## Technology

Stack: Python, Markdown
Delivery: B package (a published package: a merge releases nothing until the release pull request is merged)
Integration branch: `main`

- Check: `python3 scripts/check_repo.py`
- Test: `python3 -m unittest discover -s tests -v`
- Validate a plugin: `claude plugin validate ./plugins/<plugin>`
- Routing evals: `claude plugin eval ./plugins/<plugin> --ablation none`
- Release: release-please keeps the release pull request; merging it tags each skill and plugin ([docs/releasing.md](docs/releasing.md)).

## Rules for changing this repository

- A change is a branch and a pull request, squash-merged; its title is a Conventional Commit whose scope names every skill it touches (`feat(dataweave): ...`). CI checks it.
- Skills follow the writing rules in CONTRIBUTING.md: no process or person, a description that routes, short files, scripts for what has a right answer, no personal or environment facts, stable rule IDs (retire, never delete), evals and a version for every skill.
- Scripts use the Python standard library only (3.9 or newer) and start with a header saying what they do, why they exist, how to run them and what can go wrong; every block has a comment saying why.
- Everything is in English.
- A line of a repository's `AGENTS.md` that a skill starts reading is documented in [docs/agents-md.md](docs/agents-md.md) in the same pull request.
