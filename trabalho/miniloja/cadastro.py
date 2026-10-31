"""Cadastro de clientes."""
import re

_CLIENTES = []
_EMAIL = re.compile(r"[^@\s]+@[^@\s.]+(\.[^@\s.]+)+")


def _cpf_valido(cpf):
    """R3.2: dígitos verificadores válidos, nem todos iguais; aceita com ou sem pontuação."""
    if not isinstance(cpf, str):
        return False
    digitos = cpf.replace(".", "").replace("-", "")
    if len(digitos) != 11 or not digitos.isdigit():
        return False
    if len(set(digitos)) == 1:
        return False
    for tamanho in (9, 10):
        soma = sum(int(d) * (tamanho + 1 - i) for i, d in enumerate(digitos[:tamanho]))
        dv = soma * 10 % 11 % 10
        if dv != int(digitos[tamanho]):
            return False
    return True


def _email_valido(email):
    """R3.3: formato texto@texto.texto."""
    return isinstance(email, str) and _EMAIL.fullmatch(email) is not None


def cadastrar_cliente(payload):
    """Cadastra um cliente; R3.4: se inválido, devolve 422 com todos os erros."""
    erros = []
    for campo in ("nome", "email", "cpf"):
        if not payload.get(campo):
            erros.append({"campo": campo, "erro": "obrigatório"})
    if payload.get("email") and not _email_valido(payload["email"]):
        erros.append({"campo": "email", "erro": "formato inválido"})
    if payload.get("cpf") and not _cpf_valido(payload["cpf"]):
        erros.append({"campo": "cpf", "erro": "cpf inválido"})
    if erros:
        return 422, {"erros": erros}
    cliente = dict(payload, id=len(_CLIENTES) + 1)
    _CLIENTES.append(cliente)
    return 201, cliente


def limpar():
    _CLIENTES.clear()
