"""Tests for plugins/shell/skills/shell/scripts/check-shell.py.

What: each test writes a small script and checks what the script reports.
Why: the script is the check of SH-1 and SHP-3; a wrong report sends an agent
after a problem that is not there, or lets one through.
Run: python3 -m unittest discover -s tests -v (from the repository root).
"""

import unittest

from skill_script import load, run

check = load("plugins/shell/skills/shell/scripts/check-shell.py", "check_shell")


def rules(out):
    return [line.split(": ", 1)[1].split(" ", 1)[0] for line in out.splitlines()]


class CheckShellTest(unittest.TestCase):
    def test_strict_bash_script_passes(self):
        text = '#!/usr/bin/env bash\n# Builds the site.\nset -euo pipefail\nwork=$(mktemp -d)\ntrap \'rm -rf "${work:?}"\' EXIT\n'
        self.assertEqual(run(check, {"build.sh": text})[:2], (0, ""))

    def test_long_and_split_forms_count(self):
        long_form = "#!/bin/bash\nset -o errexit -o nounset -o pipefail\necho ok\n"
        split = "#!/bin/bash\nset -e\nset -u\nset -o pipefail\necho ok\n"
        for text in (long_form, split):
            self.assertEqual(run(check, {"a.sh": text})[0], 0, text)

    def test_missing_or_late_strict_mode_fails(self):
        missing = "#!/bin/bash\necho start\n"
        late = "#!/bin/bash\necho start\nset -euo pipefail\n"
        partial = "#!/bin/bash\nset -eu\necho start\n"
        for text in (missing, late, partial):
            code, out, _ = run(check, {"a.sh": text})
            self.assertEqual((code, rules(out)), (1, ["SH-1"]), text)

    def test_posix_sh_needs_only_eu(self):
        self.assertEqual(run(check, {"a.sh": "#!/bin/sh\nset -eu\necho ok\n"})[0], 0)
        code, out, _ = run(check, {"a.sh": "#!/bin/sh\necho ok\n"})
        self.assertIn("set -eu", out)

    def test_fixed_tmp_paths_fail_but_mktemp_and_tmpdir_pass(self):
        text = "#!/bin/bash\nset -euo pipefail\nlog=/tmp/build.log\ncp a /var/tmp/cache.db\n# /tmp/ok-in-a-comment\nt=$(mktemp /tmp/x.XXXXXX)\nd=\"$TMPDIR/tmp/y\"\n"
        code, out, _ = run(check, {"a.sh": text})
        self.assertEqual(rules(out), ["SHP-3", "SHP-3"])
        self.assertIn("/tmp/build.log", out)
        self.assertIn("/var/tmp/cache.db", out)

    def test_files_without_shell_marks_are_skipped_in_folders(self):
        files = {"notes.txt": "echo /tmp/x\n", "hook": "#!/bin/bash\necho x\n", "image.png": "x"}
        code, out, _ = run(check, files)
        self.assertEqual(rules(out), ["SH-1"])
        self.assertIn("hook", out)

    def test_missing_path_is_an_error(self):
        self.assertEqual(run(check, {}, ["/no/such/script.sh"])[0], 2)

    def test_zsh_setopt_counts(self):
        text = "#!/bin/zsh\nsetopt err_exit no_unset pipe_fail\necho ok\n"
        self.assertEqual(run(check, {"a.zsh": text})[:2], (0, ""))

    def test_length_expansion_is_not_a_comment(self):
        text = "#!/bin/bash\nset -euo pipefail\necho ${#arr[@]} > /tmp/count.txt # note\n"
        self.assertEqual(rules(run(check, {"a.sh": text})[1]), ["SHP-3"])


if __name__ == "__main__":
    unittest.main()
