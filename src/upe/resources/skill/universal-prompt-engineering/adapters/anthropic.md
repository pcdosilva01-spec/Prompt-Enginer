# Adaptador Anthropic: Claude Code e Claude.ai

Fonte primária verificada: [Claude Code skills](https://code.claude.com/docs/en/skills), aberta em 23/11/2026; data editorial não indicada.

- **Claude Code local:** instale a pasta sob `.claude/skills/universal-prompt-engineering/` (projeto) ou `~/.claude/skills/universal-prompt-engineering/` (pessoal). Skills em added directories e repositórios seguem config/permission local. Verifique no menu `/` ou `/skills`.
- **Extensões do Claude:** invocation controls, `allowed-tools`, contexto em fork e substituição dinâmica são campos próprios e não fazem parte do formato básico. Não inserir esses campos no frontmatter comum, a menos que seja criada uma variante local depois de validar no host.
- **Claude.ai/Cowork/cloud:** docs distinguem skills sincronizadas pela conta das skills locais do Claude Code. Colocar arquivo na pasta da máquina não garante disponibilidade na sessão cloud. Habilite/sincronize pelo fluxo oficial e verifique.
- **Recursos:** instruções e anexos podem ser carregados progressivamente; a skill não deve declarar segurança apenas por possuir fronteiras textuais. Leia trechos originais necessários.
- **Ferramentas:** a permissão e pré-aprovação pertencem à configuração Claude/harness. Não preconfigure ferramentas no pacote.

## Recomendação e entrega

Use a [seleção de modelo](../references/models/model_selection.md) por modelo Claude e superfície. Verifique o esforço naquela interface, a disponibilidade da conta e se ela permite publicar TXT. Use o [contrato de entrega](../workflows/evaluation_and_delivery.md) com fallback conversacional quando o script não for executado.
