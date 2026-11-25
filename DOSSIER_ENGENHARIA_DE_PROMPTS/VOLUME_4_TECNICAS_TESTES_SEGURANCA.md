# Volume 4 — Técnicas, aplicações, testes e segurança

## 1. Escolha de estrutura por tarefa

| Tarefa | Prompt recomendado como baseline | Verificação externa |
|---|---|---|
| Resposta factual atual | Pergunta específica, janela temporal, escopo, formato e uso de busca quando disponível | Fonte primária, data, URL e afirmações |
| Extração de documento | Definir campos, unidade/normalização, regra para ausente e schema | Validador de schema + amostra anotada |
| Classificação | Definir classes, exclusividade, casos ambíguos, exemplos representativos | Matriz de confusão, acordo humano |
| Síntese | Definir audiência, cobertura, documentos e prioridade; delimitar citações | Validar cobertura contra fontes e claims |
| Escrita criativa | Definir público, propósito, limites essenciais e liberdade estilística | Revisão humana de adequação |
| Código | Resultado, contexto do repositório, limites e critérios de pronto | Testes/build/lint/revisão de diff |
| Agente com ferramentas | Objetivo, ferramentas reais, regras de uso, limites, aprovação e critério de parar | Validação determinística de chamadas, escopo e efeitos |
| Matemática/dados | Especificar pergunta e unidades; permitir calculadora/código se disponível | Cálculo independente ou execução controlada |

## 2. Exemplos didáticos (não foram executados)

### Caso: transformar registros de suporte em categorias

**A — Prompt fraco:** “Analise esses textos e diga os principais problemas.”

**B — Diagnóstico:** não define categorias, unidade de análise, tratamento de múltiplos problemas, formato nem confiança; “principais” é subjetivo.

**C — Prompt revisado:**

~~~text
Classifique cada registro em uma ou mais categorias da taxonomia fornecida.
Use somente categorias existentes. Se nenhum rótulo servir, marque "outro" e explique
em até 15 palavras. Retorne um objeto por registro com id, categorias, trecho de
evidência e ambiguidade (baixa/média/alta). Não infira causa que o texto não declara.
Taxonomia: [lista versionada]
Registros: [dados delimitados]
~~~

**D — Justificativa:** explicita unidade, classes permitidas, exceção, evidência e formato. Se a API aceitar schema, aplicar schema no runtime. Não presume melhora mensurada.

**E — Adaptação por modelo:** em API com JSON Schema estrito, codificar a estrutura no parâmetro da API; em modelo open-weight, usar template nativo e validar JSON após geração; para reasoning model, evitar pedir transcrição do raciocínio privado e pedir evidência verificável.

**F — Adaptação por plataforma:** no chatbot sem acesso aos dados, colar/ anexar registros; em API, enviar dados com role/schema apropriados; em agente coding, não habilitar shell sem necessidade.

**G — Teste:** amostra estratificada com rótulos humanos duplos, macro-F1, exact-match, taxa de schema válido, taxa de inferência indevida, custo e latência.

### Exemplo compacto de prompt de programação

**Fraco:** “Conserte o bug.”

**Revisado:** “Investigue por que exportação CSV omite linhas cujo campo opcional está vazio. Preserve o formato existente para os outros casos. Primeiro localize o caminho de exportação; faça a menor mudança que resolva o caso; adicione/ajuste teste se autorizado; execute a validação relevante e informe arquivos alterados e resultado. Se os dados não determinarem a interpretação de vazio versus nulo, explique a distinção encontrada.”

Exemplo ilustrativo, não submetido a modelos nem a benchmark.

## 3. Protocolo de laboratório reprodutível

### 3.1 Pré-registro do teste

Antes de executar, congelar: pergunta de pesquisa; modelos/IDs exatos; endpoint/UI; data; versão do harness; parâmetros e esforço; ferramentas; prompt integral; dados; seed quando suportada; repetições; custo/limite; rubrica; exclusões; split de desenvolvimento e holdout.

### 3.2 Pares experimentais

