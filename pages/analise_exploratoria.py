import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import scipy.stats as stats
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

if "data" not in st.session_state:
    df12020 = pd.read_excel("dados/primeirosemestre2020.xlsx")
    df22020 = pd.read_excel("dados/segundosemestre2020.xls")
    df2021 = pd.read_excel("dados/ano2021.xlsx")
    df2019 = pd.read_excel("dados/seriehistorica2019.xlsx")

    # Se quiser salvar em session_state para uso futuro
    st.session_state.data = {
        "2020_1": df12020,
        "2020_2": df22020,
        "2021": df2021,
        "2019": df2019,
    }

st.title("Análise Exploratória")
st.write("Nessa página você pode interagir diretamente com a base de dados")
st.dataframe(st.session_state.data["2020_1"])
st.dataframe(st)
