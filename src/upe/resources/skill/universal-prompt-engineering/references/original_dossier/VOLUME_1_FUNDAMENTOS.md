# Volume 1 — Fundamentos e método

## 1. Síntese executiva

Engenharia de prompts é o desenho e a iteração das entradas, exemplos, contexto e instruções que orientam um modelo para uma tarefa. Em sistemas reais, o prompt é apenas uma parte do **contexto de execução**: mensagens com papéis, arquivos recuperados, ferramentas, formato de saída, parâmetros, memória, políticas e lógica do agente afetam o resultado. Assim, a pergunta útil não é “qual prompt universal funciona?”, mas “qual configuração controlada atende a esta tarefa neste modelo e ambiente, sob estes critérios?”.

**Confiança:** bem fundamentada. Definição operacional consistente com a literatura de técnicas e documentação dos fornecedores; o termo não tem uma única taxonomia normativa.

## 2. Escopo, data e método

- Pesquisa documental realizada em 23/11/2026, horário de Brasília.
- Prioridade: documentação oficial vigente, páginas de modelo/API, repositórios do desenvolvedor e estudos com método explícito.
- Fontes comunitárias não foram usadas como prova de capacidades.
- Foram consultadas páginas oficiais OpenAI, Anthropic, Google, Meta, Alibaba/Qwen, DeepSeek, Mistral e xAI, além de artigos científicos identificados no Volume 6.
- Foram registradas recomendações com versão explícita; uma diretriz de fornecedor é evidência de uso recomendado, mas não prova independente de superioridade universal.
- A pesquisa não teve acesso a API keys, planos pagos, ambientes de teste ou corpus padronizado. Não foram executados testes de modelos.
- A bibliografia inclui agora uma survey sistemática de técnicas e trabalhos de otimização de pipelines/prompts; levantamento bibliográfico não substitui avaliação atual de cada modelo.

## 3. Modelo, aplicação e sistema agêntico

| Camada | O que é | Exemplo de decisão que pertence à camada |
| --- | --- | --- |
| Modelo | Rede/modelo servido ou pesos implantados | Modalidade, janela, parâmetros de raciocínio, template nativo |
| API/runtime | Interface e parâmetros que transportam a conversa | papéis, limite de saída, JSON Schema, estado de conversa |
| Aplicativo/plataforma | Produto que compõe instruções, arquivos e ferramentas | ChatGPT, Claude.ai, Gemini, Cursor |
| Harness/agente | Loop que escolhe ferramentas, executa ações e mantém estado | Codex, Claude Code, Agents SDK |
| Ferramenta/conector | Operação executada fora do modelo | busca web, shell, browser, file search, MCP |
| Skill/instruções persistentes | Conhecimento e procedimentos carregados sob regras da plataforma | AGENTS.md, CLAUDE.md, skills |

Uma instrução “use a ferramenta X” só funciona se a camada de execução disponibilizar X, com nome e contrato compatíveis. Texto de prompt pode solicitar uma operação; não cria a ferramenta nem autoriza uma ação por si só.

## 4. Fundamentos e limites

### 4.1 In-context learning e exemplos

O modelo condiciona a geração no conteúdo fornecido durante a requisição. Zero-shot fornece tarefa sem exemplos; one/few-shot inclui exemplos input-output; many-shot escala o número/tamanho de exemplos. Exemplos podem desambiguar rótulos, estilo e formato, mas também introduzem viés, inconsistência, custo de contexto e risco de sobreajuste ao conjunto demonstrado.

