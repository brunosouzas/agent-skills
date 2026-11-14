"""Helpers shared by the tests of the skills' scripts.

What: loads a skill's script by path and runs its main() on files written to
a temporary folder, capturing the exit code, stdout and stderr.
Why: the scripts' file names have hyphens, so they cannot be imported, and
every script test needs the same temporary-folder run.
Run: imported by tests/test_*.py; python3 -m unittest discover -s tests -v.
"""

import importlib.util
import io
import tempfile
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(relative_path, name):
    # Load a script by its path; its main() and helpers become attributes.
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(module, files, args=None):
    """Write {relative name: text} to a temporary folder and run main([folder])."""
    with tempfile.TemporaryDirectory() as folder:
        for name, text in files.items():
            path = Path(folder) / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = module.main(args if args is not None else [folder])
        return code, out.getvalue(), err.getvalue()
