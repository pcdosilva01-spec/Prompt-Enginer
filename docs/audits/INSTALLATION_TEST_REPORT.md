# Installation and test report

**Environment:** Windows, Python 3.12.10, 23 November 2026. All file-operation tests use temporary directories under the test runner. No real user skill directory, host application, model endpoint, API key, or paid service was used.

## Tests actually executed

The repository-level suite was run with:

```console
python -m compileall -q src tests
python -m unittest discover -s tests -v
```

It covered CLI help/version/catalog output, each supported user/project path, manual-only rejection, frontmatter and required bundle content, manifest tamper/missing/unlisted/traversal cases, install, idempotence, dry-run, ownership receipt, update, user modification conflicts, safe uninstall, release ZIP creation/hash/no-overwrite/failure cleanup, dossier copy hashes, and path spaces. Result: **30 tests, 28 passed, 2 skipped, 0 failed**. The two skips are the Windows native directory-symlink tests described below.

The skill's own helper/package suite is separate:

```console
python -m unittest discover -s src/upe/resources/skill/universal-prompt-engineering/tests -v
```

These deterministic tests validate package/helper behavior; they do not validate an AI following the skill. See the existing `tests/behavioral_eval_protocol.md` for model/host experiments, which were not executed.

Result: **24 tests passed, 0 skipped, 0 failed**.

Together, the two local suites ran **54 tests: 52 passed, 2 skipped, 0 failed**. The compile check also exited successfully. A separate read-only scan checked 168 Markdown files for relative links; it found zero broken or escaping local links.

The installed-from-source CLI entry path was also exercised with `PYTHONPATH=src`: `version` reported `0.1.0a2`, `list-targets` enumerated the nine documented filesystem destinations and manual-only surfaces, and `doctor` reported the bundled skill **PASS (56 files checked)**. It detected `codex` and `copilot` executables on `PATH`; that is only executable detection, not proof that either host client loaded the skill.

## Environment limitations observed

- The two tests that create real Windows directory symbolic links were skipped: the environment returned Windows error 1314 (required privilege unavailable). No privilege escalation was attempted.
- `pipx` and `setuptools` are not installed in the local Python environment. No packages were installed to make the test pass. A wheel/sdist build and pipx installation are pending.
- Host applications and model APIs were not invoked. No claim of target discovery, skill activation, model adaptation quality, latency, or token cost is made.
- The GitHub Actions workflow is configured but has not run; its cross-platform matrix is a planned check, not a result.

## Result

Only outputs from the commands actually run are classified as local test results. Dry-run tests check for absence of filesystem changes. Model evaluations and cross-host protocols remain pending rather than simulated.
