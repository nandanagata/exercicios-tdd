import pytest

from src.credito import AnaliseCredito


@pytest.fixture
def analise_credito():
    return AnaliseCredito()


@pytest.mark.parametrize(
    "renda, restricao, score, limite_esperado",
    [
        # Renda abaixo do mínimo
        (1000.00, False, 700, 0.00),
        (1499.99, False, 900, 0.00),

        # Restrição no CPF
        (3000.00, True, 900, 0.00),
        (10000.00, True, 1000, 0.00),

        # Renda mínima sem bônus
        (1500.00, False, 800, 450.00),
        (2000.00, False, 700, 600.00),

        # Score acima de 800
        (1500.00, False, 801, 675.00),
        (2000.00, False, 900, 900.00),
        (5000.00, False, 850, 2250.00),
    ]
)
def test_calculo_limite(
    analise_credito,
    renda,
    restricao,
    score,
    limite_esperado
):
    limite = analise_credito.calcular_limite(
        renda,
        restricao,
        score
    )

    assert limite == limite_esperado


@pytest.mark.parametrize(
    "renda",
    [
        0,
        500,
        1000,
        1499.99
    ]
)
def test_renda_abaixo_do_minimo(
    analise_credito,
    renda
):
    assert (
        analise_credito.calcular_limite(
            renda,
            False,
            900
        )
        == 0.0
    )


def test_restricao_tem_prioridade_sobre_a_renda(
    analise_credito
):
    limite = analise_credito.calcular_limite(
        10000,
        True,
        950
    )

    assert limite == 0.0


def test_score_800_nao_recebe_bonus(
    analise_credito
):
    limite = analise_credito.calcular_limite(
        2000,
        False,
        800
    )

    assert limite == 600.0


def test_score_801_recebe_bonus(
    analise_credito
):
    limite = analise_credito.calcular_limite(
        2000,
        False,
        801
    )

    assert limite == 900.0