# AV3 B3 — escopo e plano anteriores à mudança

Data: 01/11/2026. Base: `1a12ad2`, branch `av3-b3-reserva-estoque`.

1. Objetivo: cumprir R2.2; insuficiência em qualquer item deve produzir 409 sem consumir saldo nem deixar reservas desta tentativa.
2. Pode tocar: `caso/miniloja/estoque.py`, `caso/miniloja/pedidos.py`, `caso/testes_existentes/test_pedidos.py` e novos arquivos desta pasta.
3. Não pode tocar: `testes/`, `caso/regras.md`, cálculo, cadastro, acesso, pagamentos, registros anteriores e arquivos fornecidos da AV2.
4. Invariantes: assinatura de `criar`, formato das respostas, exceção `EstoqueInsuficiente`, fluxo aprovado e comportamento de pagamento recusado. Preservar reservas de pedidos anteriores, inclusive do mesmo usuário.
5. Pronto quando: regressão comprovadamente vermelha antes e verde depois; saldo e reservas comparados exatamente; 409 sem cobrança/salvamento; suíte existente e golden conferidos; diff restrito à lista permitida.
6. Parar se: forem necessárias mudanças no contrato, dependências, cálculo, autenticação ou política de pagamento. Concorrência e persistência exigem outra solução e ficam fora desta tarefa didática em memória.

Plano revisado pelo assistente antes de editar o caso: escrever regressão com objetos reais; executar antes; adicionar `Estoque.reservar_lote`, que simula os débitos em uma cópia dos saldos e somente reserva após validar todos; usar o lote em `PedidoService`; atualizar a expectativa do teste de colaboração; executar depois e registrar resultados. A simulação deve descontar SKUs repetidos cumulativamente. Não limpar todas as reservas nem restaurar saldos globais: isso poderia apagar trabalho anterior. Não ampliar para falhas de pagamento ou exceções arbitrárias.

Modo: agente de codificação com escopo explícito e verificações locais. Raio limitado a estoque/pedidos, oráculo R2.2 e testes observáveis; familiaridade adquirida pela leitura do contrato e dos módulos. Alternativa: edição manual, com mais controle por linha, mas exigindo as mesmas provas. O estudante revisou e aceitou o escopo e o plano, conferiu a prevenção de reservas parciais e a prova de regressão, executou os comandos e registrou as saídas.