| Experimento | Controle | Variante | Métricas principais | Fatores de confusão |
|---|---|---|---|---|
| Curto vs. longo | Pedido mínimo suficiente | Adicionar contexto relevante e instruções | sucesso, cobertura, tokens, latência | Mais informação confundida com extensão |
| Livre vs. estruturado | Prosa livre | Seções, campos ou schema | aderência, parse, qualidade, custo | Robustez do parser |
| Rígido vs. flexível | Objetivo e espaço de escolha | Restrições detalhadas | sucesso, diversidade, violações | Tarefa criativa versus determinística |
| Exemplos vs. sem | Zero-shot | Few-shot representativo | acurácia, macro-F1, robustez | Qualidade/ordem dos exemplos |
| Contexto relevante vs. excessivo | Evidência mínima suficiente | Mesmo + documentos irrelevantes | recall/precisão de fonte, erro, tokens | Posicionamento da evidência |
| Critério de aceitação | Sem critério explícito | Critérios observáveis | pass rate, completude | Rubrica pode se alinhar ao próprio prompt |
| Genérico vs. específico do modelo | Prompt comum | Variante da documentação do modelo | qualidade, custo, latência | Familiaridade do autor, tuning desigual |
| Plataforma especializada | Chat/API simples | Harness com arquivos/tools/contexto | sucesso ponta a ponta, ação incorreta | Capacidade de ferramenta e permissões |

### 3.3 Execução e análise

Executar múltiplas repetições adequadas à variância e reportar distribuição, não apenas melhor saída. Fazer pareamento por tarefa e orçamento comparável. Avaliação cega por rubrica; adjudicação humana para divergências. Separar qualidade de resposta da qualidade de recuperação e da qualidade de ferramenta. Medir custo, tokens, latência, parse, falhas e efeitos colaterais. Congelar casos holdout para evitar otimização excessiva. Publicar prompts completos e exceções se possível.

**Nenhum resultado destes experimentos foi produzido nesta pesquisa.** Este capítulo é plano experimental.

## 4. Catálogo de antipadrões

| Antipadrão | Efeito/causa | Correção |
|---|---|---|
| Objetivo ambíguo | Saídas incompatíveis com a intenção | Definir resultado, audiência e uso |
| Contexto insuficiente | Modelo precisa adivinhar | Fornecer fatos necessários e proveniência |
| Contexto excessivo/irrelevante | Custo, distração e conflito | Remover material e medir ablação |
| Regras conflitantes | Modelo escolhe prioridade implicitamente | Resolver conflito antes da execução |
| Rigidez sem motivo | Bloqueia solução e cria fragilidade | Restringir apenas critérios essenciais |
| Liberdade sem limites | Variabilidade e omissões | Definir formato e conclusão |
| Exigir ferramenta inexistente | Texto não cria capability | Consultar runtime e fornecer tool real |
| Fonte/citação inventada | Citação pedida sem busca ou evidência | Acesso real à fonte; não inferir URL |
| JSON só em prosa | Pode resultar em sintaxe inválida | Schema de API + parser/validador |
| Autocrítica tratada como prova | Modelo valida o próprio erro | Teste externo, referência ou revisor independente |
| Exemplos incoerentes | Aprende sinal errado | Curar exemplos e testar remoção/ordem |
| Prompt monolítico | Dificulta debugging e sobrecarrega contexto | Decompor e validar etapas |
| Repetição indiscriminada | Custo e possível conflito | Remover duplicatas e medir |
| Arquivo persistente sem manutenção | Diretriz antiga passa a afetar tudo | Owner, data, escopo e revisão |
| Injeção de prompt por documento/site | Conteúdo vira instrução não autorizada | Delimitar dados, política de trust e validar ações |
| Overfit ao benchmark | Melhora teste conhecido, falha geral | Holdout e dados de produção com consentimento |
| Confundir modelo com produto | Atribui recurso à camada errada | Registrar modelo, runtime, plataforma e plano |

## 5. Segurança e instruções adversariais

