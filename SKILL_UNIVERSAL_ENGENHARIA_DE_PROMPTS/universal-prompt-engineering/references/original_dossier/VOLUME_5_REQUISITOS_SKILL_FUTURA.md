# Volume 5 — Requisitos da skill futura

> Este volume é uma especificação documental. Ele não cria, instala nem implementa a skill futura.

## 1. Propósito e limites

A skill futura deverá ajudar a criar, adaptar e avaliar prompts, mantendo decisões rastreáveis. Deverá consultar a base de conhecimento e fontes externas conforme a modalidade aprovada; reconhecer que recomendações dependem do modelo, da plataforma, da tarefa, dos dados e do risco. Ela não deve prometer um prompt “ótimo” sem avaliação, nem tratar nota automática como evidência.

## 2. Fluxo funcional obrigatório

### Etapa A — Entendimento

Identificar objetivo, resultado esperado, audiência, contexto, destino (modelo e superfície/plataforma), requisitos obrigatórios, preferências, restrições, formato, critérios de sucesso, risco e informações faltantes. Não solicitar de novo fatos já fornecidos.

### Etapa B — Resumo revisável

Antes do prompt final, mostrar entendimento em resumo estruturado, marcando:

- fatos ditos pelo usuário;
- inferências e suposições;
- lacunas materiais;
- conflitos;
- estratégia preliminar;
- fonte de conhecimento escolhida.

### Etapa C — Aprovação

Esperar aprovação explícita do usuário. Sem ela, não gerar o prompt definitivo. Pergunta opcional pode ser evitada se a resposta for inferível; pergunta material deve ser curta e não redundante.

### Etapa D — Correção de entendimento

Se o resumo for recusado: diagnosticar o entendimento anterior com fatos confirmados separados de hipóteses; expor omissões/erros; solicitar somente o contexto necessário; usar respostas anteriores; atualizar o resumo; submeter novamente para aprovação. Não avançar à geração final enquanto a aprovação não existir.

### Etapa E — Seleção de conhecimento

Modos disponíveis:

1. Somente base local/documental.
2. Pesquisa atual na web.
3. Híbrido.
4. Somente material do usuário.
5. Somente documentação oficial especificada.

Perguntar qual modo se a escolha mudar materialmente as conclusões e estiver indefinida. Respeitar limites de pesquisa do usuário. Registrar fontes e data de acesso para claims que dependem de informação variável.

### Etapa F — Construção e autoavaliação

Escolher formato, detalhe, exemplos, delimitadores, estrutura, ferramentas e critérios compatíveis com o modelo/plataforma. Produzir prompt final somente após aprovação. Revisar conflitos, capabilities inexistentes, risco de ferramenta e proveniência do contexto.

## 3. Rubrica de 0 a 10

| Critério | Pergunta de avaliação |
|---|---|
| Clareza | Objetivo e instruções podem ser interpretados de uma maneira previsível? |
| Precisão | Restrições e termos são concretos e não contraditórios? |
| Completude | Contém informações necessárias, sem omissões materiais? |
| Compatibilidade do modelo | Considera capacidades, interface e recomendações verificadas da versão? |
| Compatibilidade da plataforma | Os recursos solicitados existem nesse app/runtime/plano? |
| Adequação à tarefa | O método corresponde ao tipo de trabalho e risco? |
| Organização | Seções, dados e instruções são fáceis de distinguir? |
| Ambiguidades | Lacunas são resolvidas, perguntadas ou explicitamente tratadas? |
| Robustez | Funciona em variações previsíveis da entrada? |
| Eficiência | Detalhe e chamadas não excedem o necessário para qualidade esperada? |
| Testabilidade | Critérios e resultado podem ser avaliados? |
| Probabilidade fundamentada | A estimativa está apoiada por fonte/testes e tem limite declarado? |

Atribuir nota global e justificar com evidências; discriminar pontos fortes, riscos e mudanças feitas. **A rubrica é uma heurística de revisão, não probabilidade estatística.** Uma nota numérica do próprio modelo não prova qualidade. Em tarefa de alto impacto, exigir validação ou revisão apropriada.

## 4. Saída e rastreabilidade

Recomendado registrar por prompt: ID/versão; data; tarefa; plataforma/modelo com versão/alias; modo de pesquisa; fontes; texto de prompt; parâmetros relevantes; exemplos/dados; testes; métricas; limitações; responsável pela aprovação. Separar:

- **fonte** (URL e trecho/claim resumido);
- **observação** (resultado realmente obtido);
- **interpretação** (o que o resultado sugere);
- **hipótese** (o que ainda testar).

## 5. Estratégia de atualização

Versionar módulos por fornecedor, técnica e plataforma. Cada recomendação volátil tem data de conferência, fonte oficial e campo de status. Revalidar quando mudar alias, API, ferramenta, limite, template, política ou versão do produto. Não duplicar um fato em vários módulos: armazenar fonte canônica e referenciar ID. Preservar conteúdo substituído em histórico se necessário para migração, claramente rotulado como legado.

## 6. Testes de aceitação da implementação futura

1. Usuário pede prompt sem especificar plataforma: fluxo coleta ou assinala a falta antes da aprovação.
2. Resumo inclui campos aplicáveis e separa fato de hipótese.
3. Sem aprovação explícita, não há prompt marcado como final.
4. Rejeição dispara diagnóstico específico e não repete perguntas já respondidas.
5. Modo de pesquisa é respeitado e citado.
6. Modelo/plataforma desconhecidos não recebem recomendações inventadas.
7. Prompt criado passa por checagem de ferramentas, conflito, formato e segurança.
8. Autoavaliação pontua critérios e expõe limitações; não se apresenta como validação empírica.
9. Mudança de versão permite rastrear e atualizar fontes dependentes.
10. Regressão mantém dados e referências recuperáveis sem carregar todo corpus em todo pedido.

## 7. Riscos de arquitetura

- O gate de aprovação aumenta turnos e atrito; só é útil se estiver claro o que será aprovado.
- Pesquisa web pode encontrar páginas antigas ou marketing; registrar modelo, página e data.
- Recuperação pode selecionar trechos fora de contexto; preservar referência e qualificação.
- Prompts e logs podem conter segredos/dados pessoais; política de retenção e acesso.
- A nota de 0–10 gera falsa precisão; tratar como comunicação resumida com rubrica, nunca como calibração probabilística.
- Base de conhecimento pode fossilizar recomendações; owner e revisão são requisitos funcionais.

## 8. Fora de escopo nesta etapa

Não há arquivo de skill, YAML de ativação, instruções operacionais instaláveis ou integração. O resultado é conhecimento e requisitos para a etapa futura.
