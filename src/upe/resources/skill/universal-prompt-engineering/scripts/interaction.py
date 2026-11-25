"""JSON-in/JSON-out workflow for trusted host integrations, without external calls."""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import json
from pathlib import Path
import secrets
import sys

from approval_gate import ApprovalGate, GateError
from delivery_contract import digest, render_delivery
from model_selection import format_recommendation, recommend, required_text


DIAGNOSIS = {"diagnosing", "awaiting_diagnosis_confirmation", "awaiting_rejection_reason",
             "awaiting_corrected_summary"}
GATE_PHASES = {
    "new": {"new"},
    "understanding": {"new", "awaiting_summary_approval", "approved", "completed",
                      "awaiting_corrected_summary"},
    "awaiting_approval": {"awaiting_summary_approval"},
    "approved": {"approved"},
    "construction": {"approved"},
    "review": {"approved"},
    "ready": {"approved"},
    "delivered": {"completed"},
    **{phase: {phase} for phase in DIAGNOSIS},
}
TRANSITIONS = {
    "understand": {"new", "understanding", "awaiting_approval", "approved", "construction",
                   "review", "ready", "delivered", "awaiting_corrected_summary"},
    "present_summary": {"understanding"},
    "approval": {"awaiting_approval"},
    "diagnosis": {"diagnosing"},
    "diagnosis_response": {"awaiting_diagnosis_confirmation"},
    "provide_reason": {"awaiting_rejection_reason"},
    "cosmetic": {"awaiting_approval", "approved", "construction", "review", "ready", "delivered"},
    "build": {"approved"},
    "review": {"construction", "review", "ready"},
    "prepare_delivery": {"review"},
    "deliver": {"ready"},
    "no_gain": {"delivered"},
    "diagnostic": set(GATE_PHASES),
}
USER_EVENTS = {"approval", "diagnosis_response", "provide_reason", "no_gain"}


