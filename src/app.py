import streamlit as st

# --- Configuração da Página ---
# ESTA DEVE SER A PRIMEIRA INSTRUÇÃO STREAMLIT
st.set_page_config(layout="wide", page_title="Calculadora de Teste A/B")

# --- Importações ---
# Importe suas classes de entidade e componentes DEPOIS de st.set_page_config
from domain.entities.ab_tester import ABTester
from domain.entities.variation import Variation
from components.ab_tester_component import ABTesterComponent
from components.variation_component import VariationComponent
from components.results_component import ResultsComponent # Adicionada importação global

# --- Funções de Hash para suas classes customizadas ---
def hash_ab_tester_entity(tester: ABTester) -> tuple:
    """Cria uma impressão digital (hash) para a entidade ABTester."""
    return (
        tester.name, # Adicionar todos os atributos que definem o estado
        tester.start_date,
        tester.end_date,
        tester.hypothesis,
        tester.desired_confidence_level,
        # Se ABTester tiver power_level, inclua-o. Caso contrário, remova.
        # Assumindo que power_level não está em ABTester, mas sim em Variation ou é um conceito geral.
        # Se for parte do ABTester, adicione: tester.power_level,
    )

def hash_variation_entity(variation: Variation) -> tuple:
    """Cria uma impressão digital (hash) para a entidade Variation."""
    return (
        variation.variation_a_visitors,
        variation.conversions_a,
        variation.variation_b_visitors,
        variation.conversions_b,
        variation.tail_numbers,
        variation.confidence_level, # Este é o confidence_level da variação (ex: 0.95)
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
    Executa a análise estatística e retorna o componente de resultados.
    O decorator @st.cache_data garante que ela só rode se os inputs mudarem.
    """
    print("Executando a análise estatística (cache miss)...") # Para debug
    # A instância do ResultsComponent já faz os cálculos no seu __init__
    results_component = ResultsComponent(tester=tester_entity, variation=variation_entity)
    return results_component

st.title("Calculadora de Significado Estatístico para Teste A/B")

# --- Lógica do Botão de Limpeza ---
def clear_state():
    """Limpa o cache e todos os dados do session_state."""
    st.cache_data.clear()
    st.cache_resource.clear()
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    print("Cache e estado da sessão foram limpos.")
    st.rerun() # Adicionado para recarregar a página e refletir a limpeza

# --- Barra Lateral com os Formulários (Inputs) ---
with st.sidebar:
    ab_tester_form = ABTesterComponent()
    variation_form = VariationComponent()

    ab_tester_form.render_inputs()
    st.divider()
    variation_form.render_inputs()
    
    st.divider()
    calculate_button = st.button("Analisar Resultados", type="primary", use_container_width=True)
    
    st.button("Limpar Dados e Cache", on_click=clear_state, use_container_width=True)

# --- Página Principal com os Resultados (Outputs) ---
if calculate_button:
    tester_entity = ab_tester_form.get_ab_tester_entity()
    variation_entity = variation_form.get_variation_entity()

    if tester_entity and variation_entity:
        with st.spinner("Calculando resultados..."):
            # Chama a função cacheada.
            # O ResultsComponent é retornado pela função cacheada.
            results_display_component = perform_statistical_analysis(tester_entity, variation_entity)
            results_display_component.render() # Renderiza os resultados
    else:
        st.error("Por favor, preencha todos os campos corretamente antes de analisar.")
else:
    st.info("Preencha os dados do teste na barra lateral e clique em 'Analisar Resultados'.")