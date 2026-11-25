"""Verify skill metadata, internal links, and both package hash manifests."""
from __future__ import annotations

import hashlib
import json
import re
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["SKILL.md", "README.md", "INSTALLATION.md", "agents/openai.yaml", "references/KNOWLEDGE_INDEX.md", "references/COMPATIBILITY_MATRIX.md", "references/original_dossier/ORIGINALS_SHA256.json", "scripts/approval_gate.py", "scripts/package_skill.py", "tests/test_approval_gate.py", "tests/behavioral_eval_protocol.md"]
REQUIRED += [
    "scripts/editorial.py", "scripts/model_catalog.py", "references/writing/humanizer.md",
    "references/writing/HUMANIZER-LICENSE.txt", "workflows/skill_routing.md",
    "scripts/interaction.py", "scripts/delivery_contract.py", "scripts/model_selection.py",
    "workflows/interaction_integration.md", "references/models/model_selection.md",
    "tests/test_interaction.py",
]
LINK_RE = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")


def verify(root: Path = ROOT, source_dossier: Path | None = None) -> list[str]:
    errors: list[str] = []
    root = root.resolve()
    for name in REQUIRED:
        if not (root / name).is_file():
            errors.append(f"required file missing: {name}")
    for file in root.rglob("*"):
        if file.is_file() and "__pycache__" not in file.parts and file.suffix != ".pyc" and file.stat().st_size == 0:
            errors.append(f"empty file without content: {file.relative_to(root).as_posix()}")
    skill = root / "SKILL.md"
    if skill.exists():
        text = skill.read_text(encoding="utf-8")
        match = re.match(r"\A---\r?\nname:\s*([a-z0-9-]+)\r?\ndescription:\s*(.+)\r?\n---\r?\n", text)
        if not match:
            errors.append("SKILL.md frontmatter is invalid or not first")
        elif match.group(1) != root.name:
            errors.append(f"name {match.group(1)!r} does not match folder {root.name!r}")
        elif len(match.group(2)) > 1024:
            errors.append("description exceeds 1024 characters")
    openai_yaml = root / "agents/openai.yaml"
    if openai_yaml.exists():
        yaml_text = openai_yaml.read_text(encoding="utf-8")
        required_lines = ["interface:", '  display_name: "Universal Prompt Engineering"', '  short_description: "Evidence-backed prompt design and review"', '  default_prompt: "Use $universal-prompt-engineering to design or evaluate a prompt for my target model and task."', "policy:", "  allow_implicit_invocation: true"]
        if any(line not in yaml_text.splitlines() for line in required_lines):
            errors.append("agents/openai.yaml does not match the reviewed UI metadata schema")
    for md in root.rglob("*.md"):
        if "__pycache__" in md.parts:
            continue
        content = md.read_text(encoding="utf-8")
        for target in LINK_RE.findall(content):
            target = target.strip().split("#", 1)[0]
            if not target or re.match(r"^(https?://|mailto:|data:)", target, re.I):
                continue
            resolved = (md.parent / target).resolve()
            if root not in resolved.parents and resolved != root:
                errors.append(f"link escapes skill package: {md.relative_to(root).as_posix()} -> {target}")
            elif not resolved.exists():
                errors.append(f"broken internal link: {md.relative_to(root).as_posix()} -> {target}")
    originals_path = root / "references/original_dossier/ORIGINALS_SHA256.json"
    if originals_path.exists():
        try:
            original_entries = json.loads(originals_path.read_text(encoding="utf-8"))
            for name, expected in original_entries.items():
                file = root / "references/original_dossier" / name
                if not file.is_file():
                    errors.append(f"original copy missing: {name}")
                elif hashlib.sha256(file.read_bytes()).hexdigest() != expected:
                    errors.append(f"original copy hash mismatch: {name}")
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"original hash manifest invalid: {exc}")
    if source_dossier is not None:
        source = source_dossier.resolve()
        copy_dir = root / "references/original_dossier"
        source_files = {item.name for item in source.iterdir() if item.is_file()}
        copy_files = {item.name for item in copy_dir.iterdir() if item.is_file() and item.name != "ORIGINALS_SHA256.json"}
        if source_files != copy_files:
            errors.append(f"source/copy inventory differs: source-only={sorted(source_files-copy_files)}, copy-only={sorted(copy_files-source_files)}")
        for name in sorted(source_files & copy_files):
            if hashlib.sha256((source / name).read_bytes()).hexdigest() != hashlib.sha256((copy_dir / name).read_bytes()).hexdigest():
                errors.append(f"source/copy SHA-256 mismatch: {name}")
    manifest = root / "MANIFEST.sha256"
    if manifest.exists():
        listed: dict[str, str] = {}
        for line in manifest.read_text(encoding="utf-8").splitlines():
            parts = line.split("  ", 1)
            if len(parts) != 2:
                errors.append(f"malformed manifest row: {line}")
                continue
            listed[parts[1]] = parts[0]
        actual = {}
        for file in root.rglob("*"):
            if file.is_file() and file != manifest and "__pycache__" not in file.parts and file.suffix != ".pyc":
                actual[file.relative_to(root).as_posix()] = hashlib.sha256(file.read_bytes()).hexdigest()
        if listed != actual:
            missing = sorted(set(actual) - set(listed))
            extra = sorted(set(listed) - set(actual))
            changed = sorted(key for key in set(actual) & set(listed) if actual[key] != listed[key])
            errors.append(f"package manifest mismatch: missing={missing}, extra={extra}, changed={changed}")
    else:
        errors.append("MANIFEST.sha256 missing; run scripts/build_manifest.py")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dossier", type=Path, help="optional source directory for byte-for-byte comparison")
    args = parser.parse_args()
    problems = verify(source_dossier=args.source_dossier)
    if problems:
        print("Package verification failed:")
        for problem in problems:
            print(f"- {problem}")
        raise SystemExit(1)
    print("Package verification passed: metadata, internal links, original hashes, and manifest.")
