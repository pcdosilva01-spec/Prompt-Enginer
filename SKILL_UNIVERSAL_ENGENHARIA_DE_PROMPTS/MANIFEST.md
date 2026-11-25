# Manifesto do pacote

Este diretório de entrega contém relatórios da implementação; o diretório instalável é `universal-prompt-engineering/`. Dentro dele, `MANIFEST.sha256` lista SHA-256 de todos os arquivos da skill, exceto o próprio manifesto. `references/original_dossier/ORIGINALS_SHA256.json` lista os 14 documentos originais preservados.

Para gerar/verificar a lista de hashes dos originais, rode `python scripts/build_original_manifest.py --source <caminho-do-dossie-original>` na pasta da skill. Para regenerar a lista de arquivos, rode `python scripts/build_manifest.py`. Isso muda o snapshot de integridade, não o conteúdo. Para verificar o pacote e comparar com a fonte de desenvolvimento, `python scripts/verify_package.py --source-dossier <caminho-do-dossie-original>`.

O ZIP distribuível contém somente a pasta da skill, com referências, exemplos, testes e scripts. O empacotador monta e verifica um temporário antes de substituir o ZIP existente de forma atômica; se a gravação ou verificação falhar, o arquivo anterior permanece intacto. Os relatórios da implementação permanecem no diretório externo.
