"""Golden master de `calcular_total` (AV1.2, passo zero).

Grava o comportamento ATUAL (inclusive o que parece bug) e compara com
igualdade exata: o repr() do retorno é comparado como texto, sem tolerância.

Uso, na raiz do pacote:
    python -B exercicios/aula-2/golden_master.py --gravar        # grava uma vez
    python -B exercicios/aula-2/golden_master.py                 # compara
    python -B exercicios/aula-2/golden_master.py --codigo DIR    # compara outra cópia
"""
import argparse
import itertools
import json
import os
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
ARQUIVO = AQUI / "golden_master.json"

CUPONS = [None, "PROMO10", "VIP15", "FRETEGRATIS", "NATAL", "CUPOMFALSO", "promo10"]
UFS = ["PE", "SP", "RJ", "BA", "pe"]
FLAGS_NATAL = ["0", "1"]


def carrinhos():
    dados = json.loads((RAIZ / "caso" / "dados" / "carrinhos.json").read_text(encoding="utf-8"))
    base = dict(dados["carrinhos"])
    base.update({
        "vazio": [],
        "subtotal_200_exato": [{"preco": 100.0, "qtd": 2}],
        "subtotal_200_01": [{"preco": 200.01, "qtd": 1}],
        "promo10_perto_de_200": [{"preco": 222.23, "qtd": 1}],
        "centavos_quebrados": [{"preco": 33.33, "qtd": 3}, {"preco": 0.01, "qtd": 1}],
        "arredondamento_meio": [{"preco": 14.9, "qtd": 1}],
    })
    return base


def casos():
    for (nome, itens), cupom, uf, flag in itertools.product(
        carrinhos().items(), CUPONS, UFS, FLAGS_NATAL
    ):
        chave = f"{nome}|{cupom}|{uf}|NATAL={flag}"
        yield chave, itens, cupom, uf, flag


def executar(calcular_total):
    saidas = {}
    flag_original = os.environ.get("MINILOJA_PROMO_NATAL")
    try:
        for chave, itens, cupom, uf, flag in casos():
            os.environ["MINILOJA_PROMO_NATAL"] = flag
            try:
                r = calcular_total([dict(i) for i in itens], cupom, uf)
                saidas[chave] = f"{type(r).__name__}:{r!r}"
            except Exception as e:  # o comportamento atual inclui exceções
                saidas[chave] = f"EXC:{type(e).__name__}"
    finally:
        if flag_original is None:
            os.environ.pop("MINILOJA_PROMO_NATAL", None)
        else:
            os.environ["MINILOJA_PROMO_NATAL"] = flag_original
    return saidas


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--codigo", default="caso", help="pasta com o pacote miniloja")
    p.add_argument("--gravar", action="store_true", help="grava o golden master")
    args = p.parse_args()

    sys.path.insert(0, str(Path(args.codigo).resolve()))
    from miniloja.calculo import calcular_total

    obtido = executar(calcular_total)

    if args.gravar:
        ARQUIVO.write_text(json.dumps(obtido, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Gravados {len(obtido)} casos em {ARQUIVO.relative_to(RAIZ)}")
        return 0

    esperado = json.loads(ARQUIVO.read_text(encoding="utf-8"))
    divergencias = [
        (k, esperado.get(k, "<ausente>"), obtido.get(k, "<ausente>"))
        for k in sorted(set(esperado) | set(obtido))
        if esperado.get(k) != obtido.get(k)
    ]
    for chave, esp, obt in divergencias:
        print(f"DIVERGE {chave}: esperado {esp} | obtido {obt}")
    print(f"{len(esperado)} casos comparados, {len(divergencias)} divergência(s).")
    return 1 if divergencias else 0


if __name__ == "__main__":
    sys.exit(main())
