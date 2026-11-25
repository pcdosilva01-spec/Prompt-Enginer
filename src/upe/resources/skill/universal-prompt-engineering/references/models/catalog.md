# Fichas de modelos por superfície

Corte documental em 25/11/2026. Abra apenas a ficha do destino. A API de um provedor, seus pesos e o agente que ele oferece podem ter IDs, cotas, ferramentas e comportamentos distintos.

- [OpenAI API · OpenAI](catalog/openai.json)
- [Codex · OpenAI](catalog/codex.json)
- [Claude API · Anthropic](catalog/anthropic.json)
- [Gemini API · Google](catalog/google.json)
- [xAI API · xAI / SpaceXSI](catalog/xai.json)
- [DeepSeek API · DeepSeek](catalog/deepseek.json)
- [Alibaba Model Studio · Alibaba Cloud](catalog/alibaba.json)
- [Pesos Llama · Meta](catalog/meta.json)
- [Mistral API · Mistral AI](catalog/mistral.json)
- [Cohere API · Cohere](catalog/cohere.json)
- [Z.ai API · Z.ai](catalog/zai.json)
- [Pesos Kimi · Moonshot AI](catalog/moonshot.json)

## Como ler e atualizar

Cada arquivo contém o ledger das fontes dessa superfície. `publisher`, `checked`, `level` e `limits` aplicam-se aos registros. `sources` liga cada modelo aos títulos, URLs, edições e claims. E2 descreve documentação primária. `guide` é aplicação editorial da UPE (E4). `unsupported_efforts` (opcional) registra apenas valores explicitamente rejeitados na superfície da ficha; não é lista exaustiva dos demais valores aceitos. `null` significa que o campo não foi confirmado neste levantamento; uma lista de recursos vazia indica ausência de confirmação. `listed` indica oferta documentada sem afirmação de GA. `stable` exige rótulo de estabilidade. `preview` pede revisão próxima. `announced` não comprova operação. `restricted` depende de habilitação específica. `deprecated` admite integração existente enquanto servida. `retired` exclui seleção operacional nessa superfície. Não deduza datas de lançamento de números de versão.

Os limites em tokens dizem respeito ao endpoint citado. Campos de saída podem representar o caminho síncrono padrão; leia as notas de modos especiais. `schema` indica saída estruturada documentada, `json` somente JSON. Verifique o subconjunto de schema e valide o conteúdo. `pricing` registra unidade, escopo e condições. Calcule custo com entradas sem cache, leituras, escritas, saídas e ferramentas, acrescente armazenamento se aplicável. Crédito de assinatura, quota por janela e preço de API são medidas diferentes. Taxa menor por token não comprova economia por tarefa.

O host deve reconfirmar plano, acesso, região e ferramentas disponíveis no momento da seleção. Reveja preço ofertado, ID móvel, preview, sunset ou qualquer divergência material antes de aconselhar uma compra ou migração. Como triagem offline, `scripts/model_catalog.py --strict-age` cobra revisão de previews, restritos e anunciados após 7 dias, fichas com tarifa após 14, demais ativos após 30 e histórico de retirados/depreciados após 90. Uma data explícita de fim da condição antecipa o vencimento. O comando aceita `--family google` e `--as-of AAAA-MM-DD`. A verificação é local e deliberada. Reabrir fontes afetadas, atualizar claims e datas somente depois da leitura, executar os testes e regenerar o manifesto. Nenhuma consulta, cobrança ou agendamento faz parte do verificador.

## Decisões com lacunas

Instruções de sistema e exemplos fazem parte do contexto da inferência. Pesos e data de corte descrevem aprendizado anterior. Recuperação depende de índice, consulta e documentos efetivamente devolvidos. Cache reutiliza processamento de prefixos e memória depende de persistência do host. Um modelo que aceita tool calls pode sugerir argumentos; o harness valida e decide se pode executá-los. Confirme permissões e resultados antes de fundamentar uma conclusão neles.

Quando só há uma ficha de pesos, registre revisão/tokenizador, template, quantização, servidor e janela realmente configurada. Para modelos fechados, reporte apenas o mecanismo exposto (por exemplo, esforço adaptativo), o corte publicado e as limitações documentadas. Número de parâmetros, composição do corpus e receita de treino permanecem desconhecidos se a fonte não os informa. Os benchmarks do fornecedor não entram como pontuação no seletor. Não há medidas locais de latência, naturalidade ou ganho de qualidade.

Divergências preservadas: a tabela de preços xAI lista um ID que o changelog encerrou; consulte ambos na ficha xAI. No Google, datas de fim dos preços introdutórios podem vencer antes da revisão periódica. Na DeepSeek, o nome legado aceito pelo servidor pode apontar a outros pesos. Refaça a comparação quando mudar a versão mesmo que o alias continue aceito.
