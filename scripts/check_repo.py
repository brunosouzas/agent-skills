#!/usr/bin/env python3
"""Check that the marketplace, the plugins and their skills follow CONTRIBUTING.md.

What it does
    Reads the whole repository and reports every problem it finds:
    - manifests: both marketplaces list every folder in plugins/ and nothing
      else; each plugin has a Claude and a Codex plugin.json named after its
      folder;
    - skills: frontmatter (name equal to the folder, description, license,
      metadata.version on a line marked x-release-please-version,
      metadata.aliases), size (SKILL.md ~100 lines, a rules file over ~150
      lines must be split into references/), a CHANGELOG.md, no personal or
      process facts (writing rules 1 and 5);
    - names: skill names and aliases are unique across the repository;
    - rule IDs: unique across the repository, and with --base, every ID that
      exists on the base still exists (a rule is retired, never deleted);
    - versions: release-please has one package per skill and per plugin, and
      SKILL.md, the Codex plugin.json and the manifest agree;
    - evals: every skill has a case that must load it and one that must not;
    - links: every relative Markdown link points at a file that exists.

Why it exists
    These rules have one right answer, so CI checks them instead of a reviewer
    (CONTRIBUTING.md, rule 4). The workflow .github/workflows/ci.yml runs it.

How to run
    python3 scripts/check_repo.py [--base <git ref>]
    From the repository root, Python 3.9 or newer, standard library only.
    --base compares rule IDs with that ref (CI passes the pull request's base).
    Exit code: 0 clean, 1 problems printed.

What can go wrong
    - The frontmatter reader understands the subset of YAML the skills use
      (key: value, quoted strings, one nested metadata map). Anything fancier
      is reported as a problem, on purpose: keep frontmatter simple.
    - --base needs the ref fetched (actions/checkout with fetch-depth: 0).
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Limits from CONTRIBUTING.md; "about 100" and "about 150" leave a small margin.
SKILL_MAX_LINES = 110
RULES_MAX_LINES = 160
DESCRIPTION_MAX = 1024  # the Agent Skills specification's limit
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
RULE_ID_RE = re.compile(r"^- \*\*([A-Z]+-\d+)\*\*", re.MULTILINE)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")

# Writing rules 1 and 5: a specialty cites no process, person or environment.
# Matched case-insensitively in a skill's files, scripts excluded (a script may
# name a path in an example).
PERSONAL_FACTS = [
    (re.compile(r"\bAB#\d+"), "a board card"),
    (re.compile(r"/Users/|~/code/"), "a personal path"),
    (re.compile(r"\bJAVA_HOME\b"), "an environment fact"),
    (re.compile(r"\bvault\b", re.I), "a personal vault"),
    (re.compile(r"\bplaybook\b", re.I), "a process (playbook)"),
    (re.compile(r"\bbruno\b|\bbrunosouzas\b", re.I), "a person"),
]


class Report:
    def __init__(self):
        self.problems = []

    def add(self, where, message):
        self.problems.append(f"{where}: {message}")


def rel(path):
    return path.relative_to(ROOT).as_posix()


def read_json(path, report):
    # A manifest that is not valid JSON stops the checks that need it.
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        report.add(rel(path), f"cannot read JSON: {error}")
        return None


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def strip_comment(value):
    # A # starts a comment only outside quotes (the version line has one).
    quote = None
    for i, char in enumerate(value):
        if char in "\"'":
            quote = None if quote == char else (quote or char)
        elif char == "#" and quote is None and (i == 0 or value[i - 1] == " "):
            return value[:i].rstrip(), value[i:]
    return value, ""


def read_frontmatter(path, report):
    """Return ({key: value, 'metadata': {...}}, {key: raw line}) or (None, None)."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        report.add(rel(path), "no frontmatter between --- lines")
        return None, None
    block = text[4:text.index("\n---\n", 4)]
    fields, raw, current = {}, {}, None
    for line in block.splitlines():
        if not line.strip():
            continue
        # Nested keys belong to the last top-level key (only metadata nests).
        if line.startswith("  ") and current == "metadata":
            key, _, value = line.strip().partition(":")
            value, _ = strip_comment(value)
            fields["metadata"][key.strip()] = unquote(value)
            raw[f"metadata.{key.strip()}"] = line
            continue
        if line.startswith(" ") or ":" not in line:
            report.add(rel(path), f"frontmatter line not understood: {line.strip()!r}")
            continue
        key, _, value = line.partition(":")
        key, (value, _) = key.strip(), strip_comment(value)
        current = key
        fields[key] = {} if key == "metadata" and not value.strip() else unquote(value)
        raw[key] = line
    return fields, raw


