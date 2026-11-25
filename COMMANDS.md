# CLI reference

The executable is `upe-skill`; running `python -m upe` is supported after installation or when `src` is on `PYTHONPATH`.

| Command | Purpose | Writes files? |
|---|---|---:|
| `help` / `--help` | Show implemented commands | No |
| `version` | Print CLI version | No |
| `list-targets` | List target paths and evidence/lifecycle notes | No |
| `doctor [--target ID]` | Verify bundled content, report detected CLI executables, optionally resolve a path | No |
| `install ID` | Install verified bundled skill if the target is empty or absent | Yes, unless `--dry-run` |
| `update ID` | Update an installation whose receipt and installed hashes still match | Yes, unless `--dry-run` |
| `verify ID` | Check the installed files against the ownership receipt | No |
| `uninstall ID` | Remove unchanged files owned by this installer | Yes, unless `--dry-run` |

`ID` accepts a catalog entry from `list-targets`. `--scope user` is the default. Use `--scope project --project-dir PATH` for an existing project. `--dry-run` prints the proposed result without filesystem changes. ChatGPT Web is manual-only and cannot be passed to filesystem operations. Roo Code's path is marked legacy because the original product shut down and its repository is archived.

The CLI detects executable names on `PATH` only; that does not prove a client is installed correctly, recognizes skills, or will activate one. It does not launch AI clients, call a model, or run paid APIs.

Exit codes: `0` successful command/verification; `1` failed skill or installation verification; `2` invalid target, unsafe path, ownership conflict, or operation error. Argparse uses its standard nonzero code for malformed command syntax.
