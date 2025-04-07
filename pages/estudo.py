import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from scipy.stats import t

st.set_page_config(page_title="Previsão da Turbidez da Água", layout="wide")
st.title("💧 Estudo da Turbidez da Água ao Longo do Tempo")

st.markdown("""
### 📘 O que é Turbidez?

A **turbidez** é uma medida da quantidade de partículas sólidas em suspensão na água que afetam sua transparência.  
Ela é normalmente causada por argilas, siltes, matéria orgânica, algas ou outros materiais.

- A unidade de medida usada é **NTU (Unidade Nefelométrica de Turbidez)**.
- Segundo a legislação brasileira e padrões internacionais, **valores abaixo de 5 NTU** são considerados **excelentes** para água potável.

---

### 🔍 Objetivo do Estudo

Este painel analisa dados históricos de turbidez da água coletados entre 2019 e 2021.  
Aplicamos uma **regressão linear** para prever quando os níveis de turbidez podem voltar a padrões **excelentes**.
""")

# === Carregamento dos dados ===
@st.cache_data
def carregar_dados():
    arquivos = {
        "2019": "dados/seriehistorica2019.xlsx",
        "1S2020": "dados/primeirosemestre2020.xlsx",
        "2S2020": "dados/segundosemestre2020.xlsx",
        "2021": "dados/ano2021.xlsx"
    }
    lista_dfs = []

    for nome, caminho in arquivos.items():
        df = pd.read_excel(caminho)
        df.columns = df.columns.str.strip().str.lower()

        if 'data de amostragem' in df.columns and 'turbidez' in df.columns:
            dados = df[['data de amostragem', 'turbidez']].copy()
            dados['data de amostragem'] = pd.to_datetime(dados['data de amostragem'], errors='coerce')
            dados = dados.dropna(subset=['data de amostragem', 'turbidez'])
            dados['periodo'] = nome
            lista_dfs.append(dados)

    return pd.concat(lista_dfs, ignore_index=True)

df = carregar_dados()

# === Pré-processamento ===
df = df.sort_values(by='data de amostragem')
df['ano_decimal'] = df['data de amostragem'].dt.year + (df['data de amostragem'].dt.dayofyear / 365)

# === Regressão Linear ===
X = df[['ano_decimal']].values
y = df['turbidez'].values
modelo = LinearRegression()
modelo.fit(X, y)

# Previsão para anos futuros
anos_futuros = np.arange(2019, 2031, 0.1).reshape(-1, 1)
previsoes = modelo.predict(anos_futuros)

# Criar datas reais para eixo X
datas_futuras = pd.to_datetime([f"{int(a)}-01-01" for a in anos_futuros.flatten()])

# === Gráfico 1: turbidez + regressão ===
st.header("📊 Evolução da Turbidez da Água")
fig = go.Figure()

# Pontos reais
fig.add_trace(go.Scatter(x=df['data de amostragem'], y=df['turbidez'],
                         mode='markers', name='Amostras', marker=dict(color='blue', size=5)))

# Linha de regressão
fig.add_trace(go.Scatter(x=datas_futuras, y=previsoes,
                         mode='lines', name='Tendência (Regressão Linear)', line=dict(color='red')))

# Linha padrão excelente
fig.add_hline(y=5, line_dash="dash", line_color="green",
              annotation_text="Padrão Excelente (5 NTU)", annotation_position="bottom right")

fig.update_layout(title="Turbidez da Água ao Longo do Tempo",
                  xaxis_title="Data", yaxis_title="Turbidez (NTU)",
                  height=500)

st.plotly_chart(fig, use_container_width=True)

# === Previsão de retorno à qualidade excelente ===
ano_excelente = None
for ano, pred in zip(anos_futuros.flatten(), previsoes):
    if pred <= 5:
        ano_excelente = ano
        break

st.subheader("📈 Previsão com Base na Tendência Atual")

if ano_excelente:
    st.success(f"""
    ✅ A análise de regressão linear prevê que a turbidez pode atingir o padrão excelente (**≤ 5 NTU**) 
    por volta de **{int(ano_excelente)}**.
    """)
else:
    st.warning("⚠️ A projeção atual indica que os níveis de turbidez podem não atingir o padrão excelente até 2030.")

# === Explicação estatística ===
st.markdown("""
---

### 📐 Sobre o Método Estatístico

Utilizamos **regressão linear simples**, uma técnica estatística que busca ajustar uma linha reta aos dados históricos, 
assumindo uma relação linear entre o tempo e os valores de turbidez.

Com base nesse modelo, geramos uma projeção para os anos seguintes. A ideia é observar **a tendência** e estimar quando a turbidez pode cair abaixo do limite ideal.

#### E o Intervalo de Confiança?

Embora esse gráfico mostre apenas a linha média prevista, abaixo apresentamos também o **intervalo de confiança de 95%**,  
que representa a faixa dentro da qual esperamos que a verdadeira turbidez esteja com 95% de certeza, dado o modelo.
""")

