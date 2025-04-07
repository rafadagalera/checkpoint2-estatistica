import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from scipy.stats import t
from scipy import stats

st.set_page_config(page_title="Previsão da Turbidez da Água", layout="wide")
st.title("💧 Estudo da Turbidez da Água ao Longo do Tempo")
st.markdown("### 🧾 Estrutura do Dataset e Classificação das Variáveis")

# Mapeamento manual de classificação estatística
classificacao_variaveis = {
    "data de amostragem": "Qualitativa ordinal",
    "turbidez": "Quantitativa contínua",
    "periodo": "Qualitativa nominal",
    "ano decimal": "Quantitativa contínua",
    "sólidos totais": "Quantitativa contínua",
    'estação': 'Qualitativa nominal'
}

# Criar tabela de classificação
tabela_variaveis = pd.DataFrame({
    "Variável": list(classificacao_variaveis.keys()),
    "Tipo Estatístico": list(classificacao_variaveis.values())
})

st.dataframe(tabela_variaveis, use_container_width=True)

st.markdown("""
As variáveis foram classificadas de acordo com sua natureza estatística:

- **Qualitativa nominal:** categorias sem ordem definida (ex: período).
- **Qualitativa ordinal:** categorias com ordem (ex: tempo).
- **Quantitativa contínua:** números reais que admitem frações (ex: turbidez, ano decimal).
""")


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

        colunas_interesse = ['data de amostragem', 'turbidez', 'sólidos totais', 'solidos totais','estação']
        colunas_presentes = [col for col in colunas_interesse if col in df.columns]

        if 'data de amostragem' in colunas_presentes:
            dados = df[colunas_presentes].copy()
            dados['data de amostragem'] = pd.to_datetime(dados['data de amostragem'], errors='coerce')
            dados = dados.dropna(subset=['data de amostragem'])
            dados['periodo'] = nome
            lista_dfs.append(dados)

    return pd.concat(lista_dfs, ignore_index=True)



df = carregar_dados()

# Padronizar nome da coluna de sólidos totais
df = df.rename(columns={
    'solidos totais': 'sólidos totais'
})


# === Pré-processamento ===
df = df.sort_values(by='data de amostragem')
df['ano_decimal'] = df['data de amostragem'].dt.year + (df['data de amostragem'].dt.dayofyear / 365)

# === Regressão Linear ===
# Garantir que não há NaN em X e y
df_modelo = df[['ano_decimal', 'turbidez']].dropna()
X = df_modelo[['ano_decimal']].values
y = df_modelo['turbidez'].values

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

""")

st.header("🧪 Evolução dos Sólidos Totais (STD)")

if 'sólidos totais' in df.columns:
    std_data = df[['data de amostragem', 'sólidos totais']].dropna()

    fig_std = go.Figure()
    fig_std.add_trace(go.Scatter(
        x=std_data['data de amostragem'],
        y=std_data['sólidos totais'],
        mode='lines+markers',
        name='STD',
        line=dict(color='purple')
    ))

    fig_std.update_layout(
        title="Concentração de Sólidos Totais ao Longo do Tempo",
        xaxis_title="Data",
        yaxis_title="Concentração de STD (mg/L)",
        height=500
    )

    st.plotly_chart(fig_std, use_container_width=True)
else:
    st.info("⚠️ Nenhuma informação sobre sólidos totais foi encontrada nos dados carregados.")

# === Filtragem e gráfico das estações RD074, RD075, RD009 ===
estacoes_interesse = ['RD074', 'RD075', 'RD009']

st.header("Mapa das estações de coleta")
st.image('assets\download.png')
st.write('Declararemos as estações RD074, RD075 e RD009 como estações de interesse para o nosso estudo, devido a sua proximidade a barragem rompida')

# Filtrar os dados para as estações de interesse e as demais
df_estacoes_interesse = df[df['estação'].isin(estacoes_interesse)]
df_outros = df[~df['estação'].isin(estacoes_interesse)]

# Gráfico para comparar sólidos totais nas estações de interesse com as demais
st.header("📊 Comparação dos Sólidos Totais nas Estações RD074, RD075, RD009 com as Demais")

# Criar o gráfico
fig_comparacao = go.Figure()

# Estações de interesse
fig_comparacao.add_trace(go.Box(
    y=df_estacoes_interesse['sólidos totais'],
    x=df_estacoes_interesse['estação'],
    name='Estações de Interesse (RD074, RD075, RD009)',
    boxmean='sd',
    marker=dict(color='orange')
))

# Outras estações
fig_comparacao.add_trace(go.Box(
    y=df_outros['sólidos totais'],
    x=df_outros['estação'],
    name='Outras Estações',
    boxmean='sd',
    marker=dict(color='blue')
))

fig_comparacao.update_layout(
    title="Distribuição dos Sólidos Totais por Estação",
    xaxis_title="Estação",
    yaxis_title="Sólidos Totais (mg/L)",
    height=500
)

st.plotly_chart(fig_comparacao, use_container_width=True)

# === Análise estatística (Intervalos de Confiança e Teste T) ===
# Calcular os intervalos de confiança e o teste t

# Função para calcular intervalo de confiança para a média
def intervalo_confianca(data, confidence=0.95):
    n = len(data)
    mean = np.mean(data)
    sem = stats.sem(data)  # Erro padrão da média
    margin_of_error = sem * t.ppf((1 + confidence) / 2., n-1)  # Margem de erro
    return mean - margin_of_error, mean + margin_of_error, mean

# Intervalo de confiança para as estações de interesse
ic_interesse_lower, ic_interesse_upper, mean_interesse = intervalo_confianca(df_estacoes_interesse['sólidos totais'])

# Intervalo de confiança para as outras estações
ic_outros_lower, ic_outros_upper, mean_outros = intervalo_confianca(df_outros['sólidos totais'])

# Exibir intervalos de confiança
st.subheader("📊 Intervalo de Confiança para a Média de Sólidos Totais")
st.write(f"**Estações de Interesse (RD074, RD075, RD009):**")
st.write(f"Média: {mean_interesse:.2f} mg/L")
st.write(f"Intervalo de Confiança (95%): ({ic_interesse_lower:.2f}, {ic_interesse_upper:.2f}) mg/L")

st.write(f"**Outras Estações:**")
st.write(f"Média: {mean_outros:.2f} mg/L")
st.write(f"Intervalo de Confiança (95%): ({ic_outros_lower:.2f}, {ic_outros_upper:.2f}) mg/L")

# Teste t para comparação de médias
t_stat, p_value = stats.ttest_ind(df_estacoes_interesse['sólidos totais'].dropna(), df_outros['sólidos totais'].dropna())

st.subheader("🔬 Teste T para Comparação de Médias")
st.write(f"**Estatística t:** {t_stat:.2f}")
st.write(f"**Valor p:** {p_value:.4f}")

if p_value < 0.05:
    st.success("📉 Existe uma diferença estatisticamente significativa entre os sólidos totais das estações de interesse (RD074, RD075, RD009) e as demais.")
else:
    st.info("📈 Não existe uma diferença estatisticamente significativa entre os sólidos totais das estações de interesse e as demais.")

st.write('Nota-se que, atuando com um intervalo de confiança de 95%, as médias dos sólidos totais presentes nas amostras coletadas pelas estações de interesse ainda são quase metade dos valores comparáveis coletados nas demais estações.')
st.write('Isso pode evidenciar uma maior preocupação com a remoção dos dejetos no local de rompimento da barragem')