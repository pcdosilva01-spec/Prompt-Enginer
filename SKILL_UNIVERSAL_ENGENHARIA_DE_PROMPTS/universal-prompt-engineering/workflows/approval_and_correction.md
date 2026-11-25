# Approval and correction workflow

## State flow

`REQUEST → INTENT → REQUIREMENTS → SUMMARY_PRESENTED/AWAITING_APPROVAL → (APPROVED → KNOWLEDGE → BUILD → REVIEW → DELIVERY) or (REJECTED → DIAGNOSIS → DIAGNOSIS_CONFIRMATION → CORRECTION/REASON → REVISED_SUMMARY → AWAITING_APPROVAL)`.

The system is fail-closed: no final prompt in any state except explicit approval of the current summary. An ambiguous answer remains pending. A material change increments the revision and clears approval. Approval is for the summary content and scope, not for permission to perform unrelated external actions.

## Agent procedure

1. Present `../templates/understanding_summary.md` with proportional detail and a clear confirmation question.
2. Accept approval only when the user's reply clearly approves the current summary in context. Do not interpret silence or mere continuation as approval. If there are conflicting parts, ask one narrow disambiguating question.
3. On rejection, create `../templates/error_diagnosis.md`; cite the earlier requirement and separate confirmed/probable/possible/unresolved findings. Ask whether the diagnosis captures the error.
4. If the user rejects diagnosis, check whether they already gave the reason. If yes, use it without a redundant request; otherwise ask for the missing reason. Then revise diagnosis and summary.
5. Any material change to task, target, mandatory requirements, constraints, or output requires a new summary and approval. Cosmetic formatting changes that cannot affect the prompt may preserve approval; state why.
6. If a structured gate helper is available, pass explicit events to `../scripts/approval_gate.py`/`ApprovalGate`. It only enforces defined transitions over structured input; the agent remains responsible for correctly mapping user language and maintaining state.

## Resumption and failure

Carry state in the accessible conversation. Do not claim persistence across sessions. If the host loses context or the approved digest/revision cannot be verified, present the summary again. If a required confirmation is missing, wait and do not draft the final prompt.
