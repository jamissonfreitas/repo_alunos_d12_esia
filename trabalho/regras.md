# Contrato do caso MiniLoja (versão 1.0)

MiniLoja é um backend **fictício** de pedidos de uma loja de material esportivo. Este documento é o **contrato**: define como o sistema deve funcionar. O "esperado" de qualquer teste deve vir daqui, e não do código. Os dados são sintéticos; escopo: entradas controladas, sem autenticação real nem integração externa.

## R1 · Cálculo do total do pedido
1. **Subtotal** = soma de `preço × quantidade` de todos os itens.
2. **Desconto**, aplicado ao subtotal:
   - `PROMO10`: 10%. `VIP15`: 15%.
   - `NATAL`: 20%, somente com a campanha ativa (variável de ambiente `MINILOJA_PROMO_NATAL=1`).
   - `FRETEGRATIS`: não altera o valor, mas zera o frete.
   - Cupom desconhecido: **ignorado**, sem erro.
3. **Frete**:
   - É **grátis** quando o subtotal **com desconto** é **maior ou igual a R$ 200,00**, ou com o cupom `FRETEGRATIS`.
   - Caso contrário, por UF: PE R$ 12,90 · SP R$ 19,90 · RJ R$ 21,50 · demais UFs R$ 29,90.
4. **Taxa de serviço** sobre (subtotal com desconto + frete): PE 5% · SP 7% · RJ 6% · demais 8%.
5. **Arredondamento:** duas casas decimais, **meio para cima** (R$ 15,645 vira R$ 15,65).
6. **Ordem:** desconto, depois frete, depois taxa.

## R2 · Pedido
1. Pedido **sem itens** é rejeitado (`400`).
2. Todos os itens precisam ter estoque. Se algum não tiver, o pedido é recusado (`409`) e **nenhuma reserva pode permanecer**.
3. Pagamento recusado **não salva** o pedido (`402`).

## R3 · Cadastro de cliente
1. Campos obrigatórios: `nome`, `email` e `cpf`.
2. O `cpf` deve ter **dígitos verificadores válidos** e **não pode ter todos os dígitos iguais**. Aceita com ou sem pontuação.
3. O `email` deve ter o formato `texto@texto.texto`.
4. Cadastro inválido responde **`422`** com a **lista de todos os erros** de uma vez: `{"erros": [{"campo": "...", "erro": "..."}]}`. Não responde só o primeiro erro.
5. Cadastro válido responde `201` com o cliente e um `id` sequencial.

## R4 · Acesso
1. Um usuário só pode ver os **próprios** pedidos.

## Dados de apoio
`caso/dados/cpfs.json` (CPFs fictícios válidos e inválidos) e `caso/dados/carrinhos.json` (carrinhos de exemplo).
