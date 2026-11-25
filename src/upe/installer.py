"""Safe, offline installation and removal of the bundled Agent Skill."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import tempfile
from typing import Any

from . import __version__
from .integrity import MANIFEST_NAME, _digest, _entries, bundled_skill_path, verify_skill

RECEIPT_SCHEMA = 1
_HASH_RE = re.compile(r"^[0-9a-f]{64}$")


class InstallationError(RuntimeError):
    """Base error for safe installation operations."""


class InstallationConflict(InstallationError):
    """Raised when an operation would overwrite or delete user changes."""


class InstallationStateError(InstallationError):
    """Raised when ownership state is missing, unsafe, or malformed."""


@dataclass(frozen=True)
class OperationResult:
    action: str
    destination: Path
    files: int
    message: str


@dataclass(frozen=True)
class InstallationVerification:
    valid: bool
    checked_files: int
    errors: tuple[str, ...]
    warnings: tuple[str, ...] = ()


def default_state_root() -> Path:
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA")
        return (Path(base) if base else Path.home() / "AppData" / "Local") / "upe-skill"
    base = os.environ.get("XDG_STATE_HOME")
    return (Path(base).expanduser() if base else Path.home() / ".local" / "state") / "upe-skill"


def _canonical(path: Path) -> Path:
    # Keep the lexical path: resolve() follows a final or parent symlink before
    # the installer can reject it. abspath normalizes `..` without following links.
    return Path(os.path.abspath(Path(path).expanduser()))


def _is_linklike(path: Path) -> bool:
    is_junction = getattr(path, "is_junction", None)
    return path.is_symlink() or bool(is_junction and is_junction())


def _assert_no_link_components(path: Path) -> None:
    """Reject links/junctions in an absolute managed path before file I/O."""
    path = _canonical(path)
    current = Path(path.anchor)
    if _is_linklike(current):
        raise InstallationConflict(f"refusing linked path component: {current}")
    for part in path.parts[1:]:
        current = current / part
        if _is_linklike(current):
            raise InstallationConflict(f"refusing linked path component: {current}")


def _receipt_path(destination: Path, state_root: Path) -> Path:
    key = hashlib.sha256(str(_canonical(destination)).encode("utf-8")).hexdigest()
    return Path(state_root).expanduser() / "installations" / f"{key}.json"


def _safe_relative(value: str) -> str:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or ".." in path.parts or "\\" in value or not path.parts:
        raise InstallationStateError(f"unsafe managed path in receipt: {value!r}")
    return path.as_posix()


def _load_receipt(destination: Path, state_root: Path) -> tuple[Path, dict[str, Any]]:
    receipt_path = _receipt_path(destination, state_root)
    if _is_linklike(receipt_path):
        raise InstallationStateError("installation receipt must not be a symlink")
    if not receipt_path.is_file():
        raise InstallationStateError("no UPE-managed installation receipt exists for this target")
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InstallationStateError(f"installation receipt cannot be read: {exc}") from exc
    if not isinstance(receipt, dict) or receipt.get("schema") != RECEIPT_SCHEMA:
        raise InstallationStateError("installation receipt schema is invalid")
    if receipt.get("destination") != str(_canonical(destination)):
        raise InstallationStateError("installation receipt destination does not match the requested target")
    files = receipt.get("files")
    if not isinstance(files, dict):
        raise InstallationStateError("installation receipt file inventory is invalid")
    normalized: dict[str, str] = {}
    for relative, digest in files.items():
        if not isinstance(relative, str) or not isinstance(digest, str) or not _HASH_RE.fullmatch(digest):
            raise InstallationStateError("installation receipt contains an invalid file entry")
        safe_name = _safe_relative(relative)
        if safe_name.casefold() in {name.casefold() for name in normalized}:
            raise InstallationStateError(f"duplicate managed path in receipt: {safe_name}")
        normalized[safe_name] = digest
    receipt["files"] = normalized
    return receipt_path, receipt


def _make_receipt(destination: Path, version: str, files: dict[str, str]) -> dict[str, Any]:
    return {
        "schema": RECEIPT_SCHEMA,
        "package": "universal-prompt-engineering",
        "version": version,
        "destination": str(_canonical(destination)),
        "files": dict(sorted(files.items())),
    }


def _ensure_directory(path: Path, created: list[Path]) -> None:
    missing: list[Path] = []
    current = path
    while not current.exists():
        if _is_linklike(current):
            raise InstallationConflict(f"refusing symlink directory: {current}")
        missing.append(current)
        if current.parent == current:
            break
        current = current.parent
    if current.exists() and (_is_linklike(current) or not current.is_dir()):
        raise InstallationConflict(f"destination parent is not a real directory: {current}")
    for directory in reversed(missing):
        directory.mkdir()
        created.append(directory)


def _atomic_write(path: Path, content: bytes, mode: int | None = None) -> None:
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(mode="wb", dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False) as handle:
            temp_path = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        if mode is not None:
            try:
                os.chmod(temp_path, mode)
            except OSError:
                pass
        os.replace(temp_path, path)
        temp_path = None
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def _rollback(
    backups: dict[Path, tuple[bytes, int | None]],
    created_files: set[Path],
    created_dirs: list[Path],
) -> None:
    for path, (content, mode) in backups.items():
        if path.parent.exists():
            _atomic_write(path, content, mode)
    for path in created_files - set(backups):
        path.unlink(missing_ok=True)
    for directory in reversed(created_dirs):
        try:
            directory.rmdir()
        except OSError:
            pass


def _read_for_update(destination: Path, receipt: dict[str, Any]) -> tuple[dict[str, str], list[str]]:
    old_files: dict[str, str] = receipt["files"]
    conflicts: list[str] = []
    for relative, expected in old_files.items():
        path = destination.joinpath(*PurePosixPath(relative).parts)
        try:
            _assert_no_link_components(path)
        except InstallationConflict:
            conflicts.append(f"managed file is now a symlink: {relative}")
            continue
        if not path.is_file():
            conflicts.append(f"managed file is missing: {relative}")
        elif _digest(path) != expected:
            conflicts.append(f"managed file was modified by the user: {relative}")
    return old_files, conflicts


def install_skill(
    source: Path | None,
    destination: Path,
    state_root: Path | None = None,
    *,
    version: str = __version__,
    dry_run: bool = False,
) -> OperationResult:
    return _install_or_update(source, destination, state_root, version=version, dry_run=dry_run, update=False)


def update_skill(
    source: Path | None,
    destination: Path,
    state_root: Path | None = None,
    *,
    version: str = __version__,
    dry_run: bool = False,
) -> OperationResult:
    return _install_or_update(source, destination, state_root, version=version, dry_run=dry_run, update=True)


def _install_or_update(
    source: Path | None,
    destination: Path,
    state_root: Path | None,
    *,
    version: str,
    dry_run: bool,
    update: bool,
) -> OperationResult:
    source_root = Path(source) if source is not None else bundled_skill_path()
    if source_root.is_symlink() or not source_root.is_dir():
        raise InstallationError("skill source is missing, not a directory, or is a symlink")
    source_root = source_root.resolve()
    target = _canonical(Path(destination))
    _assert_no_link_components(target)
    if source_root == target or source_root in target.parents or target in source_root.parents:
        raise InstallationError("source and destination must not overlap")
    source_result = verify_skill(source_root)
    if not source_result.valid:
        raise InstallationError("skill source failed integrity checks: " + "; ".join(source_result.errors))
    source_files = _entries(source_root)
    source_hashes = {name: _digest(path) for name, path in source_files.items()}
    state_dir = Path(state_root) if state_root is not None else default_state_root()
    state_file = _receipt_path(target, state_dir)
    try:
        _assert_no_link_components(state_file)
    except InstallationConflict as exc:
        raise InstallationStateError(f"unsafe installation state path: {exc}") from exc
    if _is_linklike(state_file):
        raise InstallationStateError("installation receipt path is a symlink or junction")

    previous: dict[str, Any] | None = None
    if state_file.is_file():
        _, previous = _load_receipt(target, state_dir)
    elif target.exists():
        if _is_linklike(target) or not target.is_dir():
            raise InstallationConflict("existing target is not a real skill directory")
        if any(target.iterdir()):
            raise InstallationConflict("target contains unowned files; refusing to overwrite them")
    if update and previous is None:
        raise InstallationStateError("cannot update: no UPE-managed installation receipt exists")
    if previous is not None and not target.is_dir():
        raise InstallationStateError("receipt exists but the managed skill directory is missing")

    if previous is not None:
        old_files, conflicts = _read_for_update(target, previous)
        if conflicts:
            raise InstallationConflict("; ".join(conflicts))
        if old_files == source_hashes:
            if previous.get("version") == version:
                return OperationResult("unchanged", target, len(source_hashes), "The installed skill already matches this version.")
            if dry_run:
                return OperationResult("would update metadata", target, len(source_hashes), "Only the local version record would change.")
            previous["version"] = version
            _atomic_write(state_file, (json.dumps(previous, indent=2) + "\n").encode("utf-8"))
            return OperationResult("updated metadata", target, len(source_hashes), "Skill files were unchanged; local version metadata was updated.")
        if not update:
            raise InstallationConflict("a managed installation already exists; use 'update' to replace its verified files")
        for relative in source_hashes:
            path = target.joinpath(*PurePosixPath(relative).parts)
            if path.exists() and relative not in old_files:
                raise InstallationConflict(f"new package file would overwrite an unowned file: {relative}")
        action = "would update" if dry_run else "updated"
    else:
        if update:
            raise InstallationStateError("cannot update: no UPE-managed installation receipt exists")
        if dry_run:
            return OperationResult("would install", target, len(source_hashes), "No files were changed.")
        action = "installed"

    if dry_run:
        return OperationResult(action, target, len(source_hashes), "No files were changed.")

    created_dirs: list[Path] = []
    created_files: set[Path] = set()
    backups: dict[Path, tuple[bytes, int | None]] = {}
    target_existed = target.exists()
    old_file_names = set(previous["files"]) if previous is not None else set()
    obsolete = old_file_names - set(source_hashes)
    try:
        if not target.exists():
            _ensure_directory(target.parent, created_dirs)
            target.mkdir()
            created_dirs.append(target)
        if _is_linklike(target):
            raise InstallationConflict("refusing to write through a symlink target")
        for relative, source_path in source_files.items():
            path = target.joinpath(*PurePosixPath(relative).parts)
            current = path
            while current != target:
                if _is_linklike(current):
                    raise InstallationConflict(f"refusing symlink in destination path: {current.relative_to(target).as_posix()}")
                current = current.parent
            _ensure_directory(path.parent, created_dirs)
            existed = path.exists()
            if existed and (_is_linklike(path) or not path.is_file()):
                raise InstallationConflict(f"destination file is not a regular file: {relative}")
            if existed and _digest(path) == source_hashes[relative]:
                continue
            if existed:
                try:
                    mode = stat.S_IMODE(path.stat().st_mode)
                except OSError:
                    mode = None
                backups[path] = (path.read_bytes(), mode)
            else:
                created_files.add(path)
            source_mode = stat.S_IMODE(source_path.stat().st_mode)
            _atomic_write(path, source_path.read_bytes(), source_mode)
        for relative in sorted(obsolete):
            path = target.joinpath(*PurePosixPath(relative).parts)
            if path.exists():
                if _is_linklike(path) or not path.is_file():
                    raise InstallationConflict(f"refusing to remove non-regular managed path: {relative}")
                backups[path] = (path.read_bytes(), stat.S_IMODE(path.stat().st_mode))
                path.unlink()
        payload = _make_receipt(target, version, source_hashes)
        _ensure_directory(state_file.parent, created_dirs)
        if state_file.exists():
            if _is_linklike(state_file) or not state_file.is_file():
                raise InstallationStateError("installation receipt is not a regular file")
            backups[state_file] = (state_file.read_bytes(), stat.S_IMODE(state_file.stat().st_mode))
        else:
            created_files.add(state_file)
        _atomic_write(state_file, (json.dumps(payload, indent=2) + "\n").encode("utf-8"), 0o600)
        installed_hashes = {
            name: _digest(target.joinpath(*PurePosixPath(name).parts))
            for name in source_hashes
        }
        if installed_hashes != source_hashes:
            raise InstallationError("post-install file verification failed")
    except Exception as exc:
        try:
            _rollback(backups, created_files, created_dirs)
        except Exception as rollback_exc:
            raise InstallationError(f"operation failed ({exc}); rollback also failed ({rollback_exc})") from exc
        if isinstance(exc, InstallationError):
            raise
        raise InstallationError(f"installation could not be completed: {exc}") from exc
    return OperationResult(action, target, len(source_hashes), f"Installed version {version}.")


def verify_installation(destination: Path, state_root: Path | None = None) -> InstallationVerification:
    target = _canonical(Path(destination))
    state_dir = Path(state_root) if state_root is not None else default_state_root()
    try:
        _assert_no_link_components(target)
        _assert_no_link_components(_receipt_path(target, state_dir))
    except InstallationConflict as exc:
        return InstallationVerification(False, 0, (str(exc),))
    try:
        _, receipt = _load_receipt(target, state_dir)
    except InstallationStateError as exc:
        return InstallationVerification(False, 0, (str(exc),))
    errors: list[str] = []
    if _is_linklike(target) or not target.is_dir():
        return InstallationVerification(False, 0, ("managed skill directory is missing or unsafe",))
    checked = 0
    for relative, expected in receipt["files"].items():
        path = target.joinpath(*PurePosixPath(relative).parts)
        try:
            _assert_no_link_components(path)
        except InstallationConflict:
            errors.append(f"managed file path is unsafe: {relative}")
        else:
            if not path.is_file():
                errors.append(f"managed file missing or unsafe: {relative}")
            elif _digest(path) != expected:
                errors.append(f"managed file hash mismatch: {relative}")
        checked += 1
    warnings: list[str] = []
    try:
        actual = _entries(target)
        extras = sorted(set(actual) - set(receipt["files"]))
        if extras:
            warnings.append(f"unmanaged files preserved in skill directory: {extras}")
    except (OSError, ValueError) as exc:
        errors.append(str(exc))
    return InstallationVerification(not errors, checked, tuple(errors), tuple(warnings))


def uninstall_skill(
    destination: Path,
    state_root: Path | None = None,
    *,
    dry_run: bool = False,
) -> OperationResult:
    target = _canonical(Path(destination))
    state_dir = Path(state_root) if state_root is not None else default_state_root()
    _assert_no_link_components(target)
    _assert_no_link_components(_receipt_path(target, state_dir))
    state_file, receipt = _load_receipt(target, state_dir)
    if _is_linklike(target) or not target.is_dir():
        raise InstallationStateError("managed skill directory is missing or unsafe")
    conflicts: list[str] = []
    removable: list[Path] = []
    for relative, expected in receipt["files"].items():
        path = target.joinpath(*PurePosixPath(relative).parts)
        try:
            _assert_no_link_components(path)
        except InstallationConflict:
            conflicts.append(f"preserved symlink at managed path: {relative}")
            continue
        if not path.exists():
            continue
        if not path.is_file():
            conflicts.append(f"preserved non-file at managed path: {relative}")
        elif _digest(path) != expected:
            conflicts.append(f"preserved user-modified file: {relative}")
        else:
            removable.append(path)
    if dry_run:
        return OperationResult("would uninstall", target, len(removable), "No files were changed.")
    backups: dict[Path, tuple[bytes, int | None]] = {}
    removed: list[Path] = []
    try:
        for path in removable:
            backups[path] = (path.read_bytes(), stat.S_IMODE(path.stat().st_mode))
            path.unlink()
            removed.append(path)
        if not conflicts:
            backups[state_file] = (state_file.read_bytes(), stat.S_IMODE(state_file.stat().st_mode))
            state_file.unlink()
        directories = sorted((p for p in target.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True)
        for directory in directories + [target]:
            try:
                directory.rmdir()
            except OSError:
                pass
    except Exception as exc:
        for path, (content, mode) in backups.items():
            if path.parent.exists():
                _atomic_write(path, content, mode)
        raise InstallationError(f"uninstall could not be completed: {exc}") from exc
    if conflicts:
        raise InstallationConflict("some user-modified files were preserved: " + "; ".join(conflicts))
    return OperationResult("uninstalled", target, len(removed), "Managed skill files were removed; unrelated user files were preserved.")
