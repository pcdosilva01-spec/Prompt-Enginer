# Índice da skill

Data do snapshot: **23/11/2026**. Abra somente módulos relevantes; o dossiê integral está em `original_dossier/`.

| Assunto | Arquivo | Modelo/família | Plataforma | Categoria/técnicas | Versão/data | Fontes/confiança | Origem |
|---|---|---|---|---|---|---|---|
| Intenção/requisitos/estados | `../workflows/intent_and_requirements.md`, `../workflows/approval_and_correction.md` | Agnóstico | Hosts com contexto de conversa | classificar, resumir, aprovar, corrigir | skill v1; 23/11/2026 | Vol. 5 + 13 testes de helper; alta para transições estruturadas, não validada para LLM | projeto + implementação |
| Modelo | `models/model_adaptation.md` | OpenAI, Anthropic, Google, Mistral, Meta, DeepSeek, Qwen, xAI/outros | API/app separados | prompt por família/versão; CoT, examples, schema | documentação é volátil; consulta ao vivo necessária | Vols. 2/6 + doc oficial atribuída; média/alta documental, sem benchmark novo | dossiê original + módulo |
| Plataforma | `platforms/platform_adaptation.md`, `COMPATIBILITY_MATRIX.md` | Todas as famílias | Codex, Claude Code, Cursor, Gemini CLI, Antigravity, Copilot, Cline, OpenCode, Devin, Windsurf, Roo, genérico | skills, tools, arquivos, permissões | snapshot 23/11/2026; revalidar | S-01–S-15 oficiais; alta para página consultada, nenhuma instalação | pesquisa adicional + Vol. 3 |
| Técnicas | `prompting_techniques/decision_guide.md` | Agnóstico, exceções documentadas | API/chat/agent | formato, few-shot, decomposição, estrutura, tokens, validação | guidance pode mudar por modelo | Vols. 1/2/4/6; média, condicional e sem experimento desta rodada | dossiê original + síntese |
| Tarefa | `task_categories/task_playbook.md` | Agnóstico | Qualquer harness | pesquisa, código, agente, automação, extração, escrita | checklist estável, validar versão de runtime | síntese do dossiê; média, norma de projeto | Vols. 1/4/5 |
| Contexto/ferramentas | `context_engineering/context_and_tools.md` | Agnóstico | Multiplataforma | memória, retrieval, tools, agente | dependente de host | Vols. 1/3/4; alta para separação conceitual, comportamentos pedem fonte atual | dossiê original + síntese |
| Avaliação | `evaluation/prompt_rubric.md` | Agnóstico | Qualquer | prompt text score 0–10 | rubrica interna v1 | critério de projeto explícito; não calibrado em benchmark | implementação |
| Segurança | `security/threat_model.md` | Agnóstico | Ferramentas/extensions | injection, tool action, dados | revisar quando host mudar | Vol. 4 + S-04; orientação oficial/de projeto; não certificação | dossiê + fonte atual |
| Evidência | `evidence/source_policy.md` | Agnóstico | Qualquer | fonte, conflito, validade, data | E1–E5 definidos nesta versão | protocolo interno auditável; aplicação real depende de pesquisa | Vol. 6 + implementação |
| Fontes atuais de plataforma | `evidence/platform_source_ledger.md` | OpenAI, Anthropic, Google, GitHub, Cursor, Cline, OpenCode, Devin, Roo | hosts do escopo | paths, discovery, risco, status | verificação 23/11/2026 | URLs, título, editor, data editorial ou ausência e claim estreito | S-01–S-15 desta implementação |
| Pesquisa integral | `original_dossier/INDICE_GERAL.md` e seis volumes | modelos tratados no original | produtos tratados no original | referências, matrizes, protocolos, auditoria | cópia SHA-256 verificada 23/11/2026 | ledger original E-01–E-34; fontes e limites preservados | dossiê original, 14 arquivos |

**Busca simples:** procure título/termo nos Markdown do pacote. Se o claim é volátil, verifique documentação primária de novo; os registros aqui são snapshot e não promessa de atualização automática.

