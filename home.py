import streamlit as st
import pandas as pd
import numpy as np
from scripts import *
# from streamlit_extras.app_logo import add_logo

# Configuração da página
st.set_page_config(page_title="Home", layout="wide")
st.title("Análise sobre o desastre ambiental de Mariana (MG)")
st.write("Em 2015, o Brasil presenciou um dos maiores desastres ambientais da sua história: o rompimento da barragem de Fundão, em Mariana (MG). O impacto causado pelo vazamento de rejeitos de mineração devastou ecossistemas, afetou comunidades ribeirinhas e comprometeu a qualidade da água em diversos rios da bacia do Rio Doce.")
st.write("Por meio de uma análise clara, baseada em dados sobre a qualidade da água nos anos seguintes ao desastre, buscamos oferecer uma visão aprofundada sobre as transformações ambientais ocorridas ao longo do tempo.")
st.image("assets\imagem1.jpg")
st.divider()
st.header("O que você encontrará aqui")
col1, col2 = st.columns(2)
with col1:
    st.write('📊 Visualizações Interativas: gráficos e mapas que mostram a evolução de indicadores como turbidez, metais pesados, pH, oxigênio dissolvido, entre outros.')
    st.write("⌚ Comparações Temporais: análise dos dados antes e depois do rompimento da barragem.")
    st.write("🌱 Impactos Ambientais: avaliação das consequências para o ecossistema aquático.")
    
st.divider()
st.header("Por que isso importa?")    
st.write("Entender os efeitos de um desastre dessa magnitude é fundamental para prevenir novos acidentes, cobrar responsabilidade e promover políticas públicas mais eficazes. Este projeto é uma contribuição para a transparência e o acesso à informação ambiental.")
st.divider()
st.header("Sobre a tragédia")
st.write("Em 5 de novembro de 2015, o Brasil foi palco de um dos maiores desastres ambientais da sua história. Na cidade de Mariana, em Minas Gerais, a barragem de Fundão, pertencente à mineradora Samarco – uma joint venture entre a Vale e a BHP Billiton – se rompeu, liberando cerca de 39 milhões de metros cúbicos de rejeitos de mineração. A lama tóxica devastou o distrito de Bento Rodrigues, arrasando casas, destruindo a vegetação, contaminando rios e ceifando vidas.")
st.write("Dezenove pessoas morreram na tragédia, entre moradores e trabalhadores da mineradora. Comunidades inteiras foram desfeitas, e a lama percorreu mais de 600 quilômetros, atingindo o rio Doce e chegando até o oceano Atlântico no Espírito Santo, deixando um rastro de destruição por onde passou. A biodiversidade da região foi profundamente afetada, e milhares de pessoas perderam suas fontes de renda e acesso à água potável.")
st.write("Além do impacto ambiental e humano, a tragédia escancarou falhas na fiscalização e nos sistemas de segurança de barragens no Brasil. O rompimento gerou indignação nacional e internacional, levantando debates sobre a responsabilidade socioambiental das mineradoras e a eficácia das leis ambientais brasileiras.")
st.write("Mesmo anos após o desastre, os impactos ainda são sentidos. Muitas famílias seguem esperando por indenizações e reassentamentos definitivos. A tragédia de Mariana tornou-se um símbolo da luta por justiça ambiental no país e marcou profundamente a relação entre mineração e meio ambiente no Brasil.")
st.image("assets\imagem2.png")
st.divider()
st.header("Tópicos e perguntas discutidas nesse estudo")
st.subheader("❓ 1. Qual foi o impacto da lama tóxica na turbidez da água?")
st.subheader("❓ 2. O número de dejetos sólidos está diminuindo ao longo do tempo?")
st.subheader("❓ 3. Como a qualidade da água mudou ao longo do tempo?")


