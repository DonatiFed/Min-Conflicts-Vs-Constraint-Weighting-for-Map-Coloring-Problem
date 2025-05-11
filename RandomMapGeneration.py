import random
import math
import matplotlib.pyplot as plt



def generate_map_coloring_problem(n, max_colors):
    points = [(random.random(), random.random()) for _ in range(n)]
    connections = []
    edges = []
    max_degree = max_colors-1  # numero massimo di archi per nodo
    
    for i in range(n):
        for j in range(i + 1, n):
            edges.append((math.dist(points[i], points[j]), i, j))
    edges.sort()  # Ordina gli archi in base alla distanza

    parent = list(range(n))
    degrees = [0] * n

    # Funzione per trovare il rappresentante del nodo (Union-Find)
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    # Funzione per unire due insiemi (Union-Find)
    def union(x, y):
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            parent[root_y] = root_x

    # Funzione per verificare se due segmenti si intersecano
    def lines_intersect(p1, p2, p3, p4):
        def ccw(a, b, c):
            return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])
        return ccw(p1, p2, p3) != ccw(p1, p2, p4) and ccw(p3, p4, p1) != ccw(p3, p4, p2)

    # Funzione per costruire MST (usando Kruskal e controllando che non si superi il max grado o non si intersechino gli archi)
    mst_edges = []
    for _, i, j in edges:
        if find(i) != find(j) and degrees[i] < max_colors and degrees[j] < max_colors:   #controllo grado per mst
            new_line = (points[i], points[j])
            intersects = False

            for a, b in mst_edges:    #controllo intersezioni pr mst
                if lines_intersect(points[a], points[b], new_line[0], new_line[1]):
                    intersects = True
                    break

            if not intersects:
                mst_edges.append((i, j))
                union(i, j)
                degrees[i] += 1
                degrees[j] += 1

    connections.extend(mst_edges)


    is_connected = verify_connectivity(n, connections)     #verifico che l'mst sia stato generato correttamente
    max_degree_respected = verify_degrees(n, connections,max_colors)
    if not (is_connected and max_degree_respected):
        print("not enough colours to generate the map!")
        return False,points, connections
        

   
    for _, i, j in sorted(edges, key=lambda edge: (edge[0], degrees[edge[1]], degrees[edge[2]])):   #Aggiungo archi al mst rispettando il limite di grado e senza intersezioni
        if degrees[i] < max_degree and degrees[j] < max_degree and (i, j) not in connections:
            new_line = (points[i], points[j])
            intersects = False
            
            
            for a, b in connections:    #controllo intersezioni
                if lines_intersect(points[a], points[b], new_line[0], new_line[1]):
                    intersects = True
                    break

            if not intersects:
                connections.append((i, j))
                degrees[i] += 1
                degrees[j] += 1
        
    return True,points, connections

#Funzione per verificare che tutti i punti siano collegati
def verify_connectivity(n, connections):  
    parent = list(range(n))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            parent[root_y] = root_x

    for i, j in connections:
        union(i, j)

    
    root_set = set(find(i) for i in range(n)) #verifica che tutti i nodi appartengano alla stessa componente
    return len(root_set) == 1


#Funzione per verificare che il grado massimo sia rispettato
def verify_degrees(n, connections, max_colors):     
    degrees = [0] * n
    for i, j in connections:
        degrees[i] += 1
        degrees[j] += 1
    return all(deg <= max_colors for deg in degrees)

#Funzione per disegnare mappa
def plot_map_coloring_problem(points, connections):
    plt.figure(figsize=(16, 16))

    for x, y in points:         #si disegnano i punti
        plt.plot(x, y, 'o', color='blue')

    for i, j in connections:  #si disegnano gli archi
        x1, y1 = points[i]
        x2, y2 = points[j]
        plt.plot([x1, x2], [y1, y2], 'k-')

    plt.title("Problema di colorazione di mappe")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()
    

#Funzione main
if __name__ == "__main__":
    n =2000  #numero di punti
    correct_execution,points, connections = generate_map_coloring_problem(n,3)
    is_connected = verify_connectivity(n, connections)
    max_degree_respected = verify_degrees(n, connections,3 )
    print(f"Grafo connesso: {is_connected}")
    print(f"Grado massimo rispettato: {max_degree_respected}")
    if correct_execution:
        plot_map_coloring_problem(points, connections)
    
    
    