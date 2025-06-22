import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

from show_functions import show_graph_metrics, plot_hist, show_top_cent
from graph_functions import generate_graph, calc_cent, get_G
import config


st.set_page_config(page_title="Visualização de Grafos", layout="wide")
st.title("Stack Overflow Tag Network")
st.subheader("Visualização Interativa de Redes")

tipo = st.selectbox(
    "Subconjunto do grafo:",
    options=["completo", "maior_componente", "alto_grau"],
    format_func=lambda x: {
        "completo": "Grafo completo",
        "maior_componente": "Maior componente conectado",
        "alto_grau": "Top 10% por grau"
    }[x]
)

df_nodes = pd.read_csv("dataset/stack_network_nodes.csv")
grupos_disponiveis = sorted(df_nodes["group"].unique())


groups = st.multiselect(
    "Filtrar por grupo(s) (opcional):",
    options=grupos_disponiveis,
    default=grupos_disponiveis,
    help="Selecione os grupos de nós que deseja visualizar"
)


generate_graph(tipo=tipo, selected_groups=groups)

with open(config.html_file, "r", encoding="utf-8") as f:
    html_content = f.read()

components.html(html_content, height=1300, width=1300)

G = get_G()

show_graph_metrics(G)

st.subheader("Distribuição de Grau dos Nós")
plot_hist(G)

cents = calc_cent(G)
show_top_cent(cents)