"""Safe, local-only command line for installing the bundled Agent Skill."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

from . import __version__
from .integrity import bundled_skill_path, verify_skill
from .installer import (
    InstallationError,
    InstallationStateError,
    install_skill,
    uninstall_skill,
    update_skill,
    verify_installation,
)
from .targets import TARGETS, TargetError, detect_available_targets, list_targets, resolve_skill_path


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="upe-skill",
        description="Install and verify the Universal Prompt Engineering Agent Skill locally.",
    )
    sub = parser.add_subparsers(dest="command")

    for command in ("install", "update", "uninstall", "verify"):
        child = sub.add_parser(command, help=f"{command.capitalize()} a skill for a supported host")
        child.add_argument("target", choices=sorted(TARGETS), help="host identifier from list-targets")
        child.add_argument("--scope", choices=("user", "project"), default="user")
        child.add_argument("--project-dir", type=Path, help="existing project directory (required for project scope)")
        child.add_argument("--home", type=Path, help=argparse.SUPPRESS)
        if command != "verify":
            child.add_argument("--dry-run", action="store_true", help="show the operation without changing files")

    doctor = sub.add_parser("doctor", help="Check the bundled skill and local host executables")
    doctor.add_argument("--target", choices=sorted(TARGETS), help="also resolve a target install path")
    doctor.add_argument("--scope", choices=("user", "project"), default="user")
    doctor.add_argument("--project-dir", type=Path, help="existing project directory for project scope")
    doctor.add_argument("--home", type=Path, help=argparse.SUPPRESS)
    sub.add_parser("list-targets", help="List documented install locations and manual-only surfaces")
    sub.add_parser("version", help="Print the CLI version")
    sub.add_parser("help", help="Show this help")
    return parser


def _destination(args: argparse.Namespace) -> Path:
    return resolve_skill_path(
        args.target, args.scope, project_dir=args.project_dir, home=args.home,
    )


def _show_targets() -> None:
    print("Target\tInstall\tUser path\tProject path\tEvidence")
    for target in list_targets():
        user_path = "/".join(target.user_path or ()) or "manual only"
        project_path = "/".join(target.project_path or ()) or "manual only"
        status = (
            "filesystem (legacy)" if target.installable and "legacy" in target.evidence_status.lower()
            else "filesystem" if target.installable else "manual"
        )
        print(f"{target.id}\t{status}\t{user_path}\t{project_path}\t{target.evidence_status}")


def _doctor(args: argparse.Namespace) -> int:
    result = verify_skill()
    print(f"Bundled skill: {'PASS' if result.valid else 'FAIL'} ({result.checked_files} files checked)")
    for item in result.errors:
        print(f"  ERROR: {item}")
    for item in result.warnings:
        print(f"  NOTE: {item}")
    detected = detect_available_targets()
    print("Host command executables found on PATH: " + (", ".join(detected) if detected else "none"))
    print("Executable detection does not prove host support, skill discovery, or activation.")
    if args.target:
        try:
            print(f"Target location: {_destination(args)}")
        except TargetError as exc:
            print(f"Target check: FAIL ({exc})")
            return 2
    return 0 if result.valid else 1


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    if args.command is None or args.command == "help":
        parser.print_help()
        return 0
    if args.command == "version":
        print(f"upe-skill {__version__}")
        return 0
    if args.command == "list-targets":
        _show_targets()
        return 0
    if args.command == "doctor":
        return _doctor(args)
    try:
        destination = _destination(args)
        if args.command == "install":
            operation = install_skill(None, destination, dry_run=args.dry_run)
        elif args.command == "update":
            operation = update_skill(None, destination, dry_run=args.dry_run)
        elif args.command == "uninstall":
            operation = uninstall_skill(destination, dry_run=args.dry_run)
        elif args.command == "verify":
            checked = verify_installation(destination)
            print(f"Installation: {'PASS' if checked.valid else 'FAIL'} ({checked.checked_files} files checked)")
            for item in checked.errors:
                print(f"  ERROR: {item}")
            for item in checked.warnings:
                print(f"  NOTE: {item}")
            return 0 if checked.valid else 1
        else:
            parser.error("unknown command")
    except (TargetError, InstallationError, InstallationStateError, OSError, ValueError) as exc:
        print(f"upe-skill: error: {exc}", file=sys.stderr)
        return 2
    print(f"{operation.action}: {operation.destination} ({operation.files} files) — {operation.message}")
    return 0
