# Platform compatibility report

**Checked:** 23 November 2026. The compatibility level used here is “documentation-backed destination,” not host-tested support.

## Result by platform

| Platform | CLI catalog | User/project paths | Evidence class | Real host installation |
|---|---:|---|---|---|
| OpenAI Codex | Yes | `.agents/skills` / `~/.agents/skills` | Official current docs | Not run |
| Claude Code | Yes | `.claude/skills` / `~/.claude/skills` | Official current docs | Not run |
| Gemini CLI | Yes | `.gemini/skills` / `~/.gemini/skills` | Official repository docs; `.agents` alias also documented | Not run |
| Google Antigravity | Yes | `.agents/skills` / `~/.gemini/config/skills` | Official current docs; surface-specific extras noted | Not run |
| Cursor | Yes | `.cursor/skills` / `~/.cursor/skills` | Official current docs; `.agents` alternative noted | Not run |
| GitHub Copilot | Yes | `.github/skills` / `~/.copilot/skills` | Official current docs; `.agents` alternative and eligibility limits noted | Not run |
| Cline | Yes | `.cline/skills` / `~/.cline/skills` | Official project docs | Not run |
| Roo Code | Yes, **legacy** | `.roo/skills` / `~/.roo/skills` | Archived documentation + official shutdown notice | Not run; product shut down |
| OpenCode | Yes | `.opencode/skills` / `~/.config/opencode/skills` | Official current docs; shared `.agents`/`.claude` paths noted | Not run |
| ChatGPT Web | Manual | None asserted | OpenAI skill docs distinguish surfaces; no local filesystem path verified | Not applicable |
| Aider | No | Manual prompt context only | Official conventions docs | No native skill test |
| Windsurf/Cascade | No | No verified target | Legacy URL redirects into Devin docs; not enough to infer equivalent support | Not run |
| Devin Local | No | Not in catalog | Its own product docs are separate | Not run |

## Model/platform boundary

An OpenAI, Anthropic, Google, Meta, DeepSeek, Qwen, Mistral, or xAI model/API may be used through different clients and harnesses. The CLI catalog is about filesystems used by some clients. It does not select a model, prove that an API supports a particular reasoning/tool parameter, or imply that model prompting recommendations transfer unchanged to a different host. Model/version research remains indexed in the dated dossier and should be refreshed for a live task.

## Sources and availability

The primary-source ledger with titles, publishers, checked dates, date metadata, exact URLs, claims, and boundaries is [PLATFORM_RESEARCH_SNAPSHOT.md](../research/PLATFORM_RESEARCH_SNAPSHOT.md). Local client version and account entitlements were not inspected. “Listed in docs” must not be reported as “installed and working.”