def plugin_dirs():
    return sorted(p for p in (ROOT / "plugins").iterdir() if p.is_dir())


def check_marketplaces(report):
    # Both marketplaces list exactly the folders in plugins/.
    folders = {p.name for p in plugin_dirs()}
    claude = read_json(ROOT / ".claude-plugin/marketplace.json", report)
    if claude:
        listed = {}
        for entry in claude.get("plugins", []):
            listed[entry.get("name")] = entry.get("source")
        for name in folders - listed.keys():
            report.add(".claude-plugin/marketplace.json", f"plugin '{name}' is not listed")
        for name, source in listed.items():
            if source != f"./plugins/{name}":
                report.add(".claude-plugin/marketplace.json", f"plugin '{name}' must have source ./plugins/{name}")
            if "version" in next(e for e in claude["plugins"] if e.get("name") == name):
                report.add(".claude-plugin/marketplace.json", f"plugin '{name}': no version here (see docs/releasing.md)")
    codex = read_json(ROOT / ".agents/plugins/marketplace.json", report)
    if codex:
        listed = {e.get("name"): e.get("source", {}) for e in codex.get("plugins", [])}
        for name in folders - listed.keys():
            report.add(".agents/plugins/marketplace.json", f"plugin '{name}' is not listed")
        for name, source in listed.items():
            if not isinstance(source, dict) or source.get("path") != f"./plugins/{name}":
                report.add(".agents/plugins/marketplace.json", f"plugin '{name}' must have source.path ./plugins/{name}")


def check_plugin(plugin, report, versions):
    # Each plugin has both manifests, named after its folder.
    claude = read_json(plugin / ".claude-plugin/plugin.json", report)
    codex = read_json(plugin / ".codex-plugin/plugin.json", report)
    for data, file in ((claude, ".claude-plugin/plugin.json"), (codex, ".codex-plugin/plugin.json")):
        if data and data.get("name") != plugin.name:
            report.add(f"{rel(plugin)}/{file}", f"name must be '{plugin.name}'")
    if claude and "version" in claude:
        # Claude Code takes the commit as the version when there is none, so a
        # skill change always reaches users (docs/releasing.md).
        report.add(f"{rel(plugin)}/.claude-plugin/plugin.json", "must not set version (docs/releasing.md)")
    if codex:
        if codex.get("skills") != "./skills/":
            report.add(f"{rel(plugin)}/.codex-plugin/plugin.json", "skills must be ./skills/")
        expected = versions.get(rel(plugin))
        if expected and codex.get("version") != expected:
            report.add(f"{rel(plugin)}/.codex-plugin/plugin.json", f"version {codex.get('version')} differs from the manifest's {expected}")
    if not (plugin / "CHANGELOG.md").is_file():
        report.add(rel(plugin), "no CHANGELOG.md")


