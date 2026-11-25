# Intent and requirements workflow

**Input:** user request plus accessible conversational context. **Output:** classified intent and a requirement ledger, not a final prompt.

1. Classify intent and whether the requested response would include a new/re-written definitive prompt.
2. Extract objective, task, target model/version, platform/surface, result, context, mandatory requirements, preferences, restrictions, output format, tools, evidence mode, privacy/risk and acceptance criteria.
3. Mark each entry `user-stated`, `inferred`, `unknown`, or `conflicting`; preserve corrections from earlier turns.
4. Ask only material unresolved questions. If no question is essential, state minimal assumptions in the proposed summary.
5. For diagnostics that don't produce a rewritten prompt, report findings and offer next steps without triggering the approval gate for final generation.
6. For a final or rewritten prompt, proceed to `approval_and_correction.md` and stop before drafting until approval.

Template: `../templates/understanding_summary.md`.
