# Releasing

[release-please](https://github.com/googleapis/release-please) in manifest mode keeps one release pull request open on `main`. Merging it raises the versions, writes the changelogs, tags each release and creates its GitHub release. Nobody edits versions or changelogs by hand.

## Packages

[release-please-config.json](../release-please-config.json) has one package per skill and one per plugin; [.release-please-manifest.json](../.release-please-manifest.json) holds their current versions.

| Package | Path | Tag | Writes the version to |
|---|---|---|---|
| a skill | `plugins/<plugin>/skills/<skill>` | `<skill>-vX.Y.Z` | the `# x-release-please-version` line of `SKILL.md`, and its `CHANGELOG.md` |
| a plugin | `plugins/<plugin>` | `<plugin>-plugin-vX.Y.Z` | `.codex-plugin/plugin.json`, and the plugin's `CHANGELOG.md` |

release-please gives a commit to a package by the files it changes, taking the deepest package path: a commit that changes `plugins/mulesoft/skills/dataweave/rules.md` belongs to `dataweave`, not to the `mulesoft` plugin. The commit scope does not route anything; CI requires it so the title says the same thing as the paths (CONTRIBUTING.md).

## How a plugin's update reaches users

- **Claude Code** computes a plugin's version from the commit when `plugin.json` sets none. The Claude `plugin.json` and the marketplace entry therefore set no `version`, and every merged change reaches users on their next update. `scripts/check_repo.py` refuses a `version` there.
- **Codex** reads the `version` of `.codex-plugin/plugin.json`, which the plugin package raises. Because a skill-only commit belongs to the skill's package, not the plugin's, a release that changes only skills does not raise the plugin's version today. Until this is settled, a pull request that changes a skill and must reach Codex users also needs a plugin-level change (for example a line in the plugin's README) in the same commit.

## Setup on GitHub (once)

1. The release GitHub App installed on the repository (Contents, Pull requests and Issues read and write), its private key in the secret `RELEASE_APP_PRIVATE_KEY`. A pull request opened with `GITHUB_TOKEN` starts no checks, so release-please needs the app.
2. A tag ruleset on `*-v*` (the tags above) that only the app can create, and a ruleset on `main` requiring a pull request and the checks `check` and `pr-title`.
3. Squash merges only, with the pull request title as the commit title.

## The first release

The manifest starts every package at `1.0.0`, and each `CHANGELOG.md` already has its `1.0.0 (initial)` entry. `bootstrap-sha` in the config is the repository's first commit: release-please counts only the commits after it. The pull request that imports the first plugin is titled with `chore(...)`, which releases nothing, so the first release pull request appears only with the first `feat` or `fix` after it.
