# Calculadora de Validação de Testes A/B 📊

 Análise de significância estatística em testes A/B é um processo complexo e propenso a erros. Desenvolvi esta aplicação para simplificar essa rotina.

Utilizamos a metodologia de cálculo da respeitada planilha da Conversion Zone para assegurar a precisão dos resultados. O desafio é que a terminologia estatística, incluindo termos como:

- Bicaudal
- Uplift
- Z-Score

O que não faz parte do cotidiano de muitos profissionais de CRO, Produto ou Marketing.

Pensando nisso, criei esta calculadora interativa com Streamlit. A ferramenta oferece um dashboard completo, permitindo que equipes validem seus experimentos de forma rápida, visual e segura.

## 🚀 Aplicação em Produção
A calculadora está no ar e pronta para uso! Acesse através do link:

➤ https://www.calculadora-de-teste-ab.tech/

## ✨ Funcionalidades Principais

| Funcionalidade | Descrição / Benefício para o Usuário |
| :--- | :--- |
| **✅ Análise de Significância** | Descubra com confiança estatística se a Variação B é realmente diferente do Controle, utilizando métricas essenciais como **P-valor** e **Z-Score**. |
| **🔋 Medição de Poder (Power)** | Avalie a sensibilidade do seu teste. Saiba se o tamanho da sua amostra foi suficiente para detectar um efeito real, caso ele exista. |
| **📊 Intervalos de Confiança** | Visualize a faixa de valores provável para a taxa de conversão de cada grupo, permitindo uma análise de risco e potencial mais profunda. |
| **🛡️ Validação de SRM** | Garanta a integridade dos seus resultados. O sistema alerta automaticamente se a divisão de tráfego entre os grupos foi desbalanceada. |
| **⚖️ Testes Uni/Bicaudais** | Tenha flexibilidade para analisar os dados de acordo com a sua hipótese: se você busca apenas uma melhora ou qualquer tipo de diferença significativa. |
| **🎨 Interface Intuitiva** | Uma experiência de usuário limpa e direta, construída com Streamlit, que torna a análise estatística acessível a todos os níveis de conhecimento. |
| **🔄 CI/CD Automatizado** | Pipeline de deploy configurado com **GitHub Actions** e **Heroku**, garantindo que a aplicação em produção seja sempre estável e atualizada. |

## 🛠️ Tecnologias Utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9B71?style=for-the-badge&logo=pytest&logoColor=white)
![Heroku](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![UV](https://img.shields.io/badge/uv-Gerenciador%20de%20Pacotes-blue?style=for-the-badge)

## 🧠 Glossário de Termos Utilizados


**Visitantes**
> Usuários que acessam a página ou app, representando o volume total de tráfego do experimento.

**Conversões**
> Ações específicas que você deseja que os visitantes realizem (ex: compra, cadastro).

**Taxa de Conversão**
> A porcentagem de visitantes que realizam a conversão. É calculada como `(Conversões / Visitantes) * 100`.

**Erro Padrão**
> Medida da variabilidade da taxa de conversão da amostra, usada para calcular a precisão e os intervalos de confiança.

**Número de Caudas**
> Tipo de teste estatístico. **Unicaudal** (uma cauda) testa se uma variação é especificamente *melhor*. **Bicaudal** (duas caudas) testa se há qualquer *diferença* (melhor ou pior).

**Nível de Confiança (Confidence Level)**
> A probabilidade (geralmente 95%) de que os resultados encontrados sejam representativos da realidade.

**Poder do Teste Observado (Power)**
> A probabilidade de que o teste tenha detectado um efeito real, caso ele exista. Um poder de 80% ou mais é considerado ideal.

**Uplift**
> A melhoria percentual na taxa de conversão da variação em comparação com o controle.

**Z-Score**
> Medida que indica quantos desvios padrão a diferença observada está da média, ajudando a determinar a significância estatística.

**P-Value**
> A probabilidade de obter os resultados observados (ou mais extremos) se não houvesse nenhuma diferença real entre as variações. Um P-Value baixo (ex: < 0.05) indica significância estatística.

**Intervalos de Confiança**
> A faixa de valores dentro da qual a verdadeira taxa de conversão provavelmente se encontra, com base no nível de confiança.

**SRM (Sample Ratio Mismatch)**
> Ocorre quando a proporção de visitantes entre os grupos do teste não corresponde à proporção esperada, o que pode invalidar os resultados.





## 📜 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.