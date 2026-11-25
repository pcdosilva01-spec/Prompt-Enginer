"""Validate the bundled skill without network access or runtime dependencies."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import tempfile

SKILL_NAME = "universal-prompt-engineering"
BUNDLE = Path(__file__).resolve().parent / "resources" / "skill" / SKILL_NAME
MANIFEST_NAME = "MANIFEST.sha256"
REQUIRED_FILES = (
    "SKILL.md",
    "README.md",
    "INSTALLATION.md",
    "agents/openai.yaml",
    "references/KNOWLEDGE_INDEX.md",
    "references/COMPATIBILITY_MATRIX.md",
    "references/original_dossier/ORIGINALS_SHA256.json",
    "scripts/approval_gate.py",
    "scripts/interaction.py",
    "scripts/delivery_contract.py",
    "scripts/model_selection.py",
    "scripts/package_skill.py",
    "workflows/interaction_integration.md",
    "references/models/model_selection.md",
    "tests/test_approval_gate.py",
    "tests/test_interaction.py",
    "tests/behavioral_eval_protocol.md",
)
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
LINK_RE = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")


@dataclass(frozen=True)
class VerificationResult:
    valid: bool
    checked_files: int
    errors: tuple[str, ...]
    warnings: tuple[str, ...] = ()


def bundled_skill_path() -> Path:
    return BUNDLE


def _ignored(path: Path) -> bool:
    return "__pycache__" in path.parts or path.suffix == ".pyc"


def _digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _entries(root: Path) -> dict[str, Path]:
    entries: dict[str, Path] = {}
    for path in root.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"symlink is not allowed in the skill bundle: {path.relative_to(root).as_posix()}")
        if path.is_file() and path.name != MANIFEST_NAME and not _ignored(path):
            entries[path.relative_to(root).as_posix()] = path
    return entries


def write_manifest(root: Path) -> int:
    """Write the bundle inventory atomically, excluding this file and caches."""
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError("skill root must be a real directory")
    entries = _entries(root)
    rows = [f"{_digest(path)}  {name}" for name, path in sorted(entries.items())]
    target = root / MANIFEST_NAME
    if target.is_symlink():
        raise ValueError("manifest must not be a symlink")
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", dir=root, prefix=".manifest.", suffix=".tmp", delete=False) as handle:
            temp_path = Path(handle.name)
            handle.write("\n".join(rows) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, target)
        temp_path = None
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
    return len(rows)


def _check_markdown_links(root: Path, errors: list[str]) -> None:
    for markdown in root.rglob("*.md"):
        if _ignored(markdown):
            continue
        try:
            content = markdown.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"cannot read {markdown.relative_to(root).as_posix()}: {exc}")
            continue
        for target in LINK_RE.findall(content):
            target = target.strip().split("#", 1)[0]
            if not target or re.match(r"^(https?://|mailto:|data:)", target, re.I):
                continue
            resolved = (markdown.parent / target).resolve()
            if root not in resolved.parents and resolved != root:
                errors.append(f"link escapes bundle: {markdown.relative_to(root).as_posix()} -> {target}")
            elif not resolved.exists():
                errors.append(f"broken internal link: {markdown.relative_to(root).as_posix()} -> {target}")


def verify_skill(root: Path | None = None) -> VerificationResult:
    root = Path(root) if root is not None else bundled_skill_path()
    errors: list[str] = []
    warnings: list[str] = []
    if root.is_symlink() or not root.is_dir():
        return VerificationResult(False, 0, ("skill root is missing, not a directory, or is a symlink",))
    root = root.resolve()
    for name in REQUIRED_FILES:
        if not (root / name).is_file():
            errors.append(f"required file missing: {name}")
    manifest_path = root / MANIFEST_NAME
    listed: dict[str, str] = {}
    if manifest_path.is_symlink() or not manifest_path.is_file():
        errors.append("MANIFEST.sha256 is missing or is a symlink")
    else:
        for number, line in enumerate(manifest_path.read_text(encoding="utf-8").splitlines(), start=1):
            parts = line.split("  ", 1)
            if len(parts) != 2 or not HASH_RE.fullmatch(parts[0]):
                errors.append(f"malformed manifest row {number}")
                continue
            relative = PurePosixPath(parts[1])
            if relative.is_absolute() or ".." in relative.parts or "\\" in parts[1] or not relative.parts:
                errors.append(f"unsafe manifest path: {parts[1]}")
                continue
            normalized = relative.as_posix()
            if normalized.casefold() in {key.casefold() for key in listed}:
                errors.append(f"duplicate manifest path: {normalized}")
                continue
            listed[normalized] = parts[0]
    try:
        actual_files = _entries(root)
    except (OSError, ValueError) as exc:
        actual_files = {}
        errors.append(str(exc))
    actual = {name: _digest(path) for name, path in actual_files.items()}
    missing = sorted(set(actual) - set(listed))
    extra = sorted(set(listed) - set(actual))
    changed = sorted(name for name in set(actual) & set(listed) if actual[name] != listed[name])
    if missing:
        errors.append(f"unlisted bundle files: {missing}")
    if extra:
        errors.append(f"manifest entries missing from bundle: {extra}")
    if changed:
        errors.append(f"hash mismatch: {changed}")

    skill_md = root / "SKILL.md"
    if skill_md.is_file():
        text = skill_md.read_text(encoding="utf-8")
        match = re.match(r"\A---\r?\nname:\s*([a-z0-9-]+)\r?\ndescription:\s*(.+)\r?\n---\r?\n", text)
        if not match:
            errors.append("SKILL.md frontmatter is missing required name/description fields")
        elif match.group(1) != root.name:
            errors.append(f"SKILL.md name {match.group(1)!r} does not match folder {root.name!r}")
        elif len(match.group(2)) > 1024:
            errors.append("SKILL.md description exceeds 1024 characters")

    originals = root / "references" / "original_dossier" / "ORIGINALS_SHA256.json"
    if originals.is_file():
        try:
            expected = json.loads(originals.read_text(encoding="utf-8"))
            for name, digest in expected.items():
                path = root / "references" / "original_dossier" / name
                if Path(name).name != name or path.is_symlink() or not path.is_file():
                    errors.append(f"original dossier file missing or unsafe: {name}")
                elif not HASH_RE.fullmatch(digest) or _digest(path) != digest:
                    errors.append(f"original dossier hash mismatch: {name}")
            actual_originals = {
                path.name for path in originals.parent.iterdir()
                if path.is_file() and path.name != originals.name
            }
            if actual_originals != set(expected):
                errors.append("original dossier inventory differs from ORIGINALS_SHA256.json")
        except (OSError, ValueError, TypeError) as exc:
            errors.append(f"invalid original dossier hash manifest: {exc}")
    _check_markdown_links(root, errors)

    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError:
        warnings.append("full YAML parser unavailable; frontmatter was checked structurally")
    else:
        try:
            frontmatter = skill_md.read_text(encoding="utf-8").split("---", 2)[1]
            metadata = yaml.safe_load(frontmatter)
            if not isinstance(metadata, dict) or not isinstance(metadata.get("name"), str) or not isinstance(metadata.get("description"), str):
                errors.append("SKILL.md YAML frontmatter must define string name and description")
            agent_metadata = yaml.safe_load((root / "agents/openai.yaml").read_text(encoding="utf-8"))
            if not isinstance(agent_metadata, dict):
                errors.append("agents/openai.yaml must contain a YAML mapping")
        except Exception as exc:
            errors.append(f"YAML parser rejected skill metadata: {exc}")
    return VerificationResult(not errors, len(actual), tuple(errors), tuple(warnings))
