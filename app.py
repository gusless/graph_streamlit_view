import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import osmnx as ox

from functions import generate_graph
import config

HtmlFile = open(config.html_file, 'r', encoding='utf-8')
source_code = HtmlFile.read() 
components.html(source_code, height = 900, width=900)

generate_graph()

# st.markdown("<div class=\"analysis\"", unsafe_allow_html=True)

# # adicionar os graficos, etc

# st.markdown("</div>", unsafe_allow_html=True)


