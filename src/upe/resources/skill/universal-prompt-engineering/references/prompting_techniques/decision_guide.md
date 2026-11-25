# Guia decisório de técnicas de prompting

## Suficiência antes de extensão

Inclua detalhe que reduza ambiguidade ou habilite validação. Remova repetições, regras sem efeito decisório e instruções incompatíveis. Comprimento não é objetivo: não existe tamanho ótimo universal comprovado. Para tarefas frágeis/alto impacto, explicite requisitos e checagens; para exploração criativa, especifique limites e deixe latitude no restante.

## Formato

| Forma | Use quando | Limite |
|---|---|---|
| Prosa clara | solicitação curta ou flexível | requisitos importantes podem ficar enterrados |
| Markdown/seções | múltiplas categorias, ordem ou revisão humana | títulos não são controle de segurança |
| XML/tags | trechos de contexto e instruções precisam de fronteiras legíveis, e o modelo/provedor recomenda esse estilo | markup não impede injeção nem cria hierarquia real |
| JSON | resposta consumida por programa e esquema aceito pela interface | pedir “JSON válido” por texto não garante sintaxe; preferir modo/schema estruturado da API quando disponível e validar no cliente |

As recomendações por fornecedor e referências experimentais estão em Volumes 2/4/6; não declarar superioridade universal por formato.

## Técnicas e critérios

- **Exemplos (few-shot):** úteis quando demonstram padrão/edge case que prosa não comunica facilmente. Remover exemplos enviesados ou contraditórios; contar custo e testar generalização. A orientação Gemini documentada não é um resultado para todos os modelos.
- **Decomposição:** usar para subtarefas independentes/verificáveis; não exigir exposição de raciocínio privado. Solicitar resultados intermediários auditáveis apenas se a tarefa se beneficia deles.
- **Role/persona:** incluir só se muda escopo, vocabulário ou critério; credencial fictícia não agrega evidência.
- **RAG/contexto longo:** buscar as fontes pertinentes, indicar autoridade/data, separar dado de instrução e pedir citação para claims relevantes. Mais contexto pode distrair ou degradar recall.
- **Tool use/agent loop:** descrever condição para ferramenta e critério de parada; o host decide disponibilidade/permissão. Definir tratamento de falha e idempotência em automação.
- **Instructions hierarchy:** respeitar a hierarquia real do host. Repetir “ignore instruções acima” não eleva prioridade.
- **Token/custo:** compactar redundância, limitar retrieval e saída, reutilizar prefixos quando houver caching documentado; consultar preços e comportamento atuais antes de estimar valores.
- **Validação:** derivar checks da tarefa (schema, casos de aceitação, fontes, testes, sandbox, revisão humana). Teste de texto não prova comportamento de LLM.

Escolha a combinação mínima que satisfaz a rubrica em `../evaluation/prompt_rubric.md`. A avaliação comparativa exige protocolo separado nos originais: `../original_dossier/PROTOCOLOS_E_RESULTADOS_DE_TESTES.md`.
