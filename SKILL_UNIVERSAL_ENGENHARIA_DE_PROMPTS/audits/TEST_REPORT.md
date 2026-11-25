# Relatório de testes e verificação

**Data:** 23/11/2026. **Ambiente:** Python 3.12.10, Windows/PowerShell. Nenhuma API/modelo, pacote de terceiros ou crédito pago foi usado.

## Resultado da rodada de estabilização

| Verificação | Comando/método | Resultado | Limite |
|---|---|---|---|
| Suíte automatizada | `python -m unittest discover -s tests -v` | **24/24 aprovados**: 18 do gate e 6 do pacote | testa código local determinístico, não aderência de um LLM |
| Dossiê incluído | `python scripts/verify_package.py --source-dossier ..\..\DOSSIER_ENGENHARIA_DE_PROMPTS` | **14/14 arquivos e SHA-256 iguais à fonte atual** | hashes provam identidade, não validade semântica de cada claim |
| Integridade interna | `python scripts/verify_package.py` | PASS: metadados, links internos, hashes de originais e manifesto | verificação local |
| Construção protegida | falha de gravação injetada em teste | PASS: ZIP anterior preservado; temporário limpo | falha simulada por teste determinístico |
| Caminhos simbólicos | dois casos de `is_symlink` simulados em teste | PASS: rejeita entrada e saída simbólicas antes de ler/verificar/substituir | criação de symlink real bloqueada pelo privilégio Windows disponível |
| YAML de skill | regex/checagem estrutural do frontmatter + linhas/tipos esperados de `agents/openai.yaml` | PASS na verificação própria; nome coincide com pasta e limites de descrição respeitados | não foi possível usar parser YAML completo |
| YAML do Codex | conferência manual dos mapas `interface`/`policy`, valores e tipos aparentes; fonte oficial reaberta | compatível documentalmente; não é validação por parser/host | instalação e leitura pela interface não testadas |

## Sincronização e manifestos

Antes da sincronização, três cópias divergiam da fonte: `AUDITORIA_FINAL.md`, `PROTOCOLOS_E_RESULTADOS_DE_TESTES.md` e `RELATORIO_DE_MELHORIAS.md`. As versões anteriores foram preservadas em `work/skill_sync_backup_2026-11-23/`; as cópias internas foram atualizadas da pasta do dossiê, sem alterar a fonte. A comparação posterior passou para os 14 documentos. `ORIGINALS_SHA256.json` e `MANIFEST.sha256` foram regenerados.

## Validação YAML: alternativas verificadas

O ambiente não contém `PyYAML`, `ruamel.yaml`, `strictyaml`, `oyaml`, `ruby`, `yq`, módulo PowerShell YAML ou `YamlDotNet` em cache NuGet. Os módulos globais de Node disponíveis não incluem `yaml`/`js-yaml`, e não havia wheel PyYAML no cache local. O `quick_validate.py` do Skill Creator não iniciou (`ModuleNotFoundError: yaml`). Não foram instaladas dependências. Assim, a validação completa com parser continua pendente; a verificação própria é estrutural/textual e não foi apresentada como parser.

A consulta oficial atual confirma que `SKILL.md` precisa de frontmatter YAML com `name` e `description`, que `agents/openai.yaml` é metadado opcional de interface/política no Codex e lista paths `.agents/skills` para repo/user/admin. `.codex/skills/` não consta na página reaberta. Isso sustenta a atualização documental, não prova que o host carregará este pacote. Ver S-01/S-02 em `IMPLEMENTATION_SOURCE_LEDGER.md`.

## ZIP distribuível

O empacotador escreveu um ZIP temporário e o substituiu somente após passar sua verificação. CRC passou; inventário e hashes foram comparados com a pasta: **57 membros, 0 ausentes, 0 extras, 0 diferenças**. SHA-256: `12F058568D8AB1DE4FDF59E0A070D2CDDC7EAF93820CB663A1C1469C9158FDBB`.

## Testes comportamentais e instalação

- **Não executados:** 10 cenários conversacionais e 29 casos D-01–G-06; permanecem protocolo e resultados esperados, não resultados observados.
- **Não executados:** instalação ou invocação em Codex, Claude Code, Gemini CLI, Antigravity, Cursor, Copilot, Cline, OpenCode, Devin ou outro host.
- **Sem acesso/autoridade:** não foi identificado endpoint ou modelo local autorizado; não houve consumo de crédito.
- O helper não interpreta respostas em linguagem natural, não autentica JSON serializado e só valida a transição estruturada quando o host o invoca.

## Reprodutibilidade

Na pasta `universal-prompt-engineering`, com Python 3.10+:

```powershell
python scripts/build_original_manifest.py --source ..\..\DOSSIER_ENGENHARIA_DE_PROMPTS
python scripts/build_manifest.py
python -m unittest discover -s tests -v
python scripts/verify_package.py --source-dossier ..\..\DOSSIER_ENGENHARIA_DE_PROMPTS
python scripts/package_skill.py
```

O último comando constrói em temporário, verifica CRC/inventário/SHA-256 e só então substitui atomicamente o ZIP existente. Para avaliação comportamental, usar `tests/behavioral_eval_protocol.md` e registrar todos os casos, inclusive falhas e inconclusivos.
