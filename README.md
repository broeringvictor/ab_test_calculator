Calculadora de Validação de Testes A/B 📊

Uma ferramenta interativa e poderosa para validar estatisticamente os resultados de testes A/B. Esta aplicação foi desenvolvida em Python com Streamlit e oferece uma análise completa, incluindo significância estatística, poder do teste, intervalos de confiança e muito mais.

O projeto foi inspirado na Calculadora de Validação de Testes A/B da Conversion Zone e utiliza os mesmos cálculos robustos como base para suas análises.

🚀 Aplicação em Produção
A calculadora está no ar e pronta para uso! Acesse através do link:

➤ https://www.calculadora-de-teste-ab.tech/


## ✨ Funcionalidades Principais

* **✅ Análise de Significância Estatística**: Descubra com confiança se os resultados do seu teste são estatisticamente relevantes, com base em métricas essenciais como P-valor e Z-Score.

* **🔋 Medição de Poder do Teste**: Verifique o "Poder Observado" e entenda se o seu teste teve uma amostra robusta o suficiente para detectar um efeito real.

* **📊 Intervalos de Confiança**: Visualize a faixa provável da verdadeira taxa de conversão para cada variação, oferecendo uma camada extra de profundidade na análise.

* **🛡️ Validação de SRM (Sample Ratio Mismatch)**: Garanta a confiabilidade dos seus dados com a detecção automática de desbalanceamento no tráfego do teste.

* **⚖️ Suporte a Testes Uni e Bicaudais**: Configure a análise estatística de acordo com a sua hipótese (se você espera apenas uma melhoria ou qualquer tipo de diferença).

* **🎨 Interface Intuitiva e Interativa**: Construída com Streamlit para uma experiência de usuário limpa, facilitando a inserção de dados e a interpretação dos resultados.

* **🔄 CI/CD Automatizado**: Pipeline configurado com GitHub Actions para rodar testes (`pytest`) e fazer deploy automático no Heroku, garantindo estabilidade e agilidade.

🛠️ Tecnologias Utilizadas
Framework Web: Streamlit
Linguagem: Python 3.11+
Gerenciador de Pacotes: UV
Testes: Pytest
Hospedagem: Heroku
CI/CD: GitHub Actions




🧠 Glossário de Termos Utilizados
&lt;details>
&lt;summary>Clique para ver as definições das métricas usadas na calculadora&lt;/summary>

Visitantes: Usuários que acessam a página ou app, representando o volume total de tráfego do experimento.

Conversões: Ações específicas que você deseja que os visitantes realizem (ex: compra, cadastro).

Taxa de Conversão: A porcentagem de visitantes que realizam a conversão. (Conversões / Visitantes) * 100.

Erro Padrão: Medida da variabilidade da taxa de conversão da amostra, usada para calcular a precisão e os intervalos de confiança.

Número de Caudas: Tipo de teste estatístico. Unicaudal (uma cauda) testa se uma variação é especificamente melhor. Bicaudal (duas caudas) testa se há qualquer diferença (melhor ou pior).

Nível de Confiança: A probabilidade (geralmente 95%) de que os resultados encontrados sejam representativos da realidade.

Poder do Teste Observado (Power): A probabilidade de que o teste tenha detectado um efeito real, caso ele exista. Um poder de 80% ou mais é considerado ideal.

Uplift: A melhoria percentual na taxa de conversão da variação em comparação com o controle.

Z-Score: Medida que indica quantos desvios padrão a diferença observada está da média, ajudando a determinar a significância estatística.

P-Value: A probabilidade de obter os resultados observados (ou mais extremos) se não houvesse nenhuma diferença real entre as variações. Um P-Value baixo (ex: &lt; 0.05) indica significância estatística.

Intervalos de Confiança: A faixa de valores dentro da qual a verdadeira taxa de conversão provavelmente se encontra, com base no nível de confiança.

SRM (Sample Ratio Mismatch): Ocorre quando a proporção de visitantes entre os grupos do teste não corresponde à proporção esperada, o que pode invalidar os resultados.

&lt;/details>

📜 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.