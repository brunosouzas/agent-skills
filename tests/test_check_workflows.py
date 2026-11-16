"""Tests for plugins/github-actions/skills/github-actions/scripts/check-workflows.py.

What: each test writes a small workflow or action and checks what the script reports.
Why: the script is the check of GHAS-1 to GHAS-6, GHA-1 and GHA-2; a wrong
report sends an agent after a problem that is not there, or lets one through.
Run: python3 -m unittest discover -s tests -v (from the repository root).
"""

import unittest

from skill_script import ROOT, load, run

check = load("plugins/github-actions/skills/github-actions/scripts/check-workflows.py", "check_workflows")

SHA = "3d3c42e5aac5ba805825da76410c181273ba90b1"

CLEAN = f"""name: CI
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@{SHA} # v7.0.1
        with:
          persist-credentials: false
      - name: Title
        env:
          TITLE: ${{{{ github.event.pull_request.title }}}}
        run: |
          echo "$TITLE"
  release:
    uses: owner/repo/.github/workflows/release.yml@{SHA} # v0.1.0
    permissions:
      contents: write
    secrets:
      KEY: ${{{{ secrets.KEY }}}}
"""


def rules(out):
    # The rule IDs the script printed, in order.
    return [line.split(": ", 1)[1].split(" ", 1)[0] for line in out.splitlines()]


