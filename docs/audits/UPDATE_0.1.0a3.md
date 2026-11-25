# Prompter Silva 0.1.0a3

Atualização local da skill Universal Prompt Engineering em 24/11/2026.

## Diagnóstico

- O ZIP de entrada tem SHA-256 `f7dc2f441cd5f509c5b5785bfe8412d8848eb3f6e2d7c8c6329bfa8dc7f154c6`. O inventário de 181 membros passou na verificação de caminhos, duplicatas, tipos e CRC, e os arquivos de entrada correspondiam byte a byte ao workspace antes das alterações.
- O contrato anterior exigia resumo e aprovação no `SKILL.md`. O helper aplicava a aprovação ao digest, mas seu evento de entrega encerrava o fluxo sem receber prompt, formato ou avaliação. O template de entrega previa apenas uma nota e o workflow falava em notas para decisões materiais. O modelo podia encontrar formatos incompatíveis com a rubrica completa. Essas lacunas estão confirmadas no pacote. Sua relação causal com os relatos de omissão permanece hipótese porque não há transcrições daquela execução.
- O teste de integridade da linha de base ainda procurava o dossiê no diretório removido pela reorganização anterior. A asserção falhou para `AUDITORIA_FINAL.md`. O caminho foi apontado para o dossiê preservado na raiz e os 14 pares continuam sujeitos à mesma comparação SHA-256.
- A pasta e o ZIP `SKILL_UNIVERSAL_ENGENHARIA_DE_PROMPTS` são snapshots históricos. Os ZIPs versionados ativos vêm do bundle canônico. Os originais do dossiê, suas cópias embutidas e o manifesto dos originais foram preservados.

## Implementação

| Área | Arquivos e controle |
|---|---|
| Entrada e turnos | `SKILL.md`, `workflows/approval_and_correction.md`, `intent_and_requirements.md`, `generation_and_optimization.md` e `interaction_integration.md` descrevem checkpoints, rejeição, perda de estado, ajustes cosméticos e nova aprovação para otimização. |
| Integração local | `scripts/interaction.py` coordena estados e vincula aprovação à revisão e ao contexto. Reutiliza `approval_gate.py`, cuja API foi preservada para consumidores existentes. |
| Entrega | `scripts/delivery_contract.py`, `workflows/evaluation_and_delivery.md`, rubrica e templates de resumo, entrega e avaliação conferem a identidade do prompt revisado, o artefato TXT, os dez critérios, a soma ponderada, os tetos e a oferta literal. |
| Modelos | `scripts/model_selection.py`, `references/models/model_selection.md`, `model_adaptation.md`, índice e adaptadores OpenAI, Anthropic, Google, genérico e de agentes de código. Catálogo fornecido em tempo de uso, escolha do usuário preservada, alternativa e evidência condicionais. |
| Validação | `tests/test_interaction.py`, `tests/test_integrity.py`, `src/upe/integrity.py`, `scripts/verify_package.py`, cenários e protocolo comportamental. |
| Distribuição | Versão em `pyproject.toml` e `src/upe/__init__.py`, changelog, READMEs, instruções de instalação e `MANIFEST.sha256`. Os ZIPs versionados e seus checksums são gerados por `tools/build_release.py`. |

A integração gera um resumo a partir do estado e monta a resposta a partir do pacote validado. A otimização exige aceite do usuário, nova aprovação, preservação do conjunto de requisitos, mudança no texto e comparação. O agente ainda julga ganho material e fidelidade semântica. A distribuição não ativa um hook automaticamente. O host interpreta a mensagem de aprovação, mantém estado confiável, identifica suas capacidades e entrega os resultados do helper. Quando isso não estiver disponível, o fluxo em Markdown usa o histórico visível e os checkpoints explícitos. O verificador confirma bytes locais e estrutura do localizador de TXT. Cabe ao host resolver esse localizador na interface.

## Verificação local

- Windows e Python 3.12.10. A suíte de raiz registrou 28 aprovações e dois saltos entre 30 testes. Os saltos são pela permissão de criação de symlinks de diretório no Windows (WinError 1314). A suíte do bundle registrou 38 aprovações, incluindo 14 regressões novas. Os casos novos usam dados sintéticos, cálculos e resultados esperados independentes. Incluem CLI JSON, versões, estados adversos, TXT divergente e troca de catálogo.
- Compilação Python, `upe doctor` e verificação explícita de metadados, links e manifesto do bundle. O parser YAML opcional estava indisponível e o frontmatter foi verificado estruturalmente.
- A CLI da versão anterior foi instalada em projeto temporário. A CLI da versão nova fez a atualização por recibo e verificou 62 arquivos. O ZIP standalone usa seu próprio manifesto. A instalação gerenciada usa recibo de hashes, conforme o comportamento existente.
- **Não executados:** protocolo comportamental com modelo real, benchmarks de latência, ativação do agente no host, matriz remota e build wheel/sdist (backend local ausente). Nenhuma inferência de teste, chamada paga, publicação ou troca de modelo. Disponibilidade de GPT-6.2 Sol High e cota Plus da conta também não foram verificadas.

## Instalação e avaliação

Para instalação standalone, confira o SHA-256, extraia o ZIP da skill e, na pasta extraída, execute `python scripts/verify_package.py`. Copie a pasta completa `universal-prompt-engineering` para `.agents/skills/` no projeto Codex. Verifique descoberta no cliente. Em instalação já gerenciada pela CLI, use `upe-skill update codex` com o escopo e projeto originais e faça `upe-skill verify codex` com os mesmos argumentos. Veja o guia de instalação do pacote.

A atualização é verificável no nível do contrato local: os casos exercitam bloqueios e entregas pelo mesmo fluxo e o formato é montado a partir do artefato revisado. A digitação de uma aprovação por um usuário real, o julgamento da qualidade semântica pelo modelo e a apresentação no cliente dependem do host e permanecem sem ensaio comportamental. O fluxo adota carregamento progressivo e reaproveitamento de contexto. Qualquer ganho de latência ainda precisa de comparação medida.
