# Repositório: relatório de limpeza

**Data:** 24 de novembro de 2026  
**Base verificada:** `main` no commit `6bcfb75`  
**Escopo:** reduzir cópias redundantes, remover os utilitários de force-push e preservar os arquivos originais protegidos pelo usuário.

## Removido

- `docs/research/DOSSIER_ENGENHARIA_DE_PROMPTS/`: 14 arquivos. Antes da remoção, todos foram comparados por SHA-256 com os arquivos correspondentes em `DOSSIER_ENGENHARIA_DE_PROMPTS/`; os 14 pares eram idênticos.
- `docs/history/v1.0.1/`: 13 arquivos que espelhavam a distribuição legada ainda mantida na raiz. Doze tinham SHA-256 idêntico ao arquivo correspondente; o README era uma cópia com caminhos adaptados e conteúdo já presente no README legado preservado.
- `push_force_Prompter-Silva.bat` da raiz e a cópia auxiliar local `tools/push_force_Prompter-Silva.bat`. O histórico Git anterior foi mantido; não houve reescrita de commits.
- Arquivos gerados em `dist/` deixaram de ser elegíveis para o ZIP de código-fonte e a pasta passou a ser ignorada pelo Git.

## Preservado

- `DOSSIER_ENGENHARIA_DE_PROMPTS/`: os 14 arquivos originais e relatórios, sem alteração.
- `SKILL_UNIVERSAL_ENGENHARIA_DE_PROMPTS/`: os 70 arquivos legados, sem alteração.
- `SKILL_UNIVERSAL_ENGENHARIA_DE_PROMPTS.zip`: arquivo original, 119.850 bytes; SHA-256 anterior à limpeza `12F058568D8AB1DE4FDF59E0A070D2CDDC7EAF93820CB663A1C1469C9158FDBB`.
- `src/upe/resources/skill/universal-prompt-engineering/references/original_dossier/`: cópia de 14 arquivos mantida de propósito. Ela torna a Skill instalável autocontida, e seu manifesto registra hashes para verificação.
- `docs/research/PLATFORM_RESEARCH_SNAPSHOT.md` e os relatórios atuais de auditoria.

## Verificações e limites

- A comparação SHA-256 foi feita antes das exclusões; os caminhos protegidos foram confirmados presentes depois da limpeza.
- O teste automático não foi executado novamente nesta limpeza. As alterações de documentação e exclusões não foram apresentadas como testes funcionais.
- O ZIP de código-fonte anterior era anterior à limpeza; ele foi reconstruído e seu conteúdo, CRC e SHA-256 foram conferidos separadamente. O ZIP original legado acima não foi reconstruído nem substituído.
- O commit de limpeza foi publicado em `main` com avanço rápido. A verificação remota confirmou a ausência dos caminhos removidos e a permanência dos arquivos protegidos.

## Duplicações mantidas por necessidade

O espelho em `src/upe/resources/skill/...` e o pacote legado na raiz contêm arquivos iguais em parte. Ambos permanecem porque o usuário determinou a preservação integral do pacote legado, enquanto a CLI precisa carregar uma Skill autocontida em seus próprios recursos. O dossiê também continua no diretório de origem e no pacote autocontido por esse motivo.
