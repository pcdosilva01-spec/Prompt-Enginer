"""Compare preserved dossier copies to source files and write their SHA-256 inventory."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COPIES = ROOT / "references" / "original_dossier"
OUTPUT = COPIES / "ORIGINALS_SHA256.json"


def hashes(folder: Path) -> dict[str, str]:
    return {file.name: hashlib.sha256(file.read_bytes()).hexdigest() for file in sorted(folder.iterdir()) if file.is_file() and file.name != OUTPUT.name}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="original dossier directory")
    args = parser.parse_args()
    source = hashes(args.source.resolve())
    copies = hashes(COPIES)
    if set(source) != set(copies):
        print(f"File inventory differs: source-only={sorted(set(source)-set(copies))}; copy-only={sorted(set(copies)-set(source))}")
        return 1
    mismatches = [name for name in source if source[name] != copies[name]]
    if mismatches:
        print(f"Source/copy hash mismatch: {mismatches}")
        return 1
    OUTPUT.write_text(json.dumps(copies, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Preservation verified: {len(copies)} files match source SHA-256.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
