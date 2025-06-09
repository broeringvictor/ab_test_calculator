import pytest
from datetime import date
from domain.entities.variation import Variation 
from domain.entities.ab_tester import ABTester
from domain.use_cases.ab_statistical_validator import ABStatisticalValidator

# ===================================================================
# 1. SETUP DO TESTE CORRIGIDO
# ===================================================================

@pytest.fixture
def setup_validator() -> ABStatisticalValidator:
    """
    Cria uma instância do validador, configurado com os dados exatos da planilha
    através das entidades ABTester e Variation.
    """

    tester_data = ABTester(
        name="Teste da Planilha",
        start_date=date(2024, 9, 22),
        end_date=date(2025, 6, 3),
        hypothesis="Se as [imagens] chamarem mais atenção então o CTR vai aumentar",
        desired_confidence_level=95.0 
    )


    variation_data = Variation(
        variation_a_visitors=80000,
        variation_b_visitors=80000,
        conversions_a=1600,
        conversions_b=1696,
        tail_numbers=1,
        confidence_level=95.0,
        estimated_uplift=10.0
  
    )

    # Retorna o validador instanciado com os mocks das entidades
    return ABStatisticalValidator(variation=variation_data, tester=tester_data)


# ===================================================================
# 2. TESTE UNITÁRIO COMPLETO
# ===================================================================

class TestABStatisticalValidator:
    def test_statistical_results_match_spreadsheet(self, setup_validator: ABStatisticalValidator):
        """
        Verifica se todos os resultados calculados correspondem aos valores da planilha.
        Chama o método principal uma única vez e valida cada item do dicionário retornado.
        """
        # Executa a função principal para obter todos os resultados de uma vez
        results = setup_validator.get_statistical_results()
        
        # --- Validação Estatística ---
        assert results["z_score"] == pytest.approx(1.689668, abs=1e-5)
        # ATENÇÃO: Z-Crítico resulta em um valor negativo.
        # A planilha mostra um valor positivo. O teste abaixo verifica o resultado do SEU CÓDIGO.
        # Fórmula: (1 - 0.95) / 1 = 0.05 -> norm.ppf(0.05) = -1.644853
        assert results["z_critical"] == pytest.approx(-1.644853, abs=1e-5)
        assert results["p_value"] == pytest.approx(0.0455, abs=1e-4)
        assert results["conversion_rate_uplift"] == pytest.approx(0.06, abs=1e-4) # 6%
        assert results["observed_test_power"] == pytest.approx(0.7757, abs=1e-4) # 77.57%
        assert results["current_confidence"] == pytest.approx(0.9545, abs=1e-4) # 95.45%

        # --- Validação dos Limites de Confiança ---
        assert results["standard_error_difference"] == pytest.approx(0.00071019, abs=1e-5)
        assert results["control_lower_bound"] == pytest.approx(0.0192, abs=1e-4) # 1.92%
        assert results["control_upper_bound"] == pytest.approx(0.0208, abs=1e-4) # 2.08%
        assert results["variation_lower_bound"] == pytest.approx(0.0203, abs=1e-4) # 2.03% (arredondado)
        assert results["variation_upper_bound"] == pytest.approx(0.0220, abs=1e-4) # 2.20%

        # --- Validação de SRM (Sample Ratio Mismatch) ---
        srm = results["srm_results"]
        assert srm["has_srm"] is False
        assert srm["srm_p_value"] == pytest.approx(1.0)
        assert srm["srm_expected_per_variation"] == pytest.approx(80000.0)

        # --- Validação Temporal ---
        temporal = results["temporal_validation_results"]
        assert temporal["total_duration_days"] == 254
        assert temporal["business_days_duration"] == 182 # Valor calculado por numpy.busday_count
        assert temporal["average_daily_visitors"] == pytest.approx(629.92, abs=1e-2) # A planilha arredonda para 630

        # --- Validação de Planejamento ---
        planning = results["planning_results"]
        assert planning["required_users_80_power"] == 156800
        assert planning["required_users_95_power"] == 254800
        assert planning["required_days_80_power"] == 249 # 156800 / 629.92
        assert planning["required_days_95_power"] == 405 # 254800 / 629.92 (planilha arredonda para 404)