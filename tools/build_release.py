"""Create deterministic, local-only source and skill ZIPs with SHA-256 sidecars."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "universal-prompt-engineering"
ZIP_TIME = (2020, 1, 1, 0, 0, 0)
EXCLUDED_PARTS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "build", "dist", ".venv", "venv"}


def _zip_add(zf: zipfile.ZipFile, source: Path, archive_name: str) -> None:
    info = zipfile.ZipInfo(archive_name.replace("\\", "/"), ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    zf.writestr(info, source.read_bytes())


def _safe_repo_file(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    if "dist" in relative.parts:
        return False
    if any(part in EXCLUDED_PARTS for part in relative.parts):
        return False
    if path.suffix == ".pyc" or path.name.lower().startswith("push_force_"):
        return False
    return path.is_file() and not path.is_symlink()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(output_dir: Path) -> list[Path]:
    from upe.integrity import bundled_skill_path, verify_skill
    from upe import __version__

    skill = bundled_skill_path()
    verified = verify_skill(skill)
    if not verified.valid:
        raise SystemExit("Skill integrity verification failed: " + "; ".join(verified.errors))
    output_dir.mkdir(parents=True, exist_ok=True)
    skill_zip = output_dir / f"universal-prompt-engineering-skill-{__version__}.zip"
    source_zip = output_dir / f"Prompter-Silva-local-candidate-{__version__}.zip"
    expected = [skill_zip, source_zip]
    expected.extend(path.with_suffix(path.suffix + ".sha256") for path in tuple(expected))
    existing = [path for path in expected if path.exists()]
    if existing:
        raise FileExistsError("refusing to overwrite existing release candidate files: " + ", ".join(map(str, existing)))

    archives = [skill_zip, source_zip]
    sidecars: list[Path] = []
    created: list[Path] = []
    try:
        with zipfile.ZipFile(skill_zip, "x") as archive:
            created.append(skill_zip)
            for path in sorted((p for p in skill.rglob("*") if p.is_file() and not p.is_symlink()), key=lambda p: p.as_posix()):
                if "__pycache__" in path.parts or path.suffix == ".pyc":
                    continue
                _zip_add(archive, path, f"{SKILL_NAME}/{path.relative_to(skill).as_posix()}")

        with zipfile.ZipFile(source_zip, "x") as archive:
            created.append(source_zip)
            files = sorted((p for p in ROOT.rglob("*") if _safe_repo_file(p)), key=lambda p: p.relative_to(ROOT).as_posix())
            for path in files:
                _zip_add(archive, path, f"Prompter-Silva-local-candidate/{path.relative_to(ROOT).as_posix()}")

        for path in archives:
            sidecar = path.with_suffix(path.suffix + ".sha256")
            with sidecar.open("x", encoding="ascii", newline="\n") as stream:
                created.append(sidecar)
                stream.write(f"{_sha256(path)}  {path.name}\n")
            sidecars.append(sidecar)
    except Exception:
        for path in reversed(created):
            if path.is_file() and not path.is_symlink():
                path.unlink()
        raise
    return archives + sidecars


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    import sys
    sys.path.insert(0, str(ROOT / "src"))
    for output in build(args.output_dir):
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
