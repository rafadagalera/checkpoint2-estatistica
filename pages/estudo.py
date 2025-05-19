import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from scipy.stats import t, binomtest
from scipy import stats

# Configuração da página
st.set_page_config(
    page_title="Previsão da Turbidez da Água",
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
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        color: #856404;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Barra lateral com navegação
with st.sidebar:
    st.title("🌊 Navegação")
    st.markdown("- [Visão Geral](#visao-geral)")
    st.markdown("- [Classificação das Variáveis](#classificacao-variaveis)")
    st.markdown("- [Modelos de Previsão](#modelos-previsao)")
    st.markdown("- [Diagnóstico do Modelo](#diagnostico-modelo)")
    st.markdown("- [Análise Binomial](#analise-binomial)")
    st.markdown("- [Correlação entre Variáveis](#correlacao-variaveis)")
    st.markdown("- [Análise por Estação](#analise-estacao)")
    st.markdown("- [Teste de Hipótese](#teste-hipotese)")
    
    st.divider()
    st.markdown("**📅 Períodos Analisados:**")
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

# Conteúdo principal
st.markdown('<h1 class="header-text">💧 Estudo da Turbidez da Água ao Longo do Tempo</h1>', unsafe_allow_html=True)

# Seção de visão geral
st.markdown('<a name="visao-geral"></a>', unsafe_allow_html=True)
st.markdown("""
<div>
    <h3>📘 O que é Turbidez?</h3>
    <p>A <strong>turbidez</strong> é uma medida da quantidade de partículas sólidas em suspensão na água que afetam sua transparência.</p>
    <p>Ela é normalmente causada por argilas, siltes, matéria orgânica, algas ou outros materiais.</p>
    <ul>
        <li>A unidade de medida usada é <strong>NTU (Unidade Nefelométrica de Turbidez)</strong>.</li>
        <li>Segundo a legislação brasileira e padrões internacionais, <strong>valores abaixo de 5 NTU</strong> são considerados <strong>excelentes</strong> para água potável.</li>
    </ul>
    <h3>🔍 Objetivo do Estudo</h3>
    <p>Este painel analisa dados históricos de turbidez da água coletados entre 2019 e 2021.</p>
    <p>Aplicamos uma <strong>regressão linear</strong> para prever quando os níveis de turbidez podem voltar a padrões <strong>excelentes</strong>.</p>
</div>
""", unsafe_allow_html=True)

# Seção de classificação das variáveis
st.markdown('<a name="classificacao-variaveis"></a>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">🧾 Estrutura do Dataset e Classificação das Variáveis</h2>', unsafe_allow_html=True)

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

st.dataframe(tabela_variaveis.style.background_gradient(cmap='Blues'), use_container_width=True)

st.markdown("""
<div class="feature-card">
    <h4>Legenda:</h4>
    <ul>
        <li><strong>Qualitativa nominal:</strong> categorias sem ordem definida (ex: período).</li>
        <li><strong>Qualitativa ordinal:</strong> categorias com ordem (ex: tempo).</li>
        <li><strong>Quantitativa contínua:</strong> números reais que admitem frações (ex: turbidez, ano decimal).</li>
    </ul>
</div>
""", unsafe_allow_html=True)

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
df = df.rename(columns={'solidos totais': 'sólidos totais'})

# === Pré-processamento ===
df = df.sort_values(by='data de amostragem')
df['ano_decimal'] = df['data de amostragem'].dt.year + (df['data de amostragem'].dt.dayofyear / 365)

# === NOVAS FUNÇÕES ===
def intervalo_previsao(X, y, modelo, alfa=0.05):
    """Calcula intervalo de previsão para regressão linear"""
    pred = modelo.predict(X)
    n = len(y)
    mse = np.sum((y - pred) ** 2) / (n - 2)
    h = np.diag(X @ np.linalg.pinv(X.T @ X) @ X.T)
    erro = np.sqrt(mse * (1 + h))
    t_val = t.ppf(1 - alfa/2, n-2)
    return pred - t_val * erro, pred + t_val * erro

def plot_residuos(y_real, y_pred):
    residuos = y_real - y_pred
    fig = px.scatter(x=y_pred, y=residuos,
                    labels={'x': 'Valores Preditos', 'y': 'Resíduos'},
                    title="Análise de Resíduos",
                    color_discrete_sequence=['#3498db'])
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    return fig

# === MODELAGEM AVANÇADA ===
st.markdown('<a name="modelos-previsao"></a>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">📈 Modelos de Previsão de Turbidez</h2>', unsafe_allow_html=True)

# Seleção do tipo de modelo
model_type = st.radio("Tipo de Modelo:", 
                     ["Linear", "Polinomial (Grau 2)"], 
                     horizontal=True)

# Preparar dados
df_modelo = df[['ano_decimal', 'turbidez']].dropna()
X = df_modelo[['ano_decimal']].values
y = df_modelo['turbidez'].values

# Ajustar modelo selecionado
if model_type == "Linear":
    modelo = LinearRegression()
    modelo.fit(X, y)
else:
    # Modelo polinomial
    modelo = make_pipeline(
        PolynomialFeatures(degree=2),
        LinearRegression()
    )
    modelo.fit(X, y)

# Previsão para anos futuros
anos_futuros = np.arange(2019, 2031, 0.1).reshape(-1, 1)
previsoes = modelo.predict(anos_futuros)

# Calcular intervalos de confiança
if model_type == "Linear":
    ic_lower, ic_upper = intervalo_previsao(X, y, modelo)
else:
    # Para modelo polinomial, usamos um intervalo simplificado
    ic_lower = previsoes - 1.96 * np.std(y - modelo.predict(X))
    ic_upper = previsoes + 1.96 * np.std(y - modelo.predict(X))

# Criar datas reais para eixo X
datas_futuras = pd.to_datetime([f"{int(a)}-01-01" for a in anos_futuros.flatten()])

# === Gráfico de Previsão ===
fig = go.Figure()

# Pontos reais
fig.add_trace(go.Scatter(
    x=df['data de amostragem'], 
    y=df['turbidez'],
    mode='markers', 
    name='Amostras', 
    marker=dict(color='#3498db', size=5)
))

# Linha de regressão
fig.add_trace(go.Scatter(
    x=datas_futuras, 
    y=previsoes,
    mode='lines', 
    name=f'Tendência ({model_type})', 
    line=dict(color='#e74c3c')
))

# Intervalo de confiança
fig.add_trace(go.Scatter(
    x=datas_futuras, 
    y=ic_lower,
    fill=None, 
    mode='lines', 
    line=dict(width=0),
    showlegend=False
))
fig.add_trace(go.Scatter(
    x=datas_futuras, 
    y=ic_upper,
    fill='tonexty', 
    mode='lines', 
    line=dict(width=0),
    name='Intervalo 95%',
    fillcolor='rgba(231, 76, 60, 0.2)'
))

# Linha padrão excelente
fig.add_hline(
    y=5, 
    line_dash="dash", 
    line_color="#2ecc71",
    annotation_text="Padrão Excelente (5 NTU)", 
    annotation_position="bottom right"
)

fig.update_layout(
    title="Turbidez da Água ao Longo do Tempo",
    xaxis_title="Data", 
    yaxis_title="Turbidez (NTU)",
    height=500,
    plot_bgcolor='rgba(240, 242, 246, 1)',
    paper_bgcolor='rgba(240, 242, 246, 1)'
)

st.plotly_chart(fig, use_container_width=True)

# === Previsão de retorno à qualidade excelente ===
ano_excelente = None
for ano, pred in zip(anos_futuros.flatten(), previsoes):
    if pred <= 5:
        ano_excelente = ano
        break

st.subheader("📈 Previsão com Base na Tendência Atual")

if ano_excelente:
    st.markdown(f"""
    <div class="success-box">
        ✅ A análise de regressão {model_type.lower()} prevê que a turbidez pode atingir o padrão excelente (<strong>≤ 5 NTU</strong>) 
        por volta de <strong>{int(ano_excelente)}</strong>.
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="warning-box">
        ⚠️ A projeção atual indica que os níveis de turbidez podem não atingir o padrão excelente até 2030.
    </div>
    """, unsafe_allow_html=True)

# === ANÁLISE DE RESÍDUOS ===
st.markdown('<a name="diagnostico-modelo"></a>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">🔍 Diagnóstico do Modelo</h2>', unsafe_allow_html=True)

y_pred = modelo.predict(X)
fig_resid = plot_residuos(y, y_pred)
st.plotly_chart(fig_resid, use_container_width=True)

# === ANÁLISE BINOMIAL ===
st.markdown('<a name="analise-binomial"></a>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">📊 Análise Binomial de Conformidade</h2>', unsafe_allow_html=True)

limite_turbidez = st.slider("Limite de Turbidez (NTU) para conformidade:", 
                           min_value=1.0, max_value=20.0, value=5.0, step=0.5)

df['conforme'] = df['turbidez'] <= limite_turbidez
conformidade_por_ano = df.groupby(df['data de amostragem'].dt.year)['conforme'].mean().reset_index()

fig_binom = px.bar(conformidade_por_ano, 
                  x='data de amostragem', 
                  y='conforme',
                  title=f"Proporção de Amostras Conforme (≤ {limite_turbidez} NTU)",
                  labels={'conforme': 'Proporção Conforme', 'data de amostragem': 'Ano'},
                  color_discrete_sequence=['#3498db'])
st.plotly_chart(fig_binom, use_container_width=True)

# Teste binomial
total_amostras = len(df['conforme'].dropna())
amostras_conformes = sum(df['conforme'].dropna())
result = binomtest(amostras_conformes, total_amostras, 0.95)  # H0: p=95% de conformidade

st.metric("Teste Binomial", 
         f"p-value = {result.pvalue:.4f}",
         help="H0: Proporção de amostras conforme = 95%")

# === CORRELAÇÃO ENTRE VARIÁVEIS ===
st.markdown('<a name="correlacao-variaveis"></a>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">🔗 Correlação entre Turbidez e Sólidos Totais</h2>', unsafe_allow_html=True)

if 'sólidos totais' in df.columns:
    df_corr = df[['turbidez', 'sólidos totais']].dropna()
    fig_corr = px.scatter(
        df_corr, 
        x='sólidos totais', 
        y='turbidez',
        trendline="ols",
        title="Relação entre Turbidez e Sólidos Totais",
        labels={'sólidos totais': 'Sólidos Totais (mg/L)', 'turbidez': 'Turbidez (NTU)'},
        color_discrete_sequence=['#3498db']
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Calcular coeficiente de correlação
    corr_coef = np.corrcoef(df_corr['sólidos totais'], df_corr['turbidez'])[0,1]
    st.metric("Coeficiente de Correlação de Pearson", f"{corr_coef:.2f}")

# === ANÁLISE POR ESTAÇÃO ===
st.markdown('<a name="analise-estacao"></a>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">🏞️ Análise por Estação de Monitoramento</h2>', unsafe_allow_html=True)

st.header("Mapa das estações de coleta")
st.image('assets/download.png', caption="Localização das estações de monitoramento")
st.markdown("""
<div class="feature-card">
    <p>Declararemos as estações RD074, RD075 e RD009 como estações de interesse para o nosso estudo, devido a sua proximidade a barragem rompida.</p>
</div>
""", unsafe_allow_html=True)

# Filtrar os dados para as estações de interesse e as demais
estacoes_interesse = ['RD074', 'RD075', 'RD009']
df_estacoes_interesse = df[df['estação'].isin(estacoes_interesse)]
df_outros = df[~df['estação'].isin(estacoes_interesse)]

# Gráfico para comparar sólidos totais nas estações de interesse com as demais
st.markdown('<h3 class="section-title">📊 Comparação dos Sólidos Totais nas Estações RD074, RD075, RD009 com as Demais</h3>', unsafe_allow_html=True)

# Criar o gráfico
fig_comparacao = go.Figure()

# Estações de interesse
fig_comparacao.add_trace(go.Box(
    y=df_estacoes_interesse['sólidos totais'],
    x=df_estacoes_interesse['estação'],
    name='Estações de Interesse (RD074, RD075, RD009)',
    boxmean='sd',
    marker=dict(color='#e67e22')
))

# Outras estações
fig_comparacao.add_trace(go.Box(
    y=df_outros['sólidos totais'],
    x=df_outros['estação'],
    name='Outras Estações',
    boxmean='sd',
    marker=dict(color='#3498db')
))

fig_comparacao.update_layout(
    title="Distribuição dos Sólidos Totais por Estação",
    xaxis_title="Estação",
    yaxis_title="Sólidos Totais (mg/L)",
    height=500,
    plot_bgcolor='rgba(240, 242, 246, 1)',
    paper_bgcolor='rgba(240, 242, 246, 1)'
)

st.plotly_chart(fig_comparacao, use_container_width=True)

# === Análise estatística (Intervalos de Confiança e Teste T) ===
def intervalo_confianca(data, confidence=0.95):
    n = len(data)
    mean = np.mean(data)
    sem = stats.sem(data)
    margin_of_error = sem * t.ppf((1 + confidence) / 2., n-1)
    return mean - margin_of_error, mean + margin_of_error, mean

# Intervalo de confiança para as estações de interesse
ic_interesse_lower, ic_interesse_upper, mean_interesse = intervalo_confianca(df_estacoes_interesse['sólidos totais'])

# Intervalo de confiança para as outras estações
ic_outros_lower, ic_outros_upper, mean_outros = intervalo_confianca(df_outros['sólidos totais'])

# Exibir intervalos de confiança
st.subheader("📊 Intervalo de Confiança para a Média de Sólidos Totais")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h4>Estacões de Interesse (RD074, RD075, RD009):</h4>
        <p>Média: {:.2f} mg/L</p>
        <p>Intervalo de Confiança (95%): ({:.2f}, {:.2f}) mg/L</p>
    </div>
    """.format(mean_interesse, ic_interesse_lower, ic_interesse_upper), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h4>Outras Estações:</h4>
        <p>Média: {:.2f} mg/L</p>
        <p>Intervalo de Confiança (95%): ({:.2f}, {:.2f}) mg/L</p>
    </div>
    """.format(mean_outros, ic_outros_lower, ic_outros_upper), unsafe_allow_html=True)

# Teste t para comparação de médias
t_stat, p_value = stats.ttest_ind(df_estacoes_interesse['sólidos totais'].dropna(), df_outros['sólidos totais'].dropna())

st.subheader("🔬 Teste T para Comparação de Médias")
st.metric("Estatística t", f"{t_stat:.2f}")
st.metric("Valor p", f"{p_value:.4f}")

if p_value < 0.05:
    st.markdown("""
    <div class="success-box">
        📉 Existe uma diferença estatisticamente significativa entre os sólidos totais das estações de interesse (RD074, RD075, RD009) e as demais.
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="warning-box">
        📈 Não existe uma diferença estatisticamente significativa entre os sólidos totais das estações de interesse e as demais.
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="feature-card">
    <p>Nota-se que, atuando com um intervalo de confiança de 95%, as médias dos sólidos totais presentes nas amostras coletadas pelas estações de interesse ainda são quase metade dos valores comparáveis coletados nas demais estações.</p>
    <p>Isso pode evidenciar uma maior preocupação com a remoção dos dejetos no local de rompimento da barragem.</p>
</div>
""", unsafe_allow_html=True)

# Âncora e título da seção
st.markdown('<a name="teste-hipotese"></a>', unsafe_allow_html=True)
st.header("🔬 Teste de Hipótese: Turbidez > Padrão Excelente")

# Hipóteses com container destacado
with st.container():
    st.subheader("Formulação das Hipóteses")
    st.markdown("""
    **H₀ (Hipótese Nula):** A turbidez média é igual a 5 NTU (padrão excelente)  
    **H₁ (Hipótese Alternativa):** A turbidez média é maior que 5 NTU  
    *Teste unicaudal à direita com α = 0.05*
    """)
    st.markdown("---")

# Realizar o teste t (cálculos permanecem iguais)
turbidez_data = df['turbidez'].dropna()
t_stat, p_value = stats.ttest_1samp(turbidez_data, 5, alternative='greater')
ic_lower, ic_upper = stats.t.interval(0.95, len(turbidez_data)-1, 
                   loc=np.mean(turbidez_data), 
                   scale=stats.sem(turbidez_data))

# Métricas em colunas
cols = st.columns(3)
cols[0].metric("Média Observada", f"{np.mean(turbidez_data):.2f} NTU")
cols[1].metric("Estatística t", f"{t_stat:.3f}")
cols[2].metric("Valor p", f"{p_value:.4f}")

# Intervalo de Confiança
st.subheader("Intervalo de Confiança 95%")
st.write(f"{ic_lower:.2f} NTU ≤ μ ≤ {ic_upper:.2f} NTU")

# Conclusão do teste
st.subheader("Ponderação e Conclusão")
st.write("**Análise do valor-p:**")
st.markdown(f"""
- O valor-p obtido ({p_value:.4f}) é {'menor' if p_value < 0.05 else 'maior'} que o nível de significância α = 0.05
- Isso indica que há {'evidências suficientes' if p_value < 0.05 else 'evidências insuficientes'} para rejeitar a hipótese nula
""")

st.write("**Interpretação prática:**")
st.markdown(f"""
- A turbidez média observada ({np.mean(turbidez_data):.2f} NTU) está {'significativamente acima' if p_value < 0.05 else 'dentro do esperado'} do padrão excelente (5 NTU)
- O intervalo de confiança não inclui o valor de referência (5 NTU), reforçando a {'presença' if p_value < 0.05 else 'ausência'} de impacto significativo
""")

# Caixa de conclusão condicional
if p_value < 0.05:
    st.success(f"**Conclusão final:** Rejeitamos H₀ - há evidências estatísticas de que a turbidez permanece acima do padrão excelente.")
else:
    st.warning(f"**Conclusão final:** Não rejeitamos H₀ - há evidências insuficientes de que a turbidez permanece acima do padrão excelente.")