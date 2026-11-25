# Instalação e primeiro uso

## Compatibilidade

O conteúdo foi criado no formato aberto `SKILL.md` + YAML frontmatter, com referências relativas. Isso permite distribuição para hosts que documentam suporte a Agent Skills. Caminhos, descoberta, carregamento de anexos e permissões variam por produto; consulte [`COMPATIBILITY_MATRIX.md`](COMPATIBILITY_MATRIX.md). A skill **não foi instalada** neste computador nem em qualquer host.

## Codex

Conforme a documentação Codex reaberta em 23/11/2026, copie para `%USERPROFILE%\.agents\skills\universal-prompt-engineering\` no escopo de usuário ou `.agents\skills\universal-prompt-engineering\` no repositório. Codex também consulta diretórios `.agents/skills` ancestrais até a raiz do repositório e `/etc/codex/skills/` no escopo admin. A página atual não lista `.codex/skills/`; confirme superfície/versão, reinicie/recarregue quando necessário e verifique a descoberta pelo nome antes do primeiro uso.

## Outros hosts documentados

- **Claude Code:** `.claude/skills/universal-prompt-engineering/` (projeto) ou `~/.claude/skills/universal-prompt-engineering/` (pessoal); confira `/skills` ou invocação `/universal-prompt-engineering`.
- **Cursor:** `.agents/skills/` ou `.cursor/skills/` no projeto; pessoal `.agents/skills/` ou `.cursor/skills/`; confira menu `/`.
- **Gemini CLI:** `.gemini/skills/` ou `.agents/skills/` no projeto; pessoal `~/.gemini/skills/` ou `~/.agents/skills/`; confira `/skills list` e aceite o consentimento de ativação.
- **Antigravity:** `.agents/skills/` no workspace ou `~/.gemini/config/skills/` global; confira Customizations ou `/skills`.
- **Cline:** `.cline/skills/` no workspace ou `~/.cline/skills/` global; confira o painel Skills.
- **OpenCode:** `.opencode/skills/` no projeto, `.agents/skills/` ou `.claude/skills/` para compatibilidade conforme docs atuais; confira ferramenta `/skill`.
- **GitHub Copilot:** `.github/skills/`, `.agents/skills/` ou `.claude/skills/` conforme a superfície; a CLI inclui `copilot skill list`.
- **Devin Local:** `.devin/skills/` no projeto ou `.agents/skills/` documentado; valide no painel Customize.

Não use caminhos antigos por suposição. Verifique a documentação do cliente e a versão instalada antes de copiar.

## Primeiro uso

Peça, por exemplo: “Crie um prompt para [objetivo], destinado a [modelo/plataforma]; o resultado deve [requisitos].” A skill deverá responder primeiro com um resumo de entendimento e pedir confirmação. Corrija ou aprove o resumo. Só então ela poderá entregar o prompt final. Para usar o helper de estado, siga `universal-prompt-engineering/scripts/approval_gate.py --help`.

## Atualização e segurança

Revise esta matriz e seus links antes de reutilizar instruções de produto. Inspecione `SKILL.md`, scripts e referências antes de instalar skills de terceiros. Não marque permissões de shell como pré-aprovadas sem auditoria própria. Após atualizar arquivos, rode testes e `scripts/build_manifest.py`; examine o diff do manifesto.
