# Revisão e entrega

Use esta lista antes de emitir um prompt definitivo:

1. Confira aprovação explícita da revisão mais recente e preservação dos requisitos. Sem ambas, volte ao [fluxo de aprovação](approval_and_correction.md).
2. Revise o texto inteiro quanto a fidelidade, completude, clareza, consistência, destino, viabilidade, segurança e critérios de aceitação. Corrija defeitos materiais antes de liberar a entrega. Se o texto mudar, revise e avalie novamente.
3. Avalie o artefato efetivamente entregue com [os dez critérios oficiais](../references/evaluation/prompt_rubric.md). Exiba os pesos, notas e justificativas observáveis, o cálculo ponderado e a nota final. Aplique os tetos da rubrica, sem arredondar para 10. Declare pontos fracos, correções, oportunidades restantes e limites. Não declare ensaio do modelo ou latência sem medir.
4. Prepare a saída na ordem do [modelo de entrega](../templates/optimized_prompt.md): prompt completo isolado, link TXT, configurações e fundamentação, autoavaliação, limites e oferta de otimização. Use bloco de escrita nativo com cópia somente se suportado. Nos demais casos use um bloco único de texto puro, com cerca mais longa se houver crases dentro do prompt. Se houver capacidade de arquivo, grave exatamente o texto em UTF-8, sem BOM ou quebra adicional, confira a equivalência byte a byte e valide o link/anexo no host antes de anunciar. Se indisponível, explique brevemente a limitação e conserve o formato copiável.
5. Quando integrado, passe a entrega por `prepare_delivery` e `deliver` de acordo com [o contrato local](interaction_integration.md). Em fallback, faça a mesma conferência na resposta a enviar.
6. Finalize com a pergunta literal abaixo, sem texto posterior. Se o usuário aceitar, volte ao [fluxo de aprovação](approval_and_correction.md).

Deseja que eu otimize ainda mais este prompt, buscando a maior nota de qualidade tecnicamente justificável?
