# Universalization report

**Scope checked:** local repository candidate `0.1.0a2` on 23 November 2026. This report covers the existing skill and research being turned into a distributable local project; it does not implement a future product-specific skill, publish a release, or claim that a host AI loaded the skill.

## Work completed

- Preserved the installable skill bundle at `src/upe/resources/skill/universal-prompt-engineering/`, the original root dossier, and the prior root skill and ZIP snapshots. The 24 November cleanup removed redundant dossier/history mirrors while retaining the hash-verified copy required inside the self-contained skill bundle; see [repository cleanup](REPOSITORY_CLEANUP.md).
- Added a Python package with the `upe-skill` command, target catalog, SHA-256 verification, safe local install/update/verify/uninstall operations, `doctor`, help, version, and `list-targets`.
- Added project/user destinations for Codex, Claude Code, Gemini CLI, Antigravity, Cursor, GitHub Copilot, Cline, Roo Code (legacy), and OpenCode. ChatGPT Web is marked manual-only. Aider remains manual context; Windsurf/Cascade and Devin are not mapped to a shared install location.
- Added English and Brazilian Portuguese entry documentation, installation instructions, command reference, agent guide, compatibility notes, contributing/security/licensing pages, CI, and reports.
- Fixed the skill entrypoint's relative knowledge-index path. Added checks for exact bundled hashes, required files, Markdown links, original dossier hashes, and frontmatter.
- Fixed installer path canonicalization so a path is not silently resolved through a symlink before the path is checked. Added link/junction checks for target and state paths and user-change preservation safeguards.
- Documented current platform sources in `docs/research/PLATFORM_RESEARCH_SNAPSHOT.md`; preserved the six-volume dossier and its historical audits rather than rewriting their original scores.

## Problems found and corrections

The traceable record is `REGISTRO_DE_LACUNAS.md`. Its most important initial failures were absent CLI/platform modules, a syntax error in the installer, test fixtures that used a folder name inconsistent with the Agent Skills specification, and the bad relative link in `SKILL.md`. A second implementation review identified that resolving paths through symbolic links could bypass a destination check; the code now keeps lexical paths and rejects linked components before operations.

## What is not complete

- No `LICENSE` has been chosen, and third-party rights review is outstanding. Do not redistribute as an open-source release yet.
- The source candidate was pushed to public `main` in commit `6bcfb75` on 24 November 2026. No GitHub Release, package-index upload, license grant, or history rewrite was made.
- The local machine did not have `pipx` or `setuptools`; no dependency was installed and no wheel/sdist build was claimed.
- Actual installation/discovery in Codex, Claude Code, Gemini CLI, Antigravity, Cursor, Copilot, Cline, or legacy Roo was not performed. Agent behavior and model quality were not experimentally evaluated.
- Windows denied the privilege to create directory symbolic links. Two OS-level symlink tests were skipped; path rejection logic was reviewed and exercised via ordinary boundary tests, but native symlink behavior remains unverified here.
- CI is configured, but has not run on GitHub. Cross-platform and supported-Python matrix results are pending.

## Evidence

See [installation test report](INSTALLATION_TEST_REPORT.md), [platform snapshot](../research/PLATFORM_RESEARCH_SNAPSHOT.md), [knowledge integrity report](KNOWLEDGE_INTEGRITY_REPORT.md), [security audit](SECURITY_AUDIT.md), and [release readiness](RELEASE_READINESS.md). All claims distinguish code tests, documentation checks, and unrun procedures.
