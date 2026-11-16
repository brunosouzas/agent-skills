"""Tests for plugins/python/skills/python/scripts/check-encoding.py.

What: each test writes a small Python file and checks what the script reports.
Why: the script is the check of PY-4; a wrong report sends an agent after a
problem that is not there, or lets one through.
Run: python3 -m unittest discover -s tests -v (from the repository root).
"""

import unittest

from skill_script import load, run

check = load("plugins/python/skills/python/scripts/check-encoding.py", "check_encoding")


class CheckEncodingTest(unittest.TestCase):
    def lines(self, source):
        return [line for line, _ in check.check_source(source)]

    def test_text_calls_with_encoding_pass(self):
        source = (
            "from pathlib import Path\n"
            "open('a', encoding='utf-8')\n"
            "open('a', 'w', encoding='utf-8')\n"
            "Path('a').read_text(encoding='utf-8')\n"
            "Path('a').write_text('x', encoding='utf-8')\n"
            "Path('a').open('r', encoding='utf-8')\n"
        )
        self.assertEqual(self.lines(source), [])

    def test_text_calls_without_encoding_fail(self):
        source = (
            "import io\n"
            "open('a')\n"
            "open('a', mode='w')\n"
            "io.open('a', 'r')\n"
            "p.read_text()\n"
            "p.write_text('x')\n"
            "p.open()\n"
        )
        self.assertEqual(self.lines(source), [2, 3, 4, 5, 6, 7])

    def test_binary_and_non_text_opens_pass(self):
        source = (
            "import os, tarfile, gzip\n"
            "open('a', 'rb')\n"
            "p.open(mode='wb')\n"
            "os.open('a', os.O_RDONLY)\n"
            "tarfile.open('a.tgz')\n"
            "gzip.open('a.gz')\n"
            "open('a', **options)\n"
        )
        self.assertEqual(self.lines(source), [])

    def test_compressed_text_mode_and_variable_mode_fail(self):
        self.assertEqual(self.lines("import gzip\ngzip.open('a.gz', 'rt')\nopen('a', mode)\n"), [2, 3])

    def test_folders_skip_virtual_environments_and_report_files(self):
        files = {"src/app.py": "open('a')\n", ".venv/lib/x.py": "open('b')\n", "bad.py": "def (:\n"}
        code, out, err = run(check, files)
        self.assertEqual(code, 2)
        self.assertIn("app.py:1: PY-4 open()", out)
        self.assertNotIn(".venv", out)
        self.assertIn("bad.py: cannot check", err)

    def test_clean_folder_exits_zero(self):
        self.assertEqual(run(check, {"a.py": "print('x')\n"})[:2], (0, ""))

    def test_positional_encoding_counts(self):
        source = "p.read_text('utf-8')\np.write_text(data, 'utf-8')\nopen(f, 'r', -1, 'utf-8')\np.open('r', -1, 'utf-8')\n"
        self.assertEqual(self.lines(source), [])

    def test_codecs_and_other_objects_open(self):
        source = "import codecs\ncodecs.open('build.txt', 'r')\ncodecs.open('notes.txt', 'rb', 'utf-8')\nzf.open('member.txt')\np.open('w')\n"
        self.assertEqual(self.lines(source), [2, 5])

    def test_build_folders_are_checked(self):
        code, out, _ = run(check, {"src/tool/build/gen.py": "open('out.txt', 'w')\n"})
        self.assertEqual(code, 1)
        self.assertIn("gen.py:1", out)


if __name__ == "__main__":
    unittest.main()
