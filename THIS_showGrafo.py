import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Leer el archivo CSV
df = pd.read_csv('tester2.csv')

# Crear un grafo vacío
G = nx.Graph()
G2 = nx.Graph()

# Iterar sobre las filas del DataFrame
for _, row in df.iterrows():
    lugar = row['lugar']
    nodo1 = row['nodo1']
    nodo2 = row['nodo2']
    peso = row['peso']

    # Agregar nodos al grafo
    G2.add_node(lugar)
    #G.add_node(lugar)

    # Agregar arista al grafo
    G.add_edge(nodo1, nodo2, weight=peso)

# Obtener los lugares presentes en el grafo
lugares = list(G.nodes())
lugares2 = list(G2.nodes())

# Mostrar los lugares
print("Lugares presentes en el grafo:")
for lugar in lugares2:
    print(lugar)

# Graficar el grafo
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G)  # Obtener la posición de los nodos
node_labels = {node: node for node in G.nodes()}  # Etiquetas de los nodos
nx.draw_networkx(G, pos, labels=node_labels, with_labels=False, node_size=300, font_size=10)
nx.draw_networkx_edges(G, pos, width=2, edge_color='r')
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
plt.title("Grafo de accidentes")
plt.axis("off")
plt.show()

