"""Tests for plugins/mulesoft/skills/mulesoft/scripts/check-docnames.py.

What: each test writes a small Mule XML file and checks what the script reports.
Why: the script is the check of FLOW-2 and FLOW-4; a wrong report sends an agent
after a problem that is not there, or lets one through.
Run: python3 -m unittest discover -s tests -v (from the repository root).
"""

import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

# The script's file name has a hyphen, so it is loaded by path, not imported.
SCRIPT = Path(__file__).resolve().parents[1] / "plugins/mulesoft/skills/mulesoft/scripts/check-docnames.py"
spec = importlib.util.spec_from_file_location("check_docnames", SCRIPT)
check_docnames = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_docnames)

HEADER = """<?xml version="1.0" encoding="UTF-8"?>
<mule xmlns="http://www.mulesoft.org/schema/mule/core"
      xmlns:doc="http://www.mulesoft.org/schema/mule/documentation"
      xmlns:http="http://www.mulesoft.org/schema/mule/http"
      xmlns:ee="http://www.mulesoft.org/schema/mule/ee/core">
"""


def mule(body):
    return HEADER + body + "\n</mule>\n"


class CheckDocnamesTest(unittest.TestCase):
    def run_script(self, files):
        # Write the files to a temporary folder and run main() on it.
        with tempfile.TemporaryDirectory() as folder:
            for name, text in files.items():
                path = Path(folder) / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = check_docnames.main([folder])
            return code, out.getvalue(), err.getvalue()

    def test_clean_flow_passes(self):
        code, out, _ = self.run_script({"ok.xml": mule("""
  <flow name="orders-main" doc:description="Receives orders from the web shop.">
    <http:listener doc:name="Listen for Orders" config-ref="Main Http Listener Config" path="/orders"/>
    <ee:transform doc:name="Build Order Response">
      <ee:message><ee:set-payload><![CDATA[%dw 2.0
output application/json
---
payload]]></ee:set-payload></ee:message>
    </ee:transform>
    <error-handler>
      <on-error-propagate doc:name="On Error Propagate (Bad Request)" type="APIKIT:BAD_REQUEST">
        <set-variable doc:name="SET vStatus" variableName="vStatus" value="400"/>
      </on-error-propagate>
    </error-handler>
  </flow>""")})
        self.assertEqual(code, 0)
        self.assertEqual(out, "")

    def test_missing_doc_name_is_reported_with_line(self):
        code, out, _ = self.run_script({"a.xml": mule("""
  <sub-flow name="sf-build" doc:description="Builds the request.">
    <set-variable variableName="vId" value="1"/>
  </sub-flow>""")})
        self.assertEqual(code, 1)
        self.assertIn("FLOW-2 <set-variable> has no doc:name", out)
        self.assertIn("a.xml:8:", out)

    def test_palette_default_name_is_reported(self):
        code, out, _ = self.run_script({"a.xml": mule("""
  <flow name="f" doc:description="d">
    <logger doc:name="Logger" message="x"/>
    <choice doc:name="Choose Route">
      <when expression="#[true]"><ee:transform doc:name="Transform Message"/></when>
      <otherwise><flow-ref doc:name="Flow Reference" name="sf-x"/></otherwise>
    </choice>
  </flow>""")})
        self.assertEqual(code, 1)
        self.assertIn("<logger> keeps the palette default name 'Logger'", out)
        self.assertIn("<ee:transform> keeps the palette default name 'Transform Message'", out)
        self.assertIn("<flow-ref> keeps the palette default name 'Flow Reference'", out)
        self.assertNotIn("Choose Route", out)

    def test_missing_or_blank_description_is_reported(self):
        code, out, _ = self.run_script({"a.xml": mule("""
  <flow name="no-note"><logger doc:name="INFO: Log Start"/></flow>
  <sub-flow name="sf-blank" doc:description="  "><logger doc:name="DEBUG: Log X"/></sub-flow>""")})
        self.assertEqual(code, 1)
        self.assertIn("FLOW-4 flow 'no-note' has no doc:description", out)
        self.assertIn("FLOW-4 sub-flow 'sf-blank' has no doc:description", out)

    def test_value_elements_and_nested_processors_are_not_checked(self):
        # Children of a processor that is not a scope (http:request's headers,
        # a choice's when) are not processors of the flow.
        code, out, _ = self.run_script({"a.xml": mule("""
  <flow name="f" doc:description="d">
    <http:request doc:name="Query CRM Accounts" method="GET" config-ref="CRM Http Request Config">
      <http:headers><![CDATA[#[{}]]]></http:headers>
    </http:request>
    <choice doc:name="Route by Status">
      <when expression="#[true]"><logger doc:name="INFO: Log Active"/></when>
    </choice>
  </flow>""")})
        self.assertEqual(code, 0, out)

    def test_files_that_are_not_mule_config_are_skipped(self):
        code, out, _ = self.run_script({"log4j2.xml": "<Configuration><Appenders/></Configuration>"})
        self.assertEqual(code, 0)
        self.assertEqual(out, "")

    def test_malformed_file_exits_2_and_others_still_checked(self):
        code, out, err = self.run_script({
            "bad.xml": "<mule><flow>",
            "good.xml": mule('  <flow name="f"><logger doc:name="INFO: Log"/></flow>'),
        })
        self.assertEqual(code, 2)
        self.assertIn("bad.xml: cannot check", err)
        self.assertIn("FLOW-4 flow 'f'", out)


if __name__ == "__main__":
    unittest.main()
