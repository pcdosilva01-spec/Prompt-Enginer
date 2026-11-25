# Engenharia Universal de Prompts

Base de conhecimento sobre engenharia de prompts com evidências, uma Skill portátil no padrão Agent Skills e um instalador/verificador local opcional.

**Estado:** `0.1.0a5` é um candidato local com ZIP autocontido da skill e ZIP de fonte. Instalação no host e comportamento do modelo exigem validação própria. Consulte [prontidão da versão](docs/audits/RELEASE_READINESS.md) e [situação da licença](LICENSING.md) antes de redistribuir.

## Conteúdo

- `src/upe/resources/skill/universal-prompt-engineering/`: pacote canônico e autocontido da Skill.
- `src/upe/`: CLI sem dependências de execução para instalar, atualizar, verificar, remover, diagnosticar e resolver caminhos locais.
- `DOSSIER_ENGENHARIA_DE_PROMPTS/`: dossiê e relatórios originais preservados. A Skill autocontida traz uma cópia verificada por hash em `src/upe/resources/skill/universal-prompt-engineering/references/original_dossier/`.
- `docs/audits/`: relatórios de portabilidade, segurança, integridade, testes, versão, avaliação e limpeza do repositório.
- `SKILL_UNIVERSAL_ENGENHARIA_DE_PROMPTS/` e o ZIP na raiz: snapshots legados mantidos sem alteração.

A Skill não exige dependência em tempo de execução. A CLI opcional requer Python 3.10+. Consulte [instalação](INSTALLATION.md), [comandos](COMMANDS.md), [compatibilidade](COMPATIBILITY.md) e [guia para agentes](INSTALL_FOR_AI_AGENTS.md).

## Uso rápido

Em um checkout local, instale a CLI isolada com pipx:

```powershell
pipx install .
upe-skill list-targets
upe-skill doctor
upe-skill install codex --scope user --dry-run
```

Retire `--dry-run` somente depois de conferir o destino. Para escopo de projeto, informe um `--project-dir` existente. O instalador recusa substituir arquivos sem propriedade registrada ou arquivos gerenciados que foram editados; ele registra hashes de propriedade e remove somente arquivos inalterados que ele próprio instalou.

Para usar a Skill sem a CLI, copie a pasta canônica inteira, mantendo o nome `universal-prompt-engineering`, para um diretório de skills aceito pelo host. Confira a versão e a descoberta na [matriz de compatibilidade](COMPATIBILITY.md).

## Verificações de desenvolvimento

```powershell
python -m compileall -q src tests
python -m unittest discover -s tests -v
python -m unittest discover -s src/upe/resources/skill/universal-prompt-engineering/tests -v
python -m upe version
python -m upe doctor
```

CI está configurada para Windows, macOS, Linux e Python 3.10, 3.12 e 3.13. Não alegamos execução do workflow até que ele rode no GitHub.

## Licença

Nenhuma licença foi concedida. Consulte [LICENSING.md](LICENSING.md). A visibilidade pública do código não concede, por si só, autorização para redistribuí-lo.
