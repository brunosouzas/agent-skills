#!/usr/bin/env python3
"""Check that a pull request title is a Conventional Commit whose scope names every skill it touches.

What it does
    Takes the pull request title and the files it changes. The title must be a
    Conventional Commit (`type(scope)!: subject`). When a changed file is inside
    a skill (plugins/<plugin>/skills/<skill>/...), the scope must name that
    skill; several skills are separated by commas: `fix(dataweave,munit): ...`.
    The release pull request of release-please (`chore(main): release ...`) is
    exempt: it touches every released skill by design.

Why it exists
    The pull request title becomes the squash commit, and release-please writes
    each skill's CHANGELOG from it. release-please decides which skill a commit
    belongs to by the paths it touches; the scope makes the title say the same
    thing, so a changelog line and a reviewer's citation ("DW-4 (dataweave
    1.3.0)") name the skill that changed. CONTRIBUTING.md, rule 8.

How to run
    python3 scripts/check_commit_scope.py --title "feat(dataweave): ..." FILE ...
    python3 scripts/check_commit_scope.py --title "..." --base origin/main
    With --base, the changed files are `git diff --name-only <base>...HEAD`.
    Exit code: 0 the title fits, 1 it does not (the reason is printed).

What can go wrong
    - --base needs the base ref fetched (actions/checkout with fetch-depth: 0).
    - A title that names more skills than it touches passes: naming an extra
      skill is harmless; missing one is what breaks the changelog.
"""

import argparse
import re
import subprocess
import sys

TYPES = "feat|fix|perf|revert|docs|refactor|test|chore|ci|build|style"
TITLE_RE = re.compile(rf"^(?P<type>{TYPES})(\((?P<scope>[^)]+)\))?(?P<breaking>!)?: \S")
SKILL_PATH_RE = re.compile(r"^plugins/[^/]+/skills/(?P<skill>[^/]+)/")
RELEASE_TITLE_RE = re.compile(r"^chore(\([^)]*\))?: release\b")


def problems(title, files):
    """Return the list of reasons the title does not fit the files (empty: fits)."""
    if RELEASE_TITLE_RE.match(title):
        return []
    match = TITLE_RE.match(title)
    if not match:
        return [f"title is not a Conventional Commit ({TYPES.replace('|', ', ')}): {title!r}"]
    touched = sorted({m.group("skill") for f in files if (m := SKILL_PATH_RE.match(f))})
    scopes = {s.strip() for s in (match.group("scope") or "").split(",") if s.strip()}
    missing = [skill for skill in touched if skill not in scopes]
    if missing:
        wanted = ",".join(touched)
        return [f"the change touches the skill(s) {', '.join(missing)} but the scope does not name them; use {match.group('type')}({wanted}): ..."]
    return []


def changed_files(base):
    # Three dots: what the branch changed since it left the base.
    result = subprocess.run(["git", "diff", "--name-only", f"{base}...HEAD"], check=True, capture_output=True, text=True)
    return result.stdout.split()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check a pull request title's scope against the skills it touches.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--base", help="git ref; the changed files are taken from git diff <base>...HEAD")
    parser.add_argument("files", nargs="*")
    args = parser.parse_args(argv)

    files = list(args.files)
    if args.base:
        files += changed_files(args.base)
    found = problems(args.title, files)
    for problem in found:
        print(problem)
    if not found:
        print("ok")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
