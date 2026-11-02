"""Testes de revisão do PR do bloco 5 (exportação de vendas em CSV).

Não altera o repositório: copia `caso/` para uma pasta temporária, aplica o
patch do PR nessa cópia e testa a cópia. Cada teste corresponde a um achado
bloqueante do registro e deve FALHAR no código do PR; depois da correção
proposta, deve passar.

Na raiz do repositório:  python -B exercicios/aula-5/test_revisao_pr.py
Requer `git` no PATH (usado só para `git apply`).
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PATCH = os.path.join(RAIZ, "apoio", "pr-bloco5", "0001-Adiciona-exporta-o-de-vendas-em-CSV.patch")

_TMP = tempfile.mkdtemp(prefix="revisao_pr_")
shutil.copytree(os.path.join(RAIZ, "caso"), os.path.join(_TMP, "caso"),
                ignore=shutil.ignore_patterns("__pycache__"))
subprocess.run(["git", "apply", "--whitespace=nowarn", PATCH], cwd=_TMP, check=True)
sys.path.insert(0, os.path.join(_TMP, "caso"))

from miniloja import exportacao, handlers  # noqa: E402
from miniloja.repositorio import RepositorioPedidos  # noqa: E402


def tearDownModule():
    shutil.rmtree(_TMP, ignore_errors=True)


class TestRevisaoPR(unittest.TestCase):
    def setUp(self):
        self.saida = tempfile.mkdtemp(prefix="exports_")
        self.addCleanup(shutil.rmtree, self.saida, True)
        exportacao.EXPORT_DIR = os.path.join(self.saida, "exports")
        handlers._repo = RepositorioPedidos()
        handlers._repo.salvar({"usuario_id": 1, "total": 10.0})
        handlers._repo.salvar({"usuario_id": 2, "total": 20.0})

    def test_1_r4_so_pedidos_do_proprio_usuario(self):
        _, corpo = handlers.get_exportacao(1, "a.csv")
        self.assertEqual(corpo["linhas"], 1)

    def test_2_nome_com_path_traversal_e_recusado(self):
        status, _ = handlers.get_exportacao(1, "../fora.csv")
        self.assertEqual(status, 400)
        self.assertFalse(os.path.exists(os.path.join(self.saida, "fora.csv")))

    def test_3_sem_dependencia_externa(self):
        with open(os.path.join(_TMP, "caso", "requirements.txt"), encoding="utf-8") as f:
            deps = [l.strip() for l in f if l.strip() and not l.startswith("#")]
        self.assertEqual(deps, [])

    def test_4_falha_de_gravacao_nao_retorna_200(self):
        os.makedirs(os.path.join(exportacao.EXPORT_DIR, "x.csv"))  # diretório no lugar do arquivo
        status, _ = handlers.get_exportacao(1, "x.csv")
        self.assertGreaterEqual(status, 500)


if __name__ == "__main__":
    unittest.main(verbosity=2)
