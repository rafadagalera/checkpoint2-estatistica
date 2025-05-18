import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np
from scipy import stats

# Configuração da página
st.set_page_config(
    page_title="Análise de Qualidade da Água",
    layout="wide",
    page_icon="💧",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .header-text {
        font-size: 2.5rem !important;
        color: #2c3e50;
        font-weight: 700;
    }
    .section-title {
        color: #3498db;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.3rem;
    }
    .image-caption {
        text-align: center;
        font-style: italic;
        color: #7f8c8d;
        margin-top: 0.5rem;
    }
    .sidebar .sidebar-content {
        background-color: #2c3e50;
        color: white;
    }
    .sidebar .sidebar-content a {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Barra lateral com navegação
with st.sidebar:
    st.title("🌊 Navegação")
    st.markdown("- [Visão Geral](#visao-geral)")
    st.markdown("- [Estatísticas Descritivas](#estatisticas-descritivas)")
    st.markdown("- [Matriz de Correlação](#matriz-de-correlacao)")
    st.markdown("- [Distribuição dos Dados](#distribuicao-dos-dados)")
    st.markdown("- [Análise Temporal](#analise-temporal)")
    st.markdown("- [Análise por Estação](#analise-por-estacao)")
    
    st.divider()
    st.markdown("**📅 Períodos Disponíveis:**")
    st.markdown("- 2019")
    st.markdown("- 2020 (1º Semestre)")
    st.markdown("- 2020 (2º Semestre)")
    st.markdown("- 2021")
    
    st.divider()
    st.markdown("Desenvolvido por:")
    st.write("- Rafael Nascimento")
    st.write("- Iago Diniz")
    st.write("- Pedro Henrique")
    st.write("- Luis Alberto")
    st.markdown("Equipe de Análise de Dados Ambientais")
    st.markdown("Última atualização: Maio 2025")

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

# Conteúdo principal
st.markdown('<h1 class="header-text">📊 Análise Exploratória de Dados de Qualidade da Água</h1>', unsafe_allow_html=True)

# Seção de visão geral
st.markdown('<a name="visao-geral"></a>', unsafe_allow_html=True)
st.markdown("""
<div class="feature-card">
    <h3>Selecione o período para visualizar os dados:</h3>
    <p>Esta aplicação permite analisar dados de qualidade da água coletados em diferentes períodos após o desastre de Mariana.</p>
    <p>Explore as diversas seções através do menu lateral para obter insights sobre:</p>
    <ul>
        <li>Estatísticas descritivas dos parâmetros</li>
        <li>Relações entre variáveis</li>
        <li>Distribuição dos dados</li>
        <li>Variação temporal</li>
        <li>Comparação entre estações de monitoramento</li>
    </ul>
</div>
""", unsafe_allow_html=True)

dados = carregar_dados()
periodo = st.selectbox("Escolha o período:", list(dados.keys()))
df = dados[periodo]

# Seção de estatísticas descritivas
st.markdown('<a name="estatisticas-descritivas"></a>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">📈 Estatísticas Descritivas</h2>', unsafe_allow_html=True)

colunas_numericas = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

if colunas_numericas:
    col_selecionada = st.selectbox("Selecione uma variável para análise:", colunas_numericas)
    
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(analise_descritiva(df, col_selecionada).style.background_gradient(cmap='Blues'))
    
    with col2:
        # Teste de normalidade
        _, p_value = stats.normaltest(df[col_selecionada].dropna())
        st.metric("Teste de Normalidade (p-value)", f"{p_value:.4f}",
                 help="p-value < 0.05 indica que os dados não seguem uma distribuição normal")
        st.markdown("""
        <div class="feature-card">
            <h4>Interpretação:</h4>
            <ul>
                <li><strong>Média/Mediana:</strong> Tendência central dos dados</li>
                <li><strong>Desvio Padrão:</strong> Dispersão dos valores</li>
                <li><strong>Skewness:</strong> Assimetria da distribuição</li>
                <li><strong>Kurtosis:</strong> "Achatamento" da distribuição</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Matriz de correlação
st.markdown('<a name="matriz-de-correlacao"></a>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">🔗 Matriz de Correlação</h2>', unsafe_allow_html=True)

if len(colunas_numericas) > 1:
    corr_matrix = df[colunas_numericas].corr(numeric_only=True)
    fig_corr = px.imshow(corr_matrix, text_auto=True, aspect="auto",
                        title="Correlação entre Variáveis",
                        color_continuous_scale='Blues')
    st.plotly_chart(fig_corr, use_container_width=True)
    
    st.markdown("""
    <div class="feature-card">
        <h4>Como interpretar a matriz:</h4>
        <ul>
            <li><strong>Valores próximos de 1:</strong> Forte correlação positiva</li>
            <li><strong>Valores próximos de -1:</strong> Forte correlação negativa</li>
            <li><strong>Valores próximos de 0:</strong> Pouca ou nenhuma correlação</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Gráficos de distribuição
st.markdown('<a name="distribuicao-dos-dados"></a>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">📊 Distribuição dos Dados</h2>', unsafe_allow_html=True)

if colunas_numericas:
    col_dist = st.selectbox("Selecione variável para distribuição:", colunas_numericas, key='dist')
    
    tab1, tab2 = st.tabs(["Histograma", "Boxplot"])
    with tab1:
        fig_hist = px.histogram(df, x=col_dist, nbins=30, 
                              title=f"Distribuição de {col_dist}",
                              color_discrete_sequence=['#3498db'])
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with tab2:
        fig_box = px.box(df, y=col_dist, title=f"Boxplot de {col_dist}",
                        color_discrete_sequence=['#3498db'])
        st.plotly_chart(fig_box, use_container_width=True)

# Seção de análise temporal
st.markdown('<a name="analise-temporal"></a>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">⏳ Análise Temporal</h2>', unsafe_allow_html=True)

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

        fig = px.line(df, x=coluna_tempo, y=col_y, title=f"{col_y} ao longo do tempo",
                     color_discrete_sequence=['#3498db'])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Não há colunas numéricas disponíveis para análise gráfica.")
else:
    st.info("Nenhuma coluna de tempo foi detectada automaticamente. Verifique se há colunas como 'Data', 'Ano', 'Mês', etc.")

# Seção de análise por estação
st.markdown('<a name="analise-por-estacao"></a>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">🏞️ Análise por Estação de Monitoramento</h2>', unsafe_allow_html=True)

if 'Estação' in df.columns:
    colunas_numericas = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

    if colunas_numericas:
        col_variavel = st.selectbox("Escolha a variável para análise por estação:", colunas_numericas, key="por_estacao")

        tipo_agregacao = st.radio("Tipo de agregação:", ["Média", "Soma", "Máximo", "Mínimo"], horizontal=True)

        if tipo_agregacao == "Média":
            df_agg = df.groupby("Estação")[col_variavel].mean().sort_values(ascending=False)
        elif tipo_agregacao == "Soma":
            df_agg = df.groupby("Estação")[col_variavel].sum().sort_values(ascending=False)
        elif tipo_agregacao == "Máximo":
            df_agg = df.groupby("Estação")[col_variavel].max().sort_values(ascending=False)
        else:
            df_agg = df.groupby("Estação")[col_variavel].min().sort_values(ascending=False)

        fig2 = px.bar(df_agg, x=df_agg.index, y=df_agg.values,
                     labels={"x": "Estação", "y": col_variavel},
                     title=f"{tipo_agregacao} de {col_variavel} por Estação",
                     color=df_agg.values,
                     color_continuous_scale='Blues')
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Nenhuma coluna numérica disponível para análise por estação.")
else:
    st.warning("Coluna 'Estação' não encontrada nos dados.")

# Rodapé
st.divider()
st.markdown("""
<div style="text-align: center; color: #7f8c8d; font-size: 0.9rem;">
    Este projeto foi desenvolvido para fins acadêmicos e de pesquisa.<br>
    Dados coletados de fontes oficiais entre 2019-2021.<br>
    Para mais informações, entre em contato: contato@analiseambiental.org
</div>
""", unsafe_allow_html=True)