def check_skill(skill, report, versions, names, aliases):
    where = rel(skill / "SKILL.md")
    fields, raw = read_frontmatter(skill / "SKILL.md", report)
    if fields is None:
        return
    # Name: the folder's, in the Agent Skills format, unique in the repository.
    name = fields.get("name", "")
    if name != skill.name or not NAME_RE.match(name) or len(name) > 64:
        report.add(where, f"name must be the folder name '{skill.name}' (lowercase words and hyphens)")
    if name in names:
        report.add(where, f"skill name '{name}' also used by {names[name]}")
    names[name] = where
    # Description: writing rule 2 (what, when, triggers, when not).
    description = fields.get("description", "")
    if not description or len(description) > DESCRIPTION_MAX:
        report.add(where, f"description must be 1 to {DESCRIPTION_MAX} characters")
    for marker in ("Use when", "Triggers:", "Not for"):
        if marker not in description:
            report.add(where, f"description must say '{marker}' (CONTRIBUTING.md, rule 2)")
    if not fields.get("license"):
        report.add(where, "no license")
    # Version and aliases live in metadata (string values, as the standard asks).
    metadata = fields.get("metadata")
    if not isinstance(metadata, dict):
        report.add(where, "no metadata map")
        return
    version = metadata.get("version", "")
    if not SEMVER_RE.match(version):
        report.add(where, "metadata.version must be MAJOR.MINOR.PATCH")
    if "# x-release-please-version" not in raw.get("metadata.version", ""):
        report.add(where, "metadata.version line must end with # x-release-please-version")
    expected = versions.get(rel(skill))
    if expected is None:
        report.add(where, "no release-please package for this skill")
    elif version != expected:
        report.add(where, f"metadata.version {version} differs from the manifest's {expected}")
    for alias in [a.strip().lower() for a in metadata.get("aliases", "").split(",") if a.strip()]:
        if alias in aliases and aliases[alias] != name:
            report.add(where, f"alias '{alias}' also used by skill '{aliases[alias]}'")
        aliases.setdefault(alias, name)
    # Size: writing rule 3.
    lines = len((skill / "SKILL.md").read_text(encoding="utf-8").splitlines())
    if lines > SKILL_MAX_LINES:
        report.add(where, f"{lines} lines; keep SKILL.md to about 100 (CONTRIBUTING.md, rule 3)")
    for extra in skill.glob("*.md"):
        if extra.name in ("SKILL.md", "CHANGELOG.md"):
            continue
        count = len(extra.read_text(encoding="utf-8").splitlines())
        if count > RULES_MAX_LINES:
            report.add(rel(extra), f"{count} lines; split it into references/ by subject (CONTRIBUTING.md, rule 3)")
    if not (skill / "CHANGELOG.md").is_file():
        report.add(rel(skill), "no CHANGELOG.md")
    # Writing rules 1 and 5: no person, process or environment in the text.
    for path in [skill / "SKILL.md", *skill.glob("*.md"), *skill.glob("references/**/*.md")]:
        if path.name == "CHANGELOG.md":
            continue
        text = path.read_text(encoding="utf-8")
        for pattern, what in PERSONAL_FACTS:
            match = pattern.search(text)
            if match:
                report.add(rel(path), f"names {what} ('{match.group(0)}'); keep it out of a public skill")


def check_release_config(report):
    """Check release-please's config and manifest; return the manifest."""
    config = read_json(ROOT / "release-please-config.json", report) or {}
    manifest = read_json(ROOT / ".release-please-manifest.json", report) or {}
    packages = config.get("packages", {})
    wanted = set()
    for plugin in plugin_dirs():
        wanted.add(rel(plugin))
        wanted.update(rel(s) for s in sorted((plugin / "skills").iterdir()) if (s / "SKILL.md").is_file())
    for path in sorted(wanted - packages.keys()):
        report.add("release-please-config.json", f"no package for {path}")
    for path in sorted(packages.keys() - wanted):
        report.add("release-please-config.json", f"package {path} is not a plugin or a skill")
    for path in sorted(packages.keys() ^ manifest.keys()):
        report.add(".release-please-manifest.json", f"{path} must be in both the config and the manifest")
    # Each package writes its version where the tools read it.
    for path, package in packages.items():
        files = {f.get("path") for f in package.get("extra-files", [])}
        needed = ".codex-plugin/plugin.json" if path.count("/") == 1 else "SKILL.md"
        if needed not in files:
            report.add("release-please-config.json", f"{path} must list {needed} in extra-files")
    components = [p.get("component") for p in packages.values()]
    for component in {c for c in components if components.count(c) > 1}:
        report.add("release-please-config.json", f"component '{component}' is used twice (tags would collide)")
    return manifest


