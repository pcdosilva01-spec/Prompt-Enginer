"""Rank host-supplied candidates without a static catalog or external calls."""
from __future__ import annotations

from datetime import date
from urllib.parse import urlsplit

from approval_gate import GateError


def required_text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise GateError(f"{field} must be non-empty text")
    return value


def _candidate(row):
    if not isinstance(row, dict):
        raise GateError("A candidate must be an object")
    for key in ("model", "platform", "availability"):
        required_text(row.get(key), key)
    if not isinstance(row.get("reasoning"), str):
        raise GateError("Reasoning must be text, or empty for no verified setting")
    if row["availability"] not in {"confirmed", "unknown", "unavailable"}:
        raise GateError("Invalid availability")
    if any(type(row.get(key)) is not bool for key in ("sufficient", "economy")):
        raise GateError("Candidate sufficiency and economy must be booleans")
    evidence = row.get("evidence")
    if not isinstance(evidence, list) or (row["availability"] != "unknown" and not evidence):
        raise GateError("Known candidate status requires evidence")
    for entry in evidence:
        if not isinstance(entry, dict):
            raise GateError("Evidence must be an object")
        for key in ("source", "url", "date", "claim", "limits"):
            required_text(entry.get(key), key)
        try:
            access_date = date.fromisoformat(entry["date"])
            url = urlsplit(entry["url"])
        except ValueError as exc:
            raise GateError("Invalid evidence date or URL") from exc
        if access_date > date.today() or url.scheme != "https" or not url.hostname:
            raise GateError("Evidence requires a non-future date and HTTPS URL")
    if (row["reasoning"] or row["economy"]) and not evidence:
        raise GateError("Specific reasoning or economy claims require evidence")
    return {key: row[key] for key in (
        "model", "platform", "reasoning", "availability", "sufficient", "economy", "evidence"
    )}


def recommend(brief, catalog):
    """Select within one surface; preserve user choice and represent unverified access."""
    if not isinstance(brief, dict) or not isinstance(catalog, list):
        raise GateError("Brief and catalog must be an object and an array")
    fields = ("task", "complexity", "platform", "tools", "context", "plan", "quota",
              "budget", "priority", "chosen_model", "chosen_reasoning", "external_access")
    if set(brief) != set(fields):
        raise GateError("Model brief is incomplete or contains unexpected fields")
    for key in fields[:9]:
        required_text(brief[key], key)
    for key in ("chosen_model", "chosen_reasoning"):
        if not isinstance(brief[key], str):
            raise GateError(f"{key} must be text")
    if type(brief["external_access"]) is not bool:
        raise GateError("Declare whether current external research is available and permitted")
    if brief["complexity"] not in {"simple", "moderate", "complex"}:
        raise GateError("Unknown complexity")
    if brief["quota"] not in {"low", "sufficient", "unknown"}:
        raise GateError("Unknown quota classification")
    if brief["priority"] not in {"quality", "latency", "cost", "balanced"}:
        raise GateError("Unknown optimization priority")

    surface = brief["platform"]
    options = [
        row for row in map(_candidate, catalog)
        if row["platform"].casefold() == surface.casefold()
    ]
    viable = [row for row in options if row["sufficient"] and row["availability"] != "unavailable"]
    prefer_economy = (brief["quota"] == "low" or brief["priority"] in {"latency", "cost"}
                      or (brief["priority"] == "balanced" and brief["complexity"] == "simple"))
    viable.sort(key=lambda row: (row["availability"] != "confirmed",
                                 prefer_economy and not row["economy"]))
    chosen = brief["chosen_model"].strip()

    def conditional(label):
        return dict(model=label, platform=surface, reasoning="", availability="unknown",
                    sufficient=False, economy=False, evidence=[])

    if chosen:
        matches = [row for row in options if row["model"].casefold() == chosen.casefold()]
        requested = brief["chosen_reasoning"].strip()
        primary = next((row for row in matches if row["reasoning"] == requested), None)
        primary = (primary or next(iter(matches), None) or conditional(chosen)) | {"model": chosen}
        rationale = "Destino escolhido pelo usuário. Qualquer troca exige autorização."
        if requested and requested != primary["reasoning"]:
            rationale += f" Esforço solicitado ({requested}) sem suporte confirmado para esta configuração."
        if not primary["sufficient"]:
            rationale += " Viabilidade para a tarefa não confirmada."
    elif viable:
        primary = viable[0]
        rationale = ("Prioridade à suficiência com opção econômica quando verificada."
                     if prefer_economy else "Prioridade à cobertura da tarefa e ao acesso verificável.")
    else:
        primary = conditional("Modelo suficiente disponível no seletor do destino")
        rationale = "Seleção condicional até verificar acesso e capacidades na superfície."

    other = [row for row in viable if (row["model"].casefold(), row["reasoning"]) !=
             (primary["model"].casefold(), primary["reasoning"])]
    alternative = next((row for row in other if row["economy"]), None)
    alternative_rationale = "Verifique opção suficiente com menor esforço, custo ou latência."
    if alternative:
        alternative_rationale = "Alternativa marcada como econômica pelas evidências fornecidas."
    elif chosen and (primary["availability"] == "unavailable" or not primary["sufficient"]) and other:
        alternative = other[0]
        alternative_rationale = (
            "Opção suficiente para considerar se o usuário autorizar. Custo e latência relativos não verificados."
        )
    limits = []
    if not brief["external_access"]:
        limits.append("Sem consulta externa vigente. Use somente evidência já disponível e orientação condicional.")
    if brief["quota"] == "unknown":
        limits.append("Cota da conta desconhecida.")
    if brief["quota"] == "low":
        limits.append("Cota baixa declarada. Confira o saldo real na própria superfície.")
    if primary["availability"] == "unavailable":
        limits.append("Destino escolhido indisponível no acesso declarado. Alternativa depende de autorização.")
    elif primary["availability"] == "unknown":
        limits.append("Acesso ao destino ainda não confirmado.")
    return dict(brief=brief, primary=primary,
                alternative=alternative or conditional("Opção suficiente mais rápida ou econômica, se confirmada"),
                rationale=rationale,
                alternative_rationale=alternative_rationale,
                limits=limits)


def format_recommendation(selection, *, sources=False):
    brief = selection["brief"]
    lines = [f"**Destino e configuração:** {brief['platform']} · plano {brief['plan']} · "
             f"cota {brief['quota']} · orçamento {brief['budget']}."]
    if sources:
        lines.append(f"**Ferramentas previstas:** {brief['tools']}.")
    for key, title, rationale in (
        ("primary", "Modelo recomendado", "rationale"),
        ("alternative", "Alternativa", "alternative_rationale"),
    ):
        row = selection[key]
        effort = row["reasoning"] or "a confirmar ou não aplicável"
        lines.append(f"**{title}:** {row['model']} · raciocínio {effort} · "
                     f"acesso {row['availability']}. {selection[rationale]}")
    lines.extend(selection["limits"])
    if sources:
        seen = []
        for row in (selection["primary"], selection["alternative"]):
            for source in row["evidence"]:
                if source not in seen:
                    seen.append(source)
                    lines.append(f"{source['date']} · {source['claim']} · Limite: {source['limits']}. "
                                 f"[{source['source']}]({source['url']})")
    return "\n\n".join(lines)
