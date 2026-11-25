# Índice de conhecimento

Data do levantamento desta implementação: **23/11/2026**. O dossiê original contém pesquisa extensa e continua sendo a fonte arquivística completa; módulos abaixo são sínteses de uso, não substitutos destrutivos. Use links relativos a partir deste arquivo.

| Assunto | Arquivo | Modelos/famílias | Plataformas | Tarefas/técnicas | Versão/data | Fontes e confiança | Origem |
|---|---|---|---|---|---|---|---|
| Fluxo e princípios | `universal-prompt-engineering/references/foundations/operating_model.md` | Agnóstico | Todos | classificar intenção, requisito, evidência | Revisado 23/11/2026 | especificação do usuário + síntese do dossiê; média/alta | Vols. 1, 5 |
| Adaptação por modelo | `universal-prompt-engineering/references/models/model_adaptation.md` | OpenAI, Anthropic, Google, Mistral, outros | API vs app separados | contexto, exemplos, raciocínio, schema | Sempre verificar versão ao vivo | docs primários + dossiê; variável | Vols. 2, 6 |
| Adaptação de host | `universal-prompt-engineering/references/platforms/platform_adaptation.md` | Qualquer fornecedor | Codex, Claude Code, Cursor, Gemini CLI, Antigravity, Copilot, Cline, OpenCode, Devin Local, Roo | arquivos, tools, permissões | Snapshot 23/11/2026 | fontes oficiais no módulo e matriz | Vols. 3, 6 |
| Técnicas | `universal-prompt-engineering/references/prompting_techniques/decision_guide.md` | Agnóstico com ressalvas por provedor | API e produto | contexto, estrutura, demonstrações, saída | Atualizar guidance | docs e estudos no Volume 6; conclusão condicional | Vols. 1, 2, 4, 6 |
| Categorias de tarefa | `universal-prompt-engineering/references/task_categories/task_playbook.md` | Agnóstico | Chat, pesquisa, programação, agentes, automação | seleção de estrutura e validação | Estável como checklist; produto volátil | síntese técnica do dossiê | Vols. 1, 4, 5 |
| Contexto e ferramentas | `universal-prompt-engineering/references/context_engineering/context_and_tools.md` | Agnóstico | harnesses diversos | retrieval, memória, tool use, limites | Revalidar por produto | documentação de fornecedor + dossiê | Vols. 1, 3, 4 |
| Avaliação | `universal-prompt-engineering/references/evaluation/prompt_rubric.md` | Agnóstico | Variantes testadas | rubric 0–10, teste, custo | Rubrica de projeto | critério interno explícito; não benchmark | Vols. 4, 5 |
| Segurança | `universal-prompt-engineering/references/security/threat_model.md` | Agnóstico | ferramentas e extensões | injeção, permissões, dados | Revalidar antes de usar ferramentas | docs OpenAI Skills + dossiê | Vols. 1, 4, 6 |
| Evidência | `universal-prompt-engineering/references/evidence/source_policy.md` | Agnóstico | Qualquer | modo de fonte, atualidade, conflitos | Snapshot 23/11/2026 | regra de evidência auditável | Volume 6 |
| Aprovação | `universal-prompt-engineering/workflows/approval_and_correction.md` | Agnóstico | Dependente da sessão | resumo, aprovação, rejeição, correção | Spec v1 | fluxo especificado; script testa transições | Vol. 5 + requirements |
| Originais integrais | `universal-prompt-engineering/references/original_dossier/INDICE_GERAL.md` | Diversos | Diversas | pesquisa integral e fontes | Arquivos copiados 23/11/2026 | SHA-256 local | Dossiê original, 14 arquivos |

## Procedimento de busca local

1. Procure a tarefa ou plataforma nesta tabela e abra somente o módulo indicado.
2. Nesse módulo, siga as referências cruzadas ao volume e seção original pertinentes.
3. Se o claim for de produto/versão atual, confirme a fonte oficial online na data da tarefa; este snapshot não substitui consulta atual.
4. Se a documentação não responder, registre “não verificado”; não infira capacidade.

Buscas simples: PowerShell `Select-String -Path 'universal-prompt-engineering/references/**/*.md' -Pattern 'termo'`; Python: `pathlib.Path(...).rglob('*.md')`. Busca semântica externa é opcional, não necessária para localizar a base.
