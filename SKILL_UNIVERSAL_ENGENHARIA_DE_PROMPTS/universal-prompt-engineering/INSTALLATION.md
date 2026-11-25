# Install this skill

Copy this entire directory, named `universal-prompt-engineering`, to a skills location documented by your host. Current researched examples:

- Codex user: `%USERPROFILE%\.agents\skills\universal-prompt-engineering\`; project: `.agents\skills\universal-prompt-engineering\` (Codex também consulta diretórios `.agents/skills` ancestrais até a raiz do repositório, conforme docs verificadas em 23/11/2026). Admin: `/etc/codex/skills/`. Confirme a superfície/versão; `.codex/skills/` não consta como local atual na página reaberta.
- Claude Code project: `.claude/skills/universal-prompt-engineering/`; personal: `~/.claude/skills/universal-prompt-engineering/`.
- Cursor project: `.agents/skills/` or `.cursor/skills/`; personal: `~/.agents/skills/` or `~/.cursor/skills/`.
- Gemini CLI: `.gemini/skills/` or `.agents/skills/`; personal `~/.gemini/skills/` or `~/.agents/skills/`; reload/list and grant activation consent when requested.
- Antigravity: workspace `.agents/skills/`; global `~/.gemini/config/skills/` (surface may add paths).
- Cline: `.cline/skills/`; global `~/.cline/skills/`.
- OpenCode: `.opencode/skills/`; compatibility discovery can read `.agents/skills/` and `.claude/skills/`.
- GitHub Copilot: `.github/skills/`, `.agents/skills/`, or `.claude/skills/` depending on the client.

These are documented locations, not a claim that the skill was installed or loaded in your account. Check the host-specific setup and version in `references/COMPATIBILITY_MATRIX.md`, then verify discovery in the target client. Python 3.10+ is needed only to run the optional deterministic tests/helper; the core skill is Markdown.

First use: ask for a prompt, receive and review the skill's understanding summary, then explicitly approve it. After installation or file changes, reload skills if that host requires it. Do not preapprove tools because a skill exists.
