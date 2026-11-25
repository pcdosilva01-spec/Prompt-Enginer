# Registro rastreável de lacunas

**Fechamento desta rodada:** 23/11/2026. Gravidade e impacto são independentes; prioridade P1 é máxima. “Resolvida” refere-se à correção documental verificada, não a experimento não executado.

| ID | Gravidade / impacto | Lacuna ou erro | Evidência | Complexidade | Prioridade | Critério | Resolução / estado / verificação |
|---|---|---|---|---|---|---|---|
| L-01 | Alta / alta | Volume 2 alegava que não foi localizada guidance Gemini | página oficial ativa com estratégia e exemplos | Baixa | P1 | precisão, atualidade | Corrigida; few-shot é guidance atribuída, E-20; V2 |
| L-02 | Alta / alta | Roo Code tratado como lacuna sem status atual | anúncio oficial e repositório arquivado em 15/05/2026 | Baixa | P1 | atualidade, segurança de adoção | Corrigida como encerrado/legado; E-27; V3 |
| L-03 | Alta / alta | Cline sem ficha | docs oficiais de regras e Memory Bank | Média | P1 | abrangência | Ficha adicionada, regras globais/locais e precedência; E-23/24; V3 |
| L-04 | Alta / alta | OpenCode sem ficha; V1/V2 poderiam ser confundidas | docs atuais de Agents/Permissions diferenciam schema V2 | Média | P1 | precisão, atualidade | Ficha V2 e campos legados identificados; E-26; V3 |
| L-05 | Alta / alta | Gemini CLI misturado com API/AI Studio | GEMINI.md e release notes oficiais | Média | P1 | modelo/plataforma, versão | Ficha própria; v0.68.0 anunciada em 10/11/2026 como âncora, sem inferir instalação universal; E-25 |
| L-06 | Alta / alta | Windsurf sem verificação do produto atual e sem separar Cascade legado de Devin Local | blog oficial 2.0, changelog 20/11 e redirecionamentos de documentação | Média | P1 | precisão, atualidade | Parcialmente corrigida: anúncio e changelog confirmam Windsurf 2.0 ativo, Cascade legado; plano/modelos por conta não conferidos; E-28; V3 §2.1/V6 §§8–9 |
| L-07 | Alta / alta | ChatGPT, Work e Codex agrupados | Help Center/releases descrevem experiência, modelos e disponibilidade distintos | Média | P1 | precisão, atualidade | Separados por superfície; rollout/conta condicionais; E-18; V3 |
| L-08 | Alta / média | Tamanho ideal e uso de exemplos apresentados genericamente | guidance Gemini/Mistral/Anthropic varia e não é benchmark independente | Média | P1 | profundidade, confiabilidade | Transformados em hipóteses condicionais + protocolo A/B; V2/V4 |
| L-09 | Alta / alta | Possível superioridade universal de XML/Markdown/JSON | docs recomendam mecanismos por produto; schema depende de API e runtime | Média | P1 | precisão | Delimitador separado de schema/validação; E-01/06/21; V2/V4 |
| L-10 | Média / alta | Regra persistente confundida com enforcement | docs de Claude Code, Cursor, Cline e OpenCode separam contexto/permissão | Média | P1 | segurança, aplicabilidade | Modelo em camadas atualizado; V1/V3/V4 |
| L-11 | Média / alta | Evidência científica insuficiente sobre personas/otimização | estudos acadêmicos identificados e limitados por benchmark | Média | P2 | profundidade científica | V1/V6 ampliados com conclusões condicionais; E-29 a E-31 |
| L-12 | Alta / alta | Fonte sem ledger uniforme, datas e claims | datas editoriais aparecem apenas em parte das páginas | Média | P1 | referências, rastreabilidade | Ledger criado; não indicada quando a página não mostra; V6 |
| L-13 | Alta / alta | Falta de ligação requisito-verificação | índice temático não prova cobertura | Média | P1 | completude, auditoria | Matriz R-01–R-24 criada e cruzada |
| L-14 | Média / alta | Protocolos pouco operacionais | planos antigos não detalhavam execução, métricas e rubrica | Média | P2 | reprodutibilidade | P-01–P-05 especificados; execuções continuam pendentes |
| L-15 | Alta / alta | Sem testes reais de modelo | nenhum runtime local reconhecido, chave ou sessão API disponível/identificada | Alta | P1 | validação empírica | Pendência transparente; não foi chamado de teste; sem gasto; protocolos entregues |
| L-16 | Alta / alta | Auditoria interna anterior sem avaliador externo | apenas autorias internas disponíveis nesta tarefa | Alta | P1 | independência | Passagens críticas e rubricas separadas; revisor externo ainda necessário para validação independente |
| L-17 | Média / média | Continue e fornecedores agregadores sem ficha atual comparável | pesquisa desta rodada insuficiente para claims versionados | Média | P3 | abrangência | Delimitados como não verificados; V3/matriz |
| L-18 | Média / média | Planos, preços, regiões e limites voláteis | catálogos oficiais mudam e condicionam acesso | Baixa | P2 | atualidade | Data de corte e revalidação exigidas; V2/V6 |
| L-19 | Média / média | Cursor Team Rules e obediência do modelo estavam condensadas como uma só forma de “enforcement” | docs atuais separam ativar/exigir uma regra de equipe da aderência da resposta do modelo | Baixa | P2 | precisão, segurança | Corrigida: admin pode exigir regra ativa; a documentação não promete cumprimento semântico; E-14; V1/V3/V6 |
| L-20 | Média / média | Três matrizes estavam alinhadas por espaços, mas não eram tabelas Markdown válidas | inspeção de blocos de tabela em todos os Markdown encontrou V1, matriz de verificação e auditoria final | Baixa | P2 | clareza, organização, aplicabilidade | Convertidas para tabelas Markdown com separadores; varredura posterior não encontrou candidatos restantes; V1/Matriz/Auditoria |

## Encerramento

- **Resolvidas documentalmente:** L-01–L-05, L-07–L-14, L-18 a L-20, com verificações apontadas na última coluna.
- **Parcialmente resolvidas:** L-06 (Windsurf 2.0 ativo e Cascade legado confirmados; disponibilidade de modelo/rollout por conta não conferida); L-15 (protocolo pronto, resultados ausentes); L-16 (auditoria reforçada, sem terceiro independente).
- **Delimitada, não resolvida:** L-17. Não são feitas alegações atuais sobre os produtos fora da pesquisa profunda.








