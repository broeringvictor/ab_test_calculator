import pytest

from domain.entities.variation import Variation
from domain.use_cases.ab_statistical_validator import ABStatisticalValidator


@pytest.fixture
def validator() -> ABStatisticalValidator:
    """
    Cria uma instância do validador, já configurado com os dados de teste
    através da entidade Variation.
    """
    # 1. Cria a instância da sua entidade
    dados_do_teste = Variation(
        variation_a_visitors=80000,
        variation_b_visitors=80000,
        conversions_a=1600,
        conversions_b=1696,
        tail_numbers=1,
        confidence_level=95.0,
        estimated_uplift=10.0
    )
    # 2. Passa a entidade para o validador e o retorna
    return ABStatisticalValidator(dados_do_teste)


# ===================================================================
# 3. TESTES UNITÁRIOS
# ===================================================================

def test_z_score_calculation(validator: ABStatisticalValidator):
    """Verifica se o Z-Score foi calculado corretamente."""
    expected_z_score = 1.689668
    results = validator.get_statistical_results()
    assert results["z_score"] == pytest.approx(expected_z_score, abs=1e-5)

def test_standard_error_difference_calculation(validator: ABStatisticalValidator):
    """Verifica se o Erro Padrão da Diferença foi calculado corretamente."""
    expected_std_err_diff = 0.00071019
    results = validator.get_statistical_results()
    assert results["standard_error_difference"] == pytest.approx(expected_std_err_diff, abs=1e-5)

def test_z_critical_calculation_with_user_formula(validator: ABStatisticalValidator):
    """Verifica se o Z-Crítico foi calculado usando a fórmula do usuário."""
    expected_z_critical = -1.644853
    results = validator.get_statistical_results() # <-- Use 'validator' aqui também
    assert results["z_critical"] == pytest.approx(expected_z_critical, abs=1e-5)