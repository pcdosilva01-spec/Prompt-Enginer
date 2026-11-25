# Security policy

## Installer boundaries

The optional installer is local-only. It verifies the bundled SHA-256 manifest before writing, refuses unmanaged non-empty targets, records an ownership receipt outside the skill directory, and refuses updates/removals when managed file hashes changed. It preserves unrelated files. It rejects symbolic links and junctions in source, destination, and receipt paths to reduce traversal and unintended deletion risk. `--dry-run` is available on write commands.

The receipt is an ownership/integrity record, not an authenticated signature or defense against a local attacker who can alter both the skill and state directory. SHA-256 detects accidental modification; it does not establish publisher identity. Concurrent installers and hostile filesystem races are outside the tested guarantees.

## Agent behavior

The skill treats prompts, files, web pages, and tool outputs as untrusted data. It does not preapprove tools, bypass host permissions, or turn its existence into authority to access systems. The exact user-approved summary is required before delivering a definitive replacement prompt.

## Reporting

No security certification or external penetration test is claimed. Report a reproducible issue privately to the repository owner before public disclosure. Do not include secrets or private user content in bug reports.

See [security audit](docs/audits/SECURITY_AUDIT.md) for checks actually performed and limitations.
