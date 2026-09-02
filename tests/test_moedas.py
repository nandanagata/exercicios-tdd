from decimal import Decimal
from unittest.mock import Mock

import pytest

from src.moedas import (
    ConversorMoedas,
    ServicoCotacaoIndisponivelError,
)


def test_conversao_com_taxa_de_cambio():
    api = Mock()

    api.obter_taxa.return_value = Decimal("5.00")

    conversor = ConversorMoedas(api)

    resultado = conversor.converter(
        "USD",
        "BRL",
        100
    )

    # 100 * 5 = 500
    # 500 + 1.5% = 507.50
    assert resultado == Decimal("507.50")


def test_api_e_chamada_com_as_moedas_corretas():
    api = Mock()

    api.obter_taxa.return_value = Decimal("5.00")

    conversor = ConversorMoedas(api)

    conversor.converter(
        "USD",
        "BRL",
        100
    )

    api.obter_taxa.assert_called_once_with(
        "USD",
        "BRL"
    )


def test_spread_de_1_5_porcento():
    api = Mock()

    api.obter_taxa.return_value = Decimal("5.00")

    conversor = ConversorMoedas(api)

    resultado = conversor.converter(
        "USD",
        "BRL",
        100
    )

    valor_sem_spread = Decimal("500.00")

    valor_esperado = (
        valor_sem_spread
        * Decimal("1.015")
    )

    assert resultado == valor_esperado.quantize(
        Decimal("0.01")
    )


def test_api_indisponivel_lanca_excecao():
    api = Mock()

    api.obter_taxa.side_effect = Exception(
        "API fora do ar"
    )

    conversor = ConversorMoedas(api)

    with pytest.raises(
        ServicoCotacaoIndisponivelError
    ):
        conversor.converter(
            "USD",
            "BRL",
            100
        )


def test_api_nao_e_acessada_de_verdade():
    api = Mock()

    api.obter_taxa.return_value = Decimal("5.50")

    conversor = ConversorMoedas(api)

    resultado = conversor.converter(
        "EUR",
        "BRL",
        200
    )

    assert resultado == Decimal("1116.50")

    api.obter_taxa.assert_called_once()


def test_valor_zero_e_invalido():
    api = Mock()

    conversor = ConversorMoedas(api)

    with pytest.raises(ValueError):
        conversor.converter(
            "USD",
            "BRL",
            0
        )


def test_valor_negativo_e_invalido():
    api = Mock()

    conversor = ConversorMoedas(api)

    with pytest.raises(ValueError):
        conversor.converter(
            "USD",
            "BRL",
            -100
        )