import streamlit as st
import pandas as pd
import scipy.stats as stats
import plotly.graph_objects as go

st.set_page_config(page_title="Análise com Intervalo de Confiança", layout="wide")
st.title("📊 Análise com Intervalo de Confiança entre Semestres")
st.markdown("Comparação de uma variável numérica entre o 1º e o 2º semestre de 2020 usando intervalo de confiança de 95%.")

# Carrega os dados
df1 = pd.read_excel("dados/primeirosemestre2020.xlsx")
df2 = pd.read_excel("dados/segundosemestre2020.xls", engine="xlrd")

# Padroniza os nomes das colunas
df1.columns = df1.columns.str.strip().str.lower()
df2.columns = df2.columns.str.strip().str.lower()

# Mostra os tipos de dados
st.subheader("🔍 Colunas disponíveis e tipos de dados:")
col1, col2 = st.columns(2)
with col1:
    st.write("📁 1º Semestre:")
    st.dataframe(df1.dtypes)
with col2:
    st.write("📁 2º Semestre:")
    st.dataframe(df2.dtypes)

# Interseção de colunas
colunas_comuns = df1.columns.intersection(df2.columns)

# Tenta detectar colunas numéricas comuns
colunas_numericas_comuns = [col for col in colunas_comuns if pd.api.types.is_numeric_dtype(df1[col]) and pd.api.types.is_numeric_dtype(df2[col])]

st.subheader("📌 Selecione a variável numérica para análise")

if colunas_numericas_comuns:
    col_od = st.selectbox("Variáveis numéricas comuns:", colunas_numericas_comuns)
else:
    st.warning("⚠️ Nenhuma coluna numérica comum foi detectada automaticamente.")
    col_od = st.selectbox("Selecione manualmente uma coluna presente nos dois arquivos:", df1.columns)

# Verifica se a coluna existe nos dois arquivos
if col_od in df1.columns and col_od in df2.columns:
    # Converte para numérico se necessário
    od_1 = pd.to_numeric(df1[col_od], errors="coerce").dropna()
    od_2 = pd.to_numeric(df2[col_od], errors="coerce").dropna()

    def media_e_ic(dados, confianca=0.95):
        n = len(dados)
        media = dados.mean()
        erro = stats.sem(dados)
        margem = erro * stats.t.ppf((1 + confianca) / 2, df=n - 1)
        return media, media - margem, media + margem

    media1, ic1_inf, ic1_sup = media_e_ic(od_1)
    media2, ic2_inf, ic2_sup = media_e_ic(od_2)

    # Tabela de resultado
    st.subheader("📋 Estatísticas e Intervalos de Confiança (95%)")
    st.write(pd.DataFrame({
        "Semestre": ["1º Semestre 2020", "2º Semestre 2020"],
        "Média": [media1, media2],
        "IC Inferior": [ic1_inf, ic2_inf],
        "IC Superior": [ic1_sup, ic2_sup]
    }))

    # Gráfico com IC
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["1º Sem 2020", "2º Sem 2020"],
        y=[media1, media2],
        error_y=dict(type='data', array=[media1 - ic1_inf, media2 - ic2_inf]),
        name="Intervalo de Confiança"
    ))
    fig.update_layout(title=f"Média de '{col_od}' com Intervalo de Confiança (95%)",
                      yaxis_title=col_od,
                      xaxis_title="Semestre",
                      height=500)
    st.plotly_chart(fig)

    # Conclusão com base na sobreposição
    st.subheader("📌 Conclusão")
    if ic1_sup < ic2_inf or ic2_sup < ic1_inf:
        st.success("✅ Existe uma diferença estatisticamente significativa entre os semestres.")
    else:
        st.info("ℹ️ Não foi encontrada uma diferença estatisticamente significativa entre os semestres.")
else:
    st.error(f"A coluna selecionada '{col_od}' não está presente nos dois arquivos.")
