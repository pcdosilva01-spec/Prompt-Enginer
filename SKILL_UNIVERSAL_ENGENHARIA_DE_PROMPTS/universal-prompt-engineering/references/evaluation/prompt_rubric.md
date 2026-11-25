# Rubrica de prompt (0–10)

Aplicar ao **artefato prompt** após aprovação do entendimento. Cada critério recebe 0–10 com justificativa observável. Nota ponderada = Σ(nota × peso)/100. Pesos fixos nesta versão, total 100.

| Critério | Peso | Pergunta observável |
|---|---:|---|
| Objetivo e tarefa | 15 | O resultado e o que o modelo fará estão definidos? |
| Requisitos e fidelidade | 15 | Todos os requisitos obrigatórios e correções do usuário estão preservados? |
| Adequação ao modelo/superfície | 10 | As decisões específicas têm evidência para o ID/superfície ou estão marcadas como agnósticas? |
| Contexto e entradas | 10 | Fontes, dados, pressupostos e limites de contexto estão claros? |
| Restrições e escopo | 10 | Exclusões, limites e condições de parada estão explícitos onde importam? |
| Saída e formato | 10 | Formato, esquema e critérios semânticos são verificáveis? |
| Viabilidade/ferramentas | 10 | O prompt usa apenas capacidades existentes e permite tratamento de falha? |
| Validação/aceitação | 10 | Há verificação proporcional à tarefa, para além de “parece bom”? |
| Segurança | 5 | Fronteiras de confiança, dados e efeitos colaterais estão cobertos? |
| Economia/manutenção | 5 | Conteúdo evita ruído e volatilidade desnecessária? |

## Interpretação

- 0–3: incompleto ou incompatível; reconstruir após corrigir entendimento.
- 4–6: usável somente com riscos/omissões materiais declarados; revisar.
- 7–8: adequado, com limitações localizadas; aplicar correções viáveis.
- 9–9,9: forte contra a rubrica, sem defeitos materiais conhecidos.
- 10: todos os critérios atendidos, evidência específica suficiente, nada material pendente na qualidade do texto. Não significa modelo testado, resultado garantido ou compatibilidade comprovada.

## Teto e honestidade

Defeito material em objetivo/requisito/modelo limita a nota a 6; risco de segurança não mitigado limita a 3; requisito obrigatório ausente impede 10. Se falta contexto por decisão do usuário, distinguir “prompt condicionado à premissa” de erro e citar a premissa. Publicar critério e cálculo, não apenas número. Para medir desempenho real, usar experimentos do protocolo no Volume 4; esta rubrica sozinha não mede desempenho.
