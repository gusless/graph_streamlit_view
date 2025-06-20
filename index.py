import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

css_file = "style.css"
html_file = "test.html"

def main():
    global html_file
    global css_file

    HtmlFile = open(html_file, 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 900, width=900)
    graph()

def modify_css(css_file, html_file):
    with open(css_file, "r", encoding="utf-8") as f:
        css = f.read()

    custom_css = f"<style>{css}</style>"

    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace("</head>", custom_css + "</head>")

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)


def graph(physics=True): #Cria o grafo

    nx_graph = nx.cycle_graph(10)
    nx_graph.nodes[1]['title'] = 'Number 1'
    nx_graph.nodes[1]['group'] = 1
    nx_graph.nodes[3]['title'] = 'I belong to a different group!'
    nx_graph.nodes[3]['group'] = 10
    nx_graph.add_node(20, size=20, title='couple', group=2)
    nx_graph.add_node(21, size=15, title='couple', group=2)
    nx_graph.add_edge(20, 21, weight=5)
    nx_graph.add_node(25, size=25, label='lonely', title='lonely node', group=3)


    nt = Network("500px", "500px", notebook=True, heading='')
    nt.from_nx(nx_graph)

    #Physics interactivity
    if physics:
        nt.show_buttons(filter_=['physics'])

    global html_file
    global css_file

    nt.save_graph(html_file)
    modify_css(css_file, html_file)    

main()