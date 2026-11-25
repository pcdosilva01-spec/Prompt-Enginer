# Installation

## Install the optional CLI

Requirements: Python 3.10+ and pipx. The CLI has no runtime dependencies. Install pipx using its [official instructions](https://pipx.pypa.io/stable/how-to/install-pipx.html), then run from the project checkout:

```console
pipx install .
upe-skill list-targets
upe-skill doctor
```

This installs only the CLI in an isolated Python environment; it does not install a skill into an AI host. Use `upe-skill install <target> --scope user --dry-run`, inspect the path, then repeat without `--dry-run` to write the skill. Project scope requires an existing project directory:

```console
upe-skill install codex --scope project --project-dir /path/to/repository --dry-run
```

On PowerShell, use a quoted path if it contains spaces:

```powershell
upe-skill install codex --scope project --project-dir "C:\work\my project" --dry-run
```

`update` and `uninstall` require an ownership receipt written by this installer. User changes are preserved and reported as conflicts. See [COMMANDS.md](COMMANDS.md) for behavior and exit codes.

## Install the skill manually

Extract the versioned `universal-prompt-engineering-skill-0.1.0a4.zip` for a standalone install. Verify its SHA-256 sidecar first. Inside the extracted skill directory, run `python scripts/verify_package.py`. This requires Python 3.10+.

Copy the full `src/upe/resources/skill/universal-prompt-engineering/` directory into the user or project skills location documented by the target host. Keep the directory name and relative structure intact. For example, a Codex project install is:

```text
<repository>/.agents/skills/universal-prompt-engineering/SKILL.md
```

Then verify discovery in the host and run a low-risk two-turn invocation. Check for a numbered summary with model recommendation, followed after explicit approval by the copyable prompt, TXT if supported, ten scored criteria and the optimization offer. The CLI verifies installation files. The helper runs only when invoked by the host, as described in the bundle's integration guide.

## Publication and release status

Version `0.1.0a4` was prepared as a local candidate. The license choice and third-party rights review remain unresolved; see [release readiness](docs/audits/RELEASE_READINESS.md) before redistribution.
