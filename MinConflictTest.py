import RandomMapGeneration
import random
import math
import matplotlib.pyplot as plt
import time


#Funzione per decidere quale punto modificare scelto in modo casuale
def IndextoChange(extended_points):
    while True:
        index = random.randint(0, len(extended_points) - 1)
        if extended_points[index]["is_in_conflict"]:  
            return index

#Funzione per verificare che la soluzione corrente sia una soluzione corretta
def CheckSolution(connections,solution,extended_points):
    correct=True
    for i,j in connections:
        extended_points[i]["neighbors"][solution[j]] += 1 #per ogni i io ho un vettore neighbors in cui a ogni posizione corrisponde un colore, e incremento di 1 il colore di j,in posizione solutions[j] cosicché per ogni colore so quanti vicini ha i di quel colore
        extended_points[j]["neighbors"][solution[i]] += 1 #devo incrementare anche il colore di i per j
        if solution[i]==solution[j]:
            extended_points[i]["is_in_conflict"] = True
            extended_points[j]["is_in_conflict"] = True
            correct=False
    return correct        

#Funzione per determinare la soluzione casuale iniziale
def RandomSolution(n, coloursNumbers):
    return [random.choice(coloursNumbers) for _ in range(n)]

#Funzione che esegue l'algoritmo MinConflicts
def MinConflicts(csp,max_steps,colours):
    n_steps=0
    current = RandomSolution(len(csp["extended_points"]), csp["coloursNumbers"]) 

    for i in range(max_steps+1):
        for point in csp["extended_points"]: #reset degli elementi prima di ogni iterazione
            point["is_in_conflict"] = False  
            point["neighbors"] = [0] * len(point["neighbors"])  

        is_solution = CheckSolution(csp["connections"], current, csp["extended_points"])
        conflicts = sum(1 for edge in csp["connections"] if current[edge[0]] == current[edge[1]])  #numero di conflitti (archi in conflitto) 

        if is_solution:
            print("Soluzione trovata!")
            break  

        conflicts = sum(1 for edge in csp["connections"] if current[edge[0]] == current[edge[1]])
        

        index_to_change = IndextoChange(csp["extended_points"])

        min_value = min(csp["extended_points"][index_to_change]["neighbors"])#cerco tra i neighbor quello con il valore minore, ovvero il colore che compare meno volte tra i vicini e che quindi comporterà meno conflitti
        min_index = csp["extended_points"][index_to_change]["neighbors"].index(min_value) #cerco l'indice di tale colore,ovvero il colore che andrà sostituito alla variabile da modificare
        current[index_to_change] = min_index
       
        n_steps+=1

    is_solution = CheckSolution(csp["connections"], current, csp["extended_points"]) #aggiungo iterazione finale per controllare ultimo passaggio
    conflicts = sum(1 for edge in csp["connections"] if current[edge[0]] == current[edge[1]]) 

    return current,n_steps,conflicts

#Funzione che testa l'algoritmo per diversi input
def test_performance(max_n, step, max_steps):
    n_values = []
    times = []

    for n in range(step, max_n + 1, step):

        coloursNumbers = [0, 1, 2]
        colours = ["Yellow", "Green", "Blue"]
        correct_execution,points, connections = RandomMapGeneration.generate_map_coloring_problem(n,len(coloursNumbers))
            
    
        extended_points = []
        for i, point in enumerate(points):
            new_extended_point = { 
                "coordinates": point,  
                "neighbors": [0] * len(colours),  
                "is_in_conflict": False  
            }
            extended_points.append(new_extended_point)

        csp = {
            "extended_points": extended_points,
            "connections": connections,
            "coloursNumbers": coloursNumbers
        }

        if correct_execution:
            #misuro il tempo di esecuzione
            start_time = time.time()
            solution, n_steps, final_conflicts = MinConflicts(csp, max_steps=max_steps, colours=colours)
            end_time = time.time()

            
            elapsed_time = end_time - start_time

        
            n_values.append(n)
            times.append(elapsed_time)

            print(f"n: {n}, tempo: {elapsed_time:.4f} secondi, conflitti finali: {final_conflicts}")
        else :
            print("Esecuzione non riuscita")

    #al termine si produce un grafico
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, times, marker="o", linestyle="-", color="blue", label="Tempo di esecuzione")
    plt.xlabel("Numero di nodi (n)")
    plt.ylabel("Tempo di esecuzione (secondi)")
    plt.title("Prestazioni di MinConflicts al crescere di n")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    #configurazione dei parametri
    max_n = 1000  #numero massimo di nodi da testare
    step = 50   #incremento del numero di nodi
    max_steps = 100  #numero massimo di passi per l'algoritmo

    print("Esecuzione dei test...")
    test_performance(max_n, step, max_steps)

