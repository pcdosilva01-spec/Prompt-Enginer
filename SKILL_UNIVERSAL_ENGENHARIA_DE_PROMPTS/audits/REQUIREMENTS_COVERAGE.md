# Cobertura e lacunas remanescentes

## Conclusão da cobertura

Os 36 grupos do prompt de implementação e os 24 requisitos históricos foram cruzados na [`TRACEABILITY_MATRIX.md`](TRACEABILITY_MATRIX.md). A maior parte da arquitetura documental foi criada. A existência de texto não valida aderência de um modelo: os seguintes itens continuam pendentes ou parciais.

| ID/lacuna | Gravidade/impacto | Evidência | Resolução/ação | Estado verificável |
|---|---|---|---|---|
| C-01 Teste de conversa em LLM | Alta/Alta | Nenhum endpoint/runtime autorizado utilizado | Protocolo e 10 cenários fornecidos; não alegar aderência | Bloqueado por limitação externa: modelo/credencial/orçamento autorizado indisponível |
| C-02 Instalação em hosts | Média/Alta | Nenhum cliente/configuração modificado | Instruções e matriz documental; instalação pertence ao usuário e requer cliente alvo | Documentado, mas não testado |
| C-03 Revisão externa | Alta/Alta | Esta auditoria é feita na mesma sessão que implementou | Entregue ledger, hashes, testes e critérios para revisor independente | Bloqueado por limitação externa: terceiro independente não participa |
| C-04 Model catalog para cada SKU | Média/Alta | Vol. 2 tem pesquisa ampla; esta rodada foca formato/skills | Revalidar ID/endpoints na solicitação; evitar números congelados | Implementado parcialmente |
| C-05 Aider skill nativa | Média/Média | Não localizada fonte oficial atual na pesquisa da implementação | Descrever como não verificado, adaptar manualmente após consulta | Bloqueado por evidência insuficiente; nenhuma capacidade inventada |
| C-06 Windsurf/Cascade atual | Média/Alta | URL antiga redireciona para Devin Local | Marcar status da equivalência não confirmada | Documentado, mas não testado |
| C-07 Red-team de injeção do modelo | Alta/Alta | Sem execução de inferência | Threat model e casos 9; protocolo para futura execução | Bloqueado por limitação externa |
| C-08 Atualização futura | Média/Média | Fontes são páginas vivas | Data de verificação em ledger e procedimento de manutenção | Documentado, acompanhamento não automatizado |
| C-09 Tipos inesperados no helper | Média/Alta | Testes reproduziram estado falsy não-objeto e `AttributeError` em eventos/campos malformados | `GateError` explícito em state/event/reason/diagnosis; 5 testes de regressão | Corrigido e verificado |
| C-10 Substituição segura do ZIP | Média/Alta | Falha simulada mostrava truncamento do ZIP anterior durante gravação direta | staging temporário, validação CRC/hash/inventário, `os.replace`; rejeição de symlink em entrada e destino; 3 testes | Corrigido e verificado; symlink de filesystem real não foi criado por restrição do Windows |
| C-11 Cópia do dossiê desatualizada | Média/Alta | Comparação origem/cópia falhava em três relatórios após atualização da fonte | versões antigas salvas em `work/skill_sync_backup_2026-11-23`; cópias sincronizadas e manifestos regenerados | Corrigido; 14/14 SHA-256 iguais |

Não há resultado simulado apresentado como experimento. Para liberar pendências bloqueadas, serão necessários runtime/modelo e orçamento explicitamente autorizados, instalação em superfícies específicas e avaliador externo.
