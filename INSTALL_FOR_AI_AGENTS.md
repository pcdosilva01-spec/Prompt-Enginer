# Instructions for AI coding agents

This guide applies to the source candidate in the [GitHub repository](https://github.com/pcdosilva01-spec/Prompt-Enginer). Publication of source files does not prove host discovery, model behavior, or a packaged release.

## Purpose and source

Start with the canonical [SKILL.md](src/upe/resources/skill/universal-prompt-engineering/SKILL.md), consult the [knowledge index](src/upe/resources/skill/universal-prompt-engineering/references/KNOWLEDGE_INDEX.md), and load only the references relevant to the task.

Canonical skill: `src/upe/resources/skill/universal-prompt-engineering/`. It is a portable Agent Skills folder with `SKILL.md`, progressive references, workflows, templates, adapters, and deterministic helper tests. Read `README.md`, `COMPATIBILITY.md`, and `SECURITY.md` before recommending installation. For exact official support paths, follow the host's linked docs.

## Safe workflow

1. Confirm the user's target host, specific surface, version, and whether the requested scope is user or project. Do not infer that a connected web app supports local filesystem skills.
2. Explain the proposed destination and whether it is user-wide or repository-specific. Project installation changes repository content; user installation changes the user's profile.
3. Run `upe-skill doctor` and `upe-skill list-targets` if the CLI is installed. Resolve a project target only from an existing, explicitly selected project directory.
4. Show the dry-run command and resulting path. Do not use `--dry-run` as evidence that anything was installed.
5. Proceed with a write only when the user requested installation or explicitly approved the stated operation. Never force-overwrite a preexisting skill, bypass a trust prompt, preapprove tools, or delete a user-modified file.
6. After installation, run `upe-skill verify <target>` and separately check the host's own skill list/discovery UI. Keep these as two distinct results.
7. For a behavioral check, use a low-risk request and inspect the numbered summary, explicit approval, and full delivery checkpoints. The optional local helper must be called by the host to enforce its structured transitions. In other hosts use the conversational fallback. Paid model calls require authorization.

Example preview for a Codex user install:

```console
upe-skill install codex --scope user --dry-run
```

Only after approval and destination review, perform the same command without `--dry-run`. For project scope, specify `--scope project --project-dir PATH`.

## Publication and links

The canonical source path is [`src/upe/resources/skill/universal-prompt-engineering/SKILL.md`](https://github.com/pcdosilva01-spec/Prompt-Enginer/blob/master/src/upe/resources/skill/universal-prompt-engineering/SKILL.md). Verify the current commit and host-specific discovery rules before sharing installation claims.
