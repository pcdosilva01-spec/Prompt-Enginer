# Volume 6 — Auditoria, matrizes e referências

## 1. Registro de evidências

| ID | Afirmação resumida | Fonte primária / estudo | Classificação | Limite |
|---|---|---|---|---|
| E-01 | Instrução clara, contexto e saída desejada são recomendados | [OpenAI prompt guide](https://developers.openai.com/api/docs/guides/prompt-engineering) | Confirmada como recomendação oficial | Não prova ganho universal |
| E-02 | Pedir CoT pode ser desnecessário ou contraproducente para alguns reasoning models OpenAI atuais | [OpenAI reasoning guide](https://developers.openai.com/api/docs/guides/reasoning-best-practices) | Confirmada para a família/configuração coberta pelo guia | Não generalizar a outras linhas |
| E-03 | CoT few-shot elevou desempenho em tarefas/modelos antigos avaliados | [Wei et al. 2022](https://arxiv.org/abs/2201.11903) | Experimental | Resultados específicos; transferibilidade atual incerta |
| E-04 | Self-consistency ajudou benchmarks selecionados | [Wang et al. 2022](https://arxiv.org/abs/2203.11171) | Experimental | Mais chamadas/custo; não universal |
| E-05 | Posição da evidência em contexto longo afetou recuperação em modelos testados | [Liu et al. 2023](https://arxiv.org/abs/2307.03172) | Experimental | Modelos e tarefas do estudo; não regra temporal eterna |
| E-06 | Anthropic recomenda tags XML e orienta ordem de documentos/consulta em contexto longo | [Anthropic prompting guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables) | Confirmada como diretriz do fornecedor | Não é superioridade independente para outros modelos |
| E-07 | Llama 4 tem formato de prompt e ferramenta explicitados pelo projeto | [Meta prompt format](https://github.com/meta-llama/llama-models/blob/main/models/llama4/prompt_format.md) | Confirmada | Runtime/hosting altera detalhes |
| E-08 | Qwen usa chat template específico e recomenda cautela com stopword-ReAct em Qwen3 reasoning | [Qwen concepts](https://qwen.readthedocs.io/en/latest/getting_started/concepts.html), [function calling](https://qwen.readthedocs.io/en/stable/framework/function_call.html) | Confirmada | Aplicar só às versões documentadas |
| E-09 | DeepSeek tem modo thinking e migração/retirada de aliases | [Thinking mode](https://api-docs.deepseek.com/guides/thinking_mode/), [updates](https://api-docs.deepseek.com/updates/) | Confirmada | Estado muda; reconsultar |
| E-10 | xAI recomenda Responses API e preservar itens de reasoning nos fluxos documentados | [xAI best practices](https://docs.x.ai/developers/model-capabilities/text/best-practices) | Confirmada como orientação do fornecedor | Produto Grok não equivale à API |
| E-11 | Mistral catálogo contém categorias e status/depreciações | [Mistral models](https://docs.mistral.ai/models) | Confirmada | Catálogo em mudança |
| E-12 | Codex reconhece AGENTS.md; Agents API documenta execução agentiva | [Codex AGENTS.md](https://developers.openai.com/codex/guides/agents-md), [Agents API](https://developers.openai.com/api/docs/guides/agents-api/overview) | Confirmada em documentação oficial consultada em 23/11/2026 | Específico da superfície e configuração; guia GPT-5 antigo fica apenas como referência histórica |
| E-13 | Gemini API, AI Studio e serviços Google são superfícies distintas | [Gemini API docs](https://ai.google.dev/gemini-api/docs) | Confirmada | A matriz não detalha cada plano ou quota |
| E-14 | Cursor tem regras de projeto `.mdc`, usuário, equipe e `AGENTS.md`; admin pode exigir ativação de Team Rules | [Rules](https://cursor.com/docs/rules) | Confirmada em documentação atual, reaberta em 23/11/2026 | Enforcement impede desativar regra de equipe, mas não garante que o modelo siga seu conteúdo; não mede taxa real de aderência |
| E-15 | Precedência Copilot depende de superfície; vários clientes combinam instruções sem ordem geral | [GitHub custom instructions](https://docs.github.com/en/copilot/concepts/prompting-and-context/custom-instructions) | Confirmada | Feature/client matrix precisa de revisão contínua |
| E-16 | Antigravity tem agente com ferramentas, knowledge, rules/workflows e permissões | [Agent](https://antigravity.google/docs/agent), [permissions](https://antigravity.google/docs/permissions) | Confirmada | Sem teste próprio de comportamento/autonomia |
| E-17 | Aider aceita arquivo de convenções read-only como contexto | [Aider conventions](https://aider.chat/docs/usage/conventions.html) | Confirmada | Recomendações de uso, não comparação experimental |

## 2. Matriz comparativa transversal

| Recomendação | Convergência | Divergência/limite | Confiança global |
|---|---|---|---|
| Explicar resultado esperado | Alta entre guias de fornecedores | Nível de detalhamento ideal depende da tarefa | Bem fundamentada |
| Dar contexto relevante | Alta | Contexto excessivo ou mal posicionado pode atrapalhar | Bem fundamentada |
| Usar exemplos | Usado em várias recomendações e literatura | Seleção/posição pode enviesar; benefícios dependem da tarefa | Experimental/condicional |
| Usar XML/Markdown | Estruturação geralmente útil | XML é guidance explícita Anthropic; não universal | Condicional |
| Pedir CoT | Clássicos demonstraram ganhos em benchmarks históricos | Reasoning models recentes podem não precisar ou sofrer | Contraditória por geração/tarefa |
| Prompt mais longo | Sem consenso de superioridade | Custo, ruído e conflito; contexto longo não é atenção perfeita | Não estabelecida como regra |
| Regras negativas | Podem codificar limites importantes | Lista longa de proibições pode conflitar e reduzir desempenho | Hipótese dependente de tarefa |
| Autoavaliação | Útil para revisão direcionada | Não é medida independente da correção | Confirmada como limite metodológico |
| Tools/schema | APIs oferecem contratos estruturados | Implementação e validação seguem fora do texto | Bem fundamentada |

## 3. Registro de divergências e não verificados da versão-base (histórico)

- **CoT:** benefício observado em estudos de modelos específicos versus recomendações atuais de alguns modelos de raciocínio para não solicitar cadeia explícita. Decisão: usar tarefa e versão como unidade; não generalizar.
- **Posição de contexto:** estudo acadêmico encontra “lost in the middle” em testes; Anthropic prescreve uma ordem específica para uso com Claude atual. Decisão: tratar como recomendações de aplicação/modelo, testar com corpus próprio.
- **XML:** recomendação clara na documentação Anthropic; não foi encontrada evidência de superioridade universal entre os fornecedores pesquisados.
- **Produtos/plataformas na versão-base:** a primeira rodada não confirmou a situação do Windsurf. A rechecagem atual confirmou Windsurf 2.0 ativo por anúncio e changelog; Cascade é legado e a disponibilidade por plano/conta permanece fora da verificação. Cline e OpenCode já têm fichas documentais; Roo foi confirmado como encerrado. Continue, Microsoft Copilot, Perplexity e outros agregadores seguem delimitados, sem ficha profunda comparável. Ver §§8–9 e L-06/L-17.
- **Famílias adicionais:** Microsoft, Amazon e Cohere não receberam ficha de modelo auditada comparável. NÃO VERIFICADO.
- **Comprimento ideal, rigidez ideal, ordem universal, eficácia de repetição:** NÃO DETERMINADO.
- **Testes próprios:** nenhum experimento direto com versões/API foi executado. Sem resultados empíricos próprios.
- **Atualidade:** nomes e versão podem ter mudado após 23/11/2026. Revalidar antes de uso operacional.

## 4. Auditoria adversarial da versão-base (histórico)

### Cobertura

Cobertos com evidências primárias: fundamentos, OpenAI, Anthropic, Google (superfície/API em nível geral), Meta Llama, Qwen, DeepSeek, Mistral, xAI, Codex e Claude Code. Parcial: Gemini prompting detalhado, preços/limites por região, plataformas de código não OpenAI/Anthropic, frameworks de avaliação atuais, políticas de todos os produtos e modelos de Microsoft/Amazon/Cohere.

### Confiabilidade e precisão

- Corrigido o risco de chamar uma lista de fornecedores de “estado completo do mercado”: tabelas agora são explicitamente uma amostra verificada.
- Corrigida a extrapolação de CoT: achados são vinculados a tarefas e versões; incluída orientação atual divergente.
- Corrigida a confusão modelo/plataforma: separação explícita no Volume 1 e Volume 3.
- Corrigido risco de tratar schemas e marcadores como segurança: runtime continua responsável por validação/controle.
- Resultados de artigos são identificados como estudo, não evidência de teste local.
- Recomendação Anthropic de ordem/contexto e recomendações xAI/Grok estão atribuídas a seus docs e não generalizadas.

### Consistência

O dossiê não recomenda ao mesmo tempo “sempre pedir raciocínio” e “nunca pedir raciocínio”: explicita diferenças de época, modelo e objetivo. Autoavaliação é recomendada apenas como diagnóstico assistido; não como prova.

### Aplicabilidade e skill futura

Volumes 4 e 5 oferecem estrutura prática, testes, critérios e fluxos de aprovação. Isso dá uma base inicial para implementação futura, mas não substitui corpus completo de documentação por plataforma, dados empíricos atuais ou teste de aceitação real da skill.

### Falhas residuais encontradas

1. A ambição do prompt mestre supera o escopo de uma rodada de pesquisa: nem todas as 70 seções podem ser investigadas profundamente num único arquivo/turno.
2. A ficha completa para cada SKU/versão não é viável sem seleção explícita de modelos e revalidação de catálogo.
3. Algumas páginas oficiais retornadas em busca mudam rapidamente e incluem novidades de 2026; precisam de arquivo de captura/hash numa pesquisa formal.
4. Não houve triangulação independente para cada recomendação nem reprodução de experimentos.
5. A cobertura de segurança é de engenharia geral; não é auditoria de cada aplicativo.

## 5. Notas da versão-base (históricas; substituídas em 23/11/2026)

Pesos do pedido mantidos. A nota não pretende ser uma medida científica; é uma avaliação documentada de cobertura desta entrega.

| Critério | Peso | Pesquisa | Dossiê | Justificativa e deficiência |
|---|---:|---:|---:|---|
| Profundidade técnica | 15% | 7.0 | 7.0 | Técnicas, limites e fluxo explicados; faltam fichas exaustivas e estudos recentes adicionais |
| Abrangência/cobertura | 15% | 6.0 | 6.5 | Segunda rodada incluiu Cursor, Copilot, Antigravity e Aider; muitos ambientes/famílias ainda não verificados |
| Fontes/confiabilidade | 15% | 8.0 | 8.0 | Predominam fontes primárias e trabalhos acadêmicos; falta triangulação por claim |
| Atualidade | 10% | 7.5 | 7.5 | Consulta na data declarada; estado de produto pode mudar e não há snapshots preservados |
| Precisão técnica | 10% | 7.5 | 7.5 | Distinções modelo/plataforma e status de evidência explícitos; itens não auditados mantidos em aberto |
| Comparação modelos/plataformas | 10% | 6.0 | 6.5 | Matriz ampliada com mais superfícies; ainda desigual e sem testes pareados |
| Aplicabilidade | 10% | 7.5 | 8.0 | Inclui estrutura, protocolo, métricas, exemplos e fluxo de implementação futura |
| Organização/rastreabilidade | 5% | 8.0 | 8.5 | Seis volumes vinculados, evidências identificadas e links diretos |
| Análise crítica | 5% | 7.5 | 8.0 | Contradições e lacunas registradas; auditoria simulada não equivale a revisor externo |
| Preparação da skill | 5% | 7.5 | 8.0 | Requisitos e critérios de aceitação definidos; implementação deliberadamente ausente |
| **Nota ponderada** | **100%** | **7.15/10** | **7.40/10** | Bom ponto de partida, ainda com lacunas relevantes |

### Melhorias que elevariam a avaliação

1. Segunda rodada limitada e profunda para plataformas omitidas, com docs oficiais abertas e datas/planos capturados.
2. Definir shortlist de modelos e executar avaliação pareada com conjunto holdout, parâmetros e rubrica pré-registrados.
3. Acrescentar ficha por versão com contexto, saída, modalidades, preços, limites e status confirmado na API.
4. Revisão independente de fontes e de alegações críticas.

As melhorias 1–4 dependem de execução adicional de pesquisa/experimentos; não são apresentadas como concluídas. Não atribuir 9+ seria incompatível com as lacunas e ausência de ensaios atuais.

### Nota da auditoria interna da versão-base (histórica)

**8,0/10.** A auditoria distingue evidência oficial de estudo, enumera afirmações não verificadas, corrige generalizações e identifica falhas de cobertura e cálculo. Não recebe 10 porque é uma revisão interna simulada, sem auditor independente e sem rechecagem integral de todos os links, modelos, plataformas e claims.

## 6. Inventário de fontes consultadas

### Documentação oficial e projetos

- OpenAI — [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)
- OpenAI — [Reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices)
- OpenAI — [Model optimization and evals](https://developers.openai.com/api/docs/guides/model-optimization)
- OpenAI — [Models](https://developers.openai.com/api/docs/models)
- OpenAI — [Codex prompting guide](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide)
- OpenAI — [AGENTS.md configuration](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- OpenAI — [Agents API](https://developers.openai.com/api/docs/guides/agents-api/overview)
- Cursor — [Rules](https://cursor.com/docs/rules)
- GitHub — [Custom instructions](https://docs.github.com/en/copilot/concepts/prompting-and-context/custom-instructions)
- Google — [Antigravity agent](https://antigravity.google/docs/agent), [permissions](https://antigravity.google/docs/permissions)
- Aider — [Coding conventions](https://aider.chat/docs/usage/conventions.html)
- Anthropic — [Prompting best practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables)
- Anthropic — [Claude Code docs](https://code.claude.com/docs/en/)
- Google — [Gemini API docs](https://ai.google.dev/gemini-api/docs)
- Google — [Gemini pricing/model availability](https://ai.google.dev/gemini-api/docs/pricing)
- Meta — [Llama 4 prompt formats](https://github.com/meta-llama/llama-models/blob/main/models/llama4/prompt_format.md)
- Alibaba Qwen — [Concepts and chat templates](https://qwen.readthedocs.io/en/latest/getting_started/concepts.html)
- Alibaba Qwen — [Quickstart](https://qwen.readthedocs.io/en/latest/getting_started/quickstart.html)
- Alibaba Qwen — [Function calling](https://qwen.readthedocs.io/en/stable/framework/function_call.html)
- DeepSeek — [Models and pricing](https://api-docs.deepseek.com/quick_start/pricing/)
- DeepSeek — [Thinking mode](https://api-docs.deepseek.com/guides/thinking_mode/)
- DeepSeek — [Changelog](https://api-docs.deepseek.com/updates/)
- Mistral — [Models overview](https://docs.mistral.ai/models)
- xAI — [Models](https://docs.x.ai/developers/models)
- xAI — [Best practices](https://docs.x.ai/developers/model-capabilities/text/best-practices)
- xAI — [Reasoning troubleshooting](https://docs.x.ai/developers/advanced-api-usage/troubleshooting-reasoning)

### Estudos e artigos

- Wei et al., 2022 — [Chain-of-Thought Prompting Elicits Reasoning](https://arxiv.org/abs/2201.11903)
- Kojima et al., 2022 — [Large Language Models are Zero-Shot Reasoners](https://arxiv.org/abs/2205.11916)
- Wang et al., 2022 — [Self-Consistency Improves Chain of Thought Reasoning](https://arxiv.org/abs/2203.11171)
- Yao et al., 2023 — [Tree of Thoughts](https://arxiv.org/abs/2305.10601)
- Yao et al., 2023 — [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629)
- Liu et al., 2023 — [Lost in the Middle](https://arxiv.org/abs/2307.03172)
- Schulhoff et al., 2024 — [The Prompt Report: A Systematic Survey of Prompting Techniques](https://arxiv.org/abs/2406.06608)

## 7. Atualização e manutenção

- Revalidar páginas de modelos/plataformas no início de cada uso real; alvo trimestral para revisão do inventário.
- Conferir changelog, aliases, plano, endpoint, estado e limites; registrar URL, data, modelo citado e trecho sintetizado.
- Sinalizar toda recomendação antiga com versão e não reutilizar silenciosamente.
- Adicionar avaliação própria apenas com protocolo, casos, seeds quando aplicável, parâmetros, resultados e limitações completos.
- Manter lista de plataformas e famílias revisada por decisão de escopo; não declarar cobertura total da internet.

## 8. Registro complementar de fontes e rechecagem (23/11/2026)

Para fontes que não exibem data editorial ou “last updated”, a tabela diz explicitamente **não indicada na página consultada**. “Verificada” é data de acesso e confronto da afirmação. Metadados de catálogo podem mudar sem data visível; o registro é um snapshot, não garantia de disponibilidade.

| ID | Título / entidade / URL | Publicação ou atualização exibida | Verificação | Conclusão sustentada e limite |
|---|---|---|---|---|
| E-18 | OpenAI Help Center: [ChatGPT release notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes), [Work and Codex](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex), [custom instructions](https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions), [Projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt); API: [models](https://developers.openai.com/api/docs/models), [model selection](https://developers.openai.com/api/docs/guides/model-selection) | Release note ChatGPT: 23/11/2026; custom instructions: atualizado 27 dias antes da consulta; Projects: atualizado 18 horas antes; API catalog: data editorial não indicada | 23/11/2026 | ChatGPT Chat, Work e Codex têm modelos/recursos e condições de disponibilidade distintos; catálogo publica IDs e especificações. Não garante acesso por conta/região |
| E-19 | Anthropic: [Models overview](https://platform.claude.com/docs/en/models/overview), [deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations), Claude Code [memory](https://code.claude.com/docs/en/memory), [subagents](https://code.claude.com/docs/en/sub-agents), [permissions](https://code.claude.com/docs/en/permissions) | Não indicada nas páginas consultadas; versão do modelo aparece no catálogo | 23/11/2026 | IDs e lifecycle apresentados; arquivos de instrução são contexto, enquanto managed settings/hooks podem impor controle. Datas variam por host |
| E-20 | Google AI Studio: [Models](https://aistudio.google.com/docs/models), [Prompt design strategies](https://aistudio.google.com/docs/prompting-strategies) | Não indicada nas páginas consultadas | 23/11/2026 | Catálogo Gemini 4 e guidance de instruções claras, few-shot e posição de contexto longo. Orientação de fornecedor, sem ganho independente demonstrado |
| E-21 | Mistral Docs: [Models](https://docs.mistral.ai/models), [Prompting](https://docs.mistral.ai/inference/prompting) | Não indicada nas páginas consultadas | 23/11/2026 | catálogo atual e orientação system/user, estrutura, exemplos e conflitos. Guidance não prova superioridade comparativa |
| E-22 | GitHub Docs: [Custom instructions for GitHub Copilot](https://docs.github.com/en/copilot/concepts/prompting-and-context/custom-instructions) | Não indicada na página consultada | 23/11/2026 | suporte muda por cliente/surface e comportamento pode ser não determinístico. Não há uma precedência universal para todos os clientes |
| E-23 | Cline Docs: [Rules](https://docs.cline.bot/customization/cline-rules) | Não indicada na página consultada | 23/11/2026 | diretórios, combinação global/workspace e precedência documentados; não foi medida taxa de seguimento |
| E-24 | Cline Docs: [Memory Bank](https://docs.cline.bot/best-practices/memory-bank) | Não indicada na página consultada | 23/11/2026 | Memory Bank é metodologia de arquivos Markdown mais instruções; não deve ser descrita como memória nativa oculta |
| E-25 | Google Gemini CLI: [GEMINI.md](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md), [changelog](https://github.com/google-gemini/gemini-cli/blob/main/docs/changelogs/index.md), [releases](https://github.com/google-gemini/gemini-cli/releases) | v0.68.0 anunciada em 10/11/2026; changelog lista canais stable/preview/nightly | 23/11/2026 | contexto global/workspace/JIT, comandos de memória e release âncora. Instalação individual não foi inspecionada |
| E-26 | OpenCode Docs: [Agents](https://opencode.ai/docs/agents/), [Permissions](https://opencode.ai/docs/permissions), [Migrate from V1](https://opencode.ai/docs/migrate-v1) | Não indicada nas páginas consultadas | 23/11/2026 | páginas descrevem campos V2 e “última regra correspondente vence”; não misturar schema V1 |
| E-27 | RooCodeInc: [Sunsetting Roo Code](https://github.com/RooCodeInc/Roo-Code-Docs/blob/main/docs/sunset.md), [archived repository](https://github.com/RooCodeInc/Roo-Code) | sunset em 15/05/2026; repositório marcado arquivado na mesma data | 23/11/2026 | serviços/extension encerrados conforme comunicado oficial; docs antigas são históricas |
| E-28 | Cognition, [Windsurf 2.0 announcement](https://windsurf.com/blog/windsurf-2-0); [Devin Desktop (Windsurf) changelog](https://windsurf.com/changelog); [model list](https://docs.windsurf.com/windsurf/models); [Cascade memories legacy URL](https://docs.windsurf.com/windsurf/cascade/memories) → [Devin Local customizations](https://docs.devin.ai/desktop/devin-local/customizations) | Anúncio de 15/04/2026; release v3.14.30833 em 20/11/2026; data das páginas de modelo/customização não indicada | 23/11/2026 | Windsurf 2.0 ativo, Agent Command Center e Spaces documentados; Devin Cloud em rollout. Cascade é legado e novas conversas no editor de Devin usam Devin Local. Modelos listados em página Devin Desktop não garantem disponibilidade idêntica em cada plano/conta Windsurf |
| E-29 | Zheng et al., “When ‘A Helpful Assistant’ Is Not Really Helpful: Personas in System Prompts Do Not Improve Performances of Large Language Models”, [Findings of EMNLP 2024](https://aclanthology.org/2024.findings-emnlp.888/) | Publicado em 2024 (registro ACL Anthology) | 23/11/2026 | 162 papéis, 2.410 perguntas factuais e quatro famílias; sem ganho consistente frente a controle no conjunto estudado. Não generalizar além do desenho |
| E-30 | Basil et al., “Prompting Science Report 4: Playing Pretend: Expert Personas Don’t Improve Factual Accuracy”, [arXiv:2512.05858](https://arxiv.org/abs/2512.05858); Xiao et al., “When Does Persona Prompting Actually Help?”, [arXiv:2605.29420](https://arxiv.org/abs/2605.29420) | preprint submetido 05/12/2025; preprint submetido 28/05/2026 (submetido a revisão por pares) | 23/11/2026 | primeiro não achou ganho geral de factualidade em seus benchmarks; segundo reporta trade-off profundidade/clareza condicional em perguntas abertas. Ambos são estudos/preprints, não consenso |
| E-31 | Schulhoff et al., “The Prompt Report: A Systematic Survey of Prompt Engineering Techniques”, [arXiv:2406.06608](https://arxiv.org/abs/2406.06608) | submetido 06/06/2024; versão consultada revisada em 26/02/2025 | 23/11/2026 | survey de taxonomia/terminologia; evidencia diversidade e fragmentação, não ranking universal |
| E-32 | Pryzant et al., “Automatic Prompt Optimization with ‘Gradient Descent’ and Beam Search”, [arXiv:2305.03495](https://arxiv.org/abs/2305.03495) | submetido 04/05/2023, versão consultada 19/10/2023; publicado em EMNLP 2023 | 23/11/2026 | otimização automática em tarefas e dados definidos; não prova ganho fora do domínio/validação |
| E-33 | Yang et al., “Large Language Models as Optimizers” (OPRO), [ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/file/3339f19c5fcee3ad74502947a32be9e6-Paper-Conference.pdf) | publicado como artigo de conferência ICLR 2024 | 23/11/2026 | resultados em tarefas e scorers específicos; não transportar ganhos reportados como previsão atual |
| E-34 | Khattab et al., “DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines”, [ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/file/f1cf02ce09757f57c3b93c0db83181e0-Paper-Conference.pdf) | publicado como artigo de conferência ICLR 2024 | 23/11/2026 | pipelines otimizáveis com métrica/dados; não é garantia que qualquer programa/prompt melhora |

### Retificação do diagnóstico anterior

As notas e as lacunas dos §§3–5 descrevem a **versão-base** e são mantidas para histórico. Onde o texto anterior dizia que novas fontes/plataformas precisavam de pesquisa, esta revisão executou parte desse trabalho, com resultados e pendências em REGISTRO_DE_LACUNAS.md. A pontuação vigente está em AVALIACAO_FINAL.md: 9,24 pesquisa; 9,48 dossiê; 9,43 auditoria.



## 9. Metadados das evidências E-01–E-17

Este registro completa o ledger inicial. “Sem data editorial indicada” significa que a página consultada não mostrava data de publicação/atualização; a coluna de verificação fixa quando a evidência foi reaberta. Links para documentação dinâmica não congelam o conteúdo. Em páginas de repositório com branch móvel, a revisão exata não foi fixada e deve ser revalidada antes de reprodução literal.

| ID | Título, origem e URL verificada | Publicação/atualização indicada pela fonte | Data de verificação | Conclusão permitida e limite |
|---|---|---|---|---|
| E-01 | OpenAI, “Prompt engineering”, API Docs: [página atual](https://developers.openai.com/api/docs/guides/prompt-engineering) | Sem data editorial indicada na página consultada | 23/11/2026 | Guia oficial sustenta clareza, contexto e especificação de formato para a API; não prova ganho universal nem se transfere automaticamente ao ChatGPT UI. |
| E-02 | OpenAI, “Reasoning best practices”, API Docs: [página atual](https://developers.openai.com/api/docs/guides/reasoning-best-practices) | Sem data editorial indicada na página consultada | 23/11/2026 | Guidance da família/configuração descrita não recomenda solicitar CoT privado por padrão; não generalizar a outros provedores nem a todas as superfícies. |
| E-03 | Wei et al., “Chain-of-Thought Prompting Elicits Reasoning in Large Language Models”, arXiv:2201.11903: [registro](https://arxiv.org/abs/2201.11903) | Submetido em 28/01/2022; versão consultada v6 revisada em 10/01/2023 | 23/11/2026 | Experimentos com três famílias e tarefas aritméticas, de senso comum e simbólicas reportaram ganhos com demonstrações CoT; evidência histórica e específica do desenho. |
| E-04 | Wang et al., “Self-Consistency Improves Chain of Thought Reasoning in Language Models”, arXiv:2203.11171: [registro](https://arxiv.org/abs/2203.11171) | Submetido em 21/03/2022; v4 camera-ready 07/03/2023; publicado em ICLR 2023 | 23/11/2026 | Avaliação reportou ganhos em benchmarks selecionados; estratégia amostra múltiplas respostas e aumenta custo/latência. Não é garantia em produção atual. |
| E-05 | Liu et al., “Lost in the Middle: How Language Models Use Long Contexts”, arXiv:2307.03172: [registro](https://arxiv.org/abs/2307.03172) | Submetido em 06/07/2023; v3 em 20/11/2023; TACL 2023 | 23/11/2026 | Dois tipos de tarefa mostraram sensibilidade à posição da evidência em modelos testados; protocolo/achado não substitui avaliação com modelo e corpus atuais. |
| E-06 | Anthropic, “Prompting best practices”, Claude Platform Docs: [página canônica atual](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices); o URL citado no ledger legado redireciona para ela | Sem data editorial indicada na página consultada | 23/11/2026 | Guia atual apresenta orientação geral e páginas específicas por modelo para Claude; XML e ordem de contexto são recomendações do fornecedor, não prova de superioridade universal. |
| E-07 | Meta, “Llama 4 prompt format”, repositório oficial `meta-llama/llama-models`: [arquivo](https://github.com/meta-llama/llama-models/blob/main/models/llama4/prompt_format.md) | Branch `main` móvel; data editorial e commit exato não indicados no link citado | 23/11/2026 | Sustenta formato/tokenização de prompt publicada pelo projeto; runtime, checkpoint, revisão do arquivo e hosting podem alterar detalhes. |
| E-08 | Qwen Team/Alibaba, “Key Concepts” e “Function Calling”: [conceitos](https://qwen.readthedocs.io/en/latest/getting_started/concepts.html), [function calling](https://qwen.readthedocs.io/en/stable/framework/function_call.html) | Documentação `latest`/`stable`, sem data editorial indicada | 23/11/2026 | Qwen3 documenta modo híbrido e chat templates; orientação sobre parser/stopword aplica-se às versões e integração descritas, não a todo Qwen. |
| E-09 | DeepSeek, “Thinking Mode” e “Change Log”: [thinking](https://api-docs.deepseek.com/guides/thinking_mode/), [changelog](https://api-docs.deepseek.com/updates/) | Changelog consultado inclui atualização de 13/11/2026; a página de modo não exibe data editorial | 23/11/2026 | API documenta modos/controles e capacidades em evolução. Parâmetros, aliases e endpoints devem ser verificados para o ID usado; não inferir funcionamento a partir do nome do modo. |
| E-10 | xAI, “Best Practices Guide”, documentação da API: [página](https://docs.x.ai/developers/model-capabilities/text/best-practices) | Sem data editorial indicada na página consultada | 23/11/2026 | Guidance do fornecedor para fluxos de API e estado de resposta; não equivale a comportamento do app Grok nem demonstra vantagem independente. |
| E-11 | Mistral, “Models Overview”, documentação de inference/modelos: [catálogo](https://docs.mistral.ai/models) | Sem data editorial indicada; catálogo dinâmico | 23/11/2026 | Fonte oficial para a listagem e status exibidos na consulta; o catálogo inclui modelos de terceiros e pode mudar sem data visível. |
| E-12 | OpenAI, “Custom instructions with AGENTS.md” e “Agents API”: [AGENTS.md](https://developers.openai.com/codex/guides/agents-md) (redireciona ao ChatGPT Learn), [Agents API](https://developers.openai.com/api/docs/guides/agents-api/overview) | Sem data editorial indicada nas páginas consultadas | 23/11/2026 | Sustenta instruções persistentes de Codex e recursos documentados da API de agentes; não deve ser confundido com qualquer versão do app Codex. O guia legado “Codex prompting guide for GPT-5” não é base para estado atual. |
| E-13 | Google, “Welcome to Gemini API”, AI Studio Docs: [página atual](https://aistudio.google.com/docs) (o endereço legado `ai.google.dev/gemini-api/docs` redireciona) | Sem data editorial indicada na página consultada | 23/11/2026 | Distingue a API e recursos publicados no conjunto documental; não estabelece equivalência de disponibilidade entre API, AI Studio, Vertex e apps. |
| E-14 | Cursor Docs, “Rules”: [página direta](https://cursor.com/docs/rules) | Sem data editorial indicada na página consultada | 23/11/2026 | Project Rules `.mdc`, User Rules, Team Rules e `AGENTS.md` são documentados; administrador pode exigir que Team Rules estejam ativas e elas precedem regras de projeto/usuário, mas isso não garante obediência semântica do modelo. |
| E-15 | GitHub Docs, “Custom instructions for GitHub Copilot”: [página](https://docs.github.com/en/copilot/concepts/prompting-and-context/custom-instructions) | Sem data editorial indicada na página consultada | 23/11/2026 | A própria documentação delimita suporte por cliente e não determinismo de seguimento; não há uma precedência que valha para todas as superfícies. |
| E-16 | Google Antigravity Docs, “Agent Capabilities Overview” e “Permissions”: [agente](https://antigravity.google/docs/agent), [permissões](https://antigravity.google/docs/permissions) | Sem data editorial indicada nas páginas consultadas | 23/11/2026 | Sustenta as capacidades e controles descritos nas páginas; documentação não mede taxa de seguimento, autonomia ou eficácia em execução. |
| E-17 | Aider, “Specifying coding conventions”: [página](https://aider.chat/docs/usage/conventions.html) | Sem data editorial indicada na página consultada | 23/11/2026 | Documenta inclusão de convenções como contexto, inclusive em arquivo read-only; não é avaliação comparativa de qualidade dos prompts. |

### Estado de vigência da avaliação

A auditoria vigente e as três notas estão nos arquivos `AUDITORIA_FINAL.md` e `AVALIACAO_FINAL.md`. As seções 3–5 deste Volume 6 registram a versão-base e suas notas históricas; as correções posteriores constam nos registros L/M/R e nesta seção de fontes. O status atual do Windsurf é **confirmado documentalmente com delimitação**: produto Windsurf 2.0 ativo e Cascade legado; acesso a modelos/planos por conta não verificado.





