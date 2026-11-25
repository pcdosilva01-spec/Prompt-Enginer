# Ledger de fontes de plataforma desta versão

**Acesso/verificação:** 23/11/2026. Se não há data de publicação explícita, a célula indica isso; a data desta consulta não é tratada como data editorial. O ledger do dossiê integral conserva E-01–E-34 e as fontes acadêmicas/modelos originais.

| ID | Título / publisher | URL | Data editorial | Claim que sustenta | Limite |
|---|---|---|---|---|---|
| S-01 | Specification / Agent Skills | https://agentskills.io/specification | Não indicada | requisito de diretório, SKILL.md, campos name/description, suporte opcional a scripts/references | não define comportamento de cada host |
| S-02 | Build skills / OpenAI Codex (ChatGPT Learn) | https://developers.openai.com/codex/skills | Não indicada, docs vivas; destino consultado: `learn.chatgpt.com/docs/build-skills` | paths atuais `.agents/skills` (repo), `$HOME/.agents/skills` (user), `/etc/codex/skills` (admin); `agents/openai.yaml` opcional; invocação explícita/implícita via descrição | `.codex/skills` não consta na página atual; valida documentação, não instalação deste bundle; verificada diretamente em 23/11/2026 |
| S-03 | Skills / OpenAI Plugins | https://developers.openai.com/plugins/concepts/skills | Não indicada, docs vivas | divisão workflow da skill vs dado/ação MCP | produto muda e não instala pasta local |
| S-04 | Skills / OpenAI API | https://developers.openai.com/api/docs/guides/tools-skills | Não indicada, docs vivas | bundles com `SKILL.md`, uso no sandbox/API, riscos de injection/exfiltração, necessidade de controle | nenhuma chamada/upload ocorreu |
| S-05 | Extend Claude with skills / Anthropic | https://code.claude.com/docs/en/skills | Não indicada, docs vivas | paths Claude Code, frontmatter extension, resources e skill account/cloud | superfície/version/config influencia carregamento |
| S-06 | Agent Skills / Cursor | https://cursor.com/docs/skills | Não indicada, docs vivas | locations `.agents/skills`/`.cursor/skills`, auto discovery e limitações cloud/SSH | sem teste no cliente Cursor |
| S-07 | Creating Agent Skills / Google Gemini CLI | https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/creating-skills.md | `main` mutável; não indicada | estrutura YAML e diretórios do Gemini CLI | release instalada não conferida |
| S-08 | Managing Agent Skills / Google Gemini CLI | https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/using-agent-skills.md | `main` mutável; não indicada | discovery tiers, consentimento, reload/CLI | versão instalada não conferida |
| S-09 | Agent skills / Google Antigravity | https://antigravity.google/docs/skills | Não indicada, docs vivas | caminhos e comportamento por App/CLI/IDE | caminhos extras são específicos à superfície |
| S-10 | Adding agent skills / GitHub Copilot | https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills | Não indicada, docs vivas | paths e recursos suportados; risco de allowed-tools/shell | IDE support varia por versão/política |
| S-11 | Comparing customization features / GitHub | https://docs.github.com/en/enterprise-cloud%40latest/copilot/concepts/customizations/comparing-customizations | Não indicada, docs vivas | disponibilidade de skills por superfície Copilot | `latest` é mutável |
| S-12 | Skills / Cline | https://docs.cline.bot/customization/skills | Não indicada, docs vivas | caminhos, estrutura e loading progressivo em Cline | não mede aderência do modelo |
| S-13 | Skills / OpenCode | https://opencode.ai/docs/skills/ | Não indicada, docs vivas | path `.opencode/skills`, caminhos compatíveis e precedência | tools e permission seguem OpenCode |
| S-14 | Devin Local Customizations / Devin | https://docs.devin.ai/desktop/devin-local/customizations | Não indicada; URL Windsurf antiga redireciona para Devin | paths atuais Devin Local e legacy `.windsurf/skills` importados | redirect não prova equivalência de Cascade/Windsurf antigo |
| S-15 | Roo Code Docs — Extension Shutdown / Roo Code Archive | https://roocodeinc.github.io/Roo-Code/ | página marca encerramento/atualização em 15/05/2026 | extensão encerrada em 15/05/2026 | forks/sucessores têm ciclo separado |

Os links foram consultados diretamente ou abertos via busca oficial em 23/11/2026. Páginas mudam; antes de recomendar caminho, permissão, modelo ou disponibilidade, reabra a fonte e anote novo snapshot.
