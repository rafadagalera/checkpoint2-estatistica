import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np
from scipy import stats

# Função para carregar os dados
@st.cache_data
def carregar_dados():
    arquivos = {
        "2019": "dados/seriehistorica2019.xlsx",
        "2020 - 1º Semestre": "dados/primeirosemestre2020.xlsx",
        "2020 - 2º Semestre": "dados/segundosemestre2020.xlsx",
        "2021": "dados/ano2021.xlsx"
    }

    dados = {}
    for nome, caminho in arquivos.items():
        ext = os.path.splitext(caminho)[1]
        if ext == ".xls":
            dados[nome] = pd.read_excel(caminho, engine='xlrd')
        else:
            dados[nome] = pd.read_excel(caminho)
    return dados

def analise_descritiva(df, coluna):
    desc = df[coluna].describe().to_frame().T
    desc['skewness'] = stats.skew(df[coluna].dropna())
    desc['kurtosis'] = stats.kurtosis(df[coluna].dropna())
    return desc

# Streamlit App
st.title("📊 Análise Exploratória de Dados de Qualidade da Água")
st.markdown("Selecione o período para visualizar os dados:")

dados = carregar_dados()
periodo = st.selectbox("Escolha o período:", list(dados.keys()))
df = dados[periodo]

# Seção expandida de estatísticas descritivas
st.subheader("📈 Estatísticas Descritivas")
colunas_numericas = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

if colunas_numericas:
    col_selecionada = st.selectbox("Selecione uma variável para análise:", colunas_numericas)
    
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(analise_descritiva(df, col_selecionada))
    
    with col2:
        # Teste de normalidade
        _, p_value = stats.normaltest(df[col_selecionada].dropna())
        st.metric("Teste de Normalidade (p-value)", f"{p_value:.4f}")
        st.caption("p-value < 0.05 indica não-normalidade")

# Matriz de correlação
st.subheader("🔗 Matriz de Correlação")
if len(colunas_numericas) > 1:
    corr_matrix = df[colunas_numericas].corr(numeric_only=True)
    fig_corr = px.imshow(corr_matrix, text_auto=True, aspect="auto",
                        title="Correlação entre Variáveis")
    st.plotly_chart(fig_corr, use_container_width=True)

# Gráficos de distribuição
st.subheader("📊 Distribuição dos Dados")
if colunas_numericas:
    col_dist = st.selectbox("Selecione variável para distribuição:", colunas_numericas, key='dist')
    
    tab1, tab2 = st.tabs(["Histograma", "Boxplot"])
    with tab1:
        fig_hist = px.histogram(df, x=col_dist, nbins=30, 
                              title=f"Distribuição de {col_dist}")
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with tab2:
        fig_box = px.box(df, y=col_dist, title=f"Boxplot de {col_dist}")
        st.plotly_chart(fig_box, use_container_width=True)

# Tentar detectar coluna de tempo
possiveis_colunas_tempo = [col for col in df.columns if "data" in col.lower() or "ano" in col.lower() or "mês" in col.lower() or "mes" in col.lower()]
coluna_tempo = None

if possiveis_colunas_tempo:
    coluna_tempo = st.selectbox("Coluna de tempo detectada:", possiveis_colunas_tempo)
    # Converter para datetime se possível
    try:
        df[coluna_tempo] = pd.to_datetime(df[coluna_tempo])
        df = df.sort_values(by=coluna_tempo)
    except Exception as e:
        st.warning(f"Não foi possível converter {coluna_tempo} para datetime: {e}")
        coluna_tempo = None

# Gráfico com eixo do tempo fixo
if coluna_tempo:
    colunas_numericas = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
    if colunas_numericas:
        col_y = st.selectbox("Escolha a variável a ser analisada:", colunas_numericas, key="y")

        fig = px.line(df, x=coluna_tempo, y=col_y, title=f"{col_y} ao longo do tempo")
        st.plotly_chart(fig)
    else:
        st.warning("Não há colunas numéricas disponíveis para análise gráfica.")
else:
    st.info("Nenhuma coluna de tempo foi detectada automaticamente. Verifique se há colunas como 'Data', 'Ano', 'Mês', etc.")

st.subheader("🏞️ Estações com maiores valores para a variável selecionada")

coluna_estacao = df["Estação"]

colunas_numericas = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

if colunas_numericas:
    col_variavel = st.selectbox("Escolha a variável para análise por estação:", colunas_numericas, key="por_estacao")

    tipo_agregacao = st.radio("Tipo de agregação:", ["Média", "Soma"], horizontal=True)

    if tipo_agregacao == "Média":
        df_agg = df.groupby(coluna_estacao)[col_variavel].mean().sort_values(ascending=False)
    else:
        df_agg = df.groupby(coluna_estacao)[col_variavel].sum().sort_values(ascending=False)

    fig2 = px.bar(df_agg, x=df_agg.index, y=df_agg.values,
                  labels={"x": "Estação", "y": col_variavel},
                  title=f"{tipo_agregacao} de {col_variavel} por Estação")
    st.plotly_chart(fig2)
else:
    st.warning("Nenhuma coluna numérica disponível para análise por estação.")
