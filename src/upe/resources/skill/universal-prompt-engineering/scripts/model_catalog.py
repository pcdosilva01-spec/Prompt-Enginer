"""Read and audit one provider snapshot at a time. No network or account discovery."""
from __future__ import annotations

import argparse
from datetime import date, timedelta
import json
from pathlib import Path
from urllib.parse import urlsplit

from approval_gate import GateError

DIRECTORY = Path(__file__).resolve().parents[1] / "references/models/catalog"
STATES = {"listed", "stable", "preview", "announced", "deprecated", "retired", "restricted"}
FIELDS = {"id", "name", "status", "released", "modalities", "context", "output", "reasoning",
          "features", "pricing", "guide", "sources"}


def iso(value):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise GateError(f"Invalid ISO date: {value!r}") from exc


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _strings(items):
    return isinstance(items, list) and all(_text(v) for v in items) and len(items) == len(set(items))


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise GateError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def expires(record, checked):
    if record["status"] in {"preview", "announced", "restricted"}:
        days = 7
    elif record["status"] in {"deprecated", "retired"}:
        days = 90
    else:
        days = 14 if record["pricing"] else 30
    deadline = checked + timedelta(days=days)
    if "valid_through" in record:
        deadline = min(deadline, iso(record["valid_through"]))
    return deadline


def read_family(family, *, today=None, directory=DIRECTORY):
    if not isinstance(family, str) or not family.isascii() or not family.isalpha() or not family.islower():
        raise GateError("Invalid catalog family")
    try:
        data = json.loads((directory / (family + ".json")).read_text(encoding="utf-8"),
                          object_pairs_hook=_unique_object)
    except (OSError, ValueError) as exc:
        raise GateError(f"{family}: cannot read catalog: {exc}") from exc
    if not isinstance(data, dict) or not all(_text(data.get(k)) for k in ("publisher", "surface", "limits")):
        raise GateError(f"{family}: missing publisher, surface or limits")
    checked = iso(data.get("checked"))
    if checked > (today or date.today()) or data.get("level") != "E2":
        raise GateError(f"{family}: invalid primary-source snapshot")
    sources = data.get("sources")
    if not isinstance(sources, dict) or not sources:
        raise GateError(f"{family}: missing source ledger")
    for key, entry in sources.items():
        if not isinstance(entry, dict) or not all(_text(entry.get(k)) for k in ("title", "claim", "url")):
            raise GateError(f"{family}: incomplete evidence {key}")
        url = urlsplit(entry["url"])
        if url.scheme != "https" or not url.hostname or "edition" not in entry:
            raise GateError(f"{family}: invalid source URL or missing edition {key}")
    if not isinstance(data.get("models"), list) or not data["models"]:
        raise GateError(f"{family}: missing models")
    seen = set()
    for row in data["models"]:
        if not isinstance(row, dict) or FIELDS - row.keys():
            raise GateError(f"{family}: incomplete model record")
        if not all(_text(row[k]) for k in ("id", "name", "guide", "status")) or row["status"] not in STATES:
            raise GateError(f"{family}: invalid model identity/status")
        model = row["id"].casefold()
        if model in seen:
            raise GateError(f"{family}: duplicate model {model}")
        seen.add(model)
        if not _strings(row["sources"]) or not row["sources"] or set(row["sources"]) - sources.keys():
            raise GateError(f"{model}: invalid evidence references")
        if not _strings(row["features"]):
            raise GateError(f"{model}: invalid feature list")
        if "unsupported_efforts" in row and not _strings(row["unsupported_efforts"]):
            raise GateError(f"{model}: invalid unsupported effort list")
        for key in ("context", "output"):
            n = row[key]
            if n is not None and (type(n) is not int or n <= 0):
                raise GateError(f"{model}: invalid token limit {key}")
        if row["context"] and row["output"] and row["output"] > row["context"]:
            raise GateError(f"{model}: output exceeds context")
        if row["released"] and iso(row["released"]) > checked and row["status"] != "announced":
            raise GateError(f"{model}: release after snapshot")
        expires(row, checked)
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--family", help="audit only this provider file")
    parser.add_argument("--as-of", type=iso, default=date.today())
    parser.add_argument("--strict-age", action="store_true", help="exit 1 if documentary review is due")
    args = parser.parse_args()
    families = [args.family] if args.family else sorted(p.stem for p in DIRECTORY.glob("*.json"))
    identities = set()
    overdue = []
    try:
        if not families:
            raise GateError("Missing provider snapshots")
        for family in families:
            data = read_family(family, today=args.as_of)
            for row in data["models"]:
                identity = (data["surface"].casefold(), row["id"].casefold())
                if identity in identities:
                    raise GateError(f"Duplicate surface/model across files: {identity}")
                identities.add(identity)
                if args.as_of > expires(row, iso(data["checked"])):
                    overdue.append(f'{family}: {row["id"]}')
    except (ValueError, OSError) as exc:
        parser.exit(2, f"{exc}\n")
    print(f"{len(identities)} records; {len(overdue)} due for review")
    for item in overdue:
        print(item)
    return int(args.strict_age and bool(overdue))


if __name__ == "__main__":
    raise SystemExit(main())
