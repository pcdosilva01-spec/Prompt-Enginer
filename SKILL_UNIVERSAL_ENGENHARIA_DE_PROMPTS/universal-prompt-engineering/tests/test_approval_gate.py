import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from approval_gate import ApprovalGate, GateError


class ApprovalGateTests(unittest.TestCase):
    def setUp(self):
        self.gate = ApprovalGate()
        self.gate.present_summary("Criar prompt de análise para Codex")

    def test_no_final_before_approval(self):
        with self.assertRaises(GateError):
            self.gate.deliver_prompt(self.gate.summary_digest)

    def test_ambiguous_response_keeps_gate_closed(self):
        self.gate.summary_response("ambiguous")
        self.assertEqual(self.gate.phase, "awaiting_summary_approval")
        with self.assertRaises(GateError):
            self.gate.deliver_prompt(self.gate.summary_digest)

    def test_approval_requires_current_digest(self):
        with self.assertRaises(GateError):
            self.gate.summary_response("approve", "old-digest")
        self.assertEqual(self.gate.phase, "awaiting_summary_approval")

    def test_explicit_approval_allows_one_delivery(self):
        digest = self.gate.summary_digest
        self.gate.summary_response("approve", digest)
        self.assertEqual(self.gate.deliver_prompt(digest), "completed")
        with self.assertRaises(GateError):
            self.gate.deliver_prompt(digest)

    def test_rejection_enters_diagnosis_not_delivery(self):
        self.gate.summary_response("reject", reason="Escopo empresarial")
        self.assertEqual(self.gate.phase, "diagnosing")
        with self.assertRaises(GateError):
            self.gate.deliver_prompt(self.gate.summary_digest)

    def test_diagnosis_requires_confirmation(self):
        self.gate.summary_response("reject")
        self.gate.record_diagnosis("Confundi cliente com empresa")
        self.assertEqual(self.gate.phase, "awaiting_diagnosis_confirmation")
        self.gate.diagnosis_response("confirm")
        self.assertEqual(self.gate.phase, "awaiting_corrected_summary")

    def test_rejected_diagnosis_uses_existing_reason_without_reasking(self):
        self.gate.summary_response("reject", reason="Você ignorou o anexo")
        self.gate.record_diagnosis("Talvez falte especificar o escopo")
        self.gate.diagnosis_response("reject")
        self.assertEqual(self.gate.phase, "diagnosing")
        self.assertEqual(self.gate.rejection_reason, "Você ignorou o anexo")

    def test_rejected_diagnosis_without_reason_waits_for_reason(self):
        self.gate.summary_response("reject")
        self.gate.record_diagnosis("Hipótese de omissão")
        self.gate.diagnosis_response("reject")
        self.assertEqual(self.gate.phase, "awaiting_rejection_reason")
        self.gate.provide_reason("O alvo era outro modelo")
        self.assertEqual(self.gate.phase, "diagnosing")

    def test_corrected_summary_requires_new_approval(self):
        self.gate.summary_response("reject")
        self.gate.record_diagnosis("Objetivo errado")
        self.gate.diagnosis_response("confirm")
        old = self.gate.summary_digest
        self.gate.present_summary("Criar prompt de gestão financeira empresarial")
        self.assertNotEqual(old, self.gate.summary_digest)
        self.assertEqual(self.gate.phase, "awaiting_summary_approval")
        with self.assertRaises(GateError):
            self.gate.deliver_prompt(self.gate.summary_digest)

    def test_material_change_invalidates_approval(self):
        self.gate.summary_response("approve", self.gate.summary_digest)
        self.gate.material_change("Prompt para plataforma diferente")
        self.assertEqual(self.gate.phase, "awaiting_summary_approval")
        self.assertFalse(self.gate.approved_digest)
        with self.assertRaises(GateError):
            self.gate.deliver_prompt(self.gate.summary_digest)

    def test_old_digest_cannot_unlock_new_summary(self):
        old = self.gate.summary_digest
        self.gate.material_change("Novo escopo material")
        with self.assertRaises(GateError):
            self.gate.summary_response("approve", old)

    def test_material_change_cannot_skip_diagnosis_confirmation(self):
        self.gate.summary_response("reject")
        self.gate.record_diagnosis("Interpretei mal o escopo")
        with self.assertRaises(GateError):
            self.gate.material_change("Resumo corrigido sem confirmar diagnóstico")

    def test_serialized_state_rejects_stale_or_inconsistent_digest(self):
        state = self.gate.to_dict()
        state["summary_digest"] = "stale"
        with self.assertRaises(GateError):
            ApprovalGate.from_dict(state)

    def test_from_dict_rejects_falsey_non_object_state(self):
        for invalid_state in ([], "", False):
            with self.subTest(state=invalid_state):
                with self.assertRaises(GateError):
                    ApprovalGate.from_dict(invalid_state)

    def test_apply_rejects_non_object_event(self):
        for invalid_event in (None, []):
            with self.subTest(event=invalid_event):
                with self.assertRaises(GateError):
                    self.gate.apply(invalid_event)

    def test_diagnosis_fields_reject_non_string_values(self):
        with self.assertRaises(GateError):
            self.gate.record_diagnosis(123)

        self.gate.summary_response("reject")
        with self.assertRaises(GateError):
            self.gate.record_diagnosis("Objetivo incorreto")
            self.gate.diagnosis_response("reject", explanation=123)

    def test_rejection_reason_rejects_non_string_value(self):
        with self.assertRaises(GateError):
            self.gate.summary_response("reject", reason=123)

    def test_provide_reason_rejects_non_string_value(self):
        self.gate.summary_response("reject")
        self.gate.record_diagnosis("Diagnóstico inicial")
        self.gate.diagnosis_response("reject")
        with self.assertRaises(GateError):
            self.gate.provide_reason(123)


if __name__ == "__main__":
    unittest.main()