class CheckWorkflowsTest(unittest.TestCase):
    def test_clean_workflow_passes(self):
        code, out, _ = run(check, {"ci.yml": CLEAN})
        self.assertEqual((code, out), (0, ""))

    def test_tag_pin_and_short_sha_fail(self):
        text = CLEAN.replace(f"actions/checkout@{SHA}", "actions/checkout@v4")
        text = text.replace(f"release.yml@{SHA}", "release.yml@3d3c42e")
        code, out, _ = run(check, {"ci.yml": text})
        self.assertEqual(code, 1)
        self.assertEqual(rules(out), ["GHAS-1", "GHAS-1"])

    def test_local_and_digest_pins_pass(self):
        text = CLEAN.replace(f"actions/checkout@{SHA} # v7.0.1", "./.github/actions/setup") + \
            "  extra:\n    runs-on: ubuntu-24.04\n    timeout-minutes: 5\n    steps:\n      - uses: docker://alpine@sha256:" + "a" * 64 + "\n"
        code, out, _ = run(check, {"ci.yml": text})
        self.assertEqual((code, out), (0, ""))

    def test_untrusted_expression_in_run_fails(self):
        text = CLEAN.replace('echo "$TITLE"', 'echo "${{ github.event.pull_request.title }}" ${{ github.head_ref }}')
        code, out, _ = run(check, {"ci.yml": text})
        self.assertEqual(code, 1)
        self.assertEqual(rules(out), ["GHAS-3", "GHAS-3"])

    def test_inline_run_and_github_script_are_read(self):
        text = CLEAN.replace("        run: |\n          echo \"$TITLE\"", "        run: echo ${{ inputs.name }}") + \
            f"  script:\n    runs-on: ubuntu-24.04\n    timeout-minutes: 5\n    steps:\n      - uses: actions/github-script@{SHA}\n        with:\n          script: |\n            console.log(`${{{{ github.event.issue.body }}}}`)\n"
        code, out, _ = run(check, {"ci.yml": text})
        self.assertEqual(rules(out), ["GHAS-3", "GHAS-3"])

    def test_safe_expressions_in_run_pass(self):
        text = CLEAN.replace('echo "$TITLE"', 'echo "${{ github.sha }} ${{ github.event.pull_request.number }} ${{ runner.temp }}"')
        code, out, _ = run(check, {"ci.yml": text})
        self.assertEqual((code, out), (0, ""))

    def test_pull_request_target_fails_but_an_if_naming_it_passes(self):
        code, out, _ = run(check, {"ci.yml": CLEAN.replace("  pull_request:\n", "  pull_request_target:\n")})
        self.assertEqual(rules(out), ["GHAS-4"])
        text = CLEAN.replace("    runs-on: ubuntu-24.04\n    timeout-minutes: 10\n", "    if: github.event_name == 'pull_request_target'\n    runs-on: ubuntu-24.04\n    timeout-minutes: 10\n", 1)
        self.assertEqual(run(check, {"ci.yml": text})[0], 0)

    def test_checkout_without_persist_credentials_fails(self):
        code, out, _ = run(check, {"ci.yml": CLEAN.replace("        with:\n          persist-credentials: false\n", "")})
        self.assertEqual(rules(out), ["GHAS-5"])

    def test_write_permissions_at_workflow_level_and_write_all_fail(self):
        code, out, _ = run(check, {"ci.yml": CLEAN.replace("permissions:\n  contents: read\n", "permissions:\n  contents: write\n")})
        self.assertEqual(rules(out), ["GHAS-2"])
        code, out, _ = run(check, {"ci.yml": CLEAN.replace("permissions:\n  contents: read\n", "permissions: write-all\n")})
        self.assertEqual(rules(out), ["GHAS-2"])

    def test_without_workflow_permissions_every_job_needs_its_own(self):
        code, out, _ = run(check, {"ci.yml": CLEAN.replace("permissions:\n  contents: read\n", "")})
        self.assertEqual(code, 1)
        self.assertIn("job 'test' has no permissions", out)
        self.assertNotIn("job 'release'", out)

    def test_secrets_inherit_fails(self):
        text = CLEAN.replace("    secrets:\n      KEY: ${{ secrets.KEY }}\n", "    secrets: inherit\n")
        code, out, _ = run(check, {"ci.yml": text})
        self.assertEqual(rules(out), ["GHAS-6"])

    def test_latest_runner_and_missing_timeout_fail(self):
        text = CLEAN.replace("    runs-on: ubuntu-24.04\n    timeout-minutes: 10\n", "    runs-on: ubuntu-latest\n")
        code, out, _ = run(check, {"ci.yml": text})
        self.assertEqual(sorted(rules(out)), ["GHA-1", "GHA-2"])

    def test_composite_action_checks_uses_and_scripts_only(self):
        action = "name: setup\nruns:\n  using: composite\n  steps:\n    - uses: actions/setup-node@v4\n    - run: echo ${{ inputs.version }}\n      shell: bash\n"
        code, out, _ = run(check, {"action.yml": action})
        self.assertEqual(rules(out), ["GHAS-1", "GHAS-3"])

    def test_other_yaml_is_skipped_and_missing_path_is_an_error(self):
        self.assertEqual(run(check, {"config.yml": "name: x\nrun: echo ${{ inputs.x }}\n"})[0], 0)
        code, _, err = run(check, {}, ["/no/such/folder"])
        self.assertEqual(code, 2)
        self.assertIn("no such file", err)

    def test_this_repository_workflows_pass(self):
        # The repository follows the skill it publishes.
        code, out, err = run(check, {}, [str(ROOT / ".github/workflows")])
        self.assertEqual((code, out, err), (0, "", ""))

    def test_quoted_on_key_is_read(self):
        text = CLEAN.replace("on:\n  pull_request:\n", '"on":\n  pull_request_target:\n')
        self.assertEqual(rules(run(check, {"ci.yml": text})[1]), ["GHAS-4"])

    def test_more_untrusted_fields_fail_and_base_repository_name_passes(self):
        for expression in ("github.event.workflow_run.head_branch", "github.event.workflow_run.display_title",
                           "github.event.pull_request.head.repo.full_name", "github.event.head_commit.author.email"):
            text = CLEAN.replace('echo "$TITLE"', f'echo "${{{{ {expression} }}}}"')
            self.assertEqual(rules(run(check, {"ci.yml": text})[1]), ["GHAS-3"], expression)
        text = CLEAN.replace('echo "$TITLE"', 'echo "${{ github.event.repository.name }}"')
        self.assertEqual(run(check, {"ci.yml": text})[:2], (0, ""))

    def test_secret_in_script_fails(self):
        text = CLEAN.replace('echo "$TITLE"', 'echo "${{ secrets.TOKEN }}" | gh auth login --with-token')
        self.assertEqual(rules(run(check, {"ci.yml": text})[1]), ["GHAS-6"])

    def test_flow_style_persist_credentials_and_write_all_in_text(self):
        text = CLEAN.replace("        with:\n          persist-credentials: false\n", "        with: { persist-credentials: false }\n")
        text = text.replace('echo "$TITLE"', 'echo "permissions write-all are bad"')
        self.assertEqual(run(check, {"ci.yml": text})[:2], (0, ""))

    def test_latest_runner_in_a_list_fails(self):
        text = CLEAN.replace("    runs-on: ubuntu-24.04\n    timeout-minutes: 10\n", "    runs-on: [self-hosted, ubuntu-latest]\n    timeout-minutes: 10\n")
        self.assertEqual(rules(run(check, {"ci.yml": text})[1]), ["GHA-1"])


if __name__ == "__main__":
    unittest.main()
