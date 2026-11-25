# Knowledge selection workflow

Load the [surface-specific catalog](../references/models/catalog.md) only for model facts. For human-facing PT-BR output, load the [editorial block](../references/writing/humanizer.md) appropriate to recipient access. Keep the catalog and historical dossier outside the recipient prompt.

1. Read the user's requested evidence mode; default to local knowledge unless current facts materially matter or the user asks for current research.
2. Search `../references/KNOWLEDGE_INDEX.md`; choose one or a few modules. Use `../references/original_dossier/INDICE_GERAL.md` to locate detailed evidence without loading all volumes.
3. For volatile model/platform facts, query current primary docs if network and authorization are available. Check title, publisher, date/version, URL, access date and claim; open redirects and record limits.
4. Separate vendor guidance, scientific result, local experiment, inference and hypothesis. If sources conflict, preserve both and delimit applicability.
5. For unknown product/version, use a generic baseline or ask if the target materially changes the design. Do not fabricate an adapter.
6. Report missing access, outdated snapshot, paywall, unverified account/plan, and unexecuted tests explicitly.

Modes and source quality: `../references/evidence/source_policy.md`.

For editorial dependencies, use [skill routing](skill_routing.md); do not load Humanizer for unrelated outputs.
