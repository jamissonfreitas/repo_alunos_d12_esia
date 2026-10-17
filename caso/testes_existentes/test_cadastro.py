import unittest

from miniloja import cadastro


class TestCadastro(unittest.TestCase):
    def test_cadastro_sem_nome_e_rejeitado(self):
        cadastro.limpar()
        status, _ = cadastro.cadastrar_cliente({"email": "a@b.com", "cpf": "529.982.247-25"})
        self.assertEqual(status, 422)  # R3.4: contrato mudou de 400 para 422

    def test_cadastro_valido(self):
        cadastro.limpar()
        status, corpo = cadastro.cadastrar_cliente({"nome": "Ana", "email": "ana@exemplo.com", "cpf": "529.982.247-25"})
        self.assertEqual(status, 201)
        self.assertEqual(corpo["id"], 1)
