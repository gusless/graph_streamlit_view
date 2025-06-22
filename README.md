# Visualização de Grafos do Stack Overflow

Este projeto é uma aplicação interativa feita com **Streamlit** para explorar redes de tags do Stack Overflow. Utiliza bibliotecas como **NetworkX**, **Pyvis**, **Plotly** e **Pandas** para análise e visualização.

## Deploy

[Visualização hospedada pelo Streamlit Cloud](https://graphview-stack-overflow.streamlit.app)

## Funcionalidades

- Visualização interativa de redes (grafo completo, maior componente, top 10% por grau)
- Filtros por grupos temáticos de tags
- Métricas da rede:
  - Densidade / Esparsidade
  - Assortatividade
  - Clustering
  - Componentes conectados
- Distribuição de grau dos nós (histograma)
- Centralidades:
  - Eigenvector
  - Degree
  - Closeness
  - Betweenness

## Como rodar

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Execute o Streamlit:

```bash
streamlit run app.py
```
