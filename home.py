import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scripts import *

# Configuração da página
st.set_page_config(
    page_title="Mariana - Análise Ambiental",
    layout="wide",
    page_icon="🌊",
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
</style>
""", unsafe_allow_html=True)

# Barra lateral
with st.sidebar:
    st.title("Navegação")
    st.markdown("- [Visão Geral](#visao-geral)")
    st.markdown("- [Recursos](#recursos)")
    st.markdown("- [Importância](#importancia)")
    st.markdown("- [Sobre a Tragédia](#sobre-a-tragedia)")
    st.markdown("- [Perguntas Chave](#perguntas-chave)")
    
    st.divider()
    st.markdown("Desenvolvido por:")
    st.write("- Rafael Nascimento")
    st.write("- Iago Diniz")
    st.write("- Pedro Henrique")
    st.write("- Luis Alberto")
    st.markdown("Equipe de Análise de Dados Ambientais")
    st.markdown("Última atualização: Maio 2025")

# Conteúdo principal
st.markdown('<h1 class="header-text">Análise do Desastre Ambiental de Mariana (MG)</h1>', unsafe_allow_html=True)

# Seção de introdução
# Seção de introdução - Versão Ampliada
st.markdown('<a name="visao-geral"></a>', unsafe_allow_html=True)
col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("""
    <div style="text-align: justify;">
    Em <strong>5 de novembro de 2015</strong>, o Brasil foi sacudido por uma das maiores tragédias socioambientais de sua história: 
    o rompimento da barragem de Fundão, em Mariana (MG), controlada pela Samarco (joint-venture entre Vale e BHP Billiton). 
    Em questão de horas, <strong>39 milhões de metros cúbicos</strong> de rejeitos de mineração - volume equivalente a 
    15 mil piscinas olímpicas - varreram comunidades inteiras e percorreram mais de <strong>600km</strong> até o oceano Atlântico.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: justify; margin-top: 1rem;">
    O impacto foi catastrófico:
    <ul>
        <li><strong>19 vidas perdidas</strong> no distrito de Bento Rodrigues</li>
        <li><strong>1.469 hectares</strong> de vegetação destruídos</li>
        <li><strong>663 km</strong> de cursos d'água afetados</li>
        <li>Prejuízos ambientais estimados em <strong>R$ 20 bilhões</strong></li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: justify; margin-top: 1rem;">
    Este painel analítico apresenta um <strong>estudo longitudinal</strong> baseado em dados oficiais coletados entre 2019-2021, 
    revelando como os parâmetros de qualidade da água evoluíram após o desastre. Através de metodologias estatísticas robustas, 
    buscamos responder questões críticas sobre:
    <ul>
        <li>Padrões de recuperação ambiental</li>
        <li>Eficácia das medidas de reparação</li>
        <li>Persistência de contaminantes</li>
        <li>Variações geográficas nos impactos</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.image("assets/imagem1.jpg", 
             caption="Vista aérea do rompimento da barragem de Fundão - Fonte: IBAMA (2015)", 
             use_container_width=True)
    st.markdown("""
<div style="; padding: 15px; border-radius: 10px; margin-top: 10px;">
<strong>📌 Destaque:</strong> A lama de rejeitos levou apenas 
<strong>4 dias</strong> para atingir o oceano, contaminando toda a bacia do Rio Doce com:
<ul>
    <li>Metais pesados (arsênio, chumbo, mercúrio)</li>
    <li>Partículas em suspensão</li>
    <li>Alterações drásticas de pH</li>
</ul>
</div>
""", unsafe_allow_html=True)
st.divider()

# Seção de recursos
st.markdown('<a name="recursos"></a>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">O que você encontrará aqui</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    with st.container():
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Visualizações Interativas")
        st.markdown("Gráficos e mapas que mostram a evolução de indicadores como:")
        st.markdown("- Turbidez da água")
        st.markdown("- Concentração de metais pesados")
        st.markdown("- Níveis de pH e oxigênio dissolvido")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with st.container():
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### ⌚ Análise Temporal")
        st.markdown("Comparação dos dados antes e depois do rompimento:")
        st.markdown("- Evolução dos parâmetros de qualidade")
        st.markdown("- Taxas de recuperação ambiental")
        st.markdown("- Impactos de longo prazo")
        st.markdown("</div>", unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🌱 Impactos Ambientais")
        st.markdown("Avaliação das consequências para:")
        st.markdown("- Ecossistemas aquáticos")
        st.markdown("- Biodiversidade local")
        st.markdown("- Qualidade do solo")
        st.markdown("- Comunidades ribeirinhas")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with st.container():
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🔍 Análises Estatísticas")
        st.markdown("Métodos científicos aplicados:")
        st.markdown("- Modelos de regressão")
        st.markdown("- Testes de hipóteses")
        st.markdown("- Intervalos de confiança")
        st.markdown("- Análise de tendências")
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# Seção de importância
st.markdown('<a name="importancia"></a>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Por que essa análise é importante?</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="feature-card">
<div style="text-align: justify;">

**Entender os efeitos de um desastre dessa magnitude** é fundamental para:

1. **Prevenir novos acidentes** através da identificação de falhas nos sistemas de monitoramento
2. **Cobrar responsabilidades** com base em evidências científicas sólidas
3. **Promover políticas públicas** mais eficazes para proteção ambiental
4. **Acompanhar a recuperação** dos ecossistemas afetados

Este projeto representa uma contribuição valiosa para a **transparência** e o **acesso à informação ambiental**, elementos essenciais para a justiça socioambiental.
</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# Seção sobre a tragédia
st.markdown('<a name="sobre-a-tragedia"></a>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Sobre a Tragédia</h2>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 3])
with col1:
    st.image("assets/imagem2.png", caption="Localização da barragem de Fundão e área afetada", use_container_width=True)

with col2:
    st.markdown("""
    <div style="text-align: justify;">
    Em <strong>5 de novembro de 2015</strong>, a barragem de Fundão, pertencente à mineradora Samarco (joint venture entre Vale e BHP Billiton), se rompeu liberando uma onda de rejeitos que:
    
    - **Destruiu completamente** o distrito de Bento Rodrigues
    - **Matou 19 pessoas** (trabalhadores e moradores)
    - **Percorreu 600km** até o oceano Atlântico
    - **Afetou 39 municípios** em MG e ES
    
    A biodiversidade da região foi profundamente impactada, com:
    - Contaminação de rios e solos
    - Perda de habitats naturais
    - Mortandade de espécies aquáticas
    
    Mesmo anos após o desastre, <strong>muitas famílias ainda aguardam</strong> indenizações e reassentamentos definitivos.
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Seção de perguntas
st.markdown('<a name="perguntas-chave"></a>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Perguntas-Chave Respondidas</h2>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.markdown("### ❓ Qual foi o impacto da lama tóxica na turbidez da água?")
    st.markdown("""
    - Análise da evolução dos níveis de turbidez
    - Comparação com padrões de qualidade
    - Projeções de recuperação ambiental
    """)
    st.markdown("</div>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.markdown("### ❓ Como os sólidos totais se comportaram após o desastre?")
    st.markdown("""
    - Distribuição espacial dos contaminantes
    - Variação temporal das concentrações
    - Diferenças entre estações de monitoramento
    """)
    st.markdown("</div>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.markdown("### ❓ A qualidade da água mostra sinais de recuperação?")
    st.markdown("""
    - Análise de tendências de longo prazo
    - Comparação entre parâmetros físicos e químicos
    - Avaliação da eficácia das medidas de reparação
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# Rodapé
st.divider()
st.markdown("""
<div style="text-align: center; color: #7f8c8d; font-size: 0.9rem;">
    Este projeto foi desenvolvido para fins acadêmicos e de pesquisa.<br>
    Dados coletados de fontes oficiais entre 2019-2021.<br>
</div>
""", unsafe_allow_html=True)