# Protocolos e resultados de testes

**Versão:** 1.0, 23/11/2026. Este documento separa execução observada de plano futuro. Nenhuma saída simulada ou inventada é apresentada como resultado.

## 1. Estado da execução

| Item | Estado real |
|---|---|
| Testes de geração em modelo/API | Não executados |
| Testes pagos/créditos | Nenhum; nenhum crédito consumido |
| Runtimes locais verificados no PATH/processos conhecidos | Nenhum executável reconhecido encontrado |
| Corpus do usuário / holdout autorizado | Não identificado |
| Verificações realizadas | Pesquisa documental, abertura de fontes, changelogs, destinos de redirecionamento, inspeção de executáveis e varredura estrutural local dos 14 Markdown (227 destinos, 0 links relativos ausentes, 0 tabelas com colunas divergentes) |
| Resultado experimental | N/A; não há estimativas de qualidade, custo ou latência deste projeto |

A falta de teste não prova que as recomendações funcionam ou falham. Não havia serviço/modelo autorizado e acessível. Se uma conta paga ou consumo de crédito for necessário, a execução aguarda autorização específica; as alternativas locais não serão baixadas automaticamente.

## 2. Protocolo comum de pré-registro (P-01)

Antes de qualquer chamada, preencher e congelar:

1. **Pergunta e hipótese:** qual fator será variado e qual efeito se espera observar.
2. **Unidade e amostragem:** domínio, idioma, risco, origem e divisão development/holdout.
3. **Modelo e superfície:** nome/ID completo e snapshot; API, endpoint, produto, plano/região e data.
4. **Harness:** versão, instruções persistentes, contexto, ferramentas, permissões e política de retry.
5. **Prompt integral e parâmetros:** ordem de mensagens, template nativo, temperatura/effort, limite de saída, seed quando suportada.
6. **Orçamento:** quantidade máxima de chamadas, tokens e custo calculado por tabela oficial vigente; corte automático ao teto.
7. **Métricas e rubrica:** definir antes de olhar respostas e decidir a métrica primária.
8. **Repetições e exclusões:** registrar falha, timeout, bloqueio e tratamento; não descartar erro seletivamente.
9. **Cegamento:** anonimizar variante para avaliadores humanos sempre que possível.
10. **Reprodutibilidade:** arquivar versão de prompts, hash do conjunto sem dados sensíveis, logs de parâmetros, timestamp e outputs permitidos.

Não trocar modelo ou prompt durante uma execução. Repetição não equivale a amostra independente quando a mesma tarefa é usada.

## 3. Conjunto de avaliação proposto

Preparar pelo menos cinco conjuntos separados, em português e inglês se esse for o uso previsto:

- **Extração/classificação:** itens com resposta-ouro e exemplos ambíguos; incluir ausências e múltiplos rótulos.
- **Síntese factual:** documentos com claims rastreáveis e distratores; especialistas validam a rubrica.
- **Código:** issues reproduzíveis em repositórios isolados, com testes de regressão e ambiente congelado.
- **Raciocínio/cálculo:** problemas cuja resposta possa ser verificada por calculador, referência ou programa.
- **Agentes/ferramentas:** tarefas com sandbox, arquivos fictícios e efeitos colaterais observáveis; sem credenciais reais.

Sugestão inicial: piloto de 20–30 itens para estimar variância e calibrar rubrica; o tamanho final deve vir de análise de poder baseada na diferença mínima relevante, variância observada e taxa base. Não declarar que esse piloto já existe.

Manter um holdout lacrado. Duas pessoas anotam independentemente respostas sensíveis à interpretação; registrar acordo e adjudicar desacordos sem ocultar o desacordo inicial.

## 4. Comparações controladas

