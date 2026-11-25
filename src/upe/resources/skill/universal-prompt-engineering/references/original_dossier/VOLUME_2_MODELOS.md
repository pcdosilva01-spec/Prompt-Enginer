# Volume 2 — Modelos e famílias

## 1. Estado da pesquisa

Consulta feita em 23/11/2026. Esta é uma fotografia documental, não um ranking nem garantia de acesso em cada plano/região. “Ativo” significa que uma página oficial consultada documentava o modelo ou família; slugs mudam e este arquivo precisa de revisão periódica.

## 2. Matriz de famílias e recomendações

| Desenvolvedor/família | Estado verificável nesta rodada | Particularidade documentada | Recomendação prática e limite |
|---|---|---|---|
| OpenAI GPT / reasoning / Codex | Docs API incluem GPT-6.2 Astra/Sol, GPT-6.1 Terra e variantes; há guia de reasoning | Responses API, ferramentas, saída estruturada; guia atual de reasoning desaconselha CoT explícito em alguns cenários; Codex possui guia especializado | Consultar guia da versão; definir saída e usar verificadores; não transportar prompting de versões anteriores automaticamente |
| Anthropic Claude | Guia atual separa recomendações por versão e gerais | Clareza, exemplos, tags XML, documentos longos no início/pergunta no final; effort/adaptive thinking depende do modelo | Seguir seção exata da versão; retirar instruções herdadas que causem verificação excessiva se a orientação atual indicar |
| Google Gemini | Gemini API e AI Studio documentados; Interfaces e Vertex são camadas distintas | Multimodalidade e ferramentas variam por API/versão | Confirmar modelo, endpoint e produto; não inferir recursos de um app para outro |
| Meta Llama | Repositório oficial publica formatos de prompt por versão | Tokens especiais e formato de ferramentas específicos | Pesos próprios: usar chat template exato; hospedagem de terceiros adiciona camada |
| Alibaba Qwen | Docs Qwen3 documentam modelos instruct/thinking/hybrid e templates | Alternância de thinking; docs alertam que alguns templates ReAct por stopword são inadequados para Qwen3 reasoning | Usar apply_chat_template da versão e parser robusto; tool call não é apenas texto |
| DeepSeek | API consultada lista V4.1-Flash-1017 e V4-Pro-0813, contexto e funções; changelog registra migração/retirada | Thinking mode, esforço, endpoints OpenAI/Anthropic/Responses; papéis têm particularidades | Conferir alias, histórico e endpoint; não usar nomes legados sem verificação |
| Mistral | Catálogo lista modelos gerais, código e multimodais, além de retirados/depreciados | Studio, API e implantação local não equivalem | Escolher por catálogo vigente e modalidade; não declarar sintaxe universal |
| xAI Grok | Docs API listam modelos, capacidades e migrações | Reasoning effort e tools; Responses API exige preservar itens necessários em multi-turn | Seguir API vigente e preservar state; produto Grok e API são diferentes |
| Microsoft/Amazon/Cohere e demais | Sem ficha comparável completa nesta rodada | Clouds podem hospedar modelos de terceiros com wrappers e políticas próprias | Não determinado até revisar docs de modelo e do host |

## 3. Fichas por fornecedor

### OpenAI

