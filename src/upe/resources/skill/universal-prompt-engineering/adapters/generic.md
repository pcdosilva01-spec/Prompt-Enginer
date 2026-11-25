# Adaptador genérico Markdown

Para prosa brasileira em um chat sem leitura confirmada de skills ou arquivos, entregue o [núcleo portátil](../references/writing/humanizer.md) dentro do prompt.

Se o ambiente não documenta skills, use o conteúdo apenas como material de referência, copiando os pontos relevantes para o campo de instruções aceito pelo host. Preserve a ordem de prioridade que o host realmente aplica; não anuncie descoberta automática, anexos relativos, memória, ferramentas, sandbox ou enforcement sem verificação. Resuma para caber no limite conhecido e mantenha o pacote completo em armazenamento acessível. A regra de aprovação ainda pode ser seguida pelo agente, mas só tem controle externo se houver mecanismo real de estado/host.

Use a [seleção de modelo](../references/models/model_selection.md) com recomendação condicional se o catálogo não for verificável. Preserve resumo numerado e aprovação, depois use [a lista de entrega](../workflows/evaluation_and_delivery.md) com bloco único de texto se faltar componente nativo e informe limites de TXT conforme o host.
