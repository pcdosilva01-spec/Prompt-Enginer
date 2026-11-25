# Adaptador para coding agents

Verifique o ambiente onde o prompt será executado. Uma skill pessoal no editor pode estar ausente no agente remoto ou contêiner. [Integração Humanizer por capacidade](../references/writing/humanizer.md).

## Cursor

Docs oficiais atuais reconhecem `.agents/skills/`, `.cursor/skills/`, locais de usuário e carregamento compatível de `.claude/skills/` e `.codex/skills/`. Skill local não é necessariamente sincronizada para Cloud Agent/SSH. Fonte: [Cursor Skills](https://cursor.com/docs/skills), verificada em 23/11/2026.

## GitHub Copilot

Os diretórios variam por superfície; docs listam `.github/skills/`, `.agents/skills/`, `.claude/skills/`, e perfil pessoal. A feature matrix inclui Copilot App/CLI/cloud agent/code review e IDEs em versões suportadas. Prefira ausência de `allowed-tools` amplo; docs alertam que preaprovar shell remove prompts de permissão. Fontes: [adding skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) e [feature matrix](https://docs.github.com/en/enterprise-cloud%40latest/copilot/concepts/customizations/comparing-customizations), consultadas em 23/11/2026.

## Cline

Docs oficiais indicam `.cline/skills/` (projeto e global), além de compatibilidade com `.clinerules/skills/` e `.claude/skills/`; Skill menu pode ativar/desativar. Tools e acesso a arquivos são próprios do Cline. Fonte: [Cline Skills](https://docs.cline.bot/customization/skills), aberta em 23/11/2026.

## OpenCode

`.opencode/skills/<id>/`; docs também registram locais `.agents/skills/` e `.claude/skills/` e precedência. A ferramenta de skills carrega instruções; política OpenCode de tools é independente. Fonte: [OpenCode skills](https://opencode.ai/docs/skills/), consultada em 23/11/2026.

## Devin Local e Windsurf

Docs de `docs.windsurf.com/windsurf/cascade/skills` redirecionam para Devin Local. Os docs atuais de Devin descrevem `.devin/skills/`, `.agents/skills/` e legado `.windsurf/skills/`; isso não comprova que skill criada para Devin funcione integralmente em Cascade antigo. Use uma conversão/instalação apenas após verificar host e versão. Fonte: [Devin Local customizations](https://docs.devin.ai/desktop/devin-local/customizations), consultada em 23/11/2026.

## Roo Code

Docs oficiais indicam encerramento da extensão em 15/05/2026. Não há instrução de instalação operacional nesta skill. Não inferir comportamento de Cline ou de um fork. Fonte: [Roo Code archived docs](https://roocodeinc.github.io/Roo-Code/), consultada em 23/11/2026.

## Aider e demais agentes

Não afirmar suporte nativo Agent Skills sem página oficial atual. Se a plataforma só aceita instruções de repositório, converta o conteúdo indispensável para esse formato e descreva a perda de carregamento progressivo, scripts ou gate de ativação. Confirme permissões e escopo antes de recomendar execução.

Use a [seleção de modelo](../references/models/model_selection.md) antes do resumo, verificando modelo, esforço, leitura, escrita e ferramentas na superfície exata. O estado do [validador local](../workflows/interaction_integration.md) depende de uma chamada do host. A aprovação da revisão do prompt não habilita execução do agente ou alteração do repositório.