**Usar:** quando o padrão esperado é difícil de descrever em prosa ou os erros de classificação têm formas recorrentes.  
**Evitar:** quando exemplos não são representativos, contradizem a instrução ou ocupam contexto de evidência necessária.  
**Evidência:** demonstrada em tarefas específicas de modelos anteriores e reavaliar para o modelo atual; não implica ganho universal. [Wei et al. (2022)](https://arxiv.org/abs/2201.11903).

### 4.2 Instruções e hierarquia

APIs costumam distinguir papéis como system/developer/user/assistant, mas a semântica e prioridade exatas variam por endpoint, runtime e produto. Não transfira uma hierarquia de API para um chatbot ou framework sem documentação. O dado citado dentro de um documento é conteúdo; não passa a ser uma instrução privilegiada por conter palavras imperativas. O runtime deve marcar limites entre instruções confiáveis e material não confiável.

### 4.3 Context engineering

Inclui seleção, organização, recuperação e poda do que o modelo vê: instruções, histórico, documentos, resultados de ferramentas, memória e orçamento. Contexto amplo não garante atenção uniforme. Um estudo de tarefas de recuperação observou piora quando a evidência relevante ficava no meio de entradas longas, para os modelos testados; não se deve transformar isso em lei para modelos atuais. [Liu et al. (2023)](https://arxiv.org/abs/2307.03172). Documentação Anthropic recomenda documentos extensos no início e a pergunta no final para seus modelos atuais; isso é diretriz de fornecedor e deve ser validada no domínio. [Anthropic: prompting best practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables).

### 4.4 Geração, raciocínio e cadeia de pensamento

O texto “passo a passo” é uma técnica de elicitação estudada em certos modelos e benchmarks, não acesso garantido ao processo interno verdadeiro. Cadeias podem conter erros, racionalizações ou propagar premissas erradas. Para modelos de raciocínio recentes, OpenAI recomenda evitar instruções CoT em alguns cenários, pois o raciocínio é interno e o pedido pode não ajudar ou prejudicar; a recomendação é específica à linha e configuração. [OpenAI reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices). Prefira pedir resultado, premissas relevantes, verificações e evidência necessária em vez de exigir transcrição privada de raciocínio.

## 5. Catálogo técnico resumido

| Técnica | O que faz / quando usar | Risco e alternativa | Evidência |
| --- | --- | --- | --- |
| Zero-shot | Instrução direta, sem exemplos; baseline econômico | Pode deixar formato implícito; adicionar exemplo mínimo ou schema | Geral, validar por tarefa |
| Few-shot | Demonstra exemplos representativos | Custo, viés de posição e exemplos ruins; testar seleção e ordem | Experimental; Wei et al. |
| Role/context | Define público, domínio e objetivo | Papel decorativo não concede conhecimento/permissão e pode não melhorar factualidade | Experimental/divergente: estudos em conjuntos/modelos específicos acham efeito nulo ou dependente da tarefa |
| Decomposição | Divide entregável em subtarefas com interfaces | Mais chamadas e erros de handoff; tarefa simples pode piorar | Bem fundamentada em problemas complexos |
| Prompt chaining | Saídas intermediárias alimentam etapa seguinte | Erro inicial se propaga; validar cada interface | Arquitetural, depende do fluxo |
| ReAct / action-observation | Intercala chamada de ferramenta e observação | Loop/tool misuse; precisa executor, limites e validação | Técnica de sistema, não texto isolado |
| Self-consistency | Amostra soluções e agrega respostas | Mais custo/latência; votos correlacionados podem escolher erro | Experimental e benchmark-específica; [Wang et al. (2022)](https://arxiv.org/abs/2203.11171) |
| Tree of Thoughts | Explora ramos e avalia estados intermediários | Busca cara e avaliador imperfeito | Experimental; [Yao et al. (2023)](https://arxiv.org/abs/2305.10601) |
| Critique/revision | Uma chamada revisa saída contra critérios | Autocrítica pode aprovar erro inicial; usar verificadores externos | Depende do domínio; nunca é prova independente |
| RAG/grounding | Busca evidência externa e fornece ao modelo | Recuperação ruim, fontes contaminadas ou citações falsas | Arquitetura para atualidade; medir retrieval e answer separately |
| Tool/function calling | Emite estrutura de chamada para executor real | Sintaxe válida não garante ação correta/segura | APIs oficiais; validação determinística obrigatória |
| Structured output | Restringe forma, frequentemente via schema | Schema válido não garante veracidade/conteúdo completo | Alta para validade estrutural quando modo suportado |
| XML/Markdown delimitadores | Sinalizam fronteiras semânticas em texto | Não são fronteiras de segurança nem tokens mágicos universais | Diretriz por fornecedor/modelo; XML especificamente recomendado pela Anthropic |
| Otimização automática | Pesquisa variantes e escolhe por métrica/dev set; ex. APE/OPRO | Otimizador pode overfit ao scorer, exemplos e domínio; validação fora da amostra necessária | Experimental; [APE](https://arxiv.org/abs/2305.03495), [OPRO](https://proceedings.iclr.cc/paper_files/paper/2024/file/3339f19c5fcee3ad74502947a32be9e6-Paper-Conference.pdf) |
| Programmatic prompting / DSPy | Define assinaturas e módulos de um pipeline; compila demos/instruções para métrica | Resultado depende do programa, métrica, dados e otimizador; não é “prompt melhor” garantido | Experimental; paper [DSPy](https://proceedings.iclr.cc/paper_files/paper/2024/file/f1cf02ce09757f57c3b93c0db83181e0-Paper-Conference.pdf) |
| Memória | Persiste fatos/preferências/progresso fora do turno | Informação velha, incorreta ou excessiva; proveniência e expiração | Arquitetural, depende do aplicativo |

### Exemplo de saída estruturada segura

```json
{
  "answer": "...",
  "evidence": [{"source_id": "S1", "claim": "..."}],
  "uncertainties": [],
  "status": "complete"
}
```

Use schema/API estrita quando disponível; valide tipos e campos no código. Markdown ou JSON pedido apenas em prosa não fornece garantia de parse.

## 6. Princípios condicionais

1. Especifique tarefa, público, contexto essencial, formato e critério de conclusão.
2. Dê exemplos quando forem mais precisos que descrição abstrata e realmente representativos.
3. Torne instruções mutuamente compatíveis e priorize restrições importantes sem repetição indiscriminada.
4. Separe instruções, dados de referência e saídas de ferramentas com rótulos claros.
5. Coloque informação necessária onde o modelo/plataforma possa consumi-la; teste recuperação em contextos longos.
6. Use ferramenta ou cálculo determinístico quando o resultado precisa ser atualizado, exato ou executável.
7. Teste o prompt em conjunto representativo, com modelo, parâmetros, harness e data fixos.
8. Revise toda recomendação que dependa de versão após mudança de modelo, API ou aplicação.

**Não estabelecido:** existe uma posição universalmente melhor para a consulta; tamanho ótimo universal; sintaxe delimitadora superior em todos os modelos; número ideal de exemplos. Trate tudo isso como parâmetro experimental.

## 7. Estado da evidência por prática popular

### Persona de especialista

“Aja como especialista” pode orientar tom, vocabulário e gênero textual, mas não transfere competência nem garante maior precisão factual. Um estudo submetido em 2023 e publicado em Findings of EMNLP em 2024 testou 162 papéis e 2.410 perguntas factuais; em seu conjunto, adicionar persona não elevou desempenho frente ao controle de modo consistente ([Zheng et al.](https://aclanthology.org/2024.findings-emnlp.888/)). Um relatório preprint posterior avaliou benchmarks e modelos diferentes e também encontrou ganhos não significativos na maioria dos casos, com exceção específica de modelo/tarefa ([Prompting Science Report 4](https://arxiv.org/abs/2512.05858)). Estudos recentes de persona em perguntas abertas reportam efeitos condicionais e trade-offs ([When Does Persona Prompting Actually Help?](https://arxiv.org/abs/2605.29420)).

**Conclusão:** use persona para calibrar perspectiva comunicativa quando necessária; não como substituto de contexto, fontes ou expertise externa. Classificação: **contraditória/condicional**, pois o efeito depende da tarefa, modelo e métrica.

### Prompt engineering como otimização

Uma survey sistemática organiza dezenas de famílias de técnicas e alerta pela diversidade de nomenclatura/condições; não existe ranking agregado que declare uma técnica vencedora para todo caso ([The Prompt Report, versão revisada 2025](https://arxiv.org/abs/2406.06608)). APE e OPRO demonstram otimização automática em tarefas delimitadas; DSPy propõe compilar pipelines programáticos com métrica. Tais trabalhos justificam a abordagem experimental, não o uso sem conjunto de validação e holdout.
## 8. Procedimento para adaptar um prompt a modelo e plataforma

Use esta sequência antes de escrever instruções finais:

1. **Fixe a tarefa e seu erro caro:** factualidade, extração, estilo, cálculo, mudança de código ou ação externa pedem critérios diferentes.
2. **Identifique a superfície:** nome do produto, modelo/ID mostrado, endpoint, versão do agente, plano/região, template de mensagens, ferramentas e arquivos persistentes realmente carregados.
3. **Confira a guidance vigente da versão:** separar recomendação oficial de evidência independente. Não copiar guidance de API para ChatGPT, IDE ou agente sem conferir a camada.
4. **Escolha o mínimo suficiente:** inclua fatos de entrada, critérios de aceitação, limites e formato que reduzam ambiguidade. Não expanda por formalidade.
5. **Escolha a estrutura por função:** prosa para objetivo flexível; seções para organizar; XML quando a família recomenda e seus limites ajudam; schema de API para formato estruturado suportado. Não use delimitadores como defesa de segurança.
6. **Decida se exemplos compram clareza:** use amostras representativas e coerentes quando a regra abstrata é difícil; compare com zero-shot e contabilize tokens.
7. **Defina execução e verificação:** ferramenta existente, chamada autorizada, limite de loop, validação de output e ação; validação fora do modelo para risco alto.
8. **Teste a variante:** mantenha o mesmo modelo/runtime/conjunto, altere um fator por vez, pré-registre métricas e preserve holdout.

| Situação de modelo/plataforma | Consequência documentada para o prompt | O que precisa ser confirmado |
| --- | --- | --- |
| OpenAI reasoning model/API | guia atual recomenda não solicitar CoT explícito para os modelos cobertos; delimitadores podem tornar as seções claras | modelo exato e se recomendação aplica à linha/endpoint |
| Gemini API/AI Studio | guidance incentiva exemplos few-shot e instruções claras; sugere contexto antes da pergunta em contextos longos | tarefa, custo de contexto, modelo e se exemplos realmente melhoram no holdout |
| Claude API/Claude Code | orientação do fornecedor usa estrutura XML em certos prompts; Claude Code pode inserir arquivos persistentes | versão servida e arquivos/regras de fato carregados |
| Qwen open-weight | template nativo, modo thinking/instruct e parser de tools importam | checkpoint, runtime, quantização, template e parser |
| DeepSeek API | thinking e esforço são parâmetros de interface e podem alterar o turno; certos parâmetros são ignorados | endpoint/formato de compatibilidade e modo ativo |
| Cursor/Copilot/Cline/OpenCode | regras persistentes dependem do cliente, caminho, versão e precedência; regra em contexto não garante resposta conforme. No Cursor, admin pode exigir que Team Rules estejam ativas, o que não equivale a enforcement semântico da resposta | conteúdo efetivamente incluído, feature, permissões e logs |

A tabela não ranqueia modelos. Ela identifica configurações e mecanismos que mudam o experimento; suas fontes e data de corte estão nos Volumes 2, 3 e 6.





