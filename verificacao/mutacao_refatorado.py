#!/usr/bin/env python3
"""Mutação manual do calculo.py REFATORADO (mesma ideia de testes/mutacao_manual.py,
que não serve aqui porque procura os trechos do código original).

Para cada mutante: aplica, roda (a) a suíte do contrato e (b) o golden master, desfaz.
  python -B verificacao/mutacao_refatorado.py [--codigo trabalho]
"""
import argparse, subprocess, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

MUTACOES = [
    ("subtotal: * vira +", 'item["preco"] * item["qtd"]', 'item["preco"] + item["qtd"]'),
    ("subtotal ignora itens após o primeiro", "total = total + item", "total = item"),
    ("PROMO10 10% -> 9%", "subtotal * 0.9\n", "subtotal * 0.91\n"),
    ("VIP15 15% -> 14%", "subtotal * 0.85", "subtotal * 0.86"),
    ("NATAL 20% -> 21%", "subtotal * 0.8\n", "subtotal * 0.79\n"),
    ("NATAL ignora a flag", 'cupom == "NATAL" and flags.promo_natal_ativa()', 'cupom == "NATAL"'),
    ("NATAL nunca aplica", 'cupom == "NATAL" and flags.promo_natal_ativa()', "False"),
    ("VIP15 deixa de existir", 'cupom == "VIP15"', 'cupom == "VIP16"'),
    ("FRETEGRATIS não zera frete", 'CUPOM_FRETE_GRATIS = "FRETEGRATIS"', 'CUPOM_FRETE_GRATIS = "XFRETEGRATIS"'),
    ("frete grátis: or vira and", "CUPOM_FRETE_GRATIS or com_desconto", "CUPOM_FRETE_GRATIS and com_desconto"),
    ("limite: > vira >= (corrige D1)", "com_desconto > LIMITE", "com_desconto >= LIMITE"),
    ("limite 200 -> 300", "LIMITE_FRETE_GRATIS = 200", "LIMITE_FRETE_GRATIS = 300"),
    ("frete olha subtotal sem desconto", "+ _frete(com_desconto, cupom, uf)", "+ _frete(_subtotal(itens), cupom, uf)"),
    ("frete PE", '"PE": 12.9', '"PE": 13.9'),
    ("frete SP", '"SP": 19.9', '"SP": 20.9'),
    ("frete RJ", '"RJ": 21.5', '"RJ": 22.5'),
    ("frete demais UFs", "FRETE_DEMAIS_UFS = 29.9", "FRETE_DEMAIS_UFS = 30.9"),
    ("taxa PE", '"PE": 0.05', '"PE": 0.06'),
    ("taxa SP", '"SP": 0.07', '"SP": 0.08'),
    ("taxa RJ", '"RJ": 0.06', '"RJ": 0.07'),
    ("taxa demais UFs", "TAXA_DEMAIS_UFS = 0.08", "TAXA_DEMAIS_UFS = 0.09"),
    ("taxa ignora o frete", "base_taxa + base_taxa * TAXA", "base_taxa + com_desconto * TAXA"),
    ("arredonda em 3 casas", "round(total, 2)", "round(total, 3)"),
    ("taxa como x*(1+t)", "base_taxa + base_taxa * TAXA_POR_UF.get(uf, TAXA_DEMAIS_UFS)",
     "base_taxa * (1 + TAXA_POR_UF.get(uf, TAXA_DEMAIS_UFS))"),
    ("subtotal começa em 0.0", "    total = 0\n", "    total = 0.0\n"),
]


def roda(cmd):
    return subprocess.run(cmd, cwd=RAIZ, capture_output=True, text=True, timeout=120).returncode == 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--codigo", default="trabalho")
    a = p.parse_args()
    alvo = RAIZ / a.codigo / "miniloja" / "calculo.py"
    py = [sys.executable, "-B"]
    contrato = py + ["verificacao/test_contrato_calculo.py", "--codigo", a.codigo, "-x"]
    golden = py + ["verificacao/gerar_golden.py", "comparar", "--codigo", a.codigo]
    if not (roda(contrato) and roda(golden)):
        sys.exit("Linha de base vermelha: corrija antes de mutar.")
    original = alvo.read_text(encoding="utf-8")
    print(f"{'mutante':38} | contrato | golden")
    vivos = []
    try:
        for desc, velho, novo in MUTACOES:
            assert original.count(velho) == 1, f"trecho ausente ou repetido: {velho!r}"
            alvo.write_text(original.replace(velho, novo), encoding="utf-8")
            c, g = not roda(contrato), not roda(golden)
            alvo.write_text(original, encoding="utf-8")
            print(f"{desc:38} | {'MORTO' if c else 'vivo':8} | {'MORTO' if g else 'vivo'}")
            if not c:
                vivos.append(desc)
    finally:
        alvo.write_text(original, encoding="utf-8")
    n = len(MUTACOES)
    print(f"\nSuíte do contrato: {n - len(vivos)}/{n} mortos. Sobreviventes: {vivos or 'nenhum'}")


if __name__ == "__main__":
    main()