Fontes: [guia de prompt](https://developers.openai.com/api/docs/guides/prompt-engineering), [boas práticas de raciocínio](https://developers.openai.com/api/docs/guides/reasoning-best-practices), [modelos](https://developers.openai.com/api/docs/models), [Codex prompting guide](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide).

Conclusão sustentada: consulte guia da versão; use instruções claras e exemplos para formatos complexos quando útil. Modelos de raciocínio podem não se beneficiar de CoT explícito. Limites exatos de todos os slugs, acesso por plano/região e comparação controlada não foram auditados.

### Anthropic

Fonte: [Prompting best practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables).

Conclusão sustentada: clareza, exemplos e marcação XML de conteúdo; orientação diferencia versões. Para contexto longo, a documentação recomenda documentos antes da consulta e consulta ao final. Effort, adaptive thinking, prefill e subagentes dependem da versão. Diretrizes do fornecedor não equivalem a benchmark independente.

### Google Gemini

Fontes: [Gemini API docs](https://ai.google.dev/gemini-api/docs), [modelos](https://aistudio.google.com/docs/models), [estratégias de prompting](https://aistudio.google.com/docs/prompting-strategies).

A orientação oficial apresenta a engenharia de prompt como iterativa, recomenda instruções claras e específicas, descreve entradas por pergunta/tarefa/entidade/completação e recomenda com força exemplos few-shot para demonstrar formato, escopo e padrão de resposta. Para contexto longo, orienta colocar contexto antes e pergunta específica ao final. Essas são recomendações publicadas pelo Google para Gemini; não são prova comparativa universal nem resultado medido neste dossiê. Confirme modelo, região, endpoint e recurso do produto antes de aplicar.

### Meta Llama

Fonte: [Llama 4 prompt formats](https://github.com/meta-llama/llama-models/blob/main/models/llama4/prompt_format.md).

Usar tokens e formato previstos para a versão instalada. Template é compatibilidade, não decoração. Comportamento varia com quantização, fine-tune, runtime e serving.

### Alibaba Qwen

Fontes: [conceitos e templates](https://qwen.readthedocs.io/en/latest/getting_started/concepts.html), [quickstart](https://qwen.readthedocs.io/en/latest/getting_started/quickstart.html), [function calling](https://qwen.readthedocs.io/en/stable/framework/function_call.html).

A documentação recomenda usar chat template apropriado e alerta que tool calling baseado em stopwords (por exemplo, ReAct textual) pode falhar em Qwen3 reasoning, pois palavras podem aparecer no bloco de pensamento.

### DeepSeek

Fontes: [modelos e preços](https://api-docs.deepseek.com/quick_start/pricing/), [thinking mode](https://api-docs.deepseek.com/guides/thinking_mode/), [changelog](https://api-docs.deepseek.com/updates/).

Conferir aliases, modo thinking, contexto, endpoint e serialização do histórico. Mudanças de V3 para V4 impedem transferir automaticamente instruções antigas.

### Mistral

Fonte: [Models overview](https://docs.mistral.ai/models).

Catálogo vigente deve ser fonte de estado/depreciação. Comprimento ideal, formato ótimo e diferenças específicas não foram testados aqui.

### xAI

Fontes: [modelos](https://docs.x.ai/developers/models), [boas práticas](https://docs.x.ai/developers/model-capabilities/text/best-practices), [reasoning](https://docs.x.ai/developers/advanced-api-usage/troubleshooting-reasoning).

A documentação corrente recomenda Responses API para capacidades descritas e preservar itens de saída/reasoning que a API exige em turnos encadeados. O produto Grok não é equivalente à API.

## 4. Matriz técnica compacta

| Aspecto | Conclusão | Status |
|---|---|---|
| Tamanho ótimo por modelo | Não há tamanho universal documentado; limites não são o tamanho ótimo | Não determinado |
| Markdown/XML/JSON superior em geral | Não. XML é recomendação Anthropic; JSON Schema é interface de API onde suportada | Condicional |
| CoT universal | Não. OpenAI desencoraja em alguns modelos atuais; estudos antigos demonstram ganhos em tarefas delimitadas | Divergente por geração/tarefa |
| Formato chat nativo | Crítico especialmente para pesos abertos e templates | Confirmada |
| Modelo e plataforma afetam comportamento | Ambos alteram capacidades e contexto | Confirmada |
| Repetir instruções | Não há base para repetição sistemática; pode aumentar ruído | Hipótese; teste necessário |

## 5. Snapshot de modelos e adaptação por fornecedor

Esta tabela registra nomes/IDs que apareciam nas páginas oficiais consultadas em 23/11/2026. “Disponível” significa listado/documentado, não que o usuário tenha acesso. Páginas e aliases são voláteis; consulte a fonte antes de fixar uma implementação.

| Fornecedor e superfície | Identificadores/versões verificados | Recursos documentados relevantes | Adaptação de prompt sustentada |
|---|---|---|---|
| OpenAI API | GPT-6.2 Astra (gpt-6.2-astra), GPT-6.2 Sol (gpt-6.2-sol), GPT-6.1 Terra (gpt-6.1-terra), GPT-6 Luna (gpt-6-luna) | catálogo indica entrada texto/imagem e saída texto para a série atual; Astra/Sol: janela 1,05M e saída máxima 128K; ferramentas variam por modelo | consultar catálogo e model selection para tarefa, custo e ferramenta. Para modelos de raciocínio descritos no guia, não pedir cadeia de pensamento explícita por padrão |
| ChatGPT Chat, Work e Codex | release note de 23/11/2026 anuncia rollout GPT-6.2 no Chat; Work/Codex têm seletores próprios e rollout/acesso próprios | modelo mostrado e recursos dependem de plano, workspace, região e superfície | não atribuir ID/capacidade da API a todos os produtos. Especificar produto, plano e modelo realmente selecionado |
| Anthropic Claude API | Claude Fable 5.2 (claude-fable-5-2), Opus 5.5, Sonnet 5.5 e Haiku 5.5 | catálogo atual mostra contexto de 1M, saída máx. de 128K, entrada de texto/imagem, ferramentas e pensamento adaptativo, com effort padrão diferente entre modelos | usar guia de prompting da versão; XML e exemplos são guidance para Claude. Consultar lifecycle também no host: datas podem divergir em Bedrock/Google/Microsoft |
| Google Gemini API / AI Studio | Gemini 4 Carbon (gemini-4-carbon), Neon (gemini-4-neon), Hydrogen (gemini-4-hydrogen) e Argon (gemini-4-argon) | catálogo consultado mostra contexto de 1M; texto/imagem/áudio/vídeo/PDF; saída máxima indicada como 64K ou 1M conforme variante/modo | instruções claras; guidance oficial Gemini recomenda few-shot. Comparar zero-shot/few-shot no conjunto da tarefa, sem transportar a recomendação automaticamente |
| Meta Llama | Llama 4; formatos de conversa e tokens especiais publicados no repositório oficial | template de prompt e tool use dependem de versão e runtime de serving | usar template exato do checkpoint/hospedagem; não enviar marcadores de outra família |
| Alibaba Qwen | Qwen3; esquema de nomes distingue tamanho/tipo/data | documentação descreve modo híbrido thinking/non-thinking, versões open-weight e hospedadas, chamadas de ferramenta e templates | selecionar chat template/variante e modo corretos; docs alertam sobre parsing de stopwords ReAct em certos modelos de raciocínio |
| DeepSeek API | deepseek-flash = DeepSeek-V4.1-Flash-1017; deepseek-v4-pro = DeepSeek-V4-Pro-0813 | documentação lista contexto 1M, até 384K de saída, thinking toggle, tool calls e Responses/Anthropic format; visão listada para Flash, não para Pro | endpoint, modo e esforço fazem parte da configuração experimental; parâmetros ignorados no thinking mode não devem ser tratados como controle efetivo |
| Mistral | catálogo inclui Mistral Large 4 (v26.10, open-weight multimodal) e Small 4 (v26.03, híbrido instruct/reasoning/coding), além de modelos de terceiros | guia de prompting documenta mensagens system/user, propósito, estrutura, exemplos e aviso de contradições em system prompts longos | usar estrutura para separar seções; conferir qual família/model ID é realmente Mistral e qual é modelo terceiro hospedado no catálogo |
| xAI API | Grok 4.7 (grok-4.7) | docs listam contexto de 500K, reasoning configurável e agentic tool calling; API Responses pode transportar conteúdo reasoning | seguir documentação do endpoint/modelo e preservar itens necessários em chamadas encadeadas; o app Grok não é a API |
| Microsoft, Amazon, Cohere e outros | Não há ficha versionada profunda nesta amostra | fornecedor pode servir modelo próprio ou de terceiro sob camada de host | registrar separadamente ID do modelo, host, endpoint, contrato de ferramenta, região e versão antes de qualquer conclusão |

Fontes de estado/modelo: [OpenAI models](https://developers.openai.com/api/docs/models), [model selection](https://developers.openai.com/api/docs/guides/model-selection), [ChatGPT release notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes), [ChatGPT Work and Codex](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex), [Anthropic models overview](https://platform.claude.com/docs/en/models/overview), [model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations), [Gemini models](https://aistudio.google.com/docs/models), [Gemini prompting](https://aistudio.google.com/docs/prompting-strategies), [DeepSeek pricing/models](https://api-docs.deepseek.com/quick_start/pricing/), [Mistral models](https://docs.mistral.ai/models), [Mistral prompting](https://docs.mistral.ai/inference/prompting), [xAI models](https://docs.x.ai/developers/models).

### O que as diferenças realmente sustentam

1. **Detalhe:** os guias convergem em clareza e contexto relevante, não num número ótimo de palavras. Incluir detalhe apenas quando informa decisão, restrição, dado ou critério.
2. **Rigidez:** especificar rigidamente formato e condições de aceitação quando forem testáveis; explicitar margem de escolha em tarefas criativas ou quando a solução é indeterminada.
3. **Markdown/XML/JSON:** Gemini/Mistral usam exemplos estruturados; Anthropic explicita XML em sua guidance; OpenAI reasoning guide permite delimitadores para clareza. Não há resultado provando um formato textual vencedor em geral. Schema estruturado é outro mecanismo: depende da API e requer validação.
4. **Exemplos:** Gemini recomenda poucos exemplos de forma enfática; Mistral também documenta few-shot. Isso apoia testar exemplos, não incluí-los sempre. Medir ganho junto de custo, representatividade e regressão.
5. **Raciocínio:** OpenAI recomenda não pedir cadeia explícita para os modelos de raciocínio cobertos; DeepSeek documenta modo thinking com controles próprios; estudos clássicos usam modelos e tarefas anteriores. Não exigir chain-of-thought como regra que cruza famílias.
6. **Ferramentas:** chamada e permissão são contratos do runtime/API. O prompt deve dizer quando usar a ferramenta; runtime deve validar chamada e efeito.
7. **Tokens/custo:** prefixo reutilizado pode ser elegível para prompt caching em APIs específicas; custo também depende de tokens, saída, chamadas, região e ferramenta. Medir preço vigente e tokens reportados, não inferir apenas pelo tamanho visual.
## 5. Ficha mínima para manutenção

Registrar: fornecedor; ID e alias exatos; data/release; status; API/UI; modalidades; janela e saída; tools/schema/reasoning; template/papéis; parâmetros; recomendação oficial; plano/região; preço em registro separado; teste próprio versionado; fonte e confiança. Campo sem evidência deve constar como “não documentado na fonte consultada”.


