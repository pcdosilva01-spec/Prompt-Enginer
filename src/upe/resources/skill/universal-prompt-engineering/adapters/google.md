# Adaptador Google: Gemini CLI e Antigravity

Confirme descoberta e consentimento no Gemini CLI. No app ou em AI Studio, confira separadamente o acesso que determina o [modo Humanizer](../references/writing/humanizer.md).

Fontes primárias consultadas em 23/11/2026: [Gemini CLI creating skills](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/creating-skills.md), [Gemini CLI using skills](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/using-agent-skills.md), [Antigravity Agent Skills](https://antigravity.google/docs/skills).

## Gemini CLI

- Projeto: `.gemini/skills/<id>/` ou `.agents/skills/<id>/`; pessoal: `~/.gemini/skills/` ou `~/.agents/skills/`.
- Confirme `gemini skills list`, `/skills list`, `/skills reload`; ativação de skill pede consentimento conforme docs atuais. Workspace precisa de confiança, quando aplicável.
- O nome e a descrição YAML impulsionam descoberta; referências/scripts da pasta ficam disponíveis ao ativar.

## Antigravity

- Workspace: `.agents/skills/<id>/`; global app/IDE: `~/.gemini/config/skills/<id>/`; CLI reconhece caminhos adicionais. Não copie path de CLI cegamente para o app.
- Ativação contextual ou `/<id>`; confira Customize/`/skills`. Consentimento e ferramentas continuam no harness.

## Gemini model vs harness

Guidance do Gemini API/modelo não deve ser inferida da CLI nem da Antigravity. Consulte documentação atual do model ID e da interface; recomendações de few-shot documentadas para Gemini são vendor guidance, não prova universal. Não use versão de release encontrada em outro snapshot sem recarregar o changelog.

## Recomendação e entrega

Use a [seleção de modelo](../references/models/model_selection.md) com ID e superfície específicos. Confirme o parâmetro de thinking e as ferramentas na interface escolhida. Na [entrega](../workflows/evaluation_and_delivery.md), use apenas o formato de cópia e o mecanismo de arquivo efetivamente disponíveis.
