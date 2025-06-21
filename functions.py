import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import osmnx as ox

import config

def add_css_and_plots(css_file, html_file):
    with open(css_file, "r", encoding="utf-8") as f:
        css = f.read()

    custom_css = f"<style>{css}</style>"

    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace("</head>", custom_css + "</head>")

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)

    html = html.replace("<body>", "<body><div class='graph'>")
    html = html.replace("</body>", "</div></body>")

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)  

def generate_graph(physics=True): #Cria o grafo
    #Gerar o grafo

    place = "Lagoa Nova, Natal, Rio grande do Norte"

    G_ox = ox.graph_from_place(place, network_type="drive") # Renamed to avoid conflict

    #Remover geometria do osmnx
    for u, v, data in G_ox.edges(data=True):
        if 'geometry' in data:
            del data['geometry']

    #Osmnx para pyvis
    G = Network(height='750px', width='100%', bgcolor='#222222', font_color='white', notebook=True)
    G.from_nx(G_ox)

    # Fisica
    if physics:
        G.show_buttons(filter_=['physics'])
    G.show('test.html', notebook=True) # Added notebook=True for Colab compatibility


    add_css_and_plots(config.css_file, config.html_file)

