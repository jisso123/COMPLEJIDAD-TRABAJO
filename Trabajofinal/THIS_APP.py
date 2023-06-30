import pandas as pd
import networkx as nx
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Leer el archivo CSV
df = pd.read_csv('tester2.csv')

# Crear un grafo vacío
G = nx.Graph()

# Crear un diccionario para mapear nombres de lugares a nodos
lugares_nodos = {}

# Iterar sobre las filas del DataFrame
for _, row in df.iterrows():
    lugar = row['lugar']
    nodo1 = row['nodo1']
    nodo2 = row['nodo2']
    peso = row['peso']

    # Agregar nodos al grafo
    G.add_node(nodo1, lugar=lugar)
    G.add_node(nodo2, lugar=lugar)

    # Agregar arista al grafo
    G.add_edge(nodo1, nodo2, weight=peso)

    # Actualizar el diccionario lugares_nodos
    lugares_nodos[lugar] = nodo1

# Obtener los lugares presentes en el grafo
lugares = list(lugares_nodos.keys())


# Crear la interfaz de usuario
layout = [
    [sg.Text('¡Bienvenido! Esta es la APP- CAMINO SEGURO MADRID ')],
    [sg.Text('Por favor, seleccione el punto de origen y destino')],
    [sg.Text('Punto de origen:'), sg.InputCombo(lugares, key='-ORIGEN-')],
    [sg.Text('Punto de destino:'), sg.InputCombo(lugares, key='-DESTINO-')],
    [sg.Button('Calcular'), sg.Button('Salir')],
    [sg.Text('Grafo de accidentes:')],
    [sg.Canvas(key='-CANVAS-')],
    [sg.Output(size=(50, 10))]
]

window = sg.Window('APP- VIAJA SEGURO', layout, finalize=True)

fig, ax = plt.subplots(figsize=(8, 6))
pos = nx.spring_layout(G)  # Obtener la posición de los nodos
nx.draw_networkx(G, pos, with_labels=False, node_size=50, font_size=10)
nx.draw_networkx_edges(G, pos, width=2, edge_color='r')
#nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
canvas = FigureCanvasTkAgg(fig, master=window['-CANVAS-'].TKCanvas)
canvas.draw()
canvas.get_tk_widget().pack(side='top', fill='both', expand=True)


# Función para calcular el camino más corto seguro en base al peso
def calcular_camino_mas_corto(origen_nombre, destino_nombre):
    if origen_nombre not in lugares_nodos or destino_nombre not in lugares_nodos:
        print("Al menos uno de los puntos ingresados no existe en el grafo.")
    else:
        origen = lugares_nodos[origen_nombre]
        destino = lugares_nodos[destino_nombre]

        # Implementar el algoritmo de Dijkstra 
        distances = {node: float('inf') for node in G.nodes()}  # Inicializar todas las distancias como infinito
        distances[origen] = 0  # La distancia al nodo de origen es 0
        visited = set()  # Conjunto de nodos visitados

        while len(visited) < len(G.nodes()):
            # Obtener el nodo no visitado con la distancia más pequeña
            current_node = min(
                (node for node in G.nodes() if node not in visited),
                key=lambda x: distances[x]
            )

            visited.add(current_node)

            # Actualizar las distancias de los nodos adyacentes no visitados
            for neighbor in G.neighbors(current_node):
                if neighbor not in visited:
                    weight = G[current_node][neighbor]['weight']
                    new_distance = distances[current_node] + weight
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance

        # Reconstruir el camino más corto
        shortest_path = [destino]
        current_node = destino
        while current_node != origen:
            neighbors = list(G.neighbors(current_node))
            neighbor_distances = [distances[node] for node in neighbors]
            min_distance = min(neighbor_distances)
            next_node = neighbors[neighbor_distances.index(min_distance)]
            shortest_path.insert(0, next_node)
            current_node = next_node

        # Actualizar la figura con el camino más corto resaltado
        ax.clear()
        nx.draw_networkx(G, pos, with_labels=False, node_size=50, font_size=10)
        nx.draw_networkx_edges(G, pos, width=2, edge_color='r')
        #nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
        path_edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=2, edge_color='g')
        canvas.draw()

        # Imprimir el camino más corto
        print("Camino más corto-seguro de {} a {}: {}".format(origen_nombre, destino_nombre, shortest_path))


# la interfaz de usuario
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Salir':
        break
    elif event == 'Calcular':
        origen_nombre = values['-ORIGEN-']
        destino_nombre = values['-DESTINO-']
        calcular_camino_mas_corto(origen_nombre, destino_nombre)

window.close()

