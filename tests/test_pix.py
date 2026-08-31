import pytest

from src.pix import ChavePixInvalidaError, validar_chave_pix


@pytest.mark.parametrize(
    ("chave", "tipo_esperado"),
    [
        ("52998224725", "CPF"),
        ("fernanda@exemplo.com", "EMAIL"),
        ("+5511999999999", "TELEFONE"),
        ("123e4567-e89b-42d3-a456-426614174000", "EVP"),
    ],
)
def test_deve_identificar_chaves_pix_validas(chave, tipo_esperado):
    assert validar_chave_pix(chave) == tipo_esperado


@pytest.mark.parametrize(
    "chave",
    [
        "52998224724",  # CPF com dígito verificador incorreto
        "11111111111",  # CPF com todos os dígitos iguais
        "fernanda.com",  # e-mail sem @
        "fernanda@exemplo",  # e-mail sem extensão
        "5511999999999",  # telefone sem +
        "+551199999",  # telefone incompleto
        "não-é-um-uuid",
        "123e4567-e89b-12d3-a456-426614174000",  # UUID, mas não v4
    ],
)
def test_deve_lancar_excecao_para_chave_pix_invalida(chave):
    with pytest.raises(ChavePixInvalidaError):
        validar_chave_pix(chave)