| ID | Pergunta | Controle | Variante | Métrica primária | Controle de confusão |
|---|---|---|---|---|---|
| P-02A | Mais detalhe ajuda? | pedido mínimo suficiente | acrescentar contexto e instruções relevantes | taxa de sucesso por tarefa | separar quantidade de informação da quantidade de palavras com variante fatorial |
| P-02B | Estrutura melhora aderência? | prosa concisa | mesmos requisitos em seções Markdown/XML | rubric score e omissões | conteúdo semântico idêntico; comparabilidade de tokens registrada |
| P-02C | Schema melhora extração? | saída JSON pedida em prosa | JSON Schema/structured output suportado pela API | taxa de parse e exact match | registrar mecanismo do runtime; não atribuir o efeito só ao prompt |
| P-02D | Exemplos ajudam? | zero-shot | few-shot consistente e representativo | macro-F1 / exact match | congelar exemplos; medir tokens e testar qualidade/ordem como fatores separados |
| P-02E | Persona ajuda a factualidade? | sem persona | papel contextual curto | claims corretos e suportados | manter domínio/contexto igual; não pontuar apenas estilo |
| P-02F | Pedido explícito de CoT ajuda? | solicitar resposta e checagem verificável | instrução de “passo a passo” somente se permitido pelo modelo | acurácia e segurança da justificativa | nunca solicitar cadeia privada em sistema que orienta a não fazê-lo; medir output final |
| P-02G | Posição importa em contexto longo? | evidência na posição fixa de controle | mesma evidência deslocada início/meio/fim | recall de fonte e resposta correta | texto total e evidência idênticos; permutar posição em pares |
| P-02H | Prompt específico do fornecedor vence um genérico? | baseline comum | guidance atual para a versão | qualidade, custo, latência | mesmo orçamento; registrar tuning e risco de otimização desigual |
| P-02I | Harness muda sucesso ponta a ponta? | chamada sem ferramenta/contexto adicional | ferramenta/agent conforme tarefa | sucesso ponta a ponta e ação incorreta | reportar separadamente qualidade do modelo, retrieval, ferramenta e runtime |

Não concluir causalidade entre modelo e plataforma a partir de uma comparação em que ambos mudaram. Para comparação entre fornecedores, rodar cada prompt em cada versão e apresentar interação modelo×variante, não apenas médias agregadas.

## 5. Métricas e análise

- **Exatidão:** exact match, acurácia ou macro-F1, segundo a tarefa e distribuição de classes.
- **Grounding:** fração de claims corretos e fração de claims com suporte; citar fonte errada conta como erro.
- **Aderência:** itens de rubrica cumpridos; gravidade de violações pré-definida.
- **Estrutura:** JSON parseável e válido contra schema, além de correção dos valores.
- **Código:** testes preexistentes, novos testes relevantes, regressões e avaliação cega do diff.
- **Agente:** ferramenta escolhida, argumentos válidos, permissões respeitadas, efeito colateral correto e recuperação de falha.
- **Consistência:** distribuição entre repetições; não usar melhor amostra como resultado.
- **Custo/latência:** tokens cobrados ou reportados, tarifa e região vigentes, tempo medido pelo harness e chamadas adicionais.
- **Segurança:** violações do threat model, injeção, vazamento ou ação proibida; critérios de parada imediata.

Reportar intervalos de confiança pareados por bootstrap para métricas contínuas e teste pareado apropriado para rótulos binários; corrigir multiplicidade quando houver várias hipóteses primárias. Publicar tamanho do efeito e intervalo, não apenas valor-p. Se o tamanho amostral não permitir conclusão, marcar como inconclusivo. As métricas automáticas devem ser validadas contra avaliação humana para os domínios em que a rubrica depende de julgamento.

## 6. Sequência de execução recomendada

1. Escolher uma tarefa de baixo risco e um modelo/plataforma realmente disponíveis.
2. Congelar prompt e conjunto de desenvolvimento; fazer piloto e análise de poder.
3. Ajustar apenas no conjunto de desenvolvimento.
4. Pré-registrar variantes, métrica primária, limites e orçamento.
5. Executar todas as variantes em pares sobre o mesmo holdout e sob iguais condições.
6. Fazer avaliação cega e adjudicar divergências.
7. Comparar qualidade, segurança, custo e latência; reportar interações e efeitos negativos.
8. Repetir após mudança de versão de modelo, template, ferramenta ou produto.
9. Arquivar protocolo, resultados, logs redigidos e decisões; revisão externa antes de recomendar implementação em alto impacto.

## 7. Critério de decisão

Uma variante só é recomendada quando melhora a métrica primária acima de uma diferença mínima prática definida antes, não degrada métricas de segurança/estrutura consideradas críticas e cabe no orçamento. Se qualidade empata, preferir solução mais simples apenas depois de registrar custo total e robustez. Resultado só vale para a combinação testada de tarefa, modelo, versão, plataforma, parâmetros e corpus.

