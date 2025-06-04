
import pytest
from ..variation import Variation

# Testes para inicialização e armazenamento de atributos básicos
def test_variation_initialization_stores_attributes():
    """Testa se os atributos de entrada são armazenados corretamente."""
    v = Variation(
        variation_a_visitors=100,
        variation_b_visitors=110,
        conversions_a=10,
        conversions_b=12
    )
    assert v.variation_a_visitors == 100
    assert v.variation_b_visitors == 110
    assert v.conversions_a == 10
    assert v.conversions_b == 12

# Testes parametrizados para cálculos de taxa de conversão
@pytest.mark.parametrize(
    "va_visitors, vb_visitors, ca, cb, expected_rate_a, expected_rate_b",
    [
        (100, 100, 10, 20, 0.10, 0.20),      # Caso base
        (200, 250, 50, 75, 0.25, 0.30),      # Outro caso base
        (0, 100, 0, 10, 0.0, 0.10),          # Visitantes de A são zero, conversões de A são 0
        (100, 0, 10, 0, 0.10, 0.0),          # Visitantes de B são zero, conversões de B são 0
        (0, 0, 0, 0, 0.0, 0.0),              # Ambos os visitantes são zero
        (100, 100, 0, 0, 0.0, 0.0),          # Zero conversões para ambos
        (50, 60, 0, 12, 0.0, 0.20),          # Zero conversões para A
        (70, 80, 14, 0, 0.20, 0.0),          # Zero conversões para B
        (100, 100, 100, 100, 1.0, 1.0),      # 100% de taxa de conversão
        (50, 50, 25, 50, 0.50, 1.0),         # Diferentes taxas, uma sendo 100%
        (123, 456, 12, 34, 12/123, 34/456),  # Números arbitrários
        # Casos onde conversões poderiam ser > visitantes (a classe atual permite isso, embora não seja lógico)
        # Se a classe não deve permitir, ela precisaria de validação interna.
        # Para a classe fornecida, o cálculo prosseguirá:
        (10, 10, 15, 5, 1.5, 0.5), # Taxa > 100% para A se não houver validação
    ]
)
def test_conversion_rate_calculations(
    va_visitors, vb_visitors, ca, cb, expected_rate_a, expected_rate_b
):
    """Testa o cálculo da taxa de conversão para vários cenários."""
    # Nota: Para o caso (0, 100, 10, 10), se conversions_a for >0 e variation_a_visitors for 0,
    # a lógica atual resultaria em conversion_rate_a = 0.0.
    # Se conversions_a for 10 e variation_a_visitors for 0, a taxa de A é 0.0.
    # Isto está coberto implicitamente, mas é bom ter em mente.
    # A parametrização já inclui casos com va_visitors=0, ca=0 -> expected_rate_a=0.0.

    v = Variation(
        variation_a_visitors=va_visitors,
        variation_b_visitors=vb_visitors,
        conversions_a=ca,
        conversions_b=cb
    )
    assert v.conversion_rate_a == pytest.approx(expected_rate_a)
    assert v.conversion_rate_b == pytest.approx(expected_rate_b)

# Teste específico para zero conversões com visitantes válidos
def test_zero_conversions_with_valid_visitors():
    """Testa se a taxa de conversão é 0.0 quando há zero conversões."""
    v = Variation(
        variation_a_visitors=100,
        variation_b_visitors=150,
        conversions_a=0,
        conversions_b=0
    )
    assert v.conversion_rate_a == 0.0
    assert v.conversion_rate_b == 0.0
    assert v.conversions_a == 0 # Verifica também o armazenamento
    assert v.conversions_b == 0

# Teste específico para taxa de conversão de 100%
def test_full_conversion_rate_when_conversions_equal_visitors():
    """Testa se a taxa de conversão é 1.0 quando conversões igualam visitantes."""
    v = Variation(
        variation_a_visitors=75,
        variation_b_visitors=85,
        conversions_a=75,
        conversions_b=85
    )
    assert v.conversion_rate_a == 1.0
    assert v.conversion_rate_b == 1.0

# O que acontece se entradas não inteiras ou negativas forem passadas?
# A classe como definida não tem validação explícita para isso.
# Python pode levantar um TypeError na divisão se, por exemplo, uma string for usada.
# Valores negativos seriam processados resultando em taxas possivelmente negativas ou >1.
# Testar esses comportamentos padrão do Python (sem validação customizada) pode ser feito assim:

def test_division_by_zero_standard_python_error_if_not_int_or_unhandled_type():
    """Testa o comportamento padrão do Python para tipos inválidos na divisão."""
    # Se passarmos algo que não seja número para os visitantes e não for 0,
    # a divisão pode falhar com TypeError.
    # O construtor espera 'int'. Se um tipo incorreto for passado,
    # e esse tipo não suportar divisão, um TypeError ocorrerá na linha de cálculo da taxa.
    with pytest.raises(TypeError):
        Variation(variation_a_visitors="abc", variation_b_visitors=100, conversions_a=10, conversions_b=10)

    # Se conversions_a for string e variation_a_visitors for um int != 0:
    with pytest.raises(TypeError):
        Variation(variation_a_visitors=100, variation_b_visitors=100, conversions_a="xyz", conversions_b=10)

def test_negative_inputs_are_processed_without_error_by_this_class_version():
    """
    Testa que a classe, como definida, processa números negativos
    sem levantar erro, resultando em taxas de conversão que podem ser negativas.
    """
    # Este teste verifica o comportamento da *sua classe como está escrita*.
    # Se este comportamento não é o desejado, a classe precisaria de validação.
    v = Variation(
        variation_a_visitors=-100,
        variation_b_visitors=100,
        conversions_a=-10, # -10 / -100 = 0.1
        conversions_b=10
    )
    assert v.conversion_rate_a == pytest.approx(0.1) # (-10 / -100)
    assert v.variation_a_visitors == -100 # Armazena o negativo
    assert v.conversions_a == -10

    v2 = Variation(
        variation_a_visitors=100,
        variation_b_visitors=100,
        conversions_a=-10, # -10 / 100 = -0.1
        conversions_b=10
    )
    assert v2.conversion_rate_a == pytest.approx(-0.1)