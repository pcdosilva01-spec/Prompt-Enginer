"""Regenerate MANIFEST.sha256 for the portable skill directory."""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.sha256"


def entries() -> list[str]:
    rows = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path == MANIFEST or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append(f"{digest}  {path.relative_to(ROOT).as_posix()}")
    return rows


if __name__ == "__main__":
    MANIFEST.write_text("\n".join(entries()) + "\n", encoding="utf-8")
    print(f"Wrote {len(entries())} SHA-256 entries to {MANIFEST.name}")
