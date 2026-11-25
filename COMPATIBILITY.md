# Host compatibility snapshot

**Document check: 23 November 2026.** These are documented filesystem conventions, not results of installing or invoking the skill in each host. Client version, account, plan, policy, trust state, and product surface can change discovery. Recheck the linked primary source before use.

| Host / surface | Project path selected by installer | User path selected by installer | Status and verification limit | Primary documentation |
|---|---|---|---|---|
| OpenAI Codex | `.agents/skills/` | `~/.agents/skills/` | Documented path; client discovery not tested. OpenAI docs page redirected to ChatGPT Learn on check date. | [Codex skills](https://developers.openai.com/codex/skills) |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | Documented; local CLI/account/cloud behavior varies; no host test. | [Claude Code skills](https://code.claude.com/docs/en/skills) |
| Gemini CLI | `.gemini/skills/` | `~/.gemini/skills/` | Documented; `.agents/skills/` is an additional alias; CLI discovery not tested. | [Gemini CLI skills](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/using-agent-skills.md) |
| Google Antigravity App/CLI/IDE | `.agents/skills/` | `~/.gemini/config/skills/` | Documented for named surfaces; CLI also documents extra locations. No client test. | [Antigravity skills](https://antigravity.google/docs/skills) |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` | Documented; `.agents/skills/` is also supported. Local-to-cloud sync is separate; no client test. | [Cursor Agent Skills](https://cursor.com/docs/skills) |
| GitHub Copilot | `.github/skills/` | `~/.copilot/skills/` | Documented; `.agents/skills/` is also supported. Feature availability depends on Copilot surface/version/policy; no client test. | [Copilot Agent Skills](https://docs.github.com/en/copilot/concepts/customizations/agent-skills) |
| Cline | `.cline/skills/` | `~/.cline/skills/` | Documented; the legacy `.clinerules/skills/` and `.claude/skills/` alternatives are not selected here. No extension test. | [Cline skills](https://github.com/cline/cline/blob/main/docs/customization/skills.mdx) |
| Roo Code | `.roo/skills/` | `~/.roo/skills/` | **Legacy only:** the original extension, cloud, and router shut down on 15 May 2026. File-copy support in archived docs does not mean the host is maintained or safe for new deployment. | [Roo shutdown notice](https://github.com/RooCodeInc/Roo-Code-Docs/blob/main/docs/sunset.md), [legacy skills docs](https://roocodeinc.github.io/Roo-Code/features/skills/) |
| OpenCode | `.opencode/skills/` | `~/.config/opencode/skills/` | Documented; `.agents/skills/` and `.claude/skills/` compatibility roots also exist. No host test. | [OpenCode skills](https://opencode.ai/docs/skills/) |
| ChatGPT Web | Manual only | Manual only | No verified filesystem install path; use attachment/import features only if that exact surface exposes them. | [OpenAI skill docs](https://developers.openai.com/codex/skills) |
| Aider | Manual context only | Manual context only | Aider conventions can add read-only prompt context; native Agent Skills discovery is not claimed. | [Aider conventions](https://aider.chat/docs/usage/conventions.html) |
| Windsurf / Cascade | Manual/undetermined | Manual/undetermined | Older Cascade docs redirect into Devin documentation; this is insufficient proof of current Windsurf skill loading. No install target. | [Windsurf docs](https://docs.windsurf.com/windsurf/cascade/memories), [Devin Local customizations](https://docs.devin.ai/desktop/devin-local/customizations) |
| Devin Local | Not in CLI catalog | Not in CLI catalog | Separate product documentation; not treated as equivalent to Windsurf/Cascade. No tested adapter. | [Devin Local customizations](https://docs.devin.ai/desktop/devin-local/customizations) |

## Models versus platforms

This table describes where a skill folder may be discovered. It does not say that a model family follows identical prompting guidance across chat apps, APIs, agent harnesses, or versions. Use the [research dossier](docs/research/DOSSIER_ENGENHARIA_DE_PROMPTS/INDICE_GERAL.md) and the skill's model adapters for evidence-labeled advice. The dossier's model/API snapshots are dated and must be checked against current provider documentation before a current availability or version claim.

## Install path map in code

The executable catalog lives in `src/upe/targets.py`; this page is a human-readable record of its selected default path per scope. The installer writes files only. It cannot install a host product, enable an account feature, reload a plugin, or prove model behavior.

## Sources

The [platform research snapshot](docs/research/PLATFORM_RESEARCH_SNAPSHOT.md) records the page title, publisher, check date, date metadata, conclusion, and limitation for each source.
