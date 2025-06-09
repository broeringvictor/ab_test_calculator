import streamlit as st
from domain.entities.variation import Variation

class VariationComponent:
    """
    Componente Streamlit que usa st.session_state para persistir os dados do formulário.
    """
    def __init__(self):
        """Inicializa as chaves no session_state se ainda não existirem."""
        # Define os valores padrão apenas se não estiverem no estado da sessão
        if 'variation_a_visitors' not in st.session_state:
            st.session_state.variation_a_visitors = 10000
        if 'conversions_a' not in st.session_state:
            st.session_state.conversions_a = 500
        if 'variation_b_visitors' not in st.session_state:
            st.session_state.variation_b_visitors = 10000
        if 'conversions_b' not in st.session_state:
            st.session_state.conversions_b = 550
        if 'tail_numbers' not in st.session_state:
            st.session_state.tail_numbers = 1
        if 'estimated_uplift' not in st.session_state:
            st.session_state.estimated_uplift = 10.0

    def render_inputs(self):
        """Renderiza os inputs, usando as chaves do session_state para persistência."""
        st.header("2. Dados e Configurações do Teste")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Controle (Ho)")
            # O argumento 'key' liga o input diretamente ao st.session_state
            st.number_input(
                label="Número de Visitantes (Controle)",
                min_value=1,
                step=1,
                key='variation_a_visitors', # Chave para persistência
                help="Total de usuários expostos à versão de controle."
            )
            st.number_input(
                label="Número de Conversões (Controle)",
                min_value=0,
                step=1,
                key='conversions_a', # Chave para persistência
                help="Total de usuários que converteram na versão de controle."
            )

        with col2:
            st.subheader("Variação (H1)")
            st.number_input(
                label="Número de Visitantes (Variação)",
                min_value=1,
                step=1,
                key='variation_b_visitors', # Chave para persistência
                help="Total de usuários expostos à nova versão."
            )
            st.number_input(
                label="Número de Conversões (Variação)",
                min_value=0,
                step=1,
                key='conversions_b', # Chave para persistência
                help="Total de usuários que converteram na nova versão."
            )

        st.divider()
        st.subheader("Configurações Estatísticas")

        # Usando o 'key' também para o radio button
        st.radio(
            label="Tipo de Teste (Caudas)",
            options=[1, 2],
            index=0,
            key='tail_numbers',
            format_func=lambda x: "Unicaudal (One-Tailed)" if x == 1 else "Bicaudal (Two-Tailed)",
            horizontal=True,
            help="Unicaudal para testar se a variação é apenas 'melhor'. Bicaudal para testar qualquer diferença (melhor ou pior)."
        )
        st.number_input(
            label="Uplift Mínimo Esperado (MDE) (%)",
            min_value=0.1,
            step=0.1,
            key='estimated_uplift',
            help="O menor aumento percentual que você considera relevante para o negócio."
        )

    def get_variation_entity(self) -> Variation:
        """Cria a entidade a partir dos dados no st.session_state."""
        # Validação
        if st.session_state.conversions_a > st.session_state.variation_a_visitors:
            st.error("O número de conversões do Controle não pode ser maior que o de visitantes.")
            return None
        
        if st.session_state.conversions_b > st.session_state.variation_b_visitors:
            st.error("O número de conversões da Variação não pode ser maior que o de visitantes.")
            return None

        # Pega os valores do st.session_state em vez de atributos de 'self'
        return Variation(
            variation_a_visitors=st.session_state.variation_a_visitors,
            variation_b_visitors=st.session_state.variation_b_visitors,
            conversions_a=st.session_state.conversions_a,
            conversions_b=st.session_state.conversions_b,
            tail_numbers=st.session_state.tail_numbers,
            confidence_level=st.session_state.get('confidence_level', 95.0), # Assume que o confidence_level também está no state
            estimated_uplift=st.session_state.estimated_uplift
        )