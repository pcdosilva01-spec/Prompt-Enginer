# Volume 3 — Plataformas e agentes

## 1. A plataforma muda a tarefa

O mesmo modelo pode receber contextos diferentes por interface. Produto de chat, API, IDE e agente podem acrescentar mensagens internas, arquivos, histórico condensado, recuperação, instruções persistentes, políticas, ferramentas, permissões e validação. Comparar o mesmo texto sem registrar o ambiente não isola o efeito do prompt.

## 2. Matriz preliminar da versão-base (histórica; atualização em §2.1)

| Ambiente | Informação oficial verificada | Consequência para prompting | Confiança |
|---|---|---|---|
| ChatGPT / OpenAI API | API tem Responses, ferramentas, saída estruturada e guias por modelo; produtos têm superfícies distintas | Não presumir que recurso de API existe no chat; prover arquivos pelo mecanismo suportado | Confirmada |
| Codex | Guia descreve AGENTS.md como instruções reconhecidas; Agents API documenta harness, estado, tools, sandbox e compactação | Objetivo e critério de sucesso no pedido; instrução persistente concisa e escopada. É agente, não somente modelo | Confirmada |
| Claude.ai / Claude API | API tem parâmetros e guia; Claude Code documenta instruções e ferramentas | Não confundir aplicativo, API e agente | Bem fundamentada |
| Claude Code | Documentação cobre memória/instruções, skills, hooks e subagentes | Pedido verificável no repo; limites da mudança e critério de pronto; validar execução | Bem fundamentada |
| Gemini / AI Studio / Vertex | Docs separam API, AI Studio e serviços Google Cloud | Confirmar serviço e endpoint; capacidade do app não implica capacidade de API | Confirmada |
| Cursor | Docs oficiais atuais descrevem `.cursor/rules` em `.mdc`, User/Team Rules e `AGENTS.md`; regras aplicadas entram no contexto | Admin pode exigir que Team Rules permaneçam ativas; isso impede desativação local, mas não garante aderência semântica do modelo | Confirmada, com limite explícito |
| GitHub Copilot | GitHub documenta instruções globais, por caminho, AGENTS.md e diferenças de precedência por superfície; as instruções não garantem conformidade | Registrar cliente (github.com, VS Code, Visual Studio, CLI) e feature; não transferir precedência entre superfícies | Confirmada |
| Google Antigravity | Docs descrevem agente multi-etapas com ferramentas/browser, artifacts, knowledge, rules/workflows e permissões | Controlar permissões de ferramentas; regras automáticas e políticas variam por escopo | Confirmada |
| Aider | Docs recomendam incluir arquivo de convenções como contexto somente leitura | Contexto é escolhido/incluído pelo usuário; prompt caching pode influenciar custo | Confirmada |
| Windsurf → Devin Local (documentação atual redireciona) | URL de memórias Windsurf redireciona para documentação Devin Local; a página explica importação das regras Windsurf legadas | Não presumir nome/feature atual por documentação histórica; consultar release docs do produto e status da conta | Parcial |
| Cline, Roo, Continue, OpenCode | Sem pesquisa oficial comparável concluída nesta rodada | Não afirmar precedência ou sintaxe sem docs da versão concreta | Não verificada |
| Perplexity, Microsoft Copilot, Bedrock e Vertex | Produtos agregam modelos, ferramentas ou pesquisa; detalhes por plano/tenant não auditados | Identificar feature/versão/plano e registrar origem de pesquisa | Parcial |

## 2.1 Matriz atual verificada por plataforma (corte 23/11/2026)

