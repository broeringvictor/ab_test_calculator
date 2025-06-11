import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide", page_title="Calculadora de Teste A/B")

# --- Importações ---
from domain.entities.ab_tester import ABTester
from domain.entities.variation import Variation
from components.ab_tester_component import ABTesterComponent
from components.variation_component import VariationComponent
from components.results_component import ResultsComponent 

def load_layout_css():
    # noinspection PyStringFormat,PyUnresolvedReferences
    st.markdown(f"""
        <style>
            /* Esconde o header e footer padrão do Streamlit */
            #MainMenu, footer {{visibility: hidden;}}
            /* Adiciona um pouco mais de espaço no topo da página */
            .block-container {{padding-top: 2rem;}}
            /* Ajusta o espaçamento nas abas da sidebar */
            [data-testid="stTabs"] {{margin-top: -20px;}}
        </style>

    """, unsafe_allow_html=True)

load_layout_css()

if "init" not in st.session_state:
    st.session_state.chart_data = pd.DataFrame(
        np.random.randn(20, 3), columns=["a", "b", "c"]
    )
    st.session_state.map_data = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
        columns=["lat", "lon"],
    )
    st.session_state.init = True


def hash_ab_tester_entity(tester: ABTester) -> tuple:
    """Cria uma impressão digital (hash) para a entidade ABTester."""
    # Ajuste esta tupla para incluir todos os atributos de ABTester
    # que afetam os cálculos em ABStatisticalValidator ou a exibição em ResultsComponent.
    # Exemplo: name, start_date, end_date, hypothesis, desired_confidence_level
    return (
        tester.name,
        tester.start_date,
        tester.end_date,
        tester.hypothesis,
        tester.desired_confidence_level

    )

def hash_variation_entity(variation: Variation) -> tuple:
    """Cria uma impressão digital (hash) para a entidade Variation."""

    return (
        variation.variation_a_visitors,
        variation.conversions_a,
        variation.variation_b_visitors,
        variation.conversions_b,
        variation.tail_numbers,
        variation.confidence_level, 
        variation.estimated_uplift
    )

@st.cache_data(
    ttl=3600,
    hash_funcs={
        ABTester: hash_ab_tester_entity,
        Variation: hash_variation_entity
    }
)
def perform_statistical_analysis(tester_entity: ABTester, variation_entity: Variation):
    """
    Cria o componente de resultados. Os cálculos são feitos dentro do ResultsComponent.
    O decorator @st.cache_data garante que ela só rode se os inputs (entidades) mudarem.
    """
    print("Instanciando ResultsComponent (cache miss para perform_statistical_analysis)...") # Para debug
    # ResultsComponent agora faz os cálculos em seu __init__
    results_display_component = ResultsComponent(tester=tester_entity, variation=variation_entity)
    return results_display_component



# --- Lógica do Botão de Limpeza ---
def clear_state():
    """Limpa o cache e todos os dados do session_state."""
    st.cache_data.clear()
    st.cache_resource.clear()
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    print("Cache e estado da sessão foram limpos.")
    st.rerun()

# --- Barra Lateral com os Formulários (Inputs) ---
with st.sidebar:
    
    ab_tester_form = ABTesterComponent()
    variation_form = VariationComponent()

    ab_tester_form.render_inputs()
    st.divider()
    variation_form.render_inputs()
    
    # Adiciona um espaço para empurrar o botão para baixo
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    calculate_button = st.button("Analisar Resultados", type="primary", use_container_width=True)


# --- Página Principal com os Resultados (Outputs) ---
if calculate_button:
    tester_entity = ab_tester_form.get_ab_tester_entity()
    variation_entity = variation_form.get_variation_entity()

    if tester_entity and variation_entity:
        with st.spinner("Calculando resultados..."):
            results_component = ResultsComponent(tester=tester_entity, variation=variation_entity)
            results_component.render()
    else:
        st.error("Erro ao obter dados dos formulários. Verifique os inputs.")
else:
    st.info("Preencha os dados do teste na barra lateral e clique em 'Analisar Resultados' para começar.")
