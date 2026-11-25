"""Evidence-backed install locations for Agent Skills hosts."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil

from . import SKILL_NAME


class TargetError(ValueError):
    """Raised when a requested host or install scope is not supported."""


@dataclass(frozen=True)
class TargetSpec:
    id: str
    name: str
    installable: bool
    user_path: tuple[str, ...] | None
    project_path: tuple[str, ...] | None
    documentation_url: str
    evidence_status: str
    activation: str
    executable: str | None = None


TARGETS: dict[str, TargetSpec] = {
    "codex": TargetSpec(
        "codex", "OpenAI Codex", True, (".agents", "skills"), (".agents", "skills"),
        "https://developers.openai.com/codex/skills", "documented; host not tested",
        "Invoke by skill name or let Codex select it from its description.", "codex",
    ),
    "claude-code": TargetSpec(
        "claude-code", "Claude Code", True, (".claude", "skills"), (".claude", "skills"),
        "https://code.claude.com/docs/en/skills", "documented; host not tested",
        "Use /universal-prompt-engineering or a matching natural-language request.", "claude",
    ),
    "gemini-cli": TargetSpec(
        "gemini-cli", "Gemini CLI", True, (".gemini", "skills"), (".gemini", "skills"),
        "https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/using-agent-skills.md", "documented; host not tested",
        "Run /skills reload, then confirm discovery with /skills list.", "gemini",
    ),
    "antigravity": TargetSpec(
        "antigravity", "Google Antigravity", True, (".gemini", "config", "skills"), (".agents", "skills"),
        "https://antigravity.google/docs/skills", "documented; host not tested",
        "Use the Skills panel or a matching natural-language request.", None,
    ),
    "cursor": TargetSpec(
        "cursor", "Cursor", True, (".cursor", "skills"), (".cursor", "skills"),
        "https://cursor.com/docs/skills", "documented; host not tested",
        "Use /universal-prompt-engineering or let Agent select the skill.", "cursor",
    ),
    "copilot": TargetSpec(
        "copilot", "GitHub Copilot", True, (".copilot", "skills"), (".github", "skills"),
        "https://docs.github.com/en/copilot/concepts/customizations/agent-skills", "documented; surface-dependent; host not tested",
        "Use /universal-prompt-engineering or copilot skill list where available.", "copilot",
    ),
    "cline": TargetSpec(
        "cline", "Cline", True, (".cline", "skills"), (".cline", "skills"),
        "https://github.com/cline/cline/blob/main/docs/customization/skills.mdx", "documented; extension host not tested",
        "Use the Skills panel, slash selection, or a matching request.", None,
    ),
    "roo-code": TargetSpec(
        "roo-code", "Roo Code", True, (".roo", "skills"), (".roo", "skills"),
        "https://roocodeinc.github.io/Roo-Code/features/skills/", "documented legacy path; Roo Code product archived/shut down 15/05/2026; host not tested",
        "Enable the skill for the relevant Roo mode, then invoke or describe the task.", None,
    ),
    "opencode": TargetSpec(
        "opencode", "OpenCode", True, (".config", "opencode", "skills"), (".opencode", "skills"),
        "https://opencode.ai/docs/skills/", "documented; host not tested",
        "Mention @universal-prompt-engineering or use its skill ID.", "opencode",
    ),
    "chatgpt-web": TargetSpec(
        "chatgpt-web", "ChatGPT Web", False, None, None,
        "https://developers.openai.com/codex/skills", "manual/import path only; filesystem installation not verified",
        "Attach or paste the relevant skill files when the surface permits; otherwise use natural language.", None,
    ),
}


def list_targets() -> list[TargetSpec]:
    return [TARGETS[key] for key in sorted(TARGETS)]


def resolve_skill_path(
    target_id: str,
    scope: str,
    *,
    project_dir: Path | None = None,
    home: Path | None = None,
) -> Path:
    target = TARGETS.get(target_id)
    if target is None:
        raise TargetError(f"Unknown target {target_id!r}; run 'upe-skill list-targets'.")
    if not target.installable:
        raise TargetError(f"{target.name} has no verified filesystem installation target; use its documented manual method.")
    if scope == "user":
        base = Path(home).expanduser() if home is not None else Path.home()
        relative = target.user_path
    elif scope == "project":
        if project_dir is None:
            raise TargetError("Project scope requires an existing --project-dir.")
        base = Path(project_dir).expanduser()
        if not base.exists() or not base.is_dir():
            raise TargetError(f"Project directory does not exist or is not a directory: {base}")
        base = base.resolve()
        relative = target.project_path
    else:
        raise TargetError("Scope must be 'user' or 'project'.")
    if relative is None:
        raise TargetError(f"{target.name} does not document {scope} scope.")
    return base.joinpath(*relative, SKILL_NAME)


def detect_available_targets() -> list[str]:
    """Return supported CLI hosts whose executable is currently on PATH."""
    return [spec.id for spec in list_targets() if spec.installable and spec.executable and shutil.which(spec.executable)]
