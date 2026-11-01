"""Confere o escopo local e exporta o patch AV3, sem alterar o índice Git."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
TRACKED = {
    "caso/miniloja/estoque.py",
    "caso/miniloja/pedidos.py",
    "caso/testes_existentes/test_pedidos.py",
}
NEW = {
    "avaliacoes/av3/registro-av3-lucasmacena.md",
    "avaliacoes/av3/ESCOPO_PREVIO.md",
    "avaliacoes/av3/EVIDENCIAS.md",
    "avaliacoes/av3/DESCRICAO_PR.md",
    "avaliacoes/av3/test_reserva_estoque.py",
    "avaliacoes/av3/gerar_diff.py",
}
INPUTS = {f"avaliacoes/av2/{name}" for name in (
    "ADR-001-calcular-total.md", "ANEXO_TECNICO.md", "ESCOPO_PREVIO.md",
    "REGISTRO_AV2.md", "calculo_inicial.py", "golden.py", "mutacao.py",
    "referencia.jsonl", "test_calculo_contrato.py",
)}
OUTPUT = "avaliacoes/av3/AV3-B3.patch"
BASE = "1a12ad2"


def git(*args, accepted=(0,)):
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True)
    if result.returncode not in accepted:
        raise SystemExit(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


if __name__ == "__main__":
    changed = set(git("diff", BASE, "--name-only").decode().splitlines())
    untracked = set(git("ls-files", "--others", "--exclude-standard").decode().splitlines())
    outside = (changed - TRACKED - NEW - {OUTPUT}) | (untracked - NEW - INPUTS - {OUTPUT})
    if outside:
        raise SystemExit(f"FORA DO ESCOPO: {sorted(outside)}")
    git("diff", "--check", BASE, "--", *sorted(TRACKED | NEW))
    patch = git("diff", "--binary", BASE, "--", *sorted(TRACKED | NEW))
    for path in sorted(NEW & untracked):
        patch += git("diff", "--no-index", "--binary", "--", "/dev/null", path, accepted=(1,))
    (ROOT / OUTPUT).write_bytes(patch)
    print(f"ESCOPO OK: {len(changed)} rastreados alterados; {len(NEW & untracked)} novos AV3")
    print(f"PATCH: {OUTPUT} ({len(patch)} bytes); AV2 preservada e excluida")
