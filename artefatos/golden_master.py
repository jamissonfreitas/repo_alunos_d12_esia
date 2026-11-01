"""Capture or compare the original miniloja.calculo.calcular_total outputs.

Run from the repository root with Python 3.11+ and MINILOJA_PROMO_NATAL
unset in the parent environment. Per-case flag values are set explicitly.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "caso"))

from miniloja.calculo import calcular_total  # noqa: E402


CASES = [
    {"id": 1, "descricao": "C1 camisa e bola, sem cupom, PE", "carrinho": "C1_camisa_e_bola", "itens": [{"preco": 80.0, "qtd": 1}, {"preco": 50.0, "qtd": 1}], "cupom": None, "uf": "PE", "flag_natal": "0"},
    {"id": 2, "descricao": "C1 camisa e bola, PROMO10, SP", "carrinho": "C1_camisa_e_bola", "itens": [{"preco": 80.0, "qtd": 1}, {"preco": 50.0, "qtd": 1}], "cupom": "PROMO10", "uf": "SP", "flag_natal": "0"},
    {"id": 3, "descricao": "C1 camisa e bola, VIP15, RJ", "carrinho": "C1_camisa_e_bola", "itens": [{"preco": 80.0, "qtd": 1}, {"preco": 50.0, "qtd": 1}], "cupom": "VIP15", "uf": "RJ", "flag_natal": "0"},
    {"id": 4, "descricao": "C2 chuteira acima de R$ 200, sem cupom, PE", "carrinho": "C2_chuteira", "itens": [{"preco": 250.0, "qtd": 1}], "cupom": None, "uf": "PE", "flag_natal": "0"},
    {"id": 5, "descricao": "C2 chuteira, FRETEGRATIS, SP", "carrinho": "C2_chuteira", "itens": [{"preco": 250.0, "qtd": 1}], "cupom": "FRETEGRATIS", "uf": "SP", "flag_natal": "0"},
    {"id": 6, "descricao": "C3 três bolas, cupom inválido, RJ", "carrinho": "C3_varias_bolas", "itens": [{"preco": 19.99, "qtd": 3}], "cupom": "INVALIDO", "uf": "RJ", "flag_natal": "0"},
    {"id": 7, "descricao": "Carrinho de R$ 200,00 exatos, sem cupom, PE", "carrinho": "fronteira_200", "itens": [{"preco": 200.0, "qtd": 1}], "cupom": None, "uf": "PE", "flag_natal": "0"},
    {"id": 8, "descricao": "Carrinho de R$ 200,00 exatos, cupom PROMO10, UF MG (outra)", "carrinho": "fronteira_200", "itens": [{"preco": 200.0, "qtd": 1}], "cupom": "PROMO10", "uf": "MG", "flag_natal": "0"},
    {"id": 9, "descricao": "C1 camisa e bola, NATAL desligado, PE", "carrinho": "C1_camisa_e_bola", "itens": [{"preco": 80.0, "qtd": 1}, {"preco": 50.0, "qtd": 1}], "cupom": "NATAL", "uf": "PE", "flag_natal": "0"},
    {"id": 10, "descricao": "C1 camisa e bola, NATAL ligado, PE", "carrinho": "C1_camisa_e_bola", "itens": [{"preco": 80.0, "qtd": 1}, {"preco": 50.0, "qtd": 1}], "cupom": "NATAL", "uf": "PE", "flag_natal": "1"},
    {"id": 11, "descricao": "C3 três bolas, sem cupom, UF MG (outra)", "carrinho": "C3_varias_bolas", "itens": [{"preco": 19.99, "qtd": 3}], "cupom": None, "uf": "MG", "flag_natal": "0"},
    {"id": 12, "descricao": "Carrinho vazio, sem cupom, SP", "carrinho": "vazio", "itens": [], "cupom": None, "uf": "SP", "flag_natal": "0"},
]

DEFAULT_OUTPUT = ROOT / "artefatos" / "golden_master_original.json"
SOURCE = ROOT / "caso" / "miniloja" / "calculo.py"


def capture() -> dict:
    results = []
    for case in CASES:
        os.environ["MINILOJA_PROMO_NATAL"] = case["flag_natal"]
        result = calcular_total(case["itens"], case["cupom"], case["uf"])
        results.append({**case, "saida": result})
    return {
        "titulo": "Golden master original de calcular_total",
        "commit": "2c2fc89c8c1d2f03423ed30d31f790b8601e6c2d",
        "python": sys.version,
        "plataforma": sys.platform,
        "MINILOJA_PROMO_NATAL_ambiente_pai": "não definido; cada caso configura explicitamente 0 ou 1",
        "sha256_calculo_py": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "casos": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--capture", action="store_true", help="captura e grava saídas atuais")
    group.add_argument("--compare", action="store_true", help="compara saídas atuais exatamente com a captura")
    parser.add_argument("--arquivo", type=Path, default=DEFAULT_OUTPUT, help=f"arquivo JSON (padrão: {DEFAULT_OUTPUT})")
    args = parser.parse_args()

    if args.capture:
        data = capture()
        args.arquivo.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Capturados {len(data['casos'])} casos em {args.arquivo}")
        for case in data["casos"]:
            print(f"{case['id']:02d} {case['descricao']}: {case['saida']!r}")
        return 0

    expected = json.loads(args.arquivo.read_text(encoding="utf-8"))
    actual = capture()
    mismatches = []
    for before, now in zip(expected["casos"], actual["casos"]):
        if before["id"] != now["id"] or before["saida"] != now["saida"]:
            mismatches.append((now["id"], before["saida"], now["saida"]))
    if len(expected["casos"]) != len(actual["casos"]) or mismatches:
        print("DIVERGÊNCIA (igualdade exata):")
        for case_id, before, now in mismatches:
            print(f"{case_id:02d}: original={before!r}, atual={now!r}")
        return 1
    print(f"OK: {len(actual['casos'])} saídas iguais exatamente às capturadas em {args.arquivo}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