def rule_ids(text):
    return RULE_ID_RE.findall(text)


def check_rule_ids(report, base):
    # IDs are unique across the repository: a reviewer's citation finds one rule.
    seen, current = {}, set()
    for path in sorted(ROOT.glob("plugins/*/skills/*/**/*.md")):
        if path.name in ("SKILL.md", "CHANGELOG.md"):
            continue
        for rule in rule_ids(path.read_text(encoding="utf-8")):
            if rule in seen:
                report.add(rel(path), f"rule {rule} is also defined in {seen[rule]}")
            seen.setdefault(rule, rel(path))
            current.add(rule)
    if not base:
        return
    # Writing rule 6: an ID on the base never disappears (retire it instead).
    try:
        files = subprocess.run(["git", "ls-tree", "-r", "--name-only", base, "--", "plugins"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.split()
        before = set()
        for file in files:
            if "/skills/" in file and file.endswith(".md") and not file.endswith(("SKILL.md", "CHANGELOG.md")):
                text = subprocess.run(["git", "show", f"{base}:{file}"], cwd=ROOT, check=True, capture_output=True, text=True).stdout
                before.update(rule_ids(text))
    except subprocess.CalledProcessError as error:
        report.add("--base", f"cannot read {base}: {error.stderr.strip()}")
        return
    for rule in sorted(before - current):
        report.add("rule IDs", f"{rule} was removed; mark it retired instead (CONTRIBUTING.md, rule 6)")


def check_evals(report):
    # Writing rule 7: each skill has a case that must load it and one that must not.
    for plugin in plugin_dirs():
        cases = [p.read_text(encoding="utf-8") for p in (plugin / "evals").glob("*/case.yaml")]
        for skill in sorted((plugin / "skills").iterdir()):
            if not (skill / "SKILL.md").is_file():
                continue
            if not any(f"name: loads-{skill.name}\n" in c for c in cases):
                report.add(rel(skill), f"no eval case that must load it (a grader named loads-{skill.name})")
            if not any(f"name: does-not-load-{skill.name}\n" in c for c in cases):
                report.add(rel(skill), f"no eval case that must not load it (a grader named does-not-load-{skill.name})")


def check_links(report):
    # Every relative link in a Markdown file points at something that exists.
    for path in sorted(ROOT.rglob("*.md")):
        if any(part in (".git", "node_modules", "results") for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        # Links inside code are examples, not links.
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        text = re.sub(r"`[^`]*`", "", text)
        for target in LINK_RE.findall(text):
            if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                continue
            file = target.split("#", 1)[0]
            if file and not (path.parent / file).exists():
                report.add(rel(path), f"broken link: {target}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check the marketplace, plugins and skills against CONTRIBUTING.md.")
    parser.add_argument("--base", help="git ref to compare rule IDs with (a removed ID fails)")
    args = parser.parse_args(argv)

    report = Report()
    versions = check_release_config(report)
    check_marketplaces(report)
    names, aliases = {}, {}
    for plugin in plugin_dirs():
        check_plugin(plugin, report, versions)
        for skill in sorted((plugin / "skills").iterdir()):
            if skill.is_dir():
                if not (skill / "SKILL.md").is_file():
                    report.add(rel(skill), "folder without SKILL.md")
                    continue
                check_skill(skill, report, versions, names, aliases)
    # An alias equal to another skill's name would route a request twice.
    for alias, owner in aliases.items():
        if alias in names and alias != owner:
            report.add("aliases", f"alias '{alias}' of '{owner}' is the name of another skill")
    check_rule_ids(report, args.base)
    check_evals(report)
    check_links(report)

    for problem in report.problems:
        print(problem)
    print(f"{len(report.problems)} problem(s)" if report.problems else "ok")
    return 1 if report.problems else 0


if __name__ == "__main__":
    sys.exit(main())
