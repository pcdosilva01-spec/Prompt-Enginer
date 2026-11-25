# Especialização editorial para prosa em português brasileiro

Classifique cada parte da saída solicitada à IA destinatária. Ative Humanizer para prosa PT-BR destinada a pessoas, inclusive criação, revisão, simplificação, Discord, e-mail, apresentações, artigos, README, documentação e microtexto. Não decida pela língua do pedido nem pela palavra “humanizar”. Em pedido em PT-BR de apresentação para Discord, assuma PT-BR se não houver outro idioma indicado; explicite no resumo. Resolva ambiguidades materiais antes da aprovação.

Na tarefa mista, delimite prosa editável e trechos literais. Código, comandos, fórmulas, IDs, citações, URLs, chaves e placeholders ficam protegidos. Se JSON for estritamente literal, preserve-o inteiro; só edite valores textuais especificamente autorizados, mantendo o esquema. Em texto bilíngue, aplique somente à versão brasileira.

No resumo, registre público, canal, registro, limites e acesso confirmado **no destino**. Após aprovação, insira uma única instrução composta pelo bloco do modo selecionado e pelo núcleo comum abaixo (no modo portátil, somente o núcleo). Não execute a redação pedida ao destinatário. Revise a instrução no prompt, confira a delimitação das partes e derive o TXT só após revisão. Alteração material de acesso exige nova aprovação.

### installed

```text
Aplique a skill instalada humanizar-natural-ptbr, se compatível e reconhecida pelo destinatário; use o mecanismo nativo do host. Se a skill não puder ser carregada, siga o núcleo abaixo, sem presumir instalação ou executar scripts. O núcleo também complementa versões que não contemplam continuidade conversacional.
```

### source

```text
Aplique a Humanizer: consulte, se autorizada e disponível, https://github.com/pcdosilva01-spec/Humanizer-Skill/tree/e84cbbac87ef05d98a13539db62303edaf1c7a27, skills/humanizar-natural-ptbr/SKILL.md e, conforme a tarefa, references/fidelidade.md ou references/registros-ptbr.md dessa skill. Não instale nem execute scripts. Se a leitura falhar, use o núcleo abaixo sem alegar consulta.
```

### portable

```text
Aplique este núcleo da Humanizer apenas à prosa PT-BR destinada a pessoas. Identifique intenção, destinatário e canal; ajuste registro, ritmo e formato à voz fornecida; mantenha texto já adequado e termos técnicos. Não force gírias, contrações, emojis, vocativos, informalidade ou trocas lexicais. Em resposta para envio, considere o turno anterior e o contexto: responda ao ato atual; não repita abertura nem pergunta já respondida. Se houver mal-entendido, esclareça o ponto, sem atribuir culpa; use correções explícitas mais recentes do usuário. Não presuma que a ironia alheia autoriza ironia na resposta. Integre reciprocidade, comentário, confirmação ou pergunta breve somente se útil; encerre quando suficiente. Se faltar dado indispensável, esclareça com o usuário ou use resposta neutra fiel. Não invente fatos, estado, opinião, sentimentos, experiência, prazo ou compromisso. Confira nomes, números, datas, negações, condições, intensidade, modalidade, certeza, obrigações e formato. Preserve literais (citações, URLs, IDs, fórmulas, comandos, código, dados estruturados, chaves, placeholders) e outros idiomas. Entregue a saída pedida, pronta para uso, sem explicação editorial salvo pedido. Não alegue autoria humana nem aprovação por detectores.
```

No modo portátil, informe **fora do prompt** que o acesso do destinatário à skill completa não foi confirmado. Nos demais, não afirme carregamento real sem confirmação. No Codex, mencione a identificação reconhecida; no Claude Code, o comando `/humanizar-natural-ptbr` só cabe se listado e na interface apropriada, não em mensagens de API.

## Origem e sincronização

Adaptação de Humanizar Natural 2.0.0, Humanizar Natural contributors, MIT; revisão upstream e84cbbac87ef05d98a13539db62303edaf1c7a27, consultada em 25/11/2026. [Licença integral](HUMANIZER-LICENSE.txt). Núcleo ampliado localmente em 25/11/2026 para continuidade contextual (2.0.1-local) e ajustado na revisão 2.0.2-local para reparo e continuidade em vários turnos; sem publicação. A fonte autorizada deste modo permanece o commit upstream 2.0.0; o núcleo cobre as extensões locais. Consulte [seleção e conflitos](../../workflows/skill_routing.md). Compare a fonte canônica, licença e casos upstream antes de sincronizar, revise os modos, execute regressões e regenere o manifesto.
