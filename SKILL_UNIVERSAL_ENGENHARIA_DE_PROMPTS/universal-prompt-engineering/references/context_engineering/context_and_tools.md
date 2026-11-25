# Contexto, memória e ferramentas

## Montagem do contexto

- Use contexto atual da conversa; resuma somente para resolver limite real, preservando restrições e correções.
- Separe instrução normativa, material-fonte citado, saída de ferramentas e conteúdo não confiável.
- Recupere fontes direcionadas; avalie autoridade, data e pertinência em vez de despejar arquivos inteiros.
- Registre no prompt referências relativas e carregue só o módulo relevante para conter custo de contexto.
- Nunca declare memória permanente sem mecanismo verificável. A sessão, o projeto e a memória persistente são escopos diferentes.

## Ferramentas e agentes

Uma instrução de ferramenta deve incluir: finalidade, quando usar, entradas esperadas, restrição de acesso, validação do retorno, falha/time-out, retry permitido e critério de parada. Não instrua a chamar ferramenta inexistente. Se tool puder escrever, enviar, comprar, excluir ou publicar, obedeça o gate de autorização do host e do usuário; o prompt não substitui isso.

## Arquivos de instrução

Skill/on-demand procedure, regra persistente e agente especializado têm escopos diferentes por produto. Verifique precedência, carregamento, diretórios e compartilhamento cloud/local na documentação do host; `../COMPATIBILITY_MATRIX.md` é snapshot, não política permanente.
