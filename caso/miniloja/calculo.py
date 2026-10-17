"""Cálculo de totais de pedido."""
from miniloja import flags

FRETE_POR_UF = {"PE": 12.9, "SP": 19.9, "RJ": 21.5}
FRETE_PADRAO = 29.9
TAXA_POR_UF = {"PE": 0.05, "SP": 0.07, "RJ": 0.06}
TAXA_PADRAO = 0.08
FATOR_POR_CUPOM = {"PROMO10": 0.9, "VIP15": 0.85}
FATOR_NATAL = 0.8
LIMITE_FRETE_GRATIS = 200


def _subtotal(itens):
    # laço explícito de propósito: sum() usa soma compensada em float no 3.12+
    total = 0
    for i in itens:
        total = total + i["preco"] * i["qtd"]
    # total = round(total, 2)  # tentamos arredondar aqui em 2023, desfeito
    return total


def _aplicar_desconto(valor, cupom):
    if cupom in FATOR_POR_CUPOM:
        return valor * FATOR_POR_CUPOM[cupom]
    if cupom == "NATAL" and flags.promo_natal_ativa():
        # campanha antiga; só vale se a flag estiver ligada
        return valor * FATOR_NATAL
    # FRETEGRATIS não altera o valor; cupom desconhecido é ignorado
    return valor


def _frete(base, cupom, uf):
    if cupom == "FRETEGRATIS" or base > LIMITE_FRETE_GRATIS:
        return 0
    return FRETE_POR_UF.get(uf, FRETE_PADRAO)


def _taxa(uf):
    return TAXA_POR_UF.get(uf, TAXA_PADRAO)


def calcular_total(itens, cupom=None, uf="PE"):
    """Calcula o total do pedido: desconto, depois frete, depois taxa."""
    total = _aplicar_desconto(_subtotal(itens), cupom)
    total = total + _frete(total, cupom, uf)
    total = total + total * _taxa(uf)
    return round(total, 2)
