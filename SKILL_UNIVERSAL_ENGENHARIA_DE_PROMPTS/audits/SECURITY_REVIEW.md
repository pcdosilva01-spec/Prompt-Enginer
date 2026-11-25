# Revisão de segurança

## Escopo e método

Inspeção documental do conteúdo gerado, helper e scripts; revisão adversarial das fronteiras de confiança e permissões. Não é pentest da plataforma nem red-team de um LLM.

## Resultados

| ID | Achado | Risco | Controle aplicado | Evidência/verificação |
|---|---|---|---|---|
| SEC-01 | texto de referência pode conter prompt injection | Alto | instruções externas tratadas como dados; autoridade não sobe por conteúdo | `SKILL.md`, `threat_model.md`, cenário 9 |
| SEC-02 | agente pode confundir aprovação de resumo com execução externa | Alto | gates separados; aprovação da tarefa não concede autorização de tool | approval workflow e estados estruturados |
| SEC-03 | instrução natural não impõe política | Alto | declarar que o gate é interação, não enforcement; exigir controle host | documentação em `SKILL.md` |
| SEC-04 | `allowed-tools` amplo ou shell preapproval amplia impacto | Alto | frontmatter package não declara ferramentas pré-aprovadas; docs alertam risco | `agents/openai.yaml` contém só UI/policy |
| SEC-05 | cópia de skill de terceiro pode executar script | Alto | recomendar inspeção; scripts incluídos são locais/dependência zero | inspeção do código do pacote; sem rede |
| SEC-06 | logs/hash podem revelar dados se aplicados ao conteúdo de usuário | Médio | helper recebe resumo, não persiste estado; não incluir segredos em logs | `approval_gate.py` imprime JSON só na CLI; sem escrita a disco |
| SEC-07 | status/caminhos voláteis podem orientar instalação errada | Médio | data de verificação, claims limitados e nota de redirects/rollout | source ledger e compatibility matrix |
| SEC-08 | estado ou evento malformado podia gerar `AttributeError` no helper ou um objeto falsy não-objeto ser tratado como estado inicial | Médio | validação explícita de tipos em `from_dict`, `apply` e campos textuais; erro controlado `GateError` | 5 novos testes de entrada inválida; suíte final em `TEST_REPORT.md` |
| SEC-09 | empacotador truncava o ZIP existente antes de verificar a nova escrita | Médio | cria arquivo temporário no mesmo diretório, valida CRC/inventário/hashes e só então usa `os.replace` | teste injeta falha de escrita e confirma que o ZIP anterior fica intacto e temporário é limpo |
| SEC-10 | links simbólicos de entrada ou destino poderiam atravessar limites esperados | Médio | rejeita entradas simbólicas antes da verificação e saída simbólica antes de resolver/escrever o caminho | dois testes com condição `is_symlink` simulada; criação de symlink real não foi permitida neste Windows |

## Verificações

- Nenhum segredo foi inserido nos prompts, fontes ou scripts.
- Helper não escreve arquivos e não faz rede; só aplica eventos estruturados à instância serializada.
- Scripts package verifier/build manifest leem apenas dentro da pasta da skill e escrevem manifesto local explicitamente invocado.
- Nenhuma permissão/tool default foi ampliada.
- Os hashes confirmam integridade documental, não confiança/autenticidade de origem.
- `package_skill.py` não usa dependências externas, prepara e verifica o arquivo temporário antes de substituir o ZIP existente; falhas simuladas preservam os bytes anteriores.
- Entradas simbólicas e destino simbólico são rejeitados antes de ler conteúdo do pacote ou tocar no destino; a verificação de symlink usou simulação porque o ambiente não concede privilégio para criar symlinks reais.

## Limites e pendências

Sem host real ou modelo não é possível testar injection de runtime, vazamento, elicitação de aprovação falsa ou enforcement. O helper continua sem autenticar estado serializado e não interpreta linguagem natural; esse estado deve permanecer confiável e o host deve aplicar suas próprias permissões. Antes de uso em ações sensíveis: testar em sandbox isolado, inspecionar scripts, rever política de ferramentas e solicitar auditoria independente.