| Produto/plataforma | Configuração/instruções verificadas | Modelo, execução ou controle | Recomendação e limite |
|---|---|---|---|
| ChatGPT Chat | Custom instructions pessoais; Projects aceitam instruções de projeto, arquivos e opções de memória | release note de 23/11 anuncia rollout GPT-6.2 no Chat para planos elegíveis; modelos e recursos dependem de plano e workspace | não presumir que ID/API ou modelos de Work/Codex se apliquem ao Chat. Instruções de projeto e memória dependem da configuração |
| ChatGPT Work | Projeto e contexto persistente; superfícies de arquivos/ferramentas conforme plano | experiência de tarefas longas; modelo listado no seletor e por conta | registrar modelo, plano, workspace e ferramenta disponível em cada avaliação |
| Codex | AGENTS.md é reconhecido; guia descreve arquivos globais e por diretório injetados antes da solicitação | agente de programação/harness com ferramentas, estado, aprovação e limites próprios | critérios de sucesso, limites de mudança e validação executável; arquivos de instrução orientam o modelo, runtime governa ações |
| Claude Code | CLAUDE.md, AGENTS.md conforme configuração/versão, .claude/rules, memória automática, skills e subagentes | ferramentas e permissões configuráveis; managed settings/hooks podem impor controles | confirmar arquivos realmente carregados; CLAUDE.md é contexto, não enforcement. Arquivos locais e política gerenciada são camadas diferentes |
| Google Antigravity | rules e workflows em níveis distintos e contexto persistente | agente multi-etapas com ferramentas, navegador/artifacts/knowledge conforme documentação; permissões por ação | distinguir regra de workflow e autorização; permissões do runtime limitam ações |
| Cursor | `.cursor/rules` em `.mdc`, regras de usuário/equipe e `AGENTS.md` | regras aplicáveis entram no contexto; administrador pode exigir que Team Rules permaneçam ativadas; Team Rules têm ordem documentada | enforcement impede desativar a regra na configuração, não garante obediência do modelo; validar formato, superfície, escopo e plano |
| GitHub Copilot | instruções pessoais, de repositório, organização e por caminho onde suportado | suporte difere entre GitHub.com, VS Code, Visual Studio, JetBrains, Xcode e Eclipse | registrar cliente e feature matrix. A própria documentação diz que o modelo pode não seguir instruções sempre |
| Gemini CLI | GEMINI.md global, contexto de workspace e Just-in-time; /memory show e /memory reload | CLI oferece canais stable/preview/nightly; changelog oficial anuncia v0.68.0 em 10/11/2026 | não confundir com Gemini API/AI Studio. Verificar arquivos carregados e versão instalada |
| Aider | arquivo de convenções Markdown carregado como read-only por --read ou comando equivalente | contexto explícito do chat; caching depende de configuração/API | incluir só convenções relevantes e medir custo; exemplo da documentação é antigo e não é benchmark atual |
| Cline | .clinerules/ ou .cline/rules/, regras globais e de workspace; AGENTS.md e formatos compatíveis | regras combinadas; workspace vence conflito com regra global; painel permite ativar regras | não duplicar diretórios por padrão; distinguir regra de sistema de método Memory Bank |
| Roo Code | repositório oficial arquivado e anúncio de encerramento dos produtos em 15/05/2026 | extensão, Cloud e Router constam como encerrados; docs apenas históricas | não recomendar como plataforma ativa; preservação/migração deve ser tratada como legado |
| OpenCode | agentes Markdown e configurações por projeto/global; schema atual de agentes V2 | permissões ordenadas; última regra correspondente vence; campos V2 diferem de V1 | registrar versão/schema antes de portar arquivo legado; invisibilidade do agente não é segurança |
| Windsurf 2.0 / Devin Desktop | Página oficial confirma Agent Command Center, agentes locais e cloud, Spaces com contexto, e Devin integrado; docs de customização agora descrevem Devin Local/AGENTS.md/.devin/rules e importam regras .windsurf legadas | Changelog oficial identifica a série Devin Desktop (Windsurf), versão 3.14.30833 em 20/11/2026; Devin Cloud estava em rollout gradual | Windsurf 2.0 ativo está confirmado. Cascade é legado; disponibilidade de modelo/plano/rollout deve ser consultada no seletor. O redirect de Cascade memories não é evidência de equivalência entre produtos |
| Continue, Microsoft Copilot, Amazon Bedrock, Cohere, Perplexity e demais | não foi aberta documentação suficiente para ficha atual equivalente nesta rodada | produto/host pode combinar modelos, políticas e ferramentas | formalmente delimitados; não extrapolar de modelo/API de terceiro |

