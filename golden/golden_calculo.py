"""Golden master de calcular_total (AV1.2). Grava o comportamento ATUAL e compara com igualdade exata.

Uso, na raiz do repositório:
  python -B golden/golden_calculo.py --gravar     # uma vez, ANTES de refatorar
  python -B golden/golden_calculo.py              # compara (saída 0 = idêntico, 1 = divergiu)
"""
import json, os, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "caso"))
from miniloja.calculo import calcular_total  # noqa: E402

ARQ = Path(__file__).with_name("golden_calculo.json")
CARRINHOS = {
    "C1_camisa_e_bola": [{"preco": 80.0, "qtd": 1}, {"preco": 50.0, "qtd": 1}],
    "C2_chuteira_250": [{"preco": 250.0, "qtd": 1}],
    "C3_bolas_19_99x3": [{"preco": 19.99, "qtd": 3}],
    "vazio": [],
    "exato_200": [{"preco": 100.0, "qtd": 2}],
    "quase_200": [{"preco": 199.99, "qtd": 1}],
    "arredonda_2x1": [{"preco": 1.0, "qtd": 2}],
    "promo_cruza_200": [{"preco": 222.23, "qtd": 1}],
}
CUPONS = [None, "PROMO10", "VIP15", "FRETEGRATIS", "NATAL", "INVALIDO"]
UFS = ["PE", "SP", "RJ", "XX"]


def casos():
    for nome, itens in CARRINHOS.items():
        for cupom in CUPONS:
            for uf in UFS:
                for natal in (["0", "1"] if cupom == "NATAL" else ["0"]):
                    yield f"{nome}|{cupom}|{uf}|natal={natal}", itens, cupom, uf, natal


def executar():
    saidas = {}
    for chave, itens, cupom, uf, natal in casos():
        os.environ["MINILOJA_PROMO_NATAL"] = natal
        try:
            r = calcular_total([dict(i) for i in itens], cupom, uf)
            saidas[chave] = [type(r).__name__, repr(r)]
        except Exception as e:  # erro também é comportamento
            saidas[chave] = ["erro", type(e).__name__]
    os.environ.pop("MINILOJA_PROMO_NATAL", None)
    return saidas


if __name__ == "__main__":
    atual = executar()
    if "--gravar" in sys.argv:
        ARQ.write_text(json.dumps(atual, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"gravado: {len(atual)} entradas em {ARQ.name}")
        sys.exit(0)
    esperado = json.loads(ARQ.read_text(encoding="utf-8"))
    difs = [k for k in esperado if atual.get(k) != esperado[k]]
    for k in difs[:10]:
        print(f"DIVERGE {k}: esperado {esperado[k][1]} obtido {atual.get(k, ['', 'ausente'])[1]}")
    print(f"golden master: {len(esperado) - len(difs)}/{len(esperado)} idênticas, {len(difs)} divergências")
    sys.exit(1 if difs else 0)
