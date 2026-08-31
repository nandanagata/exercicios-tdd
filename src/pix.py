import re
import uuid


class ChavePixInvalidaError(ValueError):
    """Exceção lançada quando uma chave Pix possui formato inválido."""


def validar_chave_pix(chave: str) -> str:
    """Valida a chave Pix e retorna seu tipo."""

    if not isinstance(chave, str) or not chave:
        raise ChavePixInvalidaError("A chave Pix deve ser uma string não vazia.")

    if _cpf_valido(chave):
        return "CPF"

    if _email_valido(chave):
        return "EMAIL"

    if _telefone_valido(chave):
        return "TELEFONE"

    if _evp_valida(chave):
        return "EVP"

    raise ChavePixInvalidaError(f"Chave Pix inválida: {chave}")


def _cpf_valido(cpf: str) -> bool:
    if len(cpf) != 11 or not cpf.isdigit():
        return False

    if cpf == cpf[0] * 11:
        return False

    primeiro_digito = _calcular_digito_cpf(cpf[:9])
    segundo_digito = _calcular_digito_cpf(cpf[:9] + primeiro_digito)

    return cpf[-2:] == primeiro_digito + segundo_digito


def _calcular_digito_cpf(parte: str) -> str:
    pesos = range(len(parte) + 1, 1, -1)
    soma = sum(int(numero) * peso for numero, peso in zip(parte, pesos))

    resultado = 11 - (soma % 11)

    if resultado >= 10:
        return "0"

    return str(resultado)


def _email_valido(email: str) -> bool:
    padrao = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.fullmatch(padrao, email) is not None


def _telefone_valido(telefone: str) -> bool:
    # +55 seguido de DDD e número: 11 dígitos depois do código do país.
    padrao = r"^\+55\d{11}$"
    return re.fullmatch(padrao, telefone) is not None


def _evp_valida(chave: str) -> bool:
    if len(chave) != 36:
        return False

    try:
        valor = uuid.UUID(chave)

        return (
            valor.version == 4
            and str(valor) == chave.lower()
        )
    except (ValueError, AttributeError, TypeError):
        return False