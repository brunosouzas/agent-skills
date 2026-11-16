"""Tests for plugins/azure-devops/skills/azure-devops/scripts/check-pipelines.py.

What: each test writes a small pipeline and checks what the script reports.
Why: the script is the check of ADO-5, ADOD-2 and ADOD-3; a wrong report sends
an agent after a problem that is not there, or lets one through.
Run: python3 -m unittest discover -s tests -v (from the repository root).
"""

import unittest

from skill_script import load, run

check = load("plugins/azure-devops/skills/azure-devops/scripts/check-pipelines.py", "check_pipelines")

CLEAN = """trigger:
  branches:
    include: [main]
resources:
  repositories:
    - repository: templates
      type: github
      name: org/pipeline-templates
      endpoint: github
      ref: refs/tags/v1.4.0
      trigger:
        - main
  pipelines:
    - pipeline: upstream
      source: build
pool:
  vmImage: ubuntu-24.04
stages:
  - stage: Prod
    condition: and(succeeded(), startsWith(variables['Build.SourceBranch'], 'refs/tags/v'))
    jobs:
      - template: jobs/deploy.yml@templates
"""


def rules(out):
    return [line.split(": ", 1)[1].split(" ", 1)[0] for line in out.splitlines()]


class CheckPipelinesTest(unittest.TestCase):
    def test_clean_pipeline_passes(self):
        self.assertEqual(run(check, {"azure-pipelines.yml": CLEAN})[:2], (0, ""))

    def test_branch_missing_and_expression_refs_fail(self):
        branch = CLEAN.replace("ref: refs/tags/v1.4.0", "ref: refs/heads/main")
        missing = CLEAN.replace("      ref: refs/tags/v1.4.0\n", "")
        expression = CLEAN.replace("ref: refs/tags/v1.4.0", "ref: refs/tags/${{ variables.version }}")
        for text, words in ((branch, "follows refs/heads/main"), (missing, "has no ref"), (expression, "from an expression")):
            code, out, _ = run(check, {"azure-pipelines.yml": text})
            self.assertEqual((code, rules(out)), (1, ["ADO-5"]), text)
            self.assertIn(words, out)

    def test_flow_style_and_unindented_items_are_read(self):
        text = CLEAN.replace(
            "    - repository: templates\n      type: github\n      name: org/pipeline-templates\n      endpoint: github\n      ref: refs/tags/v1.4.0\n      trigger:\n        - main\n",
            "  - { repository: templates, type: github, name: org/t, ref: refs/heads/dev }\n  - repository: other\n    type: git\n    name: p/other\n")
        code, out, _ = run(check, {"azure-pipelines.yml": text})
        self.assertEqual(rules(out), ["ADO-5", "ADO-5"])
        self.assertIn("'templates' follows refs/heads/dev", out)
        self.assertIn("'other' has no ref", out)

    def test_latest_image_fails(self):
        code, out, _ = run(check, {"azure-pipelines.yml": CLEAN.replace("vmImage: ubuntu-24.04", "vmImage: 'ubuntu-latest'")})
        self.assertEqual(rules(out), ["ADOD-2"])

    def test_source_branch_name_in_conditions_fails(self):
        inline = CLEAN.replace("variables['Build.SourceBranch']", "variables['Build.SourceBranchName']")
        block = CLEAN.replace(
            "    condition: and(succeeded(), startsWith(variables['Build.SourceBranch'], 'refs/tags/v'))\n",
            "    condition: |\n      and(succeeded(),\n          eq(variables['Build.SourceBranchName'], 'main'))\n")
        template = CLEAN + "  - ${{ if eq(variables['Build.SourceBranchName'], 'main') }}:\n    - stage: Extra\n"
        for text in (inline, block, template):
            self.assertEqual(rules(run(check, {"azure-pipelines.yml": text})[1]), ["ADOD-3"], text)

    def test_source_branch_name_outside_a_condition_passes(self):
        text = CLEAN + "variables:\n  branchLabel: $(Build.SourceBranchName)\n"
        self.assertEqual(run(check, {"azure-pipelines.yml": text})[:2], (0, ""))

    def test_non_pipeline_yaml_is_skipped_and_missing_path_is_an_error(self):
        self.assertEqual(run(check, {"config.yaml": "vmImage: ubuntu-latest\n"})[0], 0)
        self.assertEqual(run(check, {}, ["/no/such/file.yml"])[0], 2)

    def test_quoted_keys_are_read(self):
        text = CLEAN.replace("vmImage: ubuntu-24.04", "'vmImage': ubuntu-latest")
        self.assertEqual(rules(run(check, {"azure-pipelines.yml": text})[1]), ["ADOD-2"])


if __name__ == "__main__":
    unittest.main()
