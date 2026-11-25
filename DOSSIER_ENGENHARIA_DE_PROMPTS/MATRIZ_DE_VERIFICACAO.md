# Matriz de verificação e rastreabilidade

**Data:** 23/11/2026. **Legenda:** V = verificado documentalmente; P = parcial; D = delimitado. Abrir uma página não equivale a executar o produto.

## 1. Requisitos do escopo

| ID | Requisito | Arquivo canônico | Estado | Evidência e verificação |
| --- | --- | --- | --- | --- |
| R-01 | Separar modelo, API, aplicativo, harness e ferramenta | V1 §§3–4 | V | definição operacional e comparação com docs |
| R-02 | Comparar modelos sem transformar guidance em lei | V2; V6 §2 | V | revisão claim por claim |
| R-03 | Registrar IDs e estado temporal dos modelos | V2 | P | páginas atuais verificadas; não é censo de todos os SKUs |
| R-04 | Distinguir ChatGPT, Work e Codex | V3 §2 | V | Help Center e release notes |
| R-05 | Claude Code: memória, regras, agentes, permissões | V3 §§2–4 | V | documentação oficial, inclusive carregamento e enforcement |
| R-06 | Google Antigravity: agente, regras, ferramentas e permissão | V3 §2 | V | docs oficiais do produto |
| R-07 | Cursor: regras, escopo e nível real de enforcement | V3 §2.1; V6 E-14 | V | Rules docs: `.mdc`, `AGENTS.md`, Team Rules, ordem e enforcement de ativação; regra obrigatória não garante aderência semântica |
| R-08 | Copilot: variações por cliente/superfície | V3 §2 | V | custom instructions e feature matrix do GitHub |
| R-09 | Gemini CLI separado da API Gemini | V3 §2 | V | GEMINI.md, JIT context e release oficial |
| R-10 | Aider | V3 §2 | V | arquivo de convenções read-only e prompt caching documentados |
| R-11 | Cline | V3 §2 | V | regras, precedência e Memory Bank metodológico |
| R-12 | Roo Code e estado de manutenção | V3 §2 | V | sunset oficial e arquivo de repositório |
| R-13 | OpenCode V2 e permissões | V3 §2 | V | docs atuais distinguem campos V1/V2 |
| R-14 | Windsurf atual sem inferir de URL redirecionada | V3 §2.1, V6 E-28 | P | Windsurf 2.0 ativo confirmado por anúncio/changelog; Cascade legado; modelo e rollout por conta não verificados |
| R-15 | Comprimento e rigidez do prompt | V2 §4; V4 §3 | P | fontes e hipóteses; experimento próprio pendente |
| R-16 | Markdown, XML, JSON e saída estruturada | V2 §4; V4 §1 | V | orientação por fornecedor; schema runtime quando disponível |
| R-17 | Exemplos, persona e raciocínio | V1 §7; V2; V6 | V | estudos delimitados e docs atuais |
| R-18 | Ferramentas, agentes, memória e segurança | V1/V3/V4 | V | separação de capacidades, dados e enforcement |
| R-19 | Testes reproduzíveis sem fabricar resultado | V4; Protocolos | V | pré-registro, métricas, rubrica e limitações |
| R-20 | Fonte com título, origem, data e claim | V6 §§1,6,8–9 | V | ledger; ausência de data explicitada |
| R-21 | Rastrear cada achado e resolução | Registro de lacunas | V | IDs L-01–L-20 e arquivo/verificação |
| R-22 | Três avaliações separadas e ponderadas | Avaliação final | V | rubrica, pesos e soma documentados |
| R-23 | Auditoria crítica e transparente | Auditoria final | V | passagens internas descritas; limitações externas abertas |
| R-24 | Preparar skill futura sem implementá-la | V5 | V | requisitos e critérios mantidos; nenhum artefato instalável criado |

## 2. Ledger de conclusões principais

| Fonte | Título/origem, conferido em 23/11/2026 | Conclusão que suporta | Limite |
| --- | --- | --- | --- |
| E-01/E-02 | OpenAI, Prompt engineering e Reasoning best practices, documentação oficial | diretrizes atuais para API e reasoning models descritos | não generaliza a outras linhas/superfícies |
| E-06 | Anthropic, Prompting best practices, oficial | orientação de estrutura/contexto para Claude | não demonstra superioridade entre fornecedores |
| E-18 | OpenAI Help Center/API/Codex | Chat, Work, Codex, modelos, instruções e disponibilidade são distintos | acesso depende de plano, rollout, região e workspace |
| E-19 | Anthropic Models/Claude Code | modelos, CLAUDE.md/AGENTS.md, memória e permissões documentados | regras em contexto não são enforcement |
| E-20 | Google AI Studio, Gemini models e prompting | IDs/modelos publicados e orientação Gemini sobre instruções e exemplos | few-shot não é regra universal; catálogo volátil |
| E-21 | Mistral Models/Prompting | modelos, níveis de instrução e exemplos/formatação | orientação de fornecedor, não prova comparativa |
| E-22 | GitHub, Copilot custom instructions | tipos e suporte variam por cliente; seguir não é determinístico | não extrapolar ordem entre superfícies |
| E-23/E-24 | Cline Rules/Memory Bank, docs oficiais | regras de workspace/global e método documental de memória | Memory Bank não é memória nativa oculta |
| E-25 | Google Gemini CLI, GEMINI.md/changelog | hierarquia global/workspace/JIT e versão anunciada | versão instalada pode diferir |
| E-26 | OpenCode Agents/Permissions V2 | campos V2 e ordenação “última regra aplicável” | exemplos antigos V1 não são intercambiáveis |
| E-27 | Roo Code official sunset/repository | encerramento e repositório arquivado em 15/05/2026 | não implica continuidade em sucessores |
| E-28 | Anúncio Windsurf 2.0 + changelog recente + URL legada Cascade → docs Devin Local | produto atual confirmado em fonte primária; URL de Cascade redireciona | suporta Windsurf 2.0 ativo e Cascade legado; disponibilidade por conta/plano segue não verificada; redirect não prova equivalência |
| E-29–E-31 | Artigos e survey acadêmicos em V6 | efeitos observados em benchmarks e suas limitações | não substitui nova replicação em sistemas 2026 |

## 3. Leitura dos estados

- V é validade da afirmação documental delimitada, não qualidade garantida do modelo.
- P marca cobertura parcial ou recomendação que demanda experimento.
- D marca delimitação explícita por falta de evidência atual.
- Títulos, URLs, datas editoriais apresentadas ou ausentes e metadados completos estão no Volume 6, §§8–9.









