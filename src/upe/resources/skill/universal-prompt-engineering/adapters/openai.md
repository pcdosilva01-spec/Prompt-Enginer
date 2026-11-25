# Adaptador OpenAI: Codex, ChatGPT Skills e API

**Fontes consultadas em 23/11/2026:** [Codex build skills](https://developers.openai.com/codex/skills), [Skills concepts](https://developers.openai.com/plugins/concepts/skills), [API Skills](https://developers.openai.com/api/docs/guides/tools-skills). Datas editoriais das páginas não indicadas em todos os resultados.

- **Codex:** manter `SKILL.md` conciso, frontmatter `name`/`description`, referências e scripts relativos. A documentação reaberta em 23/11/2026 lista `.agents/skills/` no repositório (incluindo diretórios ancestrais), `$HOME/.agents/skills/` para usuário e `/etc/codex/skills/` para admin. Trate `.codex/skills/` como caminho não confirmado pela página atual; verifique superfície e descoberta na sessão. `agents/openai.yaml` é metadado opcional de interface/política Codex, não requisito do padrão universal.
- **ChatGPT/plug-in:** separar workflow de ferramenta MCP. Um pacote de skill explica sequência e julgamento; o MCP fornece dados/ferramentas e controles. Não pressupor que a sessão ChatGPT carregue qualquer pasta local.
- **Responses/Agents API:** docs descrevem skills como `SKILL.md` + recursos, versionadas/uploaded ou disponíveis no sandbox do agente. Isso depende da API/sandbox e das permissões do aplicativo. Este pacote não fez upload nem chamadas API.
- **Formato/saída:** estratégia de prompt deve corresponder ao endpoint e ao model ID; utilize resposta estruturada suportada pela API quando for contrato programático e valide no consumidor.
- **Limite:** os fatos de modelos, disponibilidade e parâmetros variam. Consulte o Volume 2 e doc atual. Nenhuma rota de ferramenta é concedida pelo texto da skill.

## Recomendação e entrega

Use a [seleção de modelo](../references/models/model_selection.md) para o produto exato. ChatGPT, Codex e API têm controles de esforço e acesso distintos. Registre Plus e cota somente conforme informação disponível na superfície. A preferência do usuário não comprova disponibilidade. Confirme os recursos de cópia e TXT no host efetivo e aplique o [contrato de entrega](../workflows/evaluation_and_delivery.md).
