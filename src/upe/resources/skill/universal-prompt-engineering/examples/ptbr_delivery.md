# Casos editoriais do prompt de destino

Fixtures de conversa para verificação manual. Nos exemplos, as capacidades declaradas pertencem à IA que receberá o prompt.

## Discord em chat isolado

Pedido: “Crie um prompt para um texto de apresentação de sugestões de um servidor Discord”.

Primeiro turno esperado:

1. Construir um prompt para apresentar aos membros as sugestões que o usuário fornecer. Assumir PT-BR e tom direto e cordial. Usar um campo de entrada para as propostas.
2. Preservar cada proposta e distinguir sugestão de decisão. O destinatário recebe a Humanizer em modo portátil, pois seu acesso à skill não foi confirmado.
3. Modelo principal condicionado ao seletor do chat e à capacidade de escrever em PT-BR. Uma variante de menor custo ou esforço serve de alternativa se passar pelo mesmo teste de fidelidade. Plano e cota desconhecidos.

“Você aprova a revisão 1 como base para construir o prompt?” Encerrar o turno. Um elogio não vale como aprovação. Não redigir a apresentação.

Depois de “Aprovo a revisão 1”, o corpo do prompt inclui a tarefa específica abaixo, seguida do **bloco portable integral** de [Humanizer](../references/writing/humanizer.md):

```text
Escreva em português brasileiro uma apresentação curta para os membros do servidor Discord. Use as sugestões fornecidas abaixo. Mantenha números, nomes de canais e condições. Apresente cada ideia como proposta e respeite o grau de formalidade pedido. Se a lista estiver vazia, peça as sugestões antes de redigir.
Sugestões: [cole aqui as propostas]
```

A entrega concatena tarefa e bloco editorial em um único prompt. O TXT, se suportado, contém esses mesmos bytes UTF-8. A recomendação com alternativa, os dez itens da rubrica, a limitação de acesso e a pergunta final ficam fora do bloco. O teste `test_editorial_workflow.py` constrói e entrega uma instância completa com os dados “2 canais”, “se houver aprovação” e “Não arquivar #ajuda”.

## Contraprovas e variações

| Entrada | Decisão e trecho específico após aprovação | Falha observável |
|---|---|---|
| Ofício em PT-BR, skill reconhecida | “Aplique a skill instalada humanizar-natural-ptbr ao ofício. Preserve o registro institucional e a obrigação expressa em ‘deverá’.” | Trocar obrigação por sugestão ou acrescentar gírias. |
| README com descrição PT-BR, shell e JSON, checkout autorizado | Incluir o bloco de leitura da revisão oficial e indicar o checkout. “Revise apenas o parágrafo brasileiro. Preserve literalmente `npm ci` e o exemplo JSON.” | Substituir o comando ou traduzir chaves. |
| Mensagem bilingue PT-BR/inglês | Aplicar o bloco à versão brasileira. Redigir a parte inglesa conforme as preferências próprias dela. | Forçar registro brasileiro ao trecho inglês. |
| UI em português brasileiro | Aplicar ao rótulo e à mensagem que o usuário lerá. Manter chave de tradução e placeholders. | Alterar `{count}` ao simplificar uma frase. |
| Pedido em português de um artigo em francês | Produzir prompt para artigo em francês, sem bloco Humanizer. | Ativar pela língua do pedido. |
| Código, fórmula ou JSON literal, sem prosa | Seguir o contrato técnico e o gate da UPE. | Acrescentar introdução ou transformar os valores. |
| Diagnóstico sem prompt substituto | Explicar diretamente o problema encontrado. | Gerar a reescrita sem aprovação. |
