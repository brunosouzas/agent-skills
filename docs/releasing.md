# Releasing

[release-please](https://github.com/googleapis/release-please) in manifest mode keeps one release pull request open on `main`. Merging it raises the versions, writes the changelogs, tags each release and creates its GitHub release. Nobody edits versions or changelogs by hand.

## Packages

[release-please-config.json](../release-please-config.json) has one package per skill and one per plugin; [.release-please-manifest.json](../.release-please-manifest.json) holds their current versions.

| Package | Path | Tag | Writes the version to |
|---|---|---|---|
| a skill | `plugins/<plugin>/skills/<skill>` | `<skill>-vX.Y.Z` | the `# x-release-please-version` line of `SKILL.md`, its `package.json` and its `CHANGELOG.md` |
| a plugin | `plugins/<plugin>` | `<plugin>-plugin-vX.Y.Z` | `.codex-plugin/plugin.json`, its `package.json` and the plugin's `CHANGELOG.md` |

release-please gives a commit to a package by the files it changes, taking the deepest package path: a commit that changes `plugins/delivery/skills/merge-gates/SKILL.md` belongs to `merge-gates`, not to the `delivery` plugin. The commit scope does not route anything; CI requires it so the title says the same thing as the paths (CONTRIBUTING.md).

**The plugin's version follows its skills by itself.** Every package has `release-type: node` and a private `package.json` that is only a version record (not an npm package, never published). The plugin's `package.json` lists each of its skills as a dependency, and the `node-workspace` plugin of release-please raises a dependent whenever a dependency is released: a skill-only `feat(merge-gates)` releases `merge-gates` at its next minor **and** the `delivery` plugin at the next patch (for a one-skill plugin such as `java`, a `fix(java)` releases `java` and `java-plugin` together), with a "Dependencies" entry in the plugin's changelog. A plugin-level change bumps the plugin by its own commit type, as any package. `scripts/check_repo.py` refuses a skill missing from the plugin's dependencies, a version record that disagrees with the manifest, or a config without `node-workspace`.

Tested on 2026-11-14 (with the former `mulesoft` plugin, since moved to devFoundry) with `release-please release-pr --dry-run` (17.11.2) on a branch whose only change after `bootstrap-sha` was one `feat(dataweave)` commit: the proposed release pull request had `dataweave: 1.1.0` and `mulesoft-plugin: 1.0.1` ("The following workspace dependencies were updated"), and nothing else; its updaters wrote `SKILL.md` (generic), both `package.json` files and `.codex-plugin/plugin.json` (JSON path `$.version`). To repeat it, push a scratch branch with such a commit and run, from any folder with release-please installed:

```bash
release-please release-pr --repo-url=<owner>/agent-skills --target-branch=<scratch-branch> --dry-run --token="$(gh auth token)"
```

**Tags cannot collide.** A skill and its plugin often share a name (`java` and `java-plugin`): the skill's tag is `java-vX.Y.Z` and the plugin's `java-plugin-vX.Y.Z`. They are different strings, and release-please matches a tag to a package by its exact component followed by `-v`, so `java-plugin-v1.0.0` is never read as a release of `java`. `scripts/check_repo.py` refuses a component used twice, and `delivery` / `delivery-plugin` work this way.

## How a plugin's update reaches users

- **Claude Code** computes a plugin's version from the commit when `plugin.json` sets none. The Claude `plugin.json` and the marketplace entry therefore set no `version`, and every merged change reaches users on their next update. `scripts/check_repo.py` refuses a `version` there.
- **Codex** installs a plugin into a cache folder named after the `version` of `.codex-plugin/plugin.json` (`plugins/cache/<marketplace>/<plugin>/<version>/`). The plugin package raises it on every release of any of its skills (above), so a release always reaches Codex users with a new version.

## Setup on GitHub (once)

The release workflow calls `release-please.yml` of `brunosouzas/github-reusable-workflows` at `v0.1.0` (pinned by commit), which runs as a **release GitHub App** installed on this repository (today `brunosouzas-delivery-release`, App ID `5609269`):

1. The app has Contents, Pull requests and Issues read and write. A pull request opened with `GITHUB_TOKEN` starts no checks, so release-please needs the app; the token it gets is limited to this repository.
2. An environment `release-please` (deployment branches: `main` only, no reviewer) with the variable `RELEASE_APP_CLIENT_ID` (the app's Client ID or App ID; here the App ID) and the secret `RELEASE_APP_PRIVATE_KEY` (its private key, PEM). The call passes the secret by name; the reusable job reads both from the environment and asks GitHub for a token limited to this repository.
3. A tag ruleset on `refs/tags/*-v*` (the tags above: creation, update and deletion blocked) with the app as an `Integration` bypass, so only release-please makes tags.
4. Squash merges only, with the pull request title as the commit title (`allow_merge_commit=false`, `allow_rebase_merge=false`, `squash_merge_commit_title=PR_TITLE`), then a ruleset on `main` requiring a pull request and the checks `check` and `pr-title`.

## The first release

The manifest starts every package at `1.0.0`, and each `CHANGELOG.md` already has its `1.0.0 (initial)` entry. `bootstrap-sha` in the config is the merge commit of the pull request that imported the plugin (`6bb78e6`): release-please counts only the commits after it, so the commits of that import do not release anything. The first release pull request appears with the first `feat` or `fix` that touches a skill or a plugin after it.
