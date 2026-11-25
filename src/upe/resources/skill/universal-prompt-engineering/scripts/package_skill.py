"""Build and verify the distributable ZIP beside the delivery folder."""
from __future__ import annotations

import hashlib
import os
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT.parent.parent / f"{ROOT.parent.name}.zip"
sys.path.insert(0, str(ROOT / "scripts"))
from verify_package import verify


def _expected_files(root: Path) -> dict[str, str]:
    expected: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Refusing to package symlink: {path.relative_to(root).as_posix()}")
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        expected[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return expected


def _verify_archive(path: Path, root_name: str, expected: dict[str, str]) -> None:
    prefix = f"{root_name}/"
    with zipfile.ZipFile(path, "r") as archive:
        bad = archive.testzip()
        names = [name for name in archive.namelist() if not name.endswith("/")]
        if bad:
            raise ValueError(f"Archive CRC failure: {bad}")
        if len(names) != len(set(names)):
            raise ValueError("Archive contains duplicate file paths")
        actual: dict[str, str] = {}
        for name in names:
            member = PurePosixPath(name)
            if member.is_absolute() or ".." in member.parts or not name.startswith(prefix):
                raise ValueError(f"Unsafe or unexpected archive path: {name}")
            actual[name[len(prefix):]] = hashlib.sha256(archive.read(name)).hexdigest()
        if actual != expected:
            missing = sorted(set(expected) - set(actual))
            extra = sorted(set(actual) - set(expected))
            changed = sorted(key for key in set(expected) & set(actual) if expected[key] != actual[key])
            raise ValueError(f"Archive inventory/hash mismatch: missing={missing}; extra={extra}; changed={changed}")


def build_archive(root: Path, output: Path) -> int:
    root = root.resolve()
    output = Path(os.path.abspath(output))
    if output.is_symlink():
        raise ValueError(f"Refusing output path that is a symlink: {output}")
    output = output.parent.resolve() / output.name
    if output.exists() and not output.is_file():
        raise OSError(f"Output path is not a regular file: {output}")
    expected = _expected_files(root)
    problems = verify(root)
    if problems:
        raise ValueError("Invalid skill package:\n- " + "\n- ".join(problems))
    if not output.parent.is_dir():
        raise OSError(f"Output directory does not exist: {output.parent}")
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(prefix=f".{output.name}.", suffix=".tmp", dir=output.parent, delete=False) as handle:
            temp_path = Path(handle.name)
        with zipfile.ZipFile(temp_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for relative in expected:
                archive.write(root / Path(relative), f"{root.name}/{relative}")
        _verify_archive(temp_path, root.name, expected)
        os.replace(temp_path, output)
        temp_path = None
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
    return len(expected)


def main() -> int:
    try:
        count = build_archive(ROOT, OUTPUT)
    except (OSError, ValueError) as exc:
        print(f"Failed to create verified package: {exc}", file=sys.stderr)
        return 1
    print(f"Created and verified {OUTPUT.name}: {count} files, all SHA-256 values match.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
