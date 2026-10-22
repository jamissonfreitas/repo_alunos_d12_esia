"""Golden master de calcular_total.

Uso (rodar de dentro da pasta caso/):
    python golden_master.py gravar    # ANTES de refatorar: grava as saidas atuais
    python golden_master.py comparar  # DEPOIS de refatorar: compara com igualdade exata

Grava o repr() do float, entao a comparacao e bit a bit (sem tolerancia).
"""
import json
import os
import sys
from unittest import mock

from miniloja.calculo import calcular_total

ARQUIVO = "golden_master.json"

# carrinhos variados (inclui bordas do frete em 200 e casos de arredondamento)
CARRINHOS = {
    "vazio": [],
    "simples": [{"preco": 50.0, "qtd": 2}],                      # 100
    "quase_200": [{"preco": 199.99, "qtd": 1}],
    "exato_200": [{"preco": 100.0, "qtd": 2}],                   # borda R1 (>=200)
    "acima_200": [{"preco": 200.01, "qtd": 1}],
    "vip_cai_p_200": [{"preco": 235.30, "qtd": 1}],              # 235.30*0.85 ~ 200
    "centavos": [{"preco": 9.99, "qtd": 3}, {"preco": 0.1, "qtd": 7}],
    "qtd_zero": [{"preco": 80.0, "qtd": 0}, {"preco": 15.45, "qtd": 1}],
    "grande": [{"preco": 129.9, "qtd": 3}, {"preco": 39.9, "qtd": 5}],
}
CUPONS = [None, "PROMO10", "VIP15", "FRETEGRATIS", "NATAL", "INVALIDO", "promo10"]
UFS = ["PE", "SP", "RJ", "BA"]
NATAL_FLAG = ["0", "1"]


def gerar_casos():
    for nome, itens in CARRINHOS.items():
        for cupom in CUPONS:
            for uf in UFS:
                # a flag so faz diferenca para NATAL; evita casos duplicados
                flags = NATAL_FLAG if cupom == "NATAL" else ["0"]
                for flag in flags:
                    yield {"carrinho": nome, "cupom": cupom, "uf": uf, "natal": flag}


def executar(caso):
    with mock.patch.dict(os.environ, {"MINILOJA_PROMO_NATAL": caso["natal"]}):
        try:
            return repr(calcular_total(CARRINHOS[caso["carrinho"]],
                                       cupom=caso["cupom"], uf=caso["uf"]))
        except Exception as e:  # excecao tambem e comportamento
            return f"ERRO {type(e).__name__}: {e}"


def chave(caso):
    return f'{caso["carrinho"]}|{caso["cupom"]}|{caso["uf"]}|natal={caso["natal"]}'


def gravar():
    saidas = {chave(c): executar(c) for c in gerar_casos()}
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(saidas, f, indent=1, ensure_ascii=False)
    print(f"Gravadas {len(saidas)} entradas em {ARQUIVO}")


def comparar():
    with open(ARQUIVO, encoding="utf-8") as f:
        esperado = json.load(f)
    falhas = 0
    for c in gerar_casos():
        k, obtido = chave(c), executar(c)
        if obtido != esperado.get(k):  # igualdade exata
            falhas += 1
            print(f"DIFERENTE {k}: esperado={esperado.get(k)} obtido={obtido}")
    total = len(esperado)
    print(f"{total - falhas}/{total} iguais, {falhas} diferentes")
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    {"gravar": gravar, "comparar": comparar}[sys.argv[1]]()