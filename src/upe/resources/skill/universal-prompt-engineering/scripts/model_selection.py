"""Rank host-supplied candidates without a static catalog or external calls."""
from __future__ import annotations

from datetime import date
from math import isfinite
from urllib.parse import urlsplit

from approval_gate import GateError
from editorial import mode_for
from model_catalog import expires, iso, read_family


FAMILY_FOR_SURFACE = {
    "openai api": "openai", "codex": "codex", "claude api": "anthropic",
    "gemini api": "google", "xai api": "xai", "deepseek api": "deepseek",
    "alibaba model studio": "alibaba", "pesos llama": "meta", "mistral api": "mistral",
    "cohere api": "cohere", "z.ai api": "zai", "pesos kimi": "moonshot",
}


def _money(value):
    return type(value) in (float, int) and isfinite(value) and value >= 0


def _check_needs(needs):
    if not isinstance(needs, dict) or needs.keys() - {"context", "output", "features", "budget_usd"}:
        raise GateError("Invalid task capability requirements")
    for key in ("context", "output"):
        if key in needs and (type(needs[key]) is not int or needs[key] <= 0):
            raise GateError(f"Expected positive token count: {key}")
    features = needs.get("features", [])
    if not isinstance(features, list) or not all(isinstance(item, str) and item for item in features):
        raise GateError("Expected required feature names")
    if "budget_usd" in needs and not _money(needs["budget_usd"]):
        raise GateError("Expected a nonnegative USD budget")


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
    result = {key: row[key] for key in (
        "model", "platform", "reasoning", "availability", "sufficient", "economy", "evidence"
    )}
    if "estimated_usd" in row:
        if not _money(row["estimated_usd"]) or not evidence:
            raise GateError("Cost estimate requires a nonnegative amount and evidence")
        result["estimated_usd"] = row["estimated_usd"]
    return result


def _screen(options, surface, needs, today):
    """Apply documented limits only on their exact surface; leave semantic fit to the host."""
    family = FAMILY_FOR_SURFACE.get(surface.casefold())
    snapshot = read_family(family, today=today) if family and options else None
    records = {r["id"].casefold(): r for r in snapshot["models"]} if snapshot else {}
    notes = []
    seen = set()
    for row in options:
        identity = row["model"].casefold(), row["reasoning"]
        if identity in seen:
            raise GateError("Duplicate model/effort candidate on the same surface")
        seen.add(identity)
        facts = records.get(identity[0])
        evidence = row["evidence"]
        # The legacy host contract supplies joint evidence of availability and fit.
        stale = any((today - iso(item["date"])).days > 14 for item in evidence)
        if facts:
            checked = iso(snapshot["checked"])
            expired = today > expires(facts, checked)
            if expired:
                facts = None
                notes.append(f"{row['model']}: ficha local vencida.")
            elif facts["status"] in {"retired", "announced"}:
                row.update(availability="unavailable", sufficient=False, economy=False)
                notes.append(f"{row['model']}: estado documental {facts['status']}.")
                continue
            elif facts["status"] == "deprecated":
                notes.append(f"{row['model']}: descontinuação documentada; conferir migração.")
            if facts and row["reasoning"].strip().casefold() in {
                value.casefold() for value in facts.get("unsupported_efforts", [])
            }:
                notes.append(f"{row['model']}: esforço {row['reasoning']} rejeitado na superfície documentada.")
                row.update(availability="unavailable", sufficient=False, economy=False)
                continue
        if stale:
            row.update(availability="unknown", sufficient=False, economy=False, reasoning="")
            notes.append(f"{row['model']}: evidência vencida; revalidar acesso e configuração.")
        capacity = facts or {}
        missing = any((capacity.get(k) or 0) < needs[k] for k in ("output", "context") if k in needs)
        missing |= not set(needs.get("features", [])).issubset(capacity.get("features", []))
        if "budget_usd" in needs:
            missing |= row.get("estimated_usd", float("inf")) > needs["budget_usd"]
        if missing:
            row.update(sufficient=False, economy=False)
            notes.append(f"{row['model']}: limite, recurso ou custo exigido sem cobertura confirmada.")
    return notes


def recommend(brief, catalog):
    """Select within one surface; preserve user choice and represent unverified access."""
    if not isinstance(brief, dict) or not isinstance(catalog, list):
        raise GateError("Brief and catalog must be an object and an array")
    fields = ("task", "complexity", "platform", "tools", "context", "plan", "quota",
              "budget", "priority", "chosen_model", "chosen_reasoning", "external_access")
    if set(brief) - {"editorial", "needs"} != set(fields):
        raise GateError("Model brief is incomplete or contains unexpected fields")
    if "editorial" in brief:
        mode_for(brief["editorial"])
    needs = brief.get("needs", {})
    _check_needs(needs)
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
    limits = _screen(options, surface, needs, date.today())
    viable = [row for row in options if row["sufficient"] and row["availability"] != "unavailable"]
    prefer_economy = (brief["quota"] == "low" or brief["priority"] in {"latency", "cost"}
                      or (brief["priority"] == "balanced" and brief["complexity"] == "simple"))
    viable.sort(key=lambda row: (row["availability"] != "confirmed",
                                 prefer_economy and not row["economy"]))
    chosen = brief["chosen_model"].strip()

    def conditional(label):
        return dict(model=label, platform=surface, reasoning="", availability="unknown",
                    sufficient=False, economy=False, evidence=[])

    requested = brief["chosen_reasoning"].strip()
    if requested and not chosen:
        viable = [row for row in viable if row["reasoning"] == requested]
        if not viable:
            limits.append(f"Esforço solicitado ({requested}) sem opção suficiente verificada.")
    if chosen:
        matches = [row for row in options if row["model"].casefold() == chosen.casefold()]
        primary = next((row for row in matches if row["reasoning"] == requested), None)
        primary = (primary or next(iter(matches), None) or conditional(chosen)) | {"model": chosen}
        rationale = "Destino escolhido pelo usuário. Qualquer troca exige autorização."
        if requested and requested != primary["reasoning"]:
            rationale += f" Esforço solicitado ({requested}) sem suporte confirmado para esta configuração."
            primary = primary | {"reasoning": "", "sufficient": False}
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
