"""Tests for scripts/check_commit_scope.py and scripts/check_repo.py.

What: the scope rule on pull request titles, the frontmatter reader, and the
repository as it is (check_repo must pass on the real tree).
Why: CI trusts these scripts to block a wrong title or a broken skill; a bug
here lets a skill ship without its version, evals or changelog line.
Run: python3 -m unittest discover -s tests -v (from the repository root).
"""

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_commit_scope  # noqa: E402
import check_repo  # noqa: E402

DW = "plugins/mulesoft/skills/dataweave/rules.md"
MUNIT = "plugins/mulesoft/skills/munit/SKILL.md"


class CommitScopeTest(unittest.TestCase):
    def test_scope_naming_the_skill_passes(self):
        self.assertEqual(check_commit_scope.problems("feat(dataweave): add DW-10", [DW]), [])

    def test_missing_scope_on_a_skill_fails(self):
        found = check_commit_scope.problems("fix: typo", [DW])
        self.assertEqual(len(found), 1)
        self.assertIn("fix(dataweave): ...", found[0])

    def test_every_touched_skill_must_be_named(self):
        found = check_commit_scope.problems("fix(dataweave): x", [DW, MUNIT])
        self.assertIn("munit", found[0])
        self.assertEqual(check_commit_scope.problems("fix(dataweave, munit)!: x", [DW, MUNIT]), [])

    def test_change_outside_skills_needs_no_scope(self):
        self.assertEqual(check_commit_scope.problems("ci: pin actions", [".github/workflows/ci.yml"]), [])

    def test_title_must_be_conventional(self):
        self.assertTrue(check_commit_scope.problems("Update dataweave rules", [DW]))
        self.assertTrue(check_commit_scope.problems("feature(dataweave): x", [DW]))

    def test_release_pull_request_is_exempt(self):
        self.assertEqual(check_commit_scope.problems("chore(main): release dataweave 1.1.0", [DW]), [])


class FrontmatterTest(unittest.TestCase):
    def read(self, text):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "SKILL.md"
            path.write_text(text, encoding="utf-8")
            report = check_repo.Report()
            # rel() needs a path under the repository; point ROOT at the folder.
            root, check_repo.ROOT = check_repo.ROOT, Path(folder)
            try:
                fields, raw = check_repo.read_frontmatter(path, report)
            finally:
                check_repo.ROOT = root
            return fields, raw, report.problems

    def test_reads_metadata_and_keeps_the_marker_line(self):
        fields, raw, problems = self.read('---\nname: x\ndescription: "a: b # not a comment"\nmetadata:\n  version: "1.2.3" # x-release-please-version\n  aliases: "a, b"\n---\nbody\n')
        self.assertEqual(problems, [])
        self.assertEqual(fields["description"], "a: b # not a comment")
        self.assertEqual(fields["metadata"], {"version": "1.2.3", "aliases": "a, b"})
        self.assertIn("# x-release-please-version", raw["metadata.version"])

    def test_missing_frontmatter_is_a_problem(self):
        fields, _, problems = self.read("# no frontmatter\n")
        self.assertIsNone(fields)
        self.assertEqual(len(problems), 1)


class RepositoryTest(unittest.TestCase):
    def test_the_repository_passes_its_own_check(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = check_repo.main([])
        self.assertEqual(code, 0, out.getvalue())


if __name__ == "__main__":
    unittest.main()
