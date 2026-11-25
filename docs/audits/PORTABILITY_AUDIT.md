# Portability audit

**Audit date:** 23 November 2026. The skill is Markdown and its resources; the optional installer is Python 3.10+ and uses only the standard library at runtime.

| Area | Design/check | Observed result | Remaining limit |
|---|---|---|---|
| Path spaces | Temporary Windows paths with spaces used by installer tests | Install, verify, update, uninstall test flows pass | This proves the local Python path handling in temp dirs, not every host. |
| Path separators | `pathlib`, POSIX-relative manifest paths, no shell interpolation | Windows path tests and manifest checks pass | macOS/Linux runs are configured in CI but not executed. |
| User/project scope | Explicit target map; project scope requires existing `--project-dir` | Unit tests cover all nine installable target roots and manual-only target rejection | Paths are selected defaults; shared aliases and host policy can differ. |
| Python minimum | `requires-python >=3.10`; no runtime dependencies | Local Python 3.12.10 compiles and runs unit tests | Python 3.10/3.11/3.13 not run locally; CI pending. |
| Symlink/junction safety | Lexical path normalization plus checks on destination, receipt, and managed paths | Code-path guards added; Windows native symlink attempts were skipped | OS denied symlink privilege (WinError 1314); junction behavior and race conditions remain unverified. |
| Manual hosts | ChatGPT Web and Aider are marked manual; Windsurf/Devin not mapped | CLI catalog prevents installing ChatGPT Web and reports manual status | An attached/upload interface varies by product surface; no model app test. |
| Skill folder integrity | Required file list, frontmatter/folder-name match, links, SHA-256 manifest | Bundle verifier passes after manifest refresh | YAML parser is optional; local PyYAML unavailable, so structural check only. |
| Install ownership | State receipt records exact managed file hashes and destination | Clean install, idempotent install, safe update/uninstall logic pass temporary-dir tests | Local attacker can alter both content and receipt; receipt is not a signature. |
| Packaging | `pyproject.toml`, `MANIFEST.in`, CI build job | Source configuration added | Local setuptools/build backend absent; wheel/sdist test pending. |
| Distribution path | GitHub guide links identify the repository and canonical skill path | Source candidate is on `main`; canonical skill file is present | This does not verify host discovery or constitute a release. |

## Supported-path scope

The CLI maps Codex, Claude Code, Gemini CLI, Antigravity, Cursor, GitHub Copilot, Cline, Roo Code (legacy), and OpenCode. It writes a folder named `universal-prompt-engineering`; it does not install the AI client, configure API credentials, enable a cloud feature, or test invocation. Read [COMPATIBILITY.md](../../COMPATIBILITY.md) and the [platform source snapshot](../research/PLATFORM_RESEARCH_SNAPSHOT.md).

## Conclusion

The package is designed to be portable and has local Windows path coverage, but it has not yet met cross-platform release acceptance. The remaining portability evidence is a Python/OS CI run, native link tests where permitted, successful built-artifact inspection, and at least one manual host discovery test per target before claiming verified integration.
