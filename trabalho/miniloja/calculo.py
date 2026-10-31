"""Cálculo de totais de pedido (contrato: caso/regras.md, R1)."""
from miniloja import flags

FRETE_POR_UF = {"PE": 12.9, "SP": 19.9, "RJ": 21.5}
FRETE_DEMAIS_UFS = 29.9
TAXA_POR_UF = {"PE": 0.05, "SP": 0.07, "RJ": 0.06}
TAXA_DEMAIS_UFS = 0.08
LIMITE_FRETE_GRATIS = 200
CUPOM_FRETE_GRATIS = "FRETEGRATIS"


def calcular_total(itens, cupom=None, uf="PE"):
    """Calcula o total do pedido conforme R1: desconto, depois frete, depois taxa.

    Contrato (caso/regras.md, R1):
      1. subtotal = soma de preco * qtd;
      2. desconto sobre o subtotal: PROMO10 10%, VIP15 15%, NATAL 20% só com
         MINILOJA_PROMO_NATAL=1; FRETEGRATIS não altera o valor; cupom desconhecido
         é ignorado, sem erro;
      3. frete grátis com FRETEGRATIS ou subtotal com desconto >= R$ 200,00; senão
         PE 12,90 · SP 19,90 · RJ 21,50 · demais 29,90;
      4. taxa sobre (subtotal com desconto + frete): PE 5% · SP 7% · RJ 6% · demais 8%;
      5. duas casas, meio para cima.

    Divergências CONHECIDAS e PRESERVADAS de propósito (ver docs/ADR-001):
      D1. o frete grátis usa ``> 200`` (o contrato diz ``>= 200``): subtotal de
          exatamente R$ 200,00 ainda paga frete;
      D2. o arredondamento usa ``round()`` sobre float, que não é "meio para cima":
          2 x R$ 1,00 em PE dá 15,64 (o contrato pede 15,65).
    Esta função foi reestruturada sem mudar a saída (golden master com igualdade
    exata). Corrigir D1/D2 muda valores cobrados e é uma decisão separada.

    Por que as operações têm esta forma: o resultado é float e a ordem das
    operações faz parte do comportamento. ``base + base * taxa`` NÃO é trocado por
    ``base * (1 + taxa)``: em float os dois diferem no último bit e isso muda o
    arredondamento em alguns casos (o golden master detecta).

    Entrada fora do contrato: ``uf`` deve ser str (as tabelas são dicionários).
    """
    com_desconto = _aplicar_desconto(_subtotal(itens), cupom)
    base_taxa = com_desconto + _frete(com_desconto, cupom, uf)
    total = base_taxa + base_taxa * TAXA_POR_UF.get(uf, TAXA_DEMAIS_UFS)
    return round(total, 2)


def _subtotal(itens):
    """R1.1: soma de preco * qtd (começa em 0, como o original)."""
    total = 0
    for item in itens:
        total = total + item["preco"] * item["qtd"]
    return total


def _aplicar_desconto(subtotal, cupom):
    """R1.2: devolve o subtotal com desconto; cupom desconhecido ou None não altera."""
    if cupom == "PROMO10":
        return subtotal * 0.9
    if cupom == "VIP15":
        return subtotal * 0.85
    if cupom == "NATAL" and flags.promo_natal_ativa():  # flag só é lida para NATAL
        return subtotal * 0.8
    return subtotal


def _frete(com_desconto, cupom, uf):
    """R1.3: frete sobre o subtotal JÁ com desconto (R1.6). Ver D1 na docstring acima."""
    if cupom == CUPOM_FRETE_GRATIS or com_desconto > LIMITE_FRETE_GRATIS:
        return 0
    return FRETE_POR_UF.get(uf, FRETE_DEMAIS_UFS)