# Adaptação por plataforma e superfície

## Quatro perguntas antes de escrever

1. Qual modelo/versão será usado? (não é sinônimo de plataforma.)
2. Qual superfície exata: app, API, CLI, IDE, agente cloud/local, plugin ou SDK?
3. Que contexto/ferramentas essa superfície realmente expõe à sessão? Quais arquivos carrega e com que precedência?
4. Que operações pedem consentimento, são sandboxed ou não estão disponíveis?

Consulte `../COMPATIBILITY_MATRIX.md` para status e links conferidos em 23/11/2026 e os adapters por host. Uma matriz de compatibilidade prova que documentação foi consultada, não que esta skill foi instalada.

## Adaptar sem confundir mecanismos

- **Prompt único:** fornecer requisitos e formato na mensagem; não pressupor memória entre sessões.
- **Skill:** carregar proceduralmente instruções e referências por demanda; seu conteúdo não concede tools.
- **Regra persistente:** normalmente é contexto recorrente; confirmar precedência/escopo na doc do host. Isso não prova que a resposta obedecerá.
- **Ferramentas/MCP:** o runtime fornece. Prompt pode descrever como usar ferramenta disponível; não pode criar ou autorizar uma ferramenta.
- **Hooks, sandbox e permissões:** controles do harness. Em ação de impacto, manter aprovação exigida pelo host e validar o efeito.
- **Cloud/local:** não assumir que arquivos pessoais locais ou regras aparecem em sessões remotas; confirmar sincronização e escopo.

## Estado de evidência

Use três rótulos: **documentado** (página oficial da superfície), **inferido com limite** (conclusão explicitamente derivada) e **não verificado**. Um redirect de URL legada não demonstra continuidade funcional do produto antigo. Para Windsurf, a URL oficial antiga redireciona atualmente para docs Devin Local; isso não valida equivalência completa com Cascade. Roo Code está encerrado segundo docs oficiais; não documentar instalação nova como disponível.
