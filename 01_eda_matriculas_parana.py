# -*- coding: utf-8 -*-
"""
Projeto 1 - Análise exploratória das matrículas do Ensino Médio no Paraná

Este script faz parte da transformação do TCC do MBA em Data Science e Analytics
em um projeto de portfólio.

Objetivo:
- analisar a evolução das matrículas do Ensino Médio no Paraná;
- comparar matrículas, população jovem e emprego formal em índice base 100;
- calcular a variação percentual das matrículas por município entre 2015 e 2024;
- preparar uma base para visualização espacial no QGIS.
"""

# =========================================================
# 1. IMPORTAÇÃO DAS BIBLIOTECAS
# =========================================================

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# =========================================================
# 2. CONFIGURAÇÕES INICIAIS
# =========================================================

diretorio = Path(
    "C:/Users/davic/OneDrive/Área de Trabalho/Projetos/Portifolio_TCC/Portifolio_TCC"
)


# =========================================================
# 3. LEITURA DA BASE
# =========================================================

df = pd.read_excel("BaseFinal.xlsx")


# =========================================================
# 4. PRIMEIRA VISÃO DA BASE
# =========================================================

print("VISÃO GERAL DA BASE")
print(df.head())

print("\nDimensão da base:")
print(df.shape)

print("\nPeríodo disponível:")
print(df["ANO"].min(), "a", df["ANO"].max())

print("\nQuantidade de municípios:")
print(df["NO_MUNICIPIO"].nunique())


# =========================================================
# 5. SELEÇÃO DAS VARIÁVEIS PRINCIPAIS PARA A EDA
# =========================================================

colunas_eda = [
    "ANO",
    "CO_MUNICIPIO",
    "NO_MUNICIPIO",
    "QT_MAT_MED_TOTAL",
    "ReprovEM",
    "Emprego",
    "Pop15_19"
]

df_eda = df[colunas_eda].copy()

print("\nBASE DE EDA")
print(df_eda.head())

print("\nDimensão da base de EDA:")
print(df_eda.shape)

print("\nValores ausentes por coluna:")
print(df_eda.isna().sum())


# =========================================================
# 6. FILTRO DO PERÍODO ANALÍTICO
# =========================================================

# Mantém apenas o período com dados completos para a EDA principal.
df_eda = df_eda[
    (df_eda["ANO"] >= 2015) &
    (df_eda["ANO"] <= 2024)
].copy()

print("\nPeríodo utilizado na EDA:")
print(df_eda["ANO"].min(), "a", df_eda["ANO"].max())

print("\nDimensão após filtro do período:")
print(df_eda.shape)


# =========================================================
# 7. EVOLUÇÃO DAS MATRÍCULAS NO PARANÁ
# =========================================================

matriculas_pr = (
    df_eda
    .groupby("ANO")["QT_MAT_MED_TOTAL"]
    .sum()
    .reset_index()
)

print("\nMATRÍCULAS TOTAIS NO PARANÁ")
print(matriculas_pr)


# =========================================================
# 8. GRÁFICO: EVOLUÇÃO DAS MATRÍCULAS NO PARANÁ
# =========================================================

plt.figure(figsize=(10, 6))

plt.plot(
    matriculas_pr["ANO"],
    matriculas_pr["QT_MAT_MED_TOTAL"],
    marker="o",
    linewidth=2
)

plt.title("Evolução das matrículas do Ensino Médio no Paraná (2015–2024)")
plt.xlabel("Ano")
plt.ylabel("Número de matrículas")
plt.xticks(matriculas_pr["ANO"])
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(
    "evolucao_matriculas_parana.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()


# =========================================================
# 9. SÉRIE AGREGADA DO PARANÁ
# =========================================================

serie_pr = (
    df_eda
    .groupby("ANO")[["QT_MAT_MED_TOTAL", "Pop15_19", "Emprego"]]
    .sum()
    .reset_index()
)

print("\nSÉRIE AGREGADA DO PARANÁ")
print(serie_pr)


# =========================================================
# 10. ÍNDICE BASE 100
# =========================================================

variaveis_base100 = [
    "QT_MAT_MED_TOTAL",
    "Pop15_19",
    "Emprego"
]

for var in variaveis_base100:
    valor_base = serie_pr.loc[
        serie_pr["ANO"] == 2015,
        var
    ].iloc[0]

    serie_pr[var + "_base100"] = (
        serie_pr[var] / valor_base
    ) * 100

print("\nSÉRIE COM ÍNDICE BASE 100")
print(serie_pr.head())

serie_indice = serie_pr[
    [
        "ANO",
        "QT_MAT_MED_TOTAL_base100",
        "Pop15_19_base100",
        "Emprego_base100"
    ]
].copy()


# =========================================================
# 11. GRÁFICO: VARIÁVEIS EM ÍNDICE BASE 100
# =========================================================

plt.figure(figsize=(10, 6))

plt.plot(
    serie_indice["ANO"],
    serie_indice["QT_MAT_MED_TOTAL_base100"],
    marker="o",
    linewidth=2,
    label="Matrículas no Ensino Médio"
)

plt.plot(
    serie_indice["ANO"],
    serie_indice["Pop15_19_base100"],
    marker="o",
    linewidth=2,
    label="População de 15 a 19 anos"
)

plt.plot(
    serie_indice["ANO"],
    serie_indice["Emprego_base100"],
    marker="o",
    linewidth=2,
    label="Emprego formal"
)

plt.axhline(
    y=100,
    linestyle="--",
    alpha=0.5
)

plt.title(
    "Evolução das matrículas, população jovem e emprego formal no Paraná\n"
    "Índice base 100 (2015 = 100)"
)
plt.xlabel("Ano")
plt.ylabel("Índice base 100")
plt.xticks(serie_indice["ANO"])
plt.grid(True, alpha=0.3)
plt.legend(loc="lower left")

plt.tight_layout()
plt.savefig(
    "indice_base100_matriculas_populacao_emprego.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()


# =========================================================
# 12. VARIAÇÃO MUNICIPAL DAS MATRÍCULAS ENTRE 2015 E 2024
# =========================================================

matriculas_municipios_2015_2024 = df_eda[
    df_eda["ANO"].isin([2015, 2024])
][
    ["NO_MUNICIPIO", "ANO", "QT_MAT_MED_TOTAL"]
].copy()

print("\nBASE MUNICIPAL 2015 E 2024")
print(matriculas_municipios_2015_2024.shape)

matriculas_pivot = matriculas_municipios_2015_2024.pivot(
    index="NO_MUNICIPIO",
    columns="ANO",
    values="QT_MAT_MED_TOTAL"
)

matriculas_pivot["Variacao_percentual"] = (
    (matriculas_pivot[2024] / matriculas_pivot[2015]) - 1
) * 100

ranking_variacao_municipal = (
    matriculas_pivot
    .sort_values(by="Variacao_percentual", ascending=True)
    .rename(
        columns={
            2015: "Matriculas_2015",
            2024: "Matriculas_2024"
        }
    )
)

print("\nVARIAÇÃO MUNICIPAL DAS MATRÍCULAS")
print(ranking_variacao_municipal.head())


# =========================================================
# 13. EXPORTAÇÃO DOS RESULTADOS
# =========================================================

ranking_variacao_municipal.to_excel(
    "variacao_matriculas_municipios_2015_2024.xlsx"
)

serie_pr.to_excel(
    "serie_parana_indicadores_base100.xlsx",
    index=False
)

print("\nArquivos exportados com sucesso.")