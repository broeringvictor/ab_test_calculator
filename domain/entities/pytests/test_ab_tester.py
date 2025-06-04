import pytest
from datetime import date
from ..ab_tester import ABTester  # Ou o caminho correto se seu arquivo for diferente

def test_abtester_creation_and_attributes():
    """
    Testa a criação de uma instância de ABTester e a correta atribuição
    dos seus atributos, incluindo a conversão do nível de confiança.
    """
    # 1. Preparação (Arrange)
    # Define os dados de entrada para o teste
    test_name = "Teste de Nova Cor de Botão"
    test_start_date = date(2024, 1, 10)
    test_end_date = date(2024, 1, 24)
    test_hypothesis = "A nova cor do botão (azul) aumentará a taxa de cliques em 10%."
    input_confidence_level = 0.95  # Ex: 95%
    expected_stored_confidence_level = 95.0 # input_confidence_level * 100

    # 2. Ação (Act)
    # Cria uma instância da classe ABTester com os dados de entrada
    tester_instance = ABTester(
        name=test_name,
        start_date=test_start_date,
        end_date=test_end_date,
        hypothesis=test_hypothesis,
        desired_confidence_level=input_confidence_level
    )

    # 3. Verificação (Assert)
    # Verifica se todos os atributos da instância foram definidos corretamente
    assert tester_instance.name == test_name, "O nome do teste não foi atribuído corretamente."
    assert tester_instance.start_date == test_start_date, "A data de início não foi atribuída corretamente."
    assert tester_instance.end_date == test_end_date, "A data de término não foi atribuída corretamente."
    assert tester_instance.hypothesis == test_hypothesis, "A hipótese não foi atribuída corretamente."
    assert tester_instance.desired_confidence_level == expected_stored_confidence_level, \
        f"O nível de confiança não foi convertido e armazenado corretamente. Esperado: {expected_stored_confidence_level}, Obtido: {tester_instance.desired_confidence_level}"

    # Teste adicional para outro valor de nível de confiança (opcional, mas bom para cobrir mais casos)
    input_confidence_level_2 = 0.99
    expected_stored_confidence_level_2 = 99.0
    tester_instance_2 = ABTester("Teste 2", date(2024, 2, 1), date(2024, 2, 15), "Outra hipótese", input_confidence_level_2)
    assert tester_instance_2.desired_confidence_level == expected_stored_confidence_level_2, \
        "O nível de confiança para 0.99 não foi convertido corretamente."

    input_confidence_level_3 = 0.0
    expected_stored_confidence_level_3 = 0.0
    tester_instance_3 = ABTester("Teste 3", date(2024, 3, 1), date(2024, 3, 15), "Hipótese para 0%", input_confidence_level_3)
    assert tester_instance_3.desired_confidence_level == expected_stored_confidence_level_3, \
        "O nível de confiança para 0.0 não foi convertido corretamente."