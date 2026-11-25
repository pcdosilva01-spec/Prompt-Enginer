# Matriz de rastreabilidade da implementação

Estados: **Implementado e verificado** (artefato + verificação concreta), **Implementado parcialmente**, **Documentado, mas não testado**, **Bloqueado por limitação externa**, **Não implementado**. `T-Axx` = testes de estado; `T-Pxx` = testes de pacote; inferência em LLM/instalação real não está coberta por esses testes.

## Requisitos do projeto (seções 1–36 do pedido)

| ID | Requisito | Fonte | Implementação | Teste/evidência | Estado |
|---|---|---|---|---|---|
| G-01 | Identidade e capacidades da skill | Prompt anexado §1 | `universal-prompt-engineering/SKILL.md` | T-P01 metadata | Implementado e verificado |
| G-02 | Contexto e legado do dossiê | §2 | `references/original_dossier/` | T-P02; hashes 14/14 | Implementado e verificado |
| G-03 | Localização/estrutura modular | §3–5 | árvore da skill + README | inventário e verificação de paths | Implementado e verificado |
| G-04 | Preservação documental integral | §4 | original_dossier 14 arquivos | SHA-256 comparado com origem | Implementado e verificado |
| G-05 | Índice progressivo por metadados | §4.4, §21 | `references/KNOWLEDGE_INDEX.md` | T-P03 internal-link check | Implementado e verificado |
| G-06 | Compatibilidade por host documentada | §6 | `references/COMPATIBILITY_MATRIX.md`, adapters | fonte oficial S-01–S-15; sem instalação | Implementado parcialmente |
| G-07 | Analisar intenção e requisitos | §7 | `workflows/intent_and_requirements.md` | cenários 1,7,10; sem LLM | Documentado, mas não testado |
| G-08 | Resumo antes de prompt final | §8 | SKILL + template + gate | T-A01,A02,A11 | Implementado e verificado (estado estruturado) |
| G-09 | Diagnosticar rejeição e pedir confirmação | §9 | `approval_and_correction.md`, template | T-A05–A08 | Implementado e verificado (estado estruturado) |
| G-10 | Contexto conversacional sem alegar memória persistente | §10 | SKILL + workflow | review textual; sem teste de host | Documentado, mas não testado |
| G-11 | Máquina de estados, digest/revisão e entradas inválidas | §11 | `scripts/approval_gate.py` | 18 testes unitários do gate, incluindo tipos inválidos | Implementado e verificado para eventos estruturados |
| G-12 | Seis modos de fonte | §12 | `references/evidence/source_policy.md` | coverage documental | Implementado parcialmente; modo externo depende de acesso |
| G-13 | Inteligência por modelo/versão | §13 | `references/models/model_adaptation.md`, original V2/V6 | fontes atuais dependem da solicitação | Implementado parcialmente |
| G-14 | Inteligência por plataforma | §14 | module, matrix, adapters | 11 fontes oficiais abertas; host não instalado | Implementado parcialmente |
| G-15 | Motor proporcional de construção | §15 | decision guide + generation workflow | não houve teste de inferência | Documentado, mas não testado |
| G-16 | Diagnóstico de erro de prompt | §16 | error diagnosis template + task playbook | cenários especificados | Documentado, mas não testado |
| G-17 | Autoavaliação 0–10 ponderada | §17 | `prompt_rubric.md`, template | soma pesos=100, análise estática | Implementado e verificado metodologicamente |
| G-18 | Revisão de prompt existente | §18 | SKILL, approval and correction | sem prova behavioral LLM | Documentado, mas não testado |
| G-19 | Formatos de entrega diversos | §19 | task playbook + templates | inspeção de conteúdo | Implementado parcialmente |
| G-20 | Entrega final após aprovação | §20 | workflow delivery + gate | T-A01–A04 | Implementado e verificado em helper; agente real não testado |
| G-21 | Recuperação progressiva | §21 | Knowledge index + routing | T-P internal links/manifest | Implementado e verificado |
| G-22 | Hierarquia e injection | §22 | threat model + SKILL | revisão documental; sem red-team LLM | Implementado parcialmente |
| G-23 | Manutenção e atualização de fonte | §23 | source policy + install docs + ledger | processo documentado | Documentado, mas não testado em atualização futura |
| G-24 | Implementação de componentes e manifesto | §24 | pacote + scripts + manifest | verificação de origem, manifesto, symlink e ZIP atômico | Implementado e verificado |
| G-25 | Testes A–G | §25 | tests + 10 scenarios | 24 testes Python; sem validação behavioral de modelo | Implementado parcialmente |
| G-26 | Dez cenários conversacionais | §26 | `examples/10_conversation_scenarios.md` | casos especificados e cruzados com estados | Documentado, mas não testado em LLM |
| G-27 | Traceability | §27 | esta matriz + coverage matrix | links e check IDs | Implementado e verificado documentalmente |
| G-28 | Auditoria crítica independente | §28 | security/test/eval reports | autoría interna; sem terceiro independente | Implementado parcialmente |
| G-29 | Sistema de notas A–J | §29 | `FINAL_EVALUATION.md` | contas recalculadas na auditoria | Implementado e verificado aritmeticamente |
| G-30 | Fases de execução | §30 | report e changelog | entregáveis e verificação | Implementado e verificado |
| G-31 | Critérios de aceitação | §31 | coverage + test report | requisitos pendentes explicitados | Implementado parcialmente |
| G-32 | Proibições absolutas | §32 | SKILL + security + reports | hash/pending tests/provenance | Implementado parcialmente; aderência comportamental do agente pendente |
| G-33 | Entregáveis finais e package zip | §33 | pacote + ZIP sibling | ZIP integrity/extraction/hash | Implementado e verificado |
| G-34 | Exemplo de interação end-to-end | §34 | cenário 3 + exemplo no report | apenas especificação, não inferência real | Documentado, mas não testado |
| G-35 | excelência com preservação | §35 | camadas + hash inventory | preserved originals + selected modules | Implementado e verificado documentalmente |
| G-36 | execução, correção e transparência | §36 | report, audit, tests | estados e limites explicitados | Implementado parcialmente |

