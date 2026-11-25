"""Deterministic approval-state helper. It does not interpret natural language."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import asdict, dataclass
from typing import Any


class GateError(ValueError):
    """An event is invalid for the current approval state."""


def _digest(summary: str, revision: int) -> str:
    payload = f"{revision}\0{summary}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@dataclass
class ApprovalGate:
    phase: str = "new"
    summary: str = ""
    revision: int = 0
    summary_digest: str = ""
    approved_digest: str = ""
    diagnosis: str = ""
    rejection_reason: str = ""
    prompt_delivered: bool = False

    VALID_PHASES = {
        "new", "awaiting_summary_approval", "approved", "diagnosing",
        "awaiting_diagnosis_confirmation", "awaiting_corrected_summary",
        "awaiting_rejection_reason", "completed",
    }

    @classmethod
    def from_dict(cls, value: dict[str, Any] | None) -> "ApprovalGate":
        if value is None:
            return cls()
        if not isinstance(value, dict):
            raise GateError("Serialized state must be a JSON object")
        allowed = set(cls.__dataclass_fields__)
        if set(value) - allowed:
            raise GateError("State contains unknown fields")
        gate = cls(**value)
        gate.validate_state()
        return gate

    def validate_state(self) -> None:
        if not isinstance(self.phase, str) or not isinstance(self.summary, str):
            raise GateError("State phase and summary must be strings")
        if self.phase not in self.VALID_PHASES:
            raise GateError("State contains an unknown phase")
        if type(self.revision) is not int or self.revision < 0:
            raise GateError("State revision must be a non-negative integer")
        if not all(isinstance(item, str) for item in (self.summary_digest, self.approved_digest, self.diagnosis, self.rejection_reason)):
            raise GateError("State digests and diagnostic fields must be strings")
        if type(self.prompt_delivered) is not bool:
            raise GateError("State delivery flag must be boolean")
        if self.phase == "new":
            if self.revision != 0 or self.summary or self.summary_digest or self.approved_digest or self.prompt_delivered:
                raise GateError("Initial state is inconsistent")
            return
        if not self.summary or self.summary_digest != _digest(self.summary, self.revision):
            raise GateError("State summary digest is inconsistent")
        if self.phase in {"approved", "completed"}:
            if self.approved_digest != self.summary_digest:
                raise GateError("Approved state must match the current summary digest")
        elif self.approved_digest:
            raise GateError("Unapproved state cannot carry an approval digest")
        if self.prompt_delivered != (self.phase == "completed"):
            raise GateError("Prompt delivery flag is inconsistent with phase")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def _set_summary(self, summary: str) -> dict[str, Any]:
        if not isinstance(summary, str) or not summary.strip():
            raise GateError("A non-empty summary is required")
        self.revision += 1
        self.summary = summary
        self.summary_digest = _digest(summary, self.revision)
        self.approved_digest = ""
        self.diagnosis = ""
        self.rejection_reason = ""
        self.prompt_delivered = False
        self.phase = "awaiting_summary_approval"
        return {"revision": self.revision, "digest": self.summary_digest}

    def present_summary(self, summary: str) -> dict[str, Any]:
        if self.phase not in {"new", "awaiting_corrected_summary"}:
            raise GateError(f"Cannot present a summary while phase={self.phase}")
        return self._set_summary(summary)

    def material_change(self, summary: str) -> dict[str, Any]:
        if self.phase not in {"awaiting_summary_approval", "approved"}:
            raise GateError(f"Cannot revise an active summary while phase={self.phase}")
        return self._set_summary(summary)

    def summary_response(self, action: str, digest: str = "", reason: str = "") -> str:
        if self.phase != "awaiting_summary_approval":
            raise GateError("No current summary is awaiting approval")
        if not all(isinstance(item, str) for item in (action, digest, reason)):
            raise GateError("Approval action, digest, and reason must be strings")
        if action == "approve":
            if digest != self.summary_digest:
                raise GateError("Approval must match the exact current summary digest")
            self.approved_digest = digest
            self.phase = "approved"
            return "approved"
        if action == "reject":
            self.approved_digest = ""
            self.rejection_reason = reason.strip()
            self.phase = "diagnosing"
            return "diagnosing"
        if action == "ambiguous":
            return "awaiting_summary_approval"
        raise GateError("Action must be approve, reject, or ambiguous")

    def record_diagnosis(self, diagnosis: str) -> str:
        if self.phase != "diagnosing":
            raise GateError("A diagnosis is not currently expected")
        if not isinstance(diagnosis, str) or not diagnosis.strip():
            raise GateError("Diagnosis must be a non-empty string")
        self.diagnosis = diagnosis
        self.phase = "awaiting_diagnosis_confirmation"
        return self.phase

    def diagnosis_response(self, action: str, explanation: str = "") -> str:
        if self.phase != "awaiting_diagnosis_confirmation":
            raise GateError("No diagnosis is awaiting confirmation")
        if not isinstance(action, str) or not isinstance(explanation, str):
            raise GateError("Diagnosis action and explanation must be strings")
        if action == "confirm":
            self.phase = "awaiting_corrected_summary"
        elif action == "reject":
            supplied = explanation.strip() or self.rejection_reason
            if supplied:
                self.rejection_reason = supplied
                self.diagnosis = ""
                self.phase = "diagnosing"
            else:
                self.phase = "awaiting_rejection_reason"
        elif action != "ambiguous":
            raise GateError("Action must be confirm, reject, or ambiguous")
        return self.phase

    def provide_reason(self, reason: str) -> str:
        if self.phase != "awaiting_rejection_reason":
            raise GateError("A rejection reason is not currently requested")
        if not isinstance(reason, str) or not reason.strip():
            raise GateError("Reason must be a non-empty string")
        self.rejection_reason = reason.strip()
        self.diagnosis = ""
        self.phase = "diagnosing"
        return self.phase

    def deliver_prompt(self, digest: str) -> str:
        if self.phase != "approved" or not self.approved_digest:
            raise GateError("A final prompt requires explicit approval of the current summary")
        if digest != self.summary_digest or digest != self.approved_digest:
            raise GateError("Approved digest does not match the current summary")
        if self.prompt_delivered:
            raise GateError("Final prompt has already been delivered for this state")
        self.prompt_delivered = True
        self.phase = "completed"
        return self.phase

    def apply(self, event: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(event, dict):
            raise GateError("Event must be a JSON object")
        kind = event.get("type")
        if kind == "present_summary":
            result = self.present_summary(event.get("summary", ""))
        elif kind == "material_change":
            result = self.material_change(event.get("summary", ""))
        elif kind == "summary_response":
            result = self.summary_response(event.get("action", ""), event.get("digest", ""), event.get("reason", ""))
        elif kind == "record_diagnosis":
            result = self.record_diagnosis(event.get("diagnosis", ""))
        elif kind == "diagnosis_response":
            result = self.diagnosis_response(event.get("action", ""), event.get("explanation", ""))
        elif kind == "provide_reason":
            result = self.provide_reason(event.get("reason", ""))
        elif kind == "deliver_prompt":
            result = self.deliver_prompt(event.get("digest", ""))
        else:
            raise GateError("Unknown event type")
        return {"result": result, "state": self.to_dict()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--help-state", action="store_true", help="print supported JSON event types")
    args = parser.parse_args()
    if args.help_state:
        print(json.dumps({"events": ["present_summary", "summary_response", "record_diagnosis", "diagnosis_response", "provide_reason", "material_change", "deliver_prompt"], "input": {"state": "optional serialized state", "event": "one event object"}}, ensure_ascii=False))
        return 0
    try:
        request = json.load(sys.stdin)
        gate = ApprovalGate.from_dict(request.get("state"))
        response = gate.apply(request.get("event", {}))
        print(json.dumps(response, ensure_ascii=False))
        return 0
    except (json.JSONDecodeError, AttributeError, GateError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
