import streamlit as st
from components.results_component import ResultsComponent
from domain.entities.ab_tester import ABTester
from domain.entities.variation import Variation

# --- Funções de Hash Corrigidas ---
def _hash_ab_tester_entity(tester: ABTester) -> tuple:
    """Cria um hash para a entidade ABTester."""
    # CORRIGIDO: Usa os nomes de atributos corretos da classe ABTester
    return (
        tester.confidence_level,
        tester.power_level,
    )

def _hash_variation_entity(variation: Variation) -> tuple:
    """Cria um hash para a entidade Variation."""
    return (
        variation.variation_a_visitors,
        variation.conversions_a,
        variation.variation_b_visitors,
        variation.conversions_b,
        variation.tail_numbers,
        variation.confidence_level,
        variation.estimated_uplift
    )

# --- Função de Análise com Cache ---
@st.cache_data(
    ttl=3600,
    hash_funcs={
        ABTester: _hash_ab_tester_entity,
        Variation: _hash_variation_entity
    }
)
def perform_statistical_analysis(tester_entity: ABTester, variation_entity: Variation) -> ResultsComponent:
    """
    Executa a análise estatística e retorna o componente de resultados.
    """
    print("Executando a análise estatística (sem cache)...") # Para debug
    return ResultsComponent(tester=tester_entity, variation=variation_entity)