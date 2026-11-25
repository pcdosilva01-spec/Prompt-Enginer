"""Validate and render the exact reviewed prompt and its visible assessment."""
from __future__ import annotations

from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

from approval_gate import GateError
from model_selection import format_recommendation, required_text

OFFER = "Deseja que eu otimize ainda mais este prompt, buscando a maior nota de qualidade tecnicamente justificável?"
RUBRIC = (
    ("objective", "Objetivo e tarefa", 15),
    ("fidelity", "Requisitos e fidelidade", 15),
    ("target", "Adequação ao modelo/plataforma", 10),
    ("context", "Contexto e entradas", 10),
    ("scope", "Restrições e escopo", 10),
    ("output", "Saída e formato", 10),
    ("feasibility", "Viabilidade e ferramentas", 10),
    ("validation", "Validação e aceitação", 10),
    ("security", "Segurança", 5),
    ("economy", "Economia e manutenção", 5),
)
CAPS = {"objective": 6, "fidelity": 6, "target": 6, "mandatory": 6, "security": 3}


def digest(value):
    payload = json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _number(value, max_places=12):
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise GateError("Score must be a decimal number")
    try:
        number = Decimal(str(value))
    except InvalidOperation as exc:
        raise GateError("Invalid score") from exc
    if not number.is_finite() or not 0 <= number <= 10 or number.as_tuple().exponent < -max_places:
        raise GateError("Score must be between 0 and 10 with supported decimal precision")
    return number


def score_review(review):
    if not isinstance(review, dict):
        raise GateError("Visible review is required")
    criteria = review.get("criteria")
    if not isinstance(criteria, dict) or set(criteria) != {key for key, _, _ in RUBRIC}:
        raise GateError("Review must contain exactly the ten official criteria")
    total = Decimal(0)
    for key, _, weight in RUBRIC:
        row = criteria[key]
        if not isinstance(row, dict):
            raise GateError(f"Criterion {key} must be an object")
        required_text(row.get("evidence"), f"{key} observable evidence")
        total += _number(row.get("score")) * Decimal(weight).scaleb(-2)
    defects = review.get("defects")
    if not isinstance(defects, list) or any(not isinstance(item, str) or item not in CAPS for item in defects):
        raise GateError("Invalid rubric defect classifications")
    final = min([total, *(Decimal(CAPS[item]) for item in defects)])
    if _number(review.get("final"), max_places=14) != final:
        raise GateError(f"Incorrect final score: expected {final:f}")
    for key in ("weaknesses", "corrections", "limitations", "opportunities"):
        required_text(review.get(key), key)
    return total, final


def _verify_txt(packet, prompt, artifact_root):
    if artifact_root is None:
        raise GateError("File verification requires a trusted artifact root")
    path = Path(required_text(packet.get("txt_path"), "TXT path"))
    root = Path(artifact_root).resolve()
    if path.is_absolute() or path.drive or ".." in path.parts or path.suffix.lower() != ".txt":
        raise GateError("TXT must be a relative .txt path inside the trusted artifact root")
    target = (root / path).resolve()
    if not target.is_relative_to(root) or not target.is_file():
        raise GateError("TXT is missing or escapes the trusted artifact root")
    expected = prompt.encode("utf-8")
    try:
        with target.open("rb") as file:
            if file.read(len(expected) + 1) != expected:
                raise GateError("TXT does not exactly match the UTF-8 prompt")
    except OSError as exc:
        raise GateError("TXT could not be read") from exc
    link = required_text(packet.get("txt_link"), "TXT link")
    if not re.fullmatch(r"(?:sandbox:/|\./)?[A-Za-z0-9._/-]+", link):
        raise GateError("TXT link must be a host artifact locator or a safe relative link")
    portable = PurePosixPath(path.as_posix())
    expected_locator = f"sandbox:/mnt/data/{portable}" if link.startswith("sandbox:") else portable.as_posix()
    if link.removeprefix("./") != expected_locator:
        raise GateError("TXT link must identify the verified file")
    return f"[Baixar prompt TXT]({link})"


def render_delivery(packet, *, approval, reviewed, recommendation, optimize, artifact_root=None):
    if not isinstance(packet, dict) or not approval or packet.get("digest") != approval:
        raise GateError("Current approval is required")
    prompt = required_text(packet.get("prompt"), "Prompt")
    if "\x00" in prompt or digest(prompt) != reviewed:
        raise GateError("Prompt must match the reviewed artifact")
    if not recommendation or packet.get("recommendation") != recommendation:
        raise GateError("Delivery requires the recommendation approved in the summary")
    if packet.get("offer") != OFFER:
        raise GateError("Missing exact optimization offer")
    mode = packet.get("format")
    native = packet.get("native_supported")
    files = packet.get("files_supported")
    if type(native) is not bool or type(files) is not bool or mode != ("native" if native else "text"):
        raise GateError("Format must match the host capabilities")
    if files:
        txt = _verify_txt(packet, prompt, artifact_root)
        if packet.get("file_limitation"):
            raise GateError("TXT was verified and cannot also be marked unavailable")
        file_limitation = ""
    else:
        if "txt_path" in packet or "txt_link" in packet:
            raise GateError("Do not claim an unverified TXT")
        txt = ""
        file_limitation = required_text(packet.get("file_limitation"), "File limitation")

    review = packet.get("review")
    total, final = score_review(review)
    if review["defects"]:
        raise GateError("Resolve material defects before delivery and re-review the actual prompt")
    sections = []
    if mode == "text":
        fence = "`" * max(3, 1 + max(map(len, re.findall(r"`+", prompt)), default=0))
        sections.append(f"{fence}text\n{prompt}\n{fence}")
    if txt:
        sections.append(txt)
    sections.append(format_recommendation(recommendation, sources=True))
    if packet.get("rationale"):
        sections.append(required_text(packet["rationale"], "Delivery rationale"))
    if optimize:
        sections.append("**Comparação com a versão anterior**\n\n" +
                        required_text(packet.get("comparison"), "Comparison"))
    rows = ["| Critério | Peso | Nota | Justificativa observável |", "|---|---:|---:|---|"]
    for key, title, weight in RUBRIC:
        item = review["criteria"][key]
        evidence = item["evidence"].replace("|", "&#124;").replace("\r", "").replace("\n", " ")
        rows.append(f"| {title} | {weight}% | {_number(item['score']):f} | {evidence} |")
    sections.extend((
        "**Autoavaliação do prompt**\n\n" + "\n".join(rows),
        f"**Nota final:** {final:f}/10 (Σ nota × peso / 100 = {total:f}). "
        "A nota avalia a qualidade do texto.",
        f"**Pontos fracos:** {review['weaknesses']}\n\n"
        f"**Correções efetuadas:** {review['corrections']}\n\n"
        f"**Oportunidades restantes:** {review['opportunities']}",
        "**Limitações:** " + " ".join(filter(None, (review["limitations"], file_limitation))),
        OFFER,
    ))
    response = {"text": "\n\n".join(sections)}
    if mode == "native":
        response["native_prompt"] = prompt
    return response
