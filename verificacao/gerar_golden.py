#!/usr/bin/env python3
"""Golden master de calcular_total (somente biblioteca padrão).

Grava a saída EXATA (repr do float) do código ORIGINAL para um conjunto fixo de entradas
e depois compara outra cópia do código contra essa gravação, com igualdade exata.

  python -B verificacao/gerar_golden.py gravar   --codigo caso       # uma vez, ANTES da refatoração
  python -B verificacao/gerar_golden.py comparar --codigo trabalho   # depois de cada passo

Entradas: produto cartesiano de carrinhos x cupons x UFs x flag NATAL (ligada/desligada),
mais 3.000 carrinhos aleatórios com semente fixa. Inclui as fronteiras de R$ 200,00
(antes e depois do desconto), valores com terceira casa 5 e carrinho vazio.
"""
import argparse, itertools, json, os, random, sys
from pathlib import Path

ARQ = Path(__file__).with_name("golden_calcular_total.json")

CARRINHOS = [
    [], [(0.0, 1)], [(0.01, 1)], [(1.0, 2)], [(10.0, 0)], [(19.99, 3)], [(33.33, 1)],
    [(50.0, 2)], [(99.99, 2)], [(100.0, 2)], [(199.99, 1)], [(200.0, 1)], [(200.01, 1)],
    [(222.22, 1)], [(222.23, 1)], [(235.29, 1)], [(235.3, 1)], [(250.0, 1)],
    [(12.5, 2), (5.0, 3)], [(120.0, 1), (40.0, 2)], [(100, 1), (100, 1)], [(7, 3)],
]
CUPONS = [None, "PROMO10", "VIP15", "FRETEGRATIS", "NATAL", "", "promo10", "CUPOMFALSO"]
UFS = ["PE", "SP", "RJ", "BA", "XX", "", "pe"]


def entradas():
    for carrinho, cupom, uf, natal in itertools.product(CARRINHOS, CUPONS, UFS, ("0", "1")):
        yield carrinho, cupom, uf, natal
    rnd = random.Random(20261021)
    precos = [0.01, 0.5, 1.0, 9.9, 19.99, 25.0, 33.33, 49.9, 66.67, 99.99, 100.0, 150.0, 199.99, 200.0]
    for _ in range(3000):
        carrinho = [(rnd.choice(precos), rnd.randint(0, 5)) for _ in range(rnd.randint(0, 4))]
        yield carrinho, rnd.choice(CUPONS), rnd.choice(UFS), rnd.choice(("0", "1"))


def executar(codigo):
    sys.path.insert(0, str(Path(codigo).resolve()))
    from miniloja.calculo import calcular_total
    registros = []
    for carrinho, cupom, uf, natal in entradas():
        os.environ["MINILOJA_PROMO_NATAL"] = natal
        itens = [{"preco": p, "qtd": q} for p, q in carrinho]
        saida = calcular_total(itens, cupom, uf)
        registros.append({"itens": carrinho, "cupom": cupom, "uf": uf, "natal": natal,
                          "tipo": type(saida).__name__, "saida": repr(saida)})
    os.environ.pop("MINILOJA_PROMO_NATAL", None)
    return registros


def main():
    p = argparse.ArgumentParser()
    p.add_argument("modo", choices=["gravar", "comparar"])
    p.add_argument("--codigo", required=True)
    a = p.parse_args()
    atual = executar(a.codigo)
    if a.modo == "gravar":
        ARQ.write_text(json.dumps(atual, ensure_ascii=False, indent=0), encoding="utf-8")
        print(f"Gravados {len(atual)} casos em {ARQ.name} a partir de {a.codigo}")
        return 0
    gravado = json.loads(ARQ.read_text(encoding="utf-8"))
    for r in gravado:  # JSON devolve listas; normaliza para comparar com tuplas
        r["itens"] = [tuple(x) for x in r["itens"]]
    difs = [(g, n) for g, n in zip(gravado, atual) if g != n]
    if len(gravado) != len(atual):
        print(f"FALHA: quantidade de casos difere ({len(gravado)} x {len(atual)})")
        return 1
    if difs:
        print(f"FALHA: {len(difs)} de {len(gravado)} casos divergem. Primeiros:")
        for g, n in difs[:5]:
            print(f"  {g['itens']} {g['cupom']!r} {g['uf']!r} natal={g['natal']}: "
                  f"gravado {g['saida']} ({g['tipo']}) | atual {n['saida']} ({n['tipo']})")
        return 1
    print(f"OK: {len(gravado)} de {len(gravado)} casos idênticos (repr e tipo) em {a.codigo}")
    return 0


if __name__ == "__main__":
    sys.exit(main())