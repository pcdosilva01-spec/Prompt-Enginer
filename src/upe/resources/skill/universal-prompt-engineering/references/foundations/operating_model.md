# Modelo operacional

## Camadas que não devem ser confundidas

1. **Modelo:** família e versão/ID que produz a resposta. Catálogo, limite e guidance mudam; confirmar no provedor antes de afirmações atuais.
2. **Interface/API:** endpoint ou produto (por exemplo, aplicativo, API, CLI, IDE). Pode usar modelos diferentes e expor parâmetros distintos.
3. **Harness/plataforma:** monta instruções, contexto, ferramentas, memória e ciclos de agente.
4. **Skill/prompt:** instruções empacotadas ou enviadas àquela sessão. Não cria ferramenta nem garante obediência.
5. **Permissão/enforcement:** controles do runtime (aprovação de tool, sandbox, ACL, hooks). Uma instrução em linguagem natural não substitui esses controles.

Essa distinção é central nos Volumes 1–3 e na Matriz R-01–R-14 do dossiê original.

## Identifique a intenção antes de escolher a técnica

Classifique em: criação, reescrita, adaptação de modelo, adaptação de plataforma, diagnóstico, avaliação, comparação, template, instruções de agente, programação ou automação. Uma análise que não cria nem reescreve um prompt final pode ser entregue diretamente. Qualquer novo prompt definitivo ou versão reescrita exige aprovação prévia do resumo atual.

## Requisitos e pressupostos

Separe quatro conjuntos:

- Requisitos obrigatórios citados pelo usuário.
- Preferências desejáveis, que podem ser negociadas.
- Restrições (formato, ferramenta, dados, escopo, orçamento, risco).
- Pressupostos inferidos pelo agente, explicitamente rotulados e aprovados se materiais.

Não preencha lacunas com invenção. Faça perguntas só se a resposta alterar estratégia, segurança, resultado ou aceitação. Se algo puder ser assumido com baixo impacto, declare a suposição no resumo.

## Evidência

Uma orientação de fornecedor descreve o que aquele fornecedor recomenda para produtos/contextos indicados; não é comparação independente. Um experimento vale para a combinação exata de modelo, versão, harness, tarefa, parâmetros e corpus. Uma síntese não testada é hipótese ou regra de projeto, nunca benchmark. Consulte `../evidence/source_policy.md`.
