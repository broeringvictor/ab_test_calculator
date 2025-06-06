import pytest

from domain.entities.variation import Variation
# (Cole a classe Variation corrigida acima neste arquivo ou importe-a)


@pytest.fixture
def variation_instance() -> Variation:
    """
    Cria uma instância da entidade Variation com os dados exatos da sua imagem.
    """
    return Variation(
        variation_a_visitors=80000,
        conversions_a=1600,
        variation_b_visitors=80000,
        conversions_b=1696,
        tail_numbers=1,      # Este valor não é testado aqui, mas é necessário
        confidence_level=95.0, # Este valor não é testado aqui, mas é necessário
        estimated_uplift=10.0  # Este valor não é testado aqui, mas é necessário
    )

# --- Testes para cada atributo calculado ---

def test_conversion_rate_a(variation_instance: Variation):
    """Verifica a Taxa de Conversão do Controle (Grupo A)."""
    # Na imagem: 2.00%
    expected_rate = 0.02
    assert variation_instance.conversion_rate_a == pytest.approx(expected_rate)

def test_conversion_rate_b(variation_instance: Variation):
    """Verifica a Taxa de Conversão da Variação (Grupo B)."""
    # Na imagem: 2.12%
    expected_rate = 0.0212
    assert variation_instance.conversion_rate_b == pytest.approx(expected_rate)

def test_default_error_a(variation_instance: Variation):
    """Verifica o Erro Padrão do Controle (Grupo A)."""
    # Na imagem: 0.0495%
    expected_error = 0.000495 
    assert variation_instance.default_error_a == pytest.approx(expected_error, abs=1e-5)

def test_default_error_b(variation_instance: Variation):
    """Verifica o Erro Padrão da Variação (Grupo B)."""
    # Na imagem: 0.0509%
    expected_error = 0.000509
    assert variation_instance.default_error_b == pytest.approx(expected_error, abs=1e-5)