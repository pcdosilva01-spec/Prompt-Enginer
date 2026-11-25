# Seleção dinâmica de modelo e esforço

Aplique em toda entrega definitiva. Selecione antes de numerar o resumo e mostre a recomendação aprovada novamente nas configurações finais. Reabra a aprovação ao mudar materialmente o destino. Use [adaptação por modelo](model_adaptation.md) para ajustar o texto à superfície aprovada.

1. **Registre a demanda.** Tarefa, complexidade, contexto (volume, tipos de entrada, privacidade), ferramentas/modalidades/schema necessários, plataforma e superfície exatas, prazo/qualidade desejados, modelo/versão e esforço escolhidos, plano, orçamento e cota conhecida. Marque desconhecidos sem perguntar quando a recomendação pode ser condicional.
2. **Filtre na superfície.** Elimine opções comprovadamente indisponíveis ou insuficientes da seleção automática. Quando necessário e permitido, consulte catálogo, parâmetros e documentação oficial vigente. Separe capacidade documentada, disponibilidade no plano e acesso observado na conta por seletor/relato autorizado. Registre fonte/título e editor, URL, data de verificação, afirmação precisa e limites da evidência. Um documento oficial sobre planos não comprova cota ou acesso individual.
3. **Compare apenas opções suficientes.** Priorize compatibilidade, acesso confirmado e preferências da tarefa. Para cota baixa, custo ou rapidez, favoreça uma opção ou esforço suficiente mais econômico/rápido se a evidência sustentar. Para tarefas complexas, considere esforço adicional somente quando documentado na superfície e justificado pela tarefa. Mostre opção principal e alternativa suficiente mais rápida/econômica, ambas com justificativa curta. Sem alternativa confirmada, deixe a alternativa condicional e explique como identificá-la. Evite estimar ganhos sem comparação medida.
4. **Preserve escolha explícita.** Registre modelo/versão e esforço solicitados. Se indisponíveis ou desconhecidos, informe o limite e adapte de forma condicional ou genérica. A alternativa exige autorização para virar destino. Sem pesquisa externa, use evidência local válida, marque as lacunas e evite inventar IDs, preços, cotas, parâmetros ou acesso. Nenhuma chamada paga ou troca automática.

| Superfície | O que verificar no momento da escolha |
|---|---|
| ChatGPT | Seletor e modo de raciocínio daquele plano e interface, uploads e ferramentas. |
| Codex | Superfície, versão, seletor, esforço disponível, ferramentas e limites de uso desse produto. Plus e seus limites não são saldo de API. |
| OpenAI API | Endpoint, model ID, suporte aos parâmetros e às ferramentas, credenciais e orçamento da organização quando autorizados. |
| Claude | Identifique claude.ai, Claude Code, Cowork ou API. Verifique catálogo, ajuste de esforço e ferramentas nessa superfície. |
| Gemini | Identifique app, AI Studio/API, Gemini CLI, Antigravity ou outra superfície. Verifique versão, thinking e permissões no destino. |
| Outros | Identifique produto, versão/model card, adaptador, parâmetros, fontes primárias e acesso. Use baseline portátil se faltarem dados. |

Use o [registro de fontes](../evidence/source_policy.md) e o [adaptador](../../adapters/generic.md) pertinente. Para integração local, [o contrato JSON](../../workflows/interaction_integration.md) recebe candidatos e evidências apurados pelo host, sem chamadas externas. Ordene a entrada por melhor adequação entre opções equivalentes. Recuse inferências de acesso baseadas apenas em disponibilidade pública. A recomendação deve continuar utilizável se o catálogo mudar.