## 24 requisitos históricos do dossiê

| ID | Requisito original | Arquivo consumido | Implementação nesta skill | Estado |
|---|---|---|---|---|
| R-01 | Separar modelo, API, app, harness e ferramenta | V1 §§3–4 | operating model; adapters | Implementado e verificado documentalmente |
| R-02 | Comparar modelos sem universalizar guidance | V2; V6 §2 | model adaptation + evidence policy | Implementado e verificado documentalmente |
| R-03 | IDs/estado temporal de modelos | V2 | snapshot + atualização on-demand | Implementado parcialmente |
| R-04 | Distinguir ChatGPT/Work/Codex | V3 §2 | OpenAI adapter/matrix | Documentado, sem teste em produto |
| R-05 | Claude Code regras/agentes/permissões | V3 §§2–4 | Anthropic adapter + official docs | Implementado documentalmente |
| R-06 | Antigravity e Gemini CLI separados | V3 §2 | Google adapter + matrix | Implementado documentalmente |
| R-07 | Cursor rules e enforcement | V3 §2.1; V6 E-14 | platform model separates context/enforcement | Implementado documentalmente |
| R-08 | Copilot varia por cliente | V3 §2 | coding agent adapter + official matrix | Implementado documentalmente |
| R-09 | Gemini CLI separado da API | V3 §2 | model/platform split, Google adapter | Implementado documentalmente |
| R-10 | Aider | V3 §2 | generic adapter; no native claims | Implementado parcialmente |
| R-11 | Cline | V3 §2 | coding adapter + docs | Implementado documentalmente |
| R-12 | Roo status | V3 §2 | ended/legacy, no operational adapter | Implementado documentalmente |
| R-13 | OpenCode V2/permissões | V3 §2 | coding adapter, separate runtime policy | Implementado parcialmente; no V2 schema deep dive |
| R-14 | Windsurf sem inferir de redirect | V3 §2.1 | explicit redirect caveat and no Cascade claim | Implementado e verificado documentalmente |
| R-15 | comprimento/rigidez | V2 §4; V4 §3 | evidence-bounded decision guide | Implementado; no comparative inference test |
| R-16 | Markdown/XML/JSON/schema | V2 §4; V4 §1 | conditional format table | Implementado documentalmente |
| R-17 | exemplos/persona/raciocínio | V1/V2/V6 | conditional guidance; no private CoT request | Implementado documentalmente |
| R-18 | tools/agentes/memória/segurança | V1/V3/V4 | context and threat modules | Implementado documentalmente |
| R-19 | reprodutibilidade sem fabricação | V4 | protocol and honest state report | Implementado documentalmente |
| R-20 | fonte title/origin/date/claim | V6 | source ledger S + original E refs | Implementado e verificado documentalmente |
| R-21 | achado/resolução | gap register | G/R matrix + reports | Implementado documentalmente |
| R-22 | avaliações separadas e ponderadas | final evaluation | separate research/dossier/audit + A–J | Implementado e verificado aritmeticamente |
| R-23 | auditoria crítica/transparente | audit final | self-audit with no external independence claim | Implementado parcialmente |
| R-24 | preparar skill mantendo base original | V5 | actual skill + exact preserved dossier | Implementado e verificado |

