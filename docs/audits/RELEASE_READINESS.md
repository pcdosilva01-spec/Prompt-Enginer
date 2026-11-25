# Release readiness

**Decision:** local candidate is usable for review and deterministic tests; **not approved as a public open-source release**.

| Gate | Status | Evidence / next action |
|---|---|---|
| Canonical skill integrity | Passed locally | `MANIFEST.sha256` refreshed after the path correction; final verifier and both versioned ZIP manifests pass. |
| Unit/helper tests | Locally run; exact final count in installation report | Root installer/catalog/integrity tests plus skill helper/package tests. |
| Wheel and source distribution | Open | Local `setuptools`/build backend absent. CI build job is defined but not executed. |
| Python/OS matrix | Open | GitHub Actions configured for Windows/macOS/Linux and Python 3.10/3.12/3.13; no remote run yet. |
| Agent host discovery | Open | Install and verify in each named host/version/surface before describing as tested. |
| Model behavioral evaluation | Open | Run `tests/behavioral_eval_protocol.md` with authorized models, equal conditions, repetitions, and measured outputs. No simulated results. |
| Native symlink/junction checks | Partially open | Windows did not grant link creation privilege; two native tests skipped. Run in CI/host with permission. |
| License and provenance | **Blocking** | Rights holder must choose a license and confirm rights to dossier/research/third-party content. No license file or grant invented. |
| Public GitHub source update | Completed | Candidate source commit `6bcfb75` is on `main`; the 24 November cleanup is a follow-up commit. This is not a GitHub Release. |
| Public metadata/privacy review | Open | The earlier public commit `462cf6a` still contains its original author metadata. No history rewrite was made. |
| Release artifact | Rebuilt local candidate | On 24 November the source ZIP was regenerated with 181 members; archive CRCs and SHA-256 sidecars match, duplicate dossier/history mirrors, `dist/`, and batch files are absent. The skill-only archive is unchanged. This is not a package-index upload or GitHub Release. |

## Release steps after blockers

1. Select and validate the license/provenance.
2. Run all configured CI jobs, including actual symlink tests where supported.
3. Build wheel/sdist and confirm the packaged skill manifest with `tools/check_distribution.py`.
4. Test CLI installation using pipx and manually verify at least one representative host per distinct adapter behavior.
5. Run authorized behavioral experiments and label results by model, version, host, prompt, and date.
6. Review the current public diff and historical metadata; obtain rights clearance before creating a GitHub Release or publishing to a package index.

No timestamped release, package-index upload, or GitHub Release is claimed. The source repository update is recorded above.