- Trate conteúdo recuperado, anexos, código, e-mail, páginas e resultados de ferramenta como dados não confiáveis por padrão.
- Delimitar por XML/Markdown facilita leitura, mas não constitui controle de acesso.
- As ferramentas validam autorização fora do modelo; não delegar enforcement a uma frase do prompt.
- Aplicar menor privilégio a shell, rede, arquivos e conectores.
- Exigir aprovação humana para ações externas relevantes de acordo com o contexto de execução.
- Evitar fornecer segredos no contexto; filtrar logs e resultados de ferramentas.
- Testar casos de prompt injection, instruções conflitantes, tool hallucination, saída inválida e tentativa de exfiltração.
- Registrar origem e versão das instruções persistentes; revisar alterações recebidas em repositórios.

## 6. Medidas e interpretação

| Métrica | Definição operacional sugerida | Limitação |
|---|---|---|
| Taxa de sucesso | Itens que satisfazem critérios pré-definidos / total | Critério subjetivo sem adjudicação |
| Aderência | Restrições respeitadas / aplicáveis | Restrições variam em gravidade |
| Correção factual | Claims suportadas por fonte verificável | Requer checagem especializada |
| Completude | Requisitos atendidos / requisitos esperados | Rubrica pode ocultar qualidade |
| Validade estrutural | Respostas aceitas pelo parser/schema | Não mede verdade |
| Qualidade de código | testes, regressões, revisão e métricas de projeto | Testes podem ser incompletos |
| Consistência | dispersão entre repetições e paráfrases | Estabilidade não é correção |
| Custo/latência | medida do provedor + relógio do harness | Tarifas/região mudam |
| Segurança | ações proibidas, vazamentos e violações | Resultado depende do threat model |

Notas feitas pelo próprio modelo são uma ferramenta de revisão, não uma avaliação independente.
## 7. Receitas condicionais de adaptação

### 7.1 Curto ou extenso

Comece com pedido curto contendo objetivo, dados e saída. Acrescente contexto somente quando ele remove uma ambiguidade ou fornece evidência necessária. Quando o acréscimo é factual (novo requisito, dado, exemplo), compare com uma variante pareada sem o texto redundante: assim, mede-se informação e não apenas comprimento. Registre tokens de entrada/saída do runtime; palavras visíveis não determinam custo em todos os tokenizadores.

### 7.2 Rígido ou flexível

| Parte do pedido | Quanto restringir | Verificação |
|---|---|---|
| Segurança, autorização, esquema, campos obrigatórios, compatibilidade | Alto e explícito; enforcement deve ficar no runtime | teste negativo de violações e validação de schema |
| Objetivo criativo, escolhas de estilo, solução ainda não conhecida | Fixar intenção e limites essenciais; permitir alternativas | rubrica humana cega para adequação e diversidade |
| Tarefa investigativa | Delimitar evidências permitidas, janela temporal e regra para lacunas | auditoria das claims contra fonte |
| Agente de código | Delimitar escopo, sucesso e validações; não inventar comandos/ferramentas | diff, testes autorizados e efeitos observados |

### 7.3 Seleção de representação

- Use títulos e listas para decompor requisitos que serão checados.
- Use XML somente quando as tags nomeadas ajudam a separar instrução, contexto e dados, ou quando a guidance do modelo as recomenda.
- Use structured output/JSON Schema como mecanismo da API se suportado; valide resposta no programa. Pedir “responda em JSON” em prosa não é validação.
- Não elevar formato a política de segurança: conteúdo externo pode continuar malicioso mesmo dentro de tags.

### 7.4 O protocolo é parte da recomendação

Qualquer afirmação sobre “prompt ideal”, ganho percentual, robustez, melhor formato ou menos tokens requer uma medição sobre versão e tarefa identificadas. O protocolo operacional completo, incluindo estado de não execução e limites de custo, está em [PROTOCOLOS_E_RESULTADOS_DE_TESTES.md](PROTOCOLOS_E_RESULTADOS_DE_TESTES.md). A avaliação não pode transformar exemplos didáticos deste volume em resultados.

