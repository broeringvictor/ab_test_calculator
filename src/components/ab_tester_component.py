import streamlit as st
from datetime import date, timedelta
from domain.entities.ab_tester import ABTester # Importa sua entidade

class ABTesterComponent:
    """
    Um componente Streamlit para renderizar e gerenciar os inputs
    relacionados à entidade ABTester.
    """
    def __init__(self):
        """Inicializa o componente."""
        # Atributos para armazenar os valores dos inputs
        self.name = "Teste A/B"
        self.start_date = date.today()
        self.end_date = self.start_date + timedelta(days=14)
        self.hypothesis = ""
        self.desired_confidence_level = 95.0

    def render_inputs(self):
        """
        Renderiza todos os widgets de input do Streamlit na tela.
        Os valores selecionados pelo usuário são armazenados nos atributos da classe.
        """
        st.header("1. Definições do Teste")

        self.name = st.text_input(
            label="Nome do Teste",
            value=self.name,
            help="Dê um nome descritivo para o seu teste A/B."
        )

        self.hypothesis = st.text_area(
            label="Hipótese do Teste",
            placeholder="Ex: Se alterarmos a cor do botão 'Comprar' para verde, então a taxa de cliques aumentará pois a nova cor gera mais destaque.",
            help="Descreva o que você espera que aconteça e por quê."
        )
        
        # Usamos colunas para organizar as datas lado a lado
        col1, col2 = st.columns(2)
        with col1:
            self.start_date = st.date_input(
                label="Data de Início",
                value=self.start_date,
                min_value=date(2020, 1, 1),
                max_value=date(2030, 12, 31)
            )

        with col2:
            self.end_date = st.date_input(
                label="Data de Encerramento",
                value=self.end_date,
                min_value=self.start_date, # Data final não pode ser antes da inicial
                max_value=date(2030, 12, 31)
            )

        # Usar um selectbox para o nível de confiança evita erros de digitação
        self.desired_confidence_level = st.selectbox(
            label="Nível de Confiança Desejado",
            options=[90.0, 95.0, 99.0],
            index=1, # Deixa 95.0 como padrão
            format_func=lambda x: f"{x}%", # Formata para mostrar o % na UI
            help="O nível de confiança estatística desejado para validar o resultado."
        )

    def get_ab_tester_entity(self) -> ABTester:
        """
        Cria e retorna uma instância da entidade ABTester com os dados
        coletados dos inputs do Streamlit.

        Returns:
            ABTester: Uma instância da sua entidade de domínio.
        """
        # Validação simples para garantir que a data final não seja anterior à inicial
        if self.end_date < self.start_date:
            st.error("A data de encerramento não pode ser anterior à data de início.")
            return None # Retorna None se os dados forem inválidos

        return ABTester(
            name=self.name,
            start_date=self.start_date,
            end_date=self.end_date,
            hypothesis=self.hypothesis,
            desired_confidence_level=self.desired_confidence_level
        )

# Exemplo de como usar a classe em sua página principal do Streamlit
if __name__ == '__main__':
    st.set_page_config(layout="wide")
    st.title("Calculadora de Teste A/B")

    # Coloca os inputs na barra lateral (sidebar)
    with st.sidebar:
        # 1. Cria uma instância do componente
        ab_tester_form = ABTesterComponent()
        
        # 2. Renderiza os inputs na tela
        ab_tester_form.render_inputs()

    # 3. Recupera a entidade com os dados preenchidos
    tester_entity = ab_tester_form.get_ab_tester_entity()

    # Mostra os dados coletados na página principal (para depuração)
    if tester_entity:
        st.subheader("Dados Coletados do Formulário:")
        st.write(f"**Nome:** {tester_entity.name}")
        st.write(f"**Hipótese:** {tester_entity.hypothesis}")
        st.write(f"**Período:** {tester_entity.start_date.strftime('%d/%m/%Y')} a {tester_entity.end_date.strftime('%d/%m/%Y')}")
        # A entidade ABTester multiplica o valor, então mostramos o resultado
        st.write(f"**Nível de Confiança (na entidade):** {tester_entity.desired_confidence_level}")