"""Check that built wheel/sdist archives contain a hash-consistent skill tree."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys
import tarfile
import zipfile

SKILL_SUFFIX = "resources/skill/universal-prompt-engineering/"


def _check_manifest(files: dict[str, bytes], prefix: str, label: str) -> list[str]:
    manifest_name = prefix + "MANIFEST.sha256"
    if manifest_name not in files:
        return [f"{label}: missing {manifest_name}"]
    errors: list[str] = []
    listed: dict[str, str] = {}
    for number, line in enumerate(files[manifest_name].decode("utf-8").splitlines(), 1):
        try:
            digest, name = line.split("  ", 1)
        except ValueError:
            errors.append(f"{label}: malformed manifest row {number}")
            continue
        listed[name] = digest
    actual = {name[len(prefix):]: data for name, data in files.items() if name.startswith(prefix) and name != manifest_name}
    for name, expected in listed.items():
        data = actual.get(name)
        if data is None:
            errors.append(f"{label}: missing bundled file {name}")
        elif hashlib.sha256(data).hexdigest() != expected:
            errors.append(f"{label}: hash mismatch for {name}")
    extra = sorted(set(actual) - set(listed))
    if extra:
        errors.append(f"{label}: unlisted bundled files: {extra}")
    return errors


def _zip_files(path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(path) as archive:
        return {item.filename: archive.read(item) for item in archive.infolist() if not item.is_dir()}


def _tar_files(path: Path) -> dict[str, bytes]:
    with tarfile.open(path, "r:gz") as archive:
        return {item.name: archive.extractfile(item).read() for item in archive.getmembers() if item.isfile()}


def check(path: Path) -> list[str]:
    files = _zip_files(path) if path.suffix == ".whl" else _tar_files(path)
    manifests = [name for name in files if name.endswith("/MANIFEST.sha256") and SKILL_SUFFIX in name]
    if len(manifests) != 1:
        return [f"{path.name}: expected one packaged skill manifest, found {len(manifests)}"]
    prefix = manifests[0][:-len("MANIFEST.sha256")]
    errors = _check_manifest(files, prefix, path.name)
    if prefix + "SKILL.md" not in files:
        errors.append(f"{path.name}: missing packaged SKILL.md")
    return errors


def main() -> int:
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dist")
    artifacts = sorted([*folder.glob("*.whl"), *folder.glob("*.tar.gz")])
    if not artifacts:
        print(f"No wheel or source distribution found in {folder}", file=sys.stderr)
        return 2
    errors = [message for artifact in artifacts for message in check(artifact)]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    for artifact in artifacts:
        print(f"PASS {artifact.name}: bundled skill manifest and files verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
