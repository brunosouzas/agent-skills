# Releasing

[release-please](https://github.com/googleapis/release-please) in manifest mode keeps one release pull request open on `main`. Merging it raises the versions, writes the changelogs, tags each release and creates its GitHub release. Nobody edits versions or changelogs by hand.

## Packages

[release-please-config.json](../release-please-config.json) has one package per skill and one per plugin; [.release-please-manifest.json](../.release-please-manifest.json) holds their current versions.

| Package | Path | Tag | Writes the version to |
|---|---|---|---|
| a skill | `plugins/<plugin>/skills/<skill>` | `<skill>-vX.Y.Z` | the `# x-release-please-version` line of `SKILL.md`, its `package.json` and its `CHANGELOG.md` |
| a plugin | `plugins/<plugin>` | `<plugin>-plugin-vX.Y.Z` | `.codex-plugin/plugin.json`, its `package.json` and the plugin's `CHANGELOG.md` |

release-please gives a commit to a package by the files it changes, taking the deepest package path: a commit that changes `plugins/mulesoft/skills/dataweave/rules.md` belongs to `dataweave`, not to the `mulesoft` plugin. The commit scope does not route anything; CI requires it so the title says the same thing as the paths (CONTRIBUTING.md).

**The plugin's version follows its skills by itself.** Every package has `release-type: node` and a private `package.json` that is only a version record (not an npm package, never published). The plugin's `package.json` lists each of its skills as a dependency, and the `node-workspace` plugin of release-please raises a dependent whenever a dependency is released: a skill-only `feat(dataweave)` releases `dataweave` 1.1.0 **and** the plugin at the next patch, with a "Dependencies" entry in the plugin's changelog. A plugin-level change bumps the plugin by its own commit type, as any package. `scripts/check_repo.py` refuses a skill missing from the plugin's dependencies, a version record that disagrees with the manifest, or a config without `node-workspace`.

Tested on 2026-11-14 with `release-please release-pr --dry-run` (17.11.2) on a branch whose only change after `bootstrap-sha` was one `feat(dataweave)` commit: the proposed release pull request had `dataweave: 1.1.0` and `mulesoft-plugin: 1.0.1` ("The following workspace dependencies were updated"), and nothing else; its updaters wrote `SKILL.md` (generic), both `package.json` files and `.codex-plugin/plugin.json` (JSON path `$.version`). To repeat it, push a scratch branch with such a commit and run, from any folder with release-please installed:

```bash
release-please release-pr --repo-url=<owner>/agent-skills --target-branch=<scratch-branch> --dry-run --token="$(gh auth token)"
```

## How a plugin's update reaches users

- **Claude Code** computes a plugin's version from the commit when `plugin.json` sets none. The Claude `plugin.json` and the marketplace entry therefore set no `version`, and every merged change reaches users on their next update. `scripts/check_repo.py` refuses a `version` there.
- **Codex** installs a plugin into a cache folder named after the `version` of `.codex-plugin/plugin.json` (`plugins/cache/<marketplace>/<plugin>/<version>/`). The plugin package raises it on every release of any of its skills (above), so a release always reaches Codex users with a new version.

## Setup on GitHub (once)

1. The release GitHub App of the reusable workflow (its default `app-id`), installed on this repository, with its private key in the secret `RELEASE_APP_PRIVATE_KEY`. The workflow asks GitHub for a token limited to the calling repository. A pull request opened with `GITHUB_TOKEN` starts no checks, so release-please needs the app.
2. A tag ruleset on `*-v*` (the tags above) that only the app can create, and a ruleset on `main` requiring a pull request and the checks `check` and `pr-title`.
3. Squash merges only, with the pull request title as the commit title.

## The first release

The manifest starts every package at `1.0.0`, and each `CHANGELOG.md` already has its `1.0.0 (initial)` entry. `bootstrap-sha` in the config is the repository's first commit: release-please counts only the commits after it. The pull request that imports the first plugin is titled with `chore(...)`, which releases nothing, so the first release pull request appears only with the first `feat` or `fix` after it.
