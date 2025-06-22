import streamlit as st
import pandas as pd
import plotly.express as px
import networkx as nx

def show_graph_metrics(G_nx):
    st.subheader("Métricas Globais do Grafo")

    # Calcular métricas
    densidade = nx.density(G_nx)
    esparsidade = 1 - densidade
    clustering = nx.average_clustering(G_nx.to_undirected())
    assort = nx.degree_assortativity_coefficient(G_nx)
    num_componentes = int(nx.number_connected_components(G_nx)) if not G_nx.is_directed() else None
    scc = list(nx.strongly_connected_components(G_nx)) if G_nx.is_directed() else None
    wcc = list(nx.weakly_connected_components(G_nx)) if G_nx.is_directed() else None

    col1, col2 = st.columns(2)

    # Cartão estilizado
    def card(title, value, text):
        return f"""
        <div style='padding: 15px; background-color: #1e1e1e; border-radius: 10px;
                    border: 1px solid #444; margin-bottom: 20px'>
            <h5 style='color: #ffd700; margin-top: 0'>{title}</h5>
            <div style='font-size: 24px; color: white; font-weight: bold'>{value:.4f}</div>
            <div style='color: #aaa; font-size: 14px; margin-top: 5px'>{text}</div>
        </div>
        """

    col1.markdown(card("Densidade", densidade, "Proporção de conexões existentes no grafo"), unsafe_allow_html=True)
    col2.markdown(card("Esparsidade", esparsidade, "Proporção de conexões ausentes no grafo"), unsafe_allow_html=True)
    col1.markdown(card("Assortatividade", assort, "Correlação entre graus dos nós conectados"), unsafe_allow_html=True)
    col2.markdown(card("Clustering Médio", clustering, "Probabilidade de dois vizinhos de um nó estarem conectados"), unsafe_allow_html=True)

    if not G_nx.is_directed():
        col1.markdown(card("Componentes Conectados", num_componentes, "Número de componentes independentes"), unsafe_allow_html=True)
    else:
        col1.markdown(card("Componentes Fortemente Conectados", len(scc), "Subconjuntos fortemente interconectados"), unsafe_allow_html=True)
        col2.markdown(card("Componentes Fracamente Conectados", len(wcc), "Conectividade ignorando direção"), unsafe_allow_html=True)

    with st.expander("Explicações das métricas"):
        st.markdown("""
        - **Densidade**: mede o quão conectado o grafo está em relação ao número máximo possível de conexões. Valores próximos de 1 indicam uma rede densa; próximos de 0, uma rede esparsa.
        - **Assortatividade**: indica se os nós tendem a se conectar com outros de grau semelhante. Valores positivos indicam essa tendência; negativos indicam o oposto.
        - **Coeficiente de Clustering**: mede a tendência de formação de triângulos (grupos fechados de 3 nós). Quanto maior, mais a rede tende a formar comunidades.
        - **Componentes Conectados**:
            - Em **grafos dirigidos**, temos:
                - **Fortemente conectados**: grupos onde cada nó pode alcançar todos os outros seguindo as direções.
                - **Fracamente conectados**: grupos conectados se ignorarmos as direções das arestas.
            - Em **grafos não dirigidos**, usamos apenas "Componentes Conectados".
        """)

def show_top_cent(cents):
    st.subheader("Nós mais centrais por métrica")

    col1, col2 = st.columns(2)

    for idx, (nome, c) in enumerate(cents.items()):
        top = sorted(c.items(), key=lambda x: x[1], reverse=True)[:10]

        bloco = ""
        for n, v in top:
            bloco += f"<div style='margin-bottom:4px'><b>{n}</b>: {v:.4f}</div>"

        estilo = f"""
            <div style='padding: 15px; background-color: #1e1e1e; border-radius: 10px;
                        border: 1px solid #444; margin-bottom: 20px'>
                <h5 style='color: #ffd700; margin-top: 0'>{nome} Centrality</h5>
                {bloco}
            </div>
        """

        if idx % 2 == 0:
            col1.markdown(estilo, unsafe_allow_html=True)
        else:
            col2.markdown(estilo, unsafe_allow_html=True)

def plot_hist(G_nx):

    if G_nx.is_directed():
        graus_in = [G_nx.in_degree(n) for n in G_nx.nodes()]
        graus_out = [G_nx.out_degree(n) for n in G_nx.nodes()]

        df_in = pd.DataFrame(graus_in, columns=['grau'])
        df_out = pd.DataFrame(graus_out, columns=['grau'])

        st.markdown("**In-degree**")
        fig_in = px.histogram(df_in, x='grau', nbins=20, title="Distribuição de In-degree",
                              labels={"grau": "Grau"}, color_discrete_sequence=["#56cc9d"])
        st.plotly_chart(fig_in, use_container_width=True)

        st.markdown("**Out-degree**")
        fig_out = px.histogram(df_out, x='grau', nbins=20, title="Distribuição de Out-degree",
                               labels={"grau": "Grau"}, color_discrete_sequence=["#ff6f61"])
        st.plotly_chart(fig_out, use_container_width=True)

    else:
        graus = [G_nx.degree(n) for n in G_nx.nodes()]
        df = pd.DataFrame(graus, columns=['grau'])
        fig = px.histogram(df, x='grau', nbins=20, title="Distribuição de Grau Total",
                           labels={"grau": "Grau"}, color_discrete_sequence=["#5b8def"])
        st.plotly_chart(fig, use_container_width=True)