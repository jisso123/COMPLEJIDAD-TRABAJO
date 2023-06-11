import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Leer el archivo CSV
df = pd.read_csv('tester2.csv')

# Crear un grafo vacío
G = nx.Graph()

# Mapear los nombres de los lugares a identificadores únicos
lugar_id_map = {}
lugar_counter = 1

# Iterar sobre las filas del DataFrame
for _, row in df.iterrows():
    lugar = row['lugar']
    nodo1 = f"L{lugar_counter}"
    nodo2 = f"L{lugar_counter+1}"
    peso = row['peso']

    # Agregar nodos al grafo y asignar el atributo 'lugar'
    G.add_node(nodo1, lugar=lugar)
    G.add_node(nodo2, lugar=lugar)

    # Agregar arista al grafo
    G.add_edge(nodo1, nodo2, weight=peso)

    # Actualizar el mapeo de nombres de lugares a identificadores
    if lugar not in lugar_id_map:
        lugar_id_map[lugar] = nodo1
        lugar_counter += 1
    lugar_id_map[lugar] = nodo2

# Obtener los lugares presentes en el grafo
lugares = list(lugar_id_map.keys())

print("Lugares presentes en el grafo:")
for lugar in lugares:
    print(lugar)

# Obtener puntos de origen y destino desde el usuario
origen = input("Ingrese el punto de origen: ")
destino = input("Ingrese el punto de destino: ")

# Verificar si los puntos ingresados existen en el grafo
if origen not in lugares or destino not in lugares:
    print("Al menos uno de los puntos ingresados no existe en el grafo.")
else:
    # Obtener los identificadores de los lugares de origen y destino
    origen_id = lugar_id_map[origen]
    destino_id = lugar_id_map[destino]

    # Calcular el camino más corto utilizando el algoritmo de Dijkstra
    shortest_path = nx.dijkstra_path(G, origen_id, destino_id)

    # Obtener los nombres de los lugares en el camino más corto
    nombre_camino = [G.nodes[nodo]['lugar'] for nodo in shortest_path]

    # Graficar el grafo con el camino más corto resaltado
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)  # Obtener la posición de los nodos
    nx.draw_networkx(G, pos, with_labels=True, node_size=500, font_size=10)
    nx.draw_networkx_edges(G, pos, width=2, edge_color='r')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))

    # Resaltar el camino más corto
    path_edges = [(shortest_path[i], shortest_path[i+1]) for i in range(len(shortest_path)-1)]
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=2, edge_color='g')

    plt.title("Grafo de accidentes con el camino más corto")
    plt.axis("off")
    plt.show()

    # Imprimir el camino más corto
    print("Camino más corto de {} a {}: {}".format(origen, destino, nombre_camino))
