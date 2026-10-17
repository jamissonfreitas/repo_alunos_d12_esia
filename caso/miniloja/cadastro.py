"""Cadastro de clientes."""

_CLIENTES = []


def _cpf_valido(cpf):
    """Valida dígitos verificadores; aceita com ou sem pontuação (R3.2)."""
    digitos = [int(c) for c in str(cpf) if c.isdigit()]
    if len(digitos) != 11 or len(set(digitos)) == 1:
        return False
    for n in (9, 10):
        soma = sum(d * p for d, p in zip(digitos[:n], range(n + 1, 1, -1)))
        if digitos[n] != (soma * 10 % 11) % 10:
            return False
    return True


def _email_valido(email):
    """Formato `texto@texto.texto` (R3.3)."""
    local, arroba, dominio = str(email).partition("@")
    partes = dominio.split(".")
    return bool(local and arroba and len(partes) >= 2 and all(partes))


def cadastrar_cliente(payload):
    """Cadastra um cliente; cadastro inválido responde 422 com todos os erros (R3.4)."""
    erros = []
    if not payload.get("nome"):
        erros.append({"campo": "nome", "erro": "obrigatório"})
    if not payload.get("email"):
        erros.append({"campo": "email", "erro": "obrigatório"})
    elif not _email_valido(payload["email"]):
        erros.append({"campo": "email", "erro": "formato inválido"})
    if not payload.get("cpf"):
        erros.append({"campo": "cpf", "erro": "obrigatório"})
    elif not _cpf_valido(payload["cpf"]):
        erros.append({"campo": "cpf", "erro": "CPF inválido"})
    if erros:
        return 422, {"erros": erros}
    cliente = dict(payload, id=len(_CLIENTES) + 1)
    _CLIENTES.append(cliente)
    return 201, cliente


def limpar():
    _CLIENTES.clear()