### Fontes primárias desta matriz

- OpenAI: [ChatGPT custom instructions](https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions), [Projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt), [ChatGPT release notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes), [Work and Codex](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex), [Codex AGENTS.md](https://developers.openai.com/codex/guides/agents-md).
- Anthropic: [Claude Code memory](https://code.claude.com/docs/en/memory), [subagents](https://code.claude.com/docs/en/sub-agents), [permissions](https://code.claude.com/docs/en/permissions).
- Google: [Antigravity agent](https://antigravity.google/docs/agent), [rules](https://antigravity.google/docs/rules), [permissions](https://antigravity.google/docs/permissions), [Gemini CLI GEMINI.md](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md), [Gemini CLI release notes](https://github.com/google-gemini/gemini-cli/blob/main/docs/changelogs/index.md).
- Cursor: [Rules](https://cursor.com/docs/rules), incluindo ativação/precedência de Team Rules e escopo `.mdc`/`AGENTS.md`.
- GitHub: [custom instructions](https://docs.github.com/en/copilot/concepts/prompting-and-context/custom-instructions), [repository instructions in IDE](https://docs.github.com/en/copilot/how-tos/copilot-in-your-ide/customize-copilot/configure-custom-instructions/add-repository-instructions-in-your-ide).
- Aider: [coding conventions](https://aider.chat/docs/usage/conventions.html).
- Cline: [Rules](https://docs.cline.bot/customization/cline-rules), [Memory Bank](https://docs.cline.bot/best-practices/memory-bank).
- Roo Code: [sunset notice](https://github.com/RooCodeInc/Roo-Code-Docs/blob/main/docs/sunset.md), [archived repository](https://github.com/RooCodeInc/Roo-Code).
- OpenCode: [agents](https://opencode.ai/docs/agents/), [permissions](https://opencode.ai/docs/permissions), [V1 migration](https://opencode.ai/docs/migrate-v1).
- Windsurf: [Windsurf 2.0 announcement](https://windsurf.com/blog/windsurf-2-0), [current editor changelog](https://windsurf.com/changelog), [model list under Devin Desktop docs](https://docs.windsurf.com/windsurf/models), [legacy Cascade memories URL](https://docs.windsurf.com/windsurf/cascade/memories) and [Devin Local customizations](https://docs.devin.ai/desktop/devin-local/customizations).
## 3. Codex e instruções persistentes

OpenAI documenta AGENTS.md como instrução opcional reconhecida por Codex; seu guia descreve descoberta ao longo de diretórios e inserção antes do pedido. [Codex prompting guide](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide); [AGENTS.md docs](https://learn.chatgpt.com/docs/agent-configuration/agents-md). A Agents API descreve harness gerenciado, estado, contexto, sandbox, ferramentas e delegação. [Agents API](https://developers.openai.com/api/docs/guides/agents-api/overview).

Orientação prática: use arquivo persistente para convenções estáveis, limites e validação; deixe a solicitação imediata no pedido. Evite duplicação e conteúdo não confiável com tom de instrução.

## 4. Claude Code

Claude Code é harness, diferente do Claude API puro. A documentação oficial cobre [configuração e comandos](https://code.claude.com/docs/en/), memória, skills, hooks, subagentes e permissões. Instruções persistentes devem conter convenções duráveis, não ser depósito ilimitado. Subagentes acrescentam custo e recebem contexto mediado; delegação não é inerentemente melhor para tarefas simples.

## 5. Prompt para tarefa agentiva

~~~text
Objetivo: [resultado observável]
Contexto: [dados e arquivos relevantes; origem]
Restrições: [escopo, compatibilidade, segurança]
Ferramentas: [as realmente disponíveis]
Critérios de conclusão: [condições verificáveis]
Entrega: [formato e público]
Incertezas: [perguntar ou marcar, sem presumir]
~~~

Para agente que edita arquivos, informe limites do repo, critérios de alteração, validações e quando parar. É uma estrutura de referência, não obrigação universal.

## 6. Ferramentas, permissões e fluxo

1. Schema da ferramenta define contrato técnico; prosa não substitui schema.
2. Runtime valida permissão, parâmetros, escopo e resultado.
3. Ações externas ou irreversíveis devem passar pelos controles de aprovação do sistema.
4. Resultados de ferramenta devem ser delimitados como observação, não instrução confiável.
5. Limite iterações, duração, tokens e delegações; registre traces quando apropriado.
6. Erros e outputs parciais precisam de tratamento explícito.

## 7. Engenharia para programação

- Dê resultado esperado, contexto do repo e critério de conclusão.
- Delimite arquivos/áreas quando conhecido; peça exploração quando desconhecido.
- Para bugs, forneça sintoma, passos, comportamento esperado e observado.
- Para pesquisa, separar levantamento de implementação.
- Para código, exigir validação observável quando solicitada e disponível; relatar precisamente o que rodou.
- Para tarefas longas, checkpoints e notas com data ajudam a preservar estado.

Risco central: AGENTS.md, CLAUDE.md e arquivos equivalentes são instruções carregadas pelo agente. Conteúdo vindo de repositório, website ou anexo pode ser adversarial. Validar origem e escopo é parte da segurança, não da qualidade estilística.

## 8. Escopo e pendências atuais

A matriz de §2.1 cobre todas as plataformas nomeadas na solicitação em nível documental. Isso não equivale a paridade de profundidade, teste de produto ou comparação experimental entre elas.

- **Cobertas em fonte oficial atual:** ChatGPT, Codex, Claude Code, Gemini CLI, Antigravity, Cursor, Copilot, Aider, Cline e OpenCode.
- **Legado encerrado:** Roo Code; sua documentação de recursos é apenas histórica.
- **Atual e legado diferenciados:** Windsurf 2.0 está ativo e teve changelog até 20/11/2026; Cascade é legado, e a URL de memórias agora entrega instruções do Devin Local. O seletor e os modelos variam por plano/rollout.
- **Delimitadas sem ficha profunda:** Continue, Microsoft Copilot, Amazon Bedrock, Cohere, Perplexity e outros agregadores. Reabrir somente com documentação atual de modelo e host/plataforma.
- **Não executadas:** instalação, verificação de conta/plano, teste de precedência e ensaio de uso de ferramenta.

As fontes das superfícies ficam separadas das fichas de modelo do Volume 2. As afirmações voláteis devem ser revalidadas antes de implantação.
## Fontes primárias adicionais

- Cursor — [Rules](https://cursor.com/docs/rules)
- GitHub — [Custom instructions](https://docs.github.com/en/copilot/concepts/prompting-and-context/custom-instructions), [repository instructions in IDE](https://docs.github.com/en/copilot/how-tos/copilot-in-your-ide/customize-copilot/configure-custom-instructions/add-repository-instructions-in-your-ide)
- Google — [Antigravity agent](https://antigravity.google/docs/agent), [rules and workflows](https://antigravity.google/docs/rules-workflows/), [permissions](https://antigravity.google/docs/permissions)
- Aider — [Coding conventions](https://aider.chat/docs/usage/conventions.html)
- Windsurf — [Windsurf 2.0 announcement](https://windsurf.com/blog/windsurf-2-0) and [editor changelog](https://windsurf.com/changelog) confirm current product/activity. The legacy [Cascade memories URL](https://docs.windsurf.com/windsurf/cascade/memories) routes to Devin Local customizations; distinguish current Devin Local from legacy Cascade.





