import networkx as nx
from pyvis.network import Network
import pandas as pd

import config


G_nx = nx.Graph()

def generate_graph(tipo="completo", physics=True, selected_groups=None): #Cria o grafo
    #Gerar o grafo

    global G_nx
    G_nx.clear()

    df_nodes = pd.read_csv('dataset/stack_network_nodes.csv')
    df_edges = pd.read_csv('dataset/stack_network_links.csv')

    # color_map = {
    #     1:'#f09494', 2:'#eebcbc', 3:'#72bbd0', 4:'#91f0a1', 5:'#629fff', 6:'#bcc2f2',  
    #     7:'#eebcbc', 8:'#f1f0c0', 9:'#d2ffe7', 10:'#caf3a6', 11:'#ffdf55', 12:'#ef77aa', 
    #     13:'#d6dcff', 14:'#d2f5f0'
    # }

    if selected_groups is not None:
        df_nodes = df_nodes[df_nodes['group'].isin(selected_groups)]
        nomes_validos = set(df_nodes['name'])
        df_edges = df_edges[
            df_edges['source'].isin(nomes_validos) & df_edges['target'].isin(nomes_validos)
        ]


    def normalize(value, min_size=10, max_size=150):
        if tipo == "alto_grau":
            min_size = 40
            max_size = 50
        return min_size + (max_size - min_size) * value
    
    
    for _, row in df_nodes.iterrows():
        G_nx.add_node(row['name'], group=row['group'])

    for _, row in df_edges.iterrows():
        G_nx.add_edge(row['source'], row['target'], weight=row['value'])
    

    if tipo == "maior_componente":
        largest_cc = max(nx.connected_components(G_nx), key=len)
        G_nx = G_nx.subgraph(largest_cc).copy()
    elif tipo == "alto_grau":
        graus = dict(G_nx.degree())
        limiar = sorted(graus.values(), reverse=True)[int(len(graus)*0.1)]  # top 10%
        selecionados = [n for n, g in graus.items() if g >= limiar]
        G_nx = G_nx.subgraph(selecionados).copy()


    centrality = nx.degree_centrality(G_nx)

    G = Network(height='750px', width='100%', bgcolor='#222222', font_color='white', notebook=True)

    for node in G_nx.nodes(data=True):
        name = node[0]
        group = node[1].get('group', 1)
        color = config.color_map.get(group, "#FFFFFF")
        size = normalize(centrality.get(name, 0))
        G.add_node(name, label=name, title=group, color=color, size=size)
        title = f"{name}<br>Grupo: {group}"

        G.add_node(
        name, 
        label=name, 
        title=title, 
        color=color, 
        size=size,
        font={"size": 14}
        )

    for source, target, data in G_nx.edges(data=True):
        G.add_edge(source, target, value=data.get('weight', 1))

    # Fisica
    if physics:
        G.show_buttons(filter_=['physics'])
        G.barnes_hut(gravity=-8000, central_gravity=0.3, spring_length=150)

    G.write_html(config.html_file, notebook=False)


def calc_metrics(G_nx):
    metricas = {}

    # Densidade 
    densidade = nx.density(G_nx)
    metricas["Densidade"] = densidade
    metricas["Esparsidade"] = 1 - densidade

    # Assortatividade (baseada em grau)
    try:
        metricas["Assortatividade (grau)"] = nx.degree_assortativity_coefficient(G_nx)
    except Exception:
        metricas["Assortatividade (grau)"] = "Não foi possível calcular"

    # Clustering global
    metricas["Coeficiente de Clustering"] = nx.average_clustering(G_nx)

    # 4 e 5. Componentes Conectados
    if G_nx.is_directed():
        metricas["Componentes Fortemente Conectados"] = nx.number_strongly_connected_components(G_nx)
        metricas["Componentes Fracamente Conectados"] = nx.number_weakly_connected_components(G_nx)
    else:
        # Para grafos não dirigidos
        metricas["Componentes Conectados"] = nx.number_connected_components(G_nx)

    return metricas

def calc_cent(G_nx):
    try:
        eig = nx.eigenvector_centrality(G_nx)
    except:
        eig = {n: 0 for n in G_nx.nodes()}  # fallback caso não converja

    degree = nx.degree_centrality(G_nx)
    closeness = nx.closeness_centrality(G_nx)
    betweenness = nx.betweenness_centrality(G_nx)

    return {
        "Eigenvector": eig,
        "Degree": degree,
        "Closeness": closeness,
        "Betweenness": betweenness
    }

def get_G():
    global G_nx
    return G_nx