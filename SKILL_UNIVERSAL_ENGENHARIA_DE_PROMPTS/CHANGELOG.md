# Changelog

## 1.0.1 — 23/11/2026

- Sincronizados os três relatórios divergentes da cópia do dossiê; todos os 14 arquivos-fonte agora conferem por SHA-256.
- Rejeitados estados/eventos e campos de diagnóstico com tipos inválidos no helper de aprovação; acrescentados testes de regressão.
- O empacotador agora valida um ZIP temporário antes da substituição atômica, preserva o ZIP anterior quando a escrita falha e rejeita caminhos de entrada/saída simbólicos.
- Atualizados ledger de plataforma, manifestos e auditorias após as novas verificações.
- Testes comportamentais com LLM e instalação em hosts continuam pendentes; nenhum resultado foi simulado.

## 1.0.0 — 23/11/2026

- Criado pacote independente com skill principal, referências modulares, workflows, templates e adaptadores por superfície.
- Preservada a cópia integral dos 14 documentos do dossiê e registrado inventário SHA-256.
- Implementado helper determinístico de estado para aprovação vinculada ao resumo, diagnóstico de rejeição e invalidação por mudança material.
- Adicionadas verificações de pacote e testes automatizados; incluídos cenários conversacionais como especificações, separados de testes de inferência.
- Pesquisados documentos oficiais atuais de Agent Skills para os hosts apresentados na matriz. Sem instalação ou chamada de modelo.
