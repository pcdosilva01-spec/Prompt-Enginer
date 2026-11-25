# Relatório de melhorias do dossiê

**Data:** 23 nov. 2026 (Brasília). **Objeto:** dossiê existente, seis volumes. **Método:** leitura integral dos oito arquivos originais; nova busca e abertura direta de documentação oficial e estudos; auditoria de cobertura, precisão, consistência e rastreabilidade. A skill futura não foi implementada.

## 1. Diagnóstico das notas anteriores

As notas iniciais (pesquisa 7,15; dossiê 7,40; auditoria 8,00) correspondiam a deficiências reais. A cobertura de plataformas era desigual; a página oficial de prompting do Gemini estava marcada como não recuperada; Roo Code não estava atualizado ao estado de encerramento; Cline, OpenCode e Gemini CLI não possuíam fichas; fontes não tinham ledger uniforme de data e afirmação; não havia matriz requisito-verificação; critérios e correções não estavam ligados por IDs; os protocolos não continham plano operacional completo.

## 2. Melhorias comprováveis

| ID | Mudança executada | Evidência / verificação | Arquivos |
|---|---|---|---|
| M-01 | Corrigida a ausência atribuída ao Gemini; a documentação oficial recomenda exemplos few-shot, orientação identificada como própria do fornecedor | E-20, página aberta em 23/11/2026 | V2, V4, V6 |
| M-02 | Atualizada a fotografia dos modelos e separadas API, produto e disponibilidade | IDs exatos nos catálogos oficiais OpenAI, Anthropic, Google, DeepSeek, Mistral e xAI | V2, matriz |
| M-03 | Acrescentadas fichas de Cline, OpenCode e Gemini CLI; Roo Code classificado como projeto encerrado em 15/05/2026 | E-23 a E-27 | V3, V6 |
| M-04 | Corrigido Windsurf: anúncio e changelog recentes confirmam produto 2.0 ativo; Cascade é legado e o redirect para Devin Local não prova equivalência; disponibilidade por conta permanece não verificada | E-28, redirecionamento aberto | V3, lacunas |
| M-05 | Separados ChatGPT, Work e Codex, incluindo modelos e instruções por superfície | Help Center, release notes, docs Codex; E-18 | V3 |
| M-06 | Diferenciada instrução carregada de controle determinístico de permissões/hooks | Docs de Claude Code, Cursor, Copilot, Cline, OpenCode, Antigravity e Gemini CLI | V1, V3, V4 |
| M-07 | Registradas divergências entre recomendações sobre exemplos e formatação, sem inferir regra universal | Gemini, Mistral, Anthropic e OpenAI; E-06, E-20, E-21 | V2, V4, V6 |
| M-08 | Ampliadas fontes científicas sobre personas, otimização automática e pipelines programáticos | EMNLP Findings, APE, OPRO, DSPy e Prompt Report | V1, V6 |
| M-09 | Criado inventário de lacunas com gravidade, impacto, evidência, complexidade, prioridade, critérios e status | L-01 a L-20 | REGISTRO_DE_LACUNAS.md |
| M-10 | Criada matriz requisito→arquivo→fonte→verificação | R-01 a R-24 | MATRIZ_DE_VERIFICACAO.md |
| M-11 | Criados protocolos reproduzíveis, sem declarar experimentos fictícios | P-01 a P-05 | PROTOCOLOS_E_RESULTADOS_DE_TESTES.md |
| M-12 | Criadas rubricas separadas, com pesos, cálculo e limitações | AVALIACAO_FINAL.md, AUDITORIA_FINAL.md | Entregáveis |
| M-13 | Separado enforcement de ativação de Team Rules no Cursor de garantia de aderência do modelo | Cursor Rules oficial reaberta; L-19/E-14 | V1, V3, V6, matriz, lacunas |
| M-14 | Convertidas três matrizes com espaços em tabelas Markdown válidas | varredura de todos os Markdown; L-20 | V1, matriz de verificação, auditoria final |

## 3. Fontes complementares

Foram reconsultadas fontes primárias de OpenAI, Anthropic, Google, Meta, Qwen, DeepSeek, Mistral, xAI, GitHub, Cursor, Antigravity, Aider, Cline, OpenCode e repositórios oficiais de Gemini CLI e Roo Code, além de estudos científicos sobre prompting e avaliação. O Volume 6 registra título, instituição, URL, data publicada/atualizada quando a própria página exibe, data de verificação e o limite da conclusão. Quando a página não fornece data editorial, isso é explicitado em vez de inferido.

## 4. Arquivos

**Atualizados:** README.md, INDICE_GERAL.md, VOLUME_1_FUNDAMENTOS.md, VOLUME_2_MODELOS.md, VOLUME_3_PLATAFORMAS_AGENTES.md, VOLUME_4_TECNICAS_TESTES_SEGURANCA.md, VOLUME_6_AUDITORIA_REFERENCIAS.md.  
**Criados:** este relatório, REGISTRO_DE_LACUNAS.md, MATRIZ_DE_VERIFICACAO.md, PROTOCOLOS_E_RESULTADOS_DE_TESTES.md, AUDITORIA_FINAL.md e AVALIACAO_FINAL.md.

O Volume 5 foi lido e mantido porque seus requisitos continuavam válidos e não implementam a skill. Não houve remoção de conteúdo técnico válido. A matriz de Cursor foi refinada após nova leitura direta da seção de Team Rules; L-19 registra a correção.

## 5. Verificações e testes

Nenhum teste de inferência foi executado. Não havia chave ou sessão API, runtime local de modelo nem conjunto de avaliação autorizado identificado; nenhum crédito ou serviço pago foi utilizado. Uma inspeção local de executáveis conhecidos não encontrou Ollama, llama.cpp, LM Studio, Aider, Gemini CLI, Claude Code, Cline ou OpenCode. Foram executadas verificações documentais: abertura de páginas e changelogs, confirmação de redirecionamentos, leitura de datas apresentadas e confronto de afirmações com as fontes.

Na auditoria local final, uma varredura dos 14 arquivos Markdown encontrou zero destino relativo inexistente e zero tabela pipe com contagem divergente de colunas. A checagem cobre estrutura local; não verifica disponibilidade nem conteúdo atual das URLs remotas.

A checagem de links foi orientada por alegações e amostral, com abertura direta das fontes mais críticas; não foi crawler exaustivo de cada link de todos os volumes.

## 6. Limites restantes

1. Sem avaliação experimental pareada, versões fixadas, custos, latências ou resultados em corpus holdout.
2. Sem terceiro revisor independente; a auditoria é interna e feita em passagens separadas.
3. Alguns fornecedores/produtos agregadores seguem fora da amostra aprofundada e estão formalmente delimitados.
4. Windsurf 2.0 está ativo segundo anúncio e changelog; Cascade é legado. Disponibilidade de modelo/recurso por plano e configuração efetiva em conta não foram auditadas.
5. Várias páginas vivas não informam data de atualização; a data de verificação não substitui essa informação.
6. Modelos, preços, limites, planos, disponibilidade regional e recursos são fotografia de 23/11/2026.

## 7. Reavaliação

Notas finais: pesquisa **9,24/10**, dossiê **9,48/10**, auditoria **9,43/10**. Não atribuo 10: permanecem sem evidência os resultados empíricos e a revisão externa independente. Os critérios, pesos, contas e razões estão em AVALIACAO_FINAL.md.









