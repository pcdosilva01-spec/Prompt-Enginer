# Contributing

## Scope

Keep the canonical skill under `src/upe/resources/skill/universal-prompt-engineering/`. Keep source research, evidence, and audit records separate from host-specific installation logic. Do not update original dossier copies or legacy snapshots in place; add a dated correction or new version and retain hashes for preserved source material.

## Evidence changes

For volatile platform/model claims, record the exact URL, page title/publisher, publication/update date when visible, verification date, supported claim, and limitation in the relevant ledger. Prefer primary documentation. A vendor recommendation is not independent comparative evidence. Mark a test as pending unless it was run, with inputs and results recorded.

## Code changes

- Keep runtime dependencies at zero unless a specific need and approval are documented.
- Add regression coverage for installer safety, path handling, integrity checks, and CLI behavior.
- Do not weaken no-overwrite, user-edit preservation, receipt, or symlink/junction protections.
- Test using temporary directories; never test uninstall against a real user skills directory.
- Keep the required summary/explicit-approval workflow in the skill intact.

## Checks

```console
python -m compileall -q src tests
python -m unittest discover -s tests -v
python -m unittest discover -s src/upe/resources/skill/universal-prompt-engineering/tests -v
python -m upe doctor
```

Build checks additionally need the declared build backend; CI installs it on the runner. No release should be published until licensing, rights review, artifact verification, and the release checklist are complete.
