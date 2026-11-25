# Knowledge integrity report

**Checked:** 23 November 2026, with a repository-cleanup addendum on 24 November 2026. The skill bundle contains research modules and the original dossier; this report distinguishes content preservation from freshness of claims.

## Preservation and structure

- The canonical skill tree contains `SKILL.md`, templates, workflows, host adapters, model/technique/task/context/evaluation/security/evidence references, scripts, and tests.
- The complete 14-file dossier is bundled under `references/original_dossier/`; `ORIGINALS_SHA256.json` records per-file hashes. The preserved source is `DOSSIER_ENGENHARIA_DE_PROMPTS/` at the repository root. A redundant documentation copy was removed in the 24 November 2026 repository cleanup.
- The SHA-256 manifest for the canonical skill covers all non-cache content files. The verifier detects changed, missing, unlisted, path-traversing, duplicate, or broken internal-link entries.
- The top-level `DOSSIER_ENGENHARIA_DE_PROMPTS/`, `SKILL_UNIVERSAL_ENGENHARIA_DE_PROMPTS/`, and root ZIP are retained as immutable legacy snapshots. The root ZIP is not asserted to equal the updated canonical package.
- Model/provider claims and platform capability claims are treated as dated snapshots. Current platform evidence is supplemented in `docs/research/PLATFORM_RESEARCH_SNAPSHOT.md`; the individual model/version snapshot in the preserved dossier is not silently rewritten.

## Verification procedure

Run `upe-skill doctor` to verify the packaged skill. It uses SHA-256 and structural frontmatter checks. A full YAML parse is performed only when PyYAML happens to be installed; PyYAML is not a runtime dependency. The locally observed environment lacked the optional parser, so this run used structural validation. Original dossier hashes and full archive-member hashes are checked separately in the release report.

## Limits

Integrity does not imply factual truth, external-source availability, an academic replication, or a verified current model version. Live claims must be rechecked at task time. Changes to the original dossier are not made in place: corrections belong in a dated addendum or new version with source and hash records.

## 24 November cleanup addendum

The duplicate `docs/research/DOSSIER_ENGENHARIA_DE_PROMPTS/` mirror was removed after all 14 files were confirmed byte-identical to the preserved root dossier. The 14-file copy inside the canonical skill remains because the installed skill must carry its own research references; its SHA-256 manifest remains the integrity check. The root dossier and root legacy skill snapshots were preserved unchanged.