@dataclass
class Workflow:
    gate: ApprovalGate = field(default_factory=ApprovalGate)
    phase: str = "new"
    session: str = field(default_factory=lambda: secrets.token_hex(16))
    requirements: dict = field(default_factory=dict)
    recommendation: dict = field(default_factory=dict)
    reviewed: str = ""
    ready_packet: str = ""
    previous: str = ""
    optimize: bool = False

    def to_dict(self):
        return dict(gate=self.gate.to_dict(), phase=self.phase, session=self.session,
                    requirements=self.requirements, recommendation=self.recommendation,
                    reviewed=self.reviewed, ready_packet=self.ready_packet,
                    previous=self.previous, optimize=self.optimize)

    @classmethod
    def from_dict(cls, state):
        if state is None:
            return cls()
        if not isinstance(state, dict) or set(state) != set(cls.__dataclass_fields__):
            raise GateError("Missing or invalid workflow state; restart at understanding")
        gate = ApprovalGate.from_dict(state["gate"])
        work = cls(**(state | {"gate": gate}))
        if not isinstance(work.phase, str) or work.phase not in GATE_PHASES or gate.phase not in GATE_PHASES[work.phase]:
            raise GateError("Interaction phase is inconsistent with approval state")
        required_text(work.session, "Session identity")
        if not isinstance(work.requirements, dict) or not isinstance(work.recommendation, dict):
            raise GateError("Invalid requirement ledger or recommendation")
        if type(work.optimize) is not bool or any(
            not isinstance(value, str) for value in (work.reviewed, work.ready_packet, work.previous)
        ):
            raise GateError("Invalid review, delivery or optimization state")
        if bool(work.reviewed) != (work.phase in {"review", "ready", "delivered"}):
            raise GateError("Reviewed artifact is inconsistent with phase")
        if bool(work.ready_packet) != (work.phase in {"ready", "delivered"}):
            raise GateError("Prepared delivery is inconsistent with phase")
        if work.phase != "new" and not work.recommendation:
            raise GateError("Recommendation is missing from interaction state")
        if work.phase not in {"new", "understanding"}:
            snapshot = json.loads(gate.summary)
            if not isinstance(snapshot, dict):
                raise GateError("Invalid approval snapshot")
            for key in ("session", "requirements", "recommendation", "previous", "optimize"):
                if snapshot.get(key) != getattr(work, key):
                    raise GateError("Workflow state no longer matches the approval snapshot")
        return work

    @classmethod
    def step(cls, state, event, artifact_root=None):
        """One staged event. A failed event cannot update the caller's state."""
        if not isinstance(event, dict):
            raise GateError("Event must be an object")
        work = cls.from_dict(state)
        kind = event.get("type")
        if not isinstance(kind, str) or work.phase not in TRANSITIONS.get(kind, set()):
            raise GateError(f"Event {kind!r} unavailable while phase={work.phase}")
        actor = event.get("actor")
        if actor not in (None, "user") or (kind in USER_EVENTS and actor != "user"):
            raise GateError("A trusted user turn is required for this event")
        handler = getattr(work, f"_on_{kind}")
        fields = {key: value for key, value in event.items() if key not in {"type", "actor"}}
        if kind in {"prepare_delivery", "deliver"}:
            fields["artifact_root"] = artifact_root
        if kind == "understand":
            fields["user_initiated"] = actor == "user"
        try:
            result = handler(**fields)
        except TypeError as exc:
            raise GateError("Missing or unexpected event fields") from exc
        return work, result

    def _on_understand(self, brief, requirements, catalog=None, optimize=False, user_initiated=False):
        if not isinstance(requirements, dict):
            raise GateError("Requirements must be an object keyed by stable identifiers")
        for key, value in requirements.items():
            required_text(key, "Requirement identifier")
            required_text(value, "Requirement text")
        if type(optimize) is not bool:
            raise GateError("Optimization flag must be boolean")
        if self.phase == "delivered":
            if not optimize or not user_initiated:
                raise GateError("An optimization starts with the user's acceptance; start a new workflow for a new task")
            self.previous = self.reviewed
        if optimize or self.optimize:
            if not self.previous or any(requirements.get(key) != value for key, value in self.requirements.items()):
                raise GateError("Optimization must preserve each previous approved requirement")
            self.optimize = True
        self.requirements = requirements
        self.recommendation = recommend(brief, [] if catalog is None else catalog)
        self.reviewed = self.ready_packet = ""
        self.phase = "understanding"
        return {"recommendation": self.recommendation}

    def _on_present_summary(self, summary):
        summary = required_text(summary, "Understanding summary")
        revision = self.gate.revision + 1
        lines = [f"**Resumo de entendimento · revisão {revision}**", summary]
        if self.requirements:
            lines.append("**Requisitos obrigatórios**\n" +
                         "\n".join(f"- {text}" for text in self.requirements.values()))
        lines.extend((format_recommendation(self.recommendation),
                      f"Você aprova a revisão {revision} como base para construir o prompt?"))
        visible = "\n\n".join(lines)
        snapshot = json.dumps(dict(session=self.session, requirements=self.requirements,
                                   recommendation=self.recommendation, previous=self.previous,
                                   optimize=self.optimize, text=visible),
                              sort_keys=True, ensure_ascii=False)
        if self.gate.phase == "completed":
            self.gate = ApprovalGate(phase="awaiting_corrected_summary", revision=self.gate.revision,
                                     summary=self.gate.summary, summary_digest=self.gate.summary_digest)
        if self.gate.phase in {"awaiting_summary_approval", "approved"}:
            serial = self.gate.material_change(snapshot)
        else:
            serial = self.gate.present_summary(snapshot)
        self.phase = "awaiting_approval"
        return serial | {"text": visible}

    def _on_approval(self, action, digest="", reason=""):
        result = self.gate.summary_response(action, digest, reason)
        self.phase = "awaiting_approval" if result == "awaiting_summary_approval" else result

    def _on_diagnosis(self, diagnosis):
        self.phase = self.gate.record_diagnosis(diagnosis)

    def _on_diagnosis_response(self, action, explanation=""):
        self.phase = self.gate.diagnosis_response(action, explanation)

    def _on_provide_reason(self, reason):
        self.phase = self.gate.provide_reason(reason)

    def _on_cosmetic(self, note):
        required_text(note, "Justification for cosmetic change outside the approved content")

    def _on_build(self):
        self.phase = "construction"

    def _on_review(self, prompt):
        candidate = digest(required_text(prompt, "Complete prompt for review"))
        if candidate == self.previous:
            raise GateError("An unchanged prompt cannot be delivered as an optimization")
        self.ready_packet = ""
        self.reviewed = candidate
        self.phase = "review"

    def _on_prepare_delivery(self, packet, artifact_root):
        self._render(packet, artifact_root)
        self.ready_packet = digest(packet)
        self.phase = "ready"

    def _on_deliver(self, packet, artifact_root):
        if digest(packet) != self.ready_packet:
            raise GateError("Delivery changed after preparation")
        result = self._render(packet, artifact_root)
        self.gate.deliver_prompt(packet["digest"])
        self.phase = "delivered"
        return result

    def _render(self, packet, artifact_root):
        return render_delivery(packet, approval=self.gate.approved_digest, reviewed=self.reviewed,
                               recommendation=self.recommendation, optimize=self.optimize,
                               artifact_root=artifact_root)

    def _on_no_gain(self, reason):
        return {"text": "A versão atual atingiu um limite justificável. " +
                required_text(reason, "Reason why no material gain remains")}

    def _on_diagnostic(self, findings):
        return {"text": required_text(findings, "Diagnostic without replacement prompt")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-root", type=Path, help="trusted directory for TXT verification")
    args = parser.parse_args()
    try:
        request = json.loads(sys.stdin.buffer.read().decode("utf-8-sig"))
        work, result = Workflow.step(request.get("state"), request.get("event"), args.artifact_root)
        output = dict(state=work.to_dict(), result=result)
        sys.stdout.buffer.write(json.dumps(output, ensure_ascii=False).encode("utf-8") + b"\n")
        return 0
    except (AttributeError, OSError, ValueError) as exc:
        sys.stderr.buffer.write(json.dumps({"error": str(exc)}, ensure_ascii=False).encode("utf-8") + b"\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
