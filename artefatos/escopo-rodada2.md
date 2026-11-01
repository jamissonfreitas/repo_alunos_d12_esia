# Escopo da rodada 2 — refatoração de `calcular_total`

## Registro anterior ao pedido de plano

- **Data e hora:** 17/10/2026, 12:06:43 (America/Sao_Paulo; UTC−03:00).
- **Base lida:** roteiro da atividade, instruções locais do projeto, `exercicios/aula-2/README.md`, `caso/regras.md` (indicado no roteiro como contrato), implementação em `caso/miniloja/calculo.py` e registro de revisão já existente.

## Seis campos

- **Objetivo:** refatorar a implementação de `calcular_total` para tornar explícitas as etapas existentes de cálculo, preservando exatamente o comportamento atual.
- **Pode tocar:** somente `caso/miniloja/calculo.py`; extrair ou reorganizar helpers privados necessários à refatoração, sem mudar a interface pública.
- **Não pode tocar:** qualquer outro arquivo; assinatura pública `calcular_total(itens, cupom=None, uf="PE")`; tipos, precisão, arredondamento, ordem ou resultados do cálculo; regras, testes, golden master, flags, mensagens/erros observáveis e comportamento dos cupons.
- **Invariantes:** mesmas saídas exatas para as mesmas entradas e ambiente, inclusive casos de fronteira, entradas inválidas e erros atuais; mesma assinatura e ordem lógica subtotal → desconto → frete → taxa → arredondamento; nenhum ajuste de comportamento para alinhar implementação e contrato.
- **Critério de pronto:** refatoração limitada ao arquivo permitido, plano revisado antes da execução, comparação exata com o golden master aprovado e verificações pertinentes aprovadas, diff revisado e sem mudança observável fora da estrutura interna.
- **Critério de parada:** não executar e pedir orientação se o plano exigir outro arquivo, alterar comportamento ou interface, mudar tratamento de entradas/erros, tocar contrato/testes/golden, ou se houver ambiguidade material que impeça preservar o comportamento. Divergências entre código e contrato devem ser reportadas para decisão futura, sem correção nesta rodada.

## Plano original e revisão

- **Pedido de plano:** 17/10/2026, aproximadamente 12:07 (horário local). A solicitação não retornou um plano.
- **Plano original registrado para revisão, 17/10/2026, 12:11:04:**
  1. Antes de qualquer alteração, conferir o ponto de partida e validar que o golden master original foi capturado e pode ser comparado exatamente nas mesmas condições.
  2. Extrair a soma sequencial dos itens para um helper privado, preservando operações e ordem.
  3. Extrair a lógica de cupons para um helper privado que retorne o total e o indicador já existente de desconto; conservar literalmente as condições e a consulta à flag.
  4. Extrair frete e taxa para helpers privados, mantendo as comparações, ramificações e ordem atuais, inclusive o limite `total > 200`.
  5. Deixar `calcular_total(itens, cupom=None, uf="PE")` coordenar os helpers na ordem atual, mantendo arredondamento final, `pass` e chamadas observáveis.
  6. Revisar o diff e comparar as saídas exatas com o golden master e as verificações previstas; reportar divergências sem corrigir.
- **Revisão/cortes antes de qualquer execução:** removida do plano a ideia de substituir ramificações por dicionários/tabelas ou simplificar a lógica. Motivo: a implementação existente tem diferenças observáveis em entradas não hashable, exceções e mutabilidade que tais mudanças poderiam introduzir. Mantidas as condições e operações atuais dentro dos helpers. A etapa de validar o golden master é um bloqueio antes de executar: o roteiro exige validação pelo estudante, portanto não está presumida nem aprovada por este registro.
- **Estado:** nenhum arquivo de implementação foi alterado nesta rodada. O plano acima está registrado para revisão; execução não autorizada até validação da referência e revisão explícita do plano.
