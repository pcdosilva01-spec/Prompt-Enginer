# Adaptação por modelo

## Regra de decisão

Não existe uma técnica de prompt superior em todas as famílias, tarefas, versões e interfaces. Primeiro verifique documentação primária do **ID exato e do endpoint**; depois faça uma comparação controlada se o usuário precisa de desempenho comparativo. Caso contrário, use a síntese estável abaixo e rotule-a como orientação, não como prova de superioridade.

| Família/fonte | Distinção documentada que pode orientar | O que não concluir |
|---|---|---|
| OpenAI | Orientações de prompting e reasoning variam por modelo/tarefa/API; structured output é uma capacidade do endpoint/runtime quando suportada. Veja E-01/E-02 no Volume 6. | Não extrapolar guidance de API para ChatGPT/Codex nem exigir CoT privada. Nome de modelo não garante acesso no plano/conta. |
| Anthropic | Claude prompting docs atribuem valor a instruções claras, contexto delimitado e estruturas; Claude Code acrescenta arquivos de skill, frontmatter e controle de ferramentas. Veja E-06/E-19. | Não tratar instruções/prompt como permissão ou garantia semântica. Claude Code, claude.ai, Cowork e API diferem. |
| Google | Gemini prompting docs documentam exemplos e organização explícita; Gemini CLI/Antigravity têm camada de skill/harness distinta da API. Veja E-20/E-25. | Uma preferência documentada não é resultado comparativo. Não confundir Gemini CLI, AI Studio/API e Antigravity. |
| Mistral | Docs de prompting descrevem formatos/instruções para famílias e interfaces documentadas. Veja E-21. | Não extrapolar formatos de uma família/checkpoint para todas as variantes. |
| Meta, DeepSeek, Alibaba/Qwen, xAI e outros | Consultar o catálogo, model card e guia de prompting atuais para ID/API/peso aberto específico; o dossiê integral conserva o levantamento e suas ressalvas. | Não inventar diferenças sem fonte atual; não tratar família como modelo único nem assumir que app aceita o mesmo formato da API. |

Links primários e claims detalhados estão no Volume 2 e no ledger E-01–E-34 do Volume 6. Este pacote não tenta congelar uma lista de SKUs que envelhece rapidamente. Consultar fonte ao vivo quando versionamento/disponibilidade impactar a decisão e registrar o snapshot consultado.

## Matriz curta de decisão

- **Reasoning model:** declarar objetivo, restrições e critérios; usar esforço/parâmetros do endpoint se documentados. Pedir resposta verificável, premissas e checagem apropriada; não pedir cadeia interna privada.
- **Modelo orientado a instruções/chat:** declarar tarefa e saída; separar contexto de comando; usar exemplos só quando ensinam padrão difícil de enunciar e são representativos.
- **Código/agente:** modelo é apenas uma parte. Adaptar ao harness, contexto de repositório, ferramentas e permissões; validar diff/testes e efeitos observáveis.
- **Modelo/versão desconhecida:** oferecer baseline agnóstico, evitar sintaxe exclusiva, assinalar o que não foi verificado e perguntar pelo destino se a diferença for material.

## Atualidade e comparação

Catálogo, preço, limite de tokens, latência e rollout são voláteis. Não copie números do dossiê como estado atual. Em comparação real, mantenha constantes tarefa, versão, contexto, parâmetros e harness; pré-registre métrica e orçamento; informe resultados nulos/negativos. Se tais condições não forem satisfeitas, descreva a diferença documental sem alegar benchmark.
