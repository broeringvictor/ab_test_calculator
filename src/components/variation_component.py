import streamlit as st
from domain.entities.variation import Variation # Mantenha a importação da sua entidade

class VariationComponent:
    """
    Componente Streamlit otimizado que usa st.tabs para um layout limpo
    e st.session_state para persistir TODOS os dados do formulário.
    """
    def __init__(self):
        """
        Inicializa as chaves no session_state para os dados das variações,
        apenas se elas ainda não existirem.
        """
        # Dados de visitantes e conversões
        if 'var_control_visitors' not in st.session_state:
            st.session_state.var_control_visitors = 10000
        if 'var_control_conversions' not in st.session_state:
            st.session_state.var_control_conversions = 500
        if 'var_variant_visitors' not in st.session_state:
            st.session_state.var_variant_visitors = 10000
        if 'var_variant_conversions' not in st.session_state:
            st.session_state.var_variant_conversions = 550
            
        # --- CAMPOS REINTEGRADOS ---
        # Inicializa os campos de 'Tipo de Teste' e 'Uplift' no session_state
        if 'var_tail_numbers' not in st.session_state:
            st.session_state.var_tail_numbers = 2 # Padrão para Bicaudal (Two-Tailed)
        if 'var_estimated_uplift' not in st.session_state:
            st.session_state.var_estimated_uplift = 10.0

    def render_inputs(self):
        """
        Renderiza os inputs dentro de um st.expander. Usa st.tabs para os dados
        das variações e posiciona os outros parâmetros do teste logo abaixo.
        """
        
        with st.expander("Variações e Parâmetros", expanded=True):
            st.subheader(" ")
            
            tab_control, tab_variant = st.tabs(["Controle (H0)", "Variação (H1)"])

            with tab_control:
                st.number_input("Número de Visitantes", min_value=1, step=1, key='var_control_visitors')
                st.number_input("Número de Conversões", min_value=0, step=1, key='var_control_conversions')

            with tab_variant:
                st.number_input("Número de Visitantes", min_value=1, step=1, key='var_variant_visitors')
                st.number_input("Número de Conversões", min_value=0, step=1, key='var_variant_conversions')
            
            st.divider()
            
            
            
            
            st.radio(
                label="Tipo de Teste (Caudas)",
                options=[1, 2],
                index=1, # Padrão Bicaudal
                key='var_tail_numbers',
                format_func=lambda x: "Unicaudal (One-Tailed)" if x == 1 else "Bicaudal (Two-Tailed)",
                horizontal=True,
                help="Unicaudal para testar se a variação é apenas 'melhor'. Bicaudal para testar qualquer diferença (melhor ou pior)."
            )
            
            st.number_input(
                label="Uplift Mínimo Esperado (MDE) (%)",
                min_value=0.1,
                step=0.1,
                key='var_estimated_uplift',
                help="O menor aumento percentual que você considera relevante para o negócio."
            )

    def get_variation_entity(self) -> Variation | None:
        """
        Cria a entidade a partir dos dados no st.session_state.
        Inclui todos os campos necessários para a construção da entidade.
        """
        # Validação
        if st.session_state.var_control_conversions > st.session_state.var_control_visitors:
            st.error("Controle: O número de conversões não pode ser maior que o de visitantes.")
            return None
        
        if st.session_state.var_variant_conversions > st.session_state.var_variant_visitors:
            st.error("Variação: O número de conversões não pode ser maior que o de visitantes.")
            return None

        # --- CONSTRUÇÃO DA ENTIDADE COMPLETA ---
        # Agora passando todos os argumentos que sua entidade original esperava.
        return Variation(
            variation_a_visitors=st.session_state.var_control_visitors,
            variation_b_visitors=st.session_state.var_variant_visitors,
            conversions_a=st.session_state.var_control_conversions,
            conversions_b=st.session_state.var_variant_conversions,
            tail_numbers=st.session_state.var_tail_numbers,
            # Pega o nível de confiança do outro componente através do session_state
            confidence_level=st.session_state.get('ab_tester_confidence', 95.0),
            estimated_uplift=st.session_state.var_estimated_uplift
        )