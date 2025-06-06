📈 Ordem Lógica dos Cálculos
Calcular as Taxas de Conversão (Linhas 6 e 7)

Primeiro, calcule a Taxa de Conversão e o Erro Padrão para o Controle (coluna D) e para a Variação (coluna E).
Necessário: Visitantes e Conversões de cada grupo.
Calcular o Erro Padrão da Diferença (G13)


Com as taxas de conversão e visitantes de ambos, calcule o Standard Error Difference. Este valor é a base para o Z-Score.
Necessário: Taxa de Conversão e Visitantes (ambos os grupos).
Encontrar o Z-Crítico (G5)

Determine o Z-Table Value (Z-critical) com base no seu Nível de Confiança (D16).
Necessário: Nível de Confiança.
Calcular o Z-Score (G4)

Agora, calcule o Z-Score, que mede a força da diferença entre os dois grupos.
Necessário: Taxas de Conversão e o Erro Padrão da Diferença (passo 2).
Obter os Resultados Finais (G6, G7, G9, G10)

Com o Z-Score e o Z-Crítico, você pode finalmente calcular:
O P-Value (depende do Z-Score).
O Uplift (depende das Taxas de Conversão).
O Poder do Teste Observado (depende do Z-Score e Z-Crítico).
A Confiança Atual (depende do P-Value).
Basicamente, o fluxo é: Dados Individuais → Métrica de Diferença Combinada → Teste Estatístico (Z-Score) → Conclusões (P-Value, Poder).