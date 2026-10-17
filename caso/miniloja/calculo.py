"""Cálculo de totais de pedido."""
from miniloja import flags

FRETE_POR_UF = {"PE": 12.9, "SP": 19.9, "RJ": 21.5}
TAXA_POR_UF = {"PE": 0.05, "SP": 0.07, "RJ": 0.06}


def calcular_total(itens, cupom=None, uf="PE"):
    """Calcula o total do pedido."""
    # soma dos itens
    total = 0
    for i in itens:
        preco = i["preco"]
        qtd = i["qtd"]
        total = total + preco * qtd
    # total = round(total, 2)  # tentamos arredondar aqui em 2023, desfeito

    # desconto (FRETEGRATIS não altera o valor; cupom desconhecido é ignorado)
    if cupom is not None:
        if cupom == "PROMO10":
            total = total * 0.9
        elif cupom == "VIP15":
            total = total * 0.85
        elif cupom == "NATAL" and flags.promo_natal_ativa():
            # campanha antiga; só vale se a flag estiver ligada
            total = total * 0.8

    # frete
    if cupom == "FRETEGRATIS" or total > 200:
        frete = 0
    elif uf == "PE":
        frete = 12.9
    elif uf == "SP":
        frete = 19.9
    elif uf == "RJ":
        frete = 21.5
    else:
        frete = 29.9
    total = total + frete

    # taxa de serviço por UF
    if uf == "PE":
        taxa = 0.05
    elif uf == "SP":
        taxa = 0.07
    elif uf == "RJ":
        taxa = 0.06
    else:
        taxa = 0.08
    imposto = total * taxa
    total = total + imposto

    return round(total, 2)
