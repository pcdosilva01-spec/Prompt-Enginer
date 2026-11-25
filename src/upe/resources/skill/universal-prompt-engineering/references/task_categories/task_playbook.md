# Playbook por categoria de tarefa

Em pesquisa, código, UI e automação, verifique também a linguagem do resultado. Se houver prosa PT-BR, carregue a [especialização Humanizer](../writing/humanizer.md) e delimite os trechos editáveis.

| Tarefa | Campos que normalmente importam | Validação do resultado |
|---|---|---|
| Pergunta/resposta | pergunta, contexto de referência, limite de escopo, formato | veracidade e suporte no contexto/fonte |
| Pesquisa | pergunta, período, fontes permitidas, método, claims verificáveis, forma de citação | abrir fonte primária; comparar fontes; distinguir fato, inferência e incerteza |
| Síntese | material, público, extensão, cobertura, itens obrigatórios | verificar cobertura e fidelidade ao material, inclusive omissões |
| Extração/classificação | schema, classes, tratamento de ausente/ambíguo, exemplos | validação schema, exact match/macro-F1, auditoria de erros |
| Escrita/criação | finalidade, público, voz, limites, fatos obrigatórios, saída | critério editorial e checagem factual; evitar instruções de estilo conflitantes |
| Código | repositório/stack, comportamento, constraints, interfaces, testes, critério de conclusão | diff revisado, testes permitidos, build/lint relevantes, efeitos colaterais observáveis |
| Agente | objetivo, ferramentas permitidas, permissões, critérios de sucesso, retries, parada/falha | avaliar ação e argumentos, não só prosa; sandbox e logs redigidos |
| Automação | gatilho, entradas, destino, autorização, idempotência, reversão, erro | dry-run se possível, aprovar mutação externa, confirmar estado final |
| Saída estruturada | schema, campos required/nullable, enum, erros, versão do consumidor | parse + validação schema + correção semântica |
| Comparação/avaliação de prompts | variável isolada, modelo/superfície, corpus, métricas, orçamento | protocolo pré-registrado, múltiplas execuções/holdout e reportar limites |

Não aplique todos os campos por padrão. Se faltarem dados essenciais, pergunte antes do resumo final de entendimento ou faça hipótese explícita de baixo impacto. O fluxo de aprovação ainda se aplica antes de produzir o prompt final.
