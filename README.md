# Universal Prompt Engineering

Evidence-aware prompt engineering knowledge and a portable Agent Skill, with an optional local installer and integrity checker.

**Status:** `0.1.0a5` is a local candidate with a standalone skill ZIP and source ZIP. Host installation and model behavior require separate verification. Read [release readiness](docs/audits/RELEASE_READINESS.md) and [licensing status](LICENSING.md) before redistributing.

## What is included

- `src/upe/resources/skill/universal-prompt-engineering/`: canonical, self-contained Agent Skill bundle.
- `src/upe/`: zero-runtime-dependency CLI for safe local install, update, verification, removal, diagnostics, and host path selection.
- `DOSSIER_ENGENHARIA_DE_PROMPTS/`: preserved source dossier and audit reports. The self-contained installed skill carries a hash-verified copy at `src/upe/resources/skill/universal-prompt-engineering/references/original_dossier/`.
- `docs/audits/`: portability, security, integrity, test, release, evaluation, and repository-cleanup reports.
- `SKILL_UNIVERSAL_ENGENHARIA_DE_PROMPTS/` and the root ZIP: unchanged legacy snapshots retained from the previous project version.

The skill requires no runtime dependency. The optional CLI requires Python 3.10+. See [installation](INSTALLATION.md), [commands](COMMANDS.md), [platform compatibility](COMPATIBILITY.md), and [agent instructions](INSTALL_FOR_AI_AGENTS.md).

## Quick use

From a local checkout, install the isolated CLI with pipx:

```powershell
pipx install .
upe-skill list-targets
upe-skill doctor
upe-skill install codex --scope user --dry-run
```

Remove `--dry-run` only after checking the destination. Project-scope operations require an existing `--project-dir`. The installer refuses to overwrite unmanaged files or user-modified managed files; it records ownership hashes and removes only unchanged files that it installed.

To use the Agent Skill without the CLI, copy the entire canonical skill folder named `universal-prompt-engineering` into a host-supported skills directory. Verify the host version and discovery behavior against [COMPATIBILITY.md](COMPATIBILITY.md).

## Development checks

```powershell
python -m compileall -q src tests
python -m unittest discover -s tests -v
python -m unittest discover -s src/upe/resources/skill/universal-prompt-engineering/tests -v
python -m upe version
python -m upe doctor
```

Build and artifact checks are documented in [release readiness](docs/audits/RELEASE_READINESS.md). CI covers Windows, macOS, Linux, and Python 3.10, 3.12, and 3.13; no CI run is claimed until the workflow executes on GitHub.

## Project map

- `docs/research/`: current platform source snapshot.
- `docs/audits/`: auditable findings, changes, tests, and release gates.
- `src/upe/resources/skill/.../references/`: progressive knowledge modules and the hash-verified dossier copy required for a self-contained skill install.
- `src/upe/resources/skill/.../tests/`: approval-helper/package checks and the pending behavioral evaluation protocol.
- `dist/`: local build output; generated archives are not committed.

## Public source

Previous source is available in [Prompter-Silva on GitHub](https://github.com/pcdosilva01-spec/Prompter-Silva), including the canonical [skill entrypoint](https://github.com/pcdosilva01-spec/Prompter-Silva/blob/main/src/upe/resources/skill/universal-prompt-engineering/SKILL.md). The source commit does not constitute a package or GitHub Release.

## License

No license has been granted. See [LICENSING.md](LICENSING.md). Do not treat public visibility as permission to redistribute.
