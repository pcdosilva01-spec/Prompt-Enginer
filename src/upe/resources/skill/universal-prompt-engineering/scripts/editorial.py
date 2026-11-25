"""Resolve recipient-side instructions from the approved output and access profile."""
from pathlib import Path

from approval_gate import GateError

REFERENCE = Path(__file__).resolve().parents[1] / "references/writing/humanizer.md"
PORTABLE_LIMIT = "O acesso do destinatário à Humanizer completa não foi confirmado. O prompt inclui o núcleo portátil."


def mode_for(profile):
    if not isinstance(profile, dict) or set(profile) != {"parts", "installed", "source_readable"}:
        raise GateError("Declare output parts and verified recipient access")
    parts = profile["parts"]
    if not isinstance(parts, list) or not parts:
        raise GateError("Declare at least one output part")
    if any(type(profile[key]) is not bool for key in ("installed", "source_readable")):
        raise GateError("Recipient capabilities must be booleans")
    relevant = False
    for part in parts:
        if not isinstance(part, dict) or set(part) != {"kind", "language"}:
            raise GateError("Each output part requires kind and language")
        language = part["language"]
        if part["kind"] not in ("prose", "literal") or not isinstance(language, str) or not language.strip():
            raise GateError("Invalid output kind or language")
        if part["kind"] == "prose" and language.strip().casefold() == "pt-br":
            relevant = True
    if not relevant:
        return None
    if profile["installed"]:
        return "installed"
    return "source" if profile["source_readable"] else "portable"


MODES = ("installed", "source", "portable")
# Stable prefixes of the three distributed clauses, not language detection.
# Ordinary inactive tasks must not open the editorial reference.
CLAUSE_PREFIXES = (
    "Aplique a skill instalada humanizar-natural-ptbr",
    "Aplique a Humanizer: consulte",
    "Aplique este núcleo da Humanizer",
)


def _blocks():
    try:
        content = REFERENCE.read_text(encoding="utf-8")
        blocks = {}
        for mode in MODES:
            heading = f"### {mode}\n"
            if content.count(heading) != 1:
                raise GateError(f"Missing or duplicate Humanizer section: {mode}")
            section = content.split(heading, 1)[1].split("\n### ", 1)[0]
            if section.count("```text\n") != 1:
                raise GateError(f"Invalid Humanizer block: {mode}")
            block = section.split("```text\n", 1)[1]
            if "\n```" not in block or not block.split("\n```", 1)[0].strip():
                raise GateError(f"Empty or unterminated Humanizer block: {mode}")
            blocks[mode] = block.split("\n```", 1)[0]
        return blocks
    except (OSError, UnicodeError) as exc:
        raise GateError("Humanizer reference unavailable or unreadable") from exc


def instruction(mode):
    if mode not in MODES:
        raise GateError("Unknown Humanizer access mode")
    blocks = _blocks()
    return blocks["portable"] if mode == "portable" else blocks[mode] + "\n\n" + blocks["portable"]


def validate_instruction(mode, prompt):
    if mode is None:
        if any(prefix in prompt for prefix in CLAUSE_PREFIXES):
            blocks = _blocks()
            if any(block in prompt for block in blocks.values()):
                raise GateError("Humanizer instruction conflicts with the approved non-editorial output")
        return
    if mode not in MODES:
        raise GateError("Unknown Humanizer access mode")
    blocks = _blocks()
    expected = blocks["portable"] if mode == "portable" else blocks[mode] + "\n\n" + blocks["portable"]
    if prompt.count(expected) != 1 or prompt.count(blocks["portable"]) != 1:
        raise GateError("Include exactly one approved Humanizer instruction in the recipient prompt")
    for other in ("installed", "source"):
        if prompt.count(blocks[other]) != int(other == mode):
            raise GateError("Conflicting or duplicated Humanizer access mode")
