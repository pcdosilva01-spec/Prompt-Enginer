# Skill Universal de Engenharia de Prompts

Pacote de distribuição e auditoria da skill `universal-prompt-engineering`. A skill executável está em [`universal-prompt-engineering/`](universal-prompt-engineering/SKILL.md); copie **essa pasta** para o diretório de skills do host. Este diretório externo contém relatórios, matrizes e instruções para a distribuição.

## Conteúdo

- `universal-prompt-engineering/SKILL.md`: ponto de entrada conciso, com aprovação explícita antes de gerar prompts definitivos.
- `universal-prompt-engineering/references/`: módulos de conhecimento e cópia integral do dossiê original.
- `universal-prompt-engineering/workflows/`, `templates/`, `adapters/`, `examples/`: procedimentos e recursos de consulta progressiva.
- `universal-prompt-engineering/scripts/`, `tests/`: verificação determinística do estado de aprovação e integridade do pacote.
- `COMPATIBILITY_MATRIX.md`, `KNOWLEDGE_INDEX.md`, `INSTALLATION.md`: compatibilidade pesquisada em fontes primárias e uso por host.
- `audits/`: matriz de rastreabilidade, cobertura, testes, segurança e avaliações finais.

## Integridade do dossiê

Os 14 arquivos em `universal-prompt-engineering/references/original_dossier/` são cópias byte a byte do dossiê de origem. A verificação SHA-256 consta em `ORIGINALS_SHA256.json`; a suíte valida cada arquivo copiado. Nenhum arquivo do dossiê de origem foi editado nesta implementação.

## Validação local

Com Python 3.10+, na pasta `universal-prompt-engineering/`:

```powershell
python -m unittest discover -s tests -v
python scripts/verify_package.py --source-dossier ..\..\DOSSIER_ENGENHARIA_DE_PROMPTS
```

Consulte `INSTALLATION.md` para instalação. A execução desta suíte não representa validação comportamental em LLMs.
