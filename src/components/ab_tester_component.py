import streamlit as st
from datetime import date, timedelta
from domain.entities.ab_tester import ABTester # Sua entidade permanece a mesma

class ABTesterComponent:
    """
    Componente Streamlit corrigido para gerenciar os inputs de um teste A/B,
    usando st.session_state para persistir os dados do usuário.
    """
    def __init__(self):
        """
        Inicializa o st.session_state com valores padrão, mas APENAS
        se eles ainda não existirem. Isso garante que os dados do usuário
        sejam preservados entre as reexecuções do script.
        """
        # Define os valores no session_state para persistência de dados.
        # O 'if' garante que isso só acontece uma vez por sessão.
        if 'ab_tester_name' not in st.session_state:
            st.session_state.ab_tester_name = "Teste A/B"
        if 'ab_tester_start_date' not in st.session_state:
            st.session_state.ab_tester_start_date = date.today()
        if 'ab_tester_end_date' not in st.session_state:
            # A data final deve ser baseada na data de início do session_state
            st.session_state.ab_tester_end_date = st.session_state.ab_tester_start_date + timedelta(days=14)
        if 'ab_tester_hypothesis' not in st.session_state:
            st.session_state.ab_tester_hypothesis = ""
        if 'ab_tester_confidence' not in st.session_state:
            st.session_state.ab_tester_confidence = 95.0

    def render_inputs(self):
        """
        Renderiza os widgets de input. O parâmetro 'key' de cada widget
        conecta-o diretamente a uma chave no st.session_state,
        garantindo a leitura e escrita dos dados corretos.
        """
        st.header("Definições do Teste")

        # Não atribuímos mais a 'self.name'. O 'key' cuida de tudo.
        st.text_input(
            label="Nome do Teste",
            key='ab_tester_name', # Vinculado ao session_state
            help="Dê um nome descritivo para o seu teste A/B."
        )

        st.text_area(
            label="Hipótese do Teste",
            key='ab_tester_hypothesis', # Vinculado ao session_state
            placeholder="Ex: Se alterarmos a cor do botão 'Comprar' para verde, a taxa de cliques aumentará.",
            help="Descreva o que você espera que aconteça e por quê."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.date_input(
                label="Data de Início",
                key='ab_tester_start_date', # Vinculado ao session_state
                min_value=date(2020, 1, 1)
            )

        with col2:
            st.date_input(
                label="Data de Encerramento",
                key='ab_tester_end_date', # Vinculado ao session_state
                min_value=st.session_state.ab_tester_start_date # Validação em tempo real
            )

        st.selectbox(
            label="Nível de Confiança Desejado",
            options=[90.0, 95.0, 99.0],
            key='ab_tester_confidence', # Vinculado ao session_state
            index=1,
            format_func=lambda x: f"{int(x)}%",
            help="O nível de confiança estatística para validar o resultado."
        )

    def get_ab_tester_entity(self) -> ABTester | None:
        """
        Cria e retorna uma instância da entidade ABTester lendo os dados
        diretamente do st.session_state, que contém os valores inseridos pelo usuário.
        """
        # A validação agora usa os dados corretos do session_state
        if st.session_state.ab_tester_end_date < st.session_state.ab_tester_start_date:
            st.error("A data de encerramento não pode ser anterior à data de início.")
            return None

        # Cria a entidade a partir dos dados persistidos no session_state
        return ABTester(
            name=st.session_state.ab_tester_name,
            start_date=st.session_state.ab_tester_start_date,
            end_date=st.session_state.ab_tester_end_date,
            hypothesis=st.session_state.ab_tester_hypothesis,
            desired_confidence_level=st.session_state.ab_tester_confidence
        )