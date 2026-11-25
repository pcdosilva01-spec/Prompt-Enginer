# Auditoria final do dossiê

**Data:** 23/11/2026. **Escopo auditado:** os seis volumes, índice, README e os seis entregáveis complementares; a implementação da skill futura ficou fora do escopo conforme pedido.

## 1. Método e independência

A auditoria repetiu a revisão em três passagens distintas:

1. **Passagem de cobertura:** confrontou cada requisito do pedido com a matriz R-01–R-24 e L-01–L-20 e identificou requisitos ausentes, parciais e formalmente delimitados.
2. **Passagem adversarial de claims:** buscou falsa atualidade, mistura de modelo/produto, recomendação universal sem prova, leitura de guidance como benchmark, inferência de status a partir de redirecionamento, e confusão entre instrução e enforcement.
3. **Passagem de consistência/contabilidade:** conferiu IDs das lacunas, estados, fontes, notas anteriores/finais, critérios e somas ponderadas.

A checagem foi realizada pela mesma equipe/instância que revisou o material. As passagens são separadas e críticas, porém **não equivalem a revisor externo independente nem a múltiplos avaliadores cegos**. Essa limitação reduz a nota de independência e reprodutibilidade.

## 2. Achados críticos e resolução

| Achado | Gravidade | Evidência | Resolução | Estado |
| --- | --- | --- | --- | --- |
| Gemini prompting marcado como não localizado | Alta | página de estratégia oficial, incluindo recomendação forte de few-shot | orientação documentada e limitada ao fornecedor; L-01 | Fechado documentalmente |
| Roo Code em estado incerto | Alta | aviso oficial de sunset e repositório arquivado | classificado como encerrado/legado; L-02 | Fechado documentalmente |
| Cline/OpenCode/Gemini CLI sem pesquisa | Alta | docs primários atuais e, no Gemini CLI, changelog datado | fichas acrescidas; V3; L-03–L-05 | Fechado documentalmente |
| ChatGPT, Work e Codex tratados juntos | Alta | release notes descrevem superfície/modelos/rollout diferentes | matriz por superfície; L-07 | Fechado documentalmente |
| Status do Windsurf inferido apenas pela URL antiga de Cascade | Alta | anúncio oficial Windsurf 2.0 (15/04/2026), changelog do editor (20/11/2026) e redirect legado | confirmada atividade atual; Cascade classificado como legado; disponibilidade por conta/modelo ainda não verificada; L-06/E-28 | Parcialmente fechado |
| Métricas anteriores não tinham pontuação verificável por critérios independentes | Alta | faltava conta auditável por critério | tabelas com pesos uniformes, razões e cálculo | Fechado metodologicamente |
| Cursor Team Rules confundidas com garantia de obediência do modelo | Média | página Rules prevê ativação obrigatória pela equipe, mas não garante aderência semântica | separado enforcement da configuração de cumprimento do modelo; L-19/E-14, V1/V3/V6 | Fechado documentalmente |
| Experimentos ausentes | Alta | sem runtime/credenciais/corpus identificados | nenhum resultado alegado; protocolos preparados | Aberto por dependência de ambiente |
| Matrizes alinhadas por espaços, não por sintaxe Markdown | Média | varredura dos arquivos encontrou três tabelas inválidas | convertidas em tabelas Markdown; nova varredura sem candidatos; L-20/M-14 | Fechado documentalmente |
| Auditoria sem terceira pessoa | Alta | não houve revisor externo disponível | limitação exposta; revisão externa recomendada | Aberto |

## 3. Conclusões técnicas testadas criticamente

- **Comprimento:** não há tamanho ótimo universal demonstrado neste dossiê. Orientação “mais é melhor” foi removida; contexto adicional é variável experimental.
- **Rígido/flexível:** usar critérios rígidos para requisitos de aceitação, interfaces e segurança; deixar espaço de decisão nas partes incertas/criativas. Isso é uma regra de projeto, não um resultado de benchmark universal.
- **Markdown/XML/JSON:** delimitadores ajudam a distinguir seções segundo docs de alguns fornecedores; não são controle de segurança. JSON Schema é contrato da API quando a interface suporta e também requer validação.
- **Exemplos:** documentação Gemini recomenda incluí-los; isso é orientação do fornecedor. A decisão continua condicionada à tarefa, custo, representatividade e validação própria.
- **Raciocínio:** estudos clássicos têm resultados específicos; guias de modelos atuais divergem. Não se recomenda exigir cadeia privada. Pedir conclusão, premissas verificáveis e checagem externa é mais auditável.
- **Memória e agentes:** arquivos persistentes e memória são contexto, salvo mecanismos de enforcement. Ferramentas, hooks e permissões pertencem ao runtime.
- **Plataformas:** uma recomendação não atravessa automaticamente API, aplicativo, IDE, CLI ou plano. Matriz agora separa superfícies e suas condições.
- **Evidência científica:** estudos são relatados com seus limites e não são apresentados como replicados no projeto.

## 4. Verificações realizadas

- Leitura integral do conjunto original de oito arquivos, registrada no relatório de melhorias.
- Abertura direta de documentação oficial de modelos, prompting, permissões, regras, memória e changelogs.
- Verificação de data explícita quando exibida; “não indicada na página consultada” onde ausente.
- Abertura do anúncio Windsurf 2.0, changelog mais recente, modelo listado e destino da URL legada de Cascade; conferência do estado de arquivo do Roo Code.
- Inspeção local não invasiva de disponibilidade de runtimes conhecidos; não foram encontrados comandos/modelos locais.
- Cruzamento entre REGISTRO_DE_LACUNAS.md, MATRIZ_DE_VERIFICACAO.md, Volume 6 e avaliação.
- Varredura de sintaxe de tabelas Markdown e validação de contagem de colunas; os três blocos inválidos encontrados foram convertidos e a varredura posterior não encontrou outros candidatos.
- Varredura local dos 14 arquivos Markdown: 227 destinos Markdown identificados, nenhum link relativo inexistente e nenhuma tabela pipe com divergência de colunas. URLs remotas não são consideradas verificadas por este teste estrutural.
- Revisão de afirmações que poderiam soar universais ou experimentais; categorias de evidência ajustadas.

Não foi feito crawler de todos os links, instalação de plataformas, acesso a conta externa, execução de código fornecido por fonte, nem chamadas de modelo.

## 5. Itens para liberar 10/10 em revisão futura

1. Um segundo avaliador qualificado, sem autoria das correções, repete leitura e pontua a rubrica sem ver as notas iniciais.
2. Um terceiro avaliador faz verificação aleatória de pelo menos 20 claims e de todos os claims críticos contra a página primária.
3. Executar o protocolo P-01–P-02 com versões exatas, corpus holdout e orçamento aprovado; incluir resultados negativos e intervalos.
4. Conferir em conta/planos quais recursos e modelos estão disponíveis no Windsurf 2.0; aprofundar Continue, Microsoft Copilot, Perplexity e agregadores formalmente delimitados.
5. Conferir todos os links automaticamente e manualmente os destinos que mudaram.
6. Recalcular a avaliação depois de as dependências acima produzirem evidência real.

## 6. Parecer

O dossiê foi corrigido de forma substancial e a trilha de auditoria é verificável. Não há erro crítico conhecido não resolvido em conteúdo afirmado como atual: status desconhecidos estão marcados, e dados temporais são apresentados como snapshot. Contudo, falta evidência empírica e revisão externa independente; por isso, a auditoria não recebe 10/10. As notas e critérios finais estão em AVALIACAO_FINAL.md.







