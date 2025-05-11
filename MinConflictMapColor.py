import RandomMapGeneration
import random
import math
import matplotlib.pyplot as plt
import time
import random

# Funzione per rappresentare l'esecuzione dell'algoritmo sulla map
def plot_solution(points, connections, solution, colours, step, conflicts,execution_ended):
    plt.clf() 
    x, y = zip(*points)
    for i, j in connections:
        if solution[i] == solution[j]:
            plt.plot([points[i][0], points[j][0]], [points[i][1], points[j][1]], 'r-', linewidth=1)  #gli archi in conflitto sono rossi
        else:
            plt.plot([points[i][0], points[j][0]], [points[i][1], points[j][1]], 'k-', linewidth=1)  #gli archi che non sono in conflitto sono neri
    plt.scatter(x, y, c=[colours[c] for c in solution], s=200, edgecolors='black')
    for i, (x_coord, y_coord) in enumerate(points):
        plt.text(x_coord, y_coord, str(i), fontsize=12, ha='right', va='bottom', color='black')
    plt.title(f"Step {step} - Conflicts: {conflicts}")
    if conflicts==0 and execution_ended==True:
        plt.title(f"Soluzione trovata in {step} passi con {conflicts} conflitti rimanenti", color="green", fontsize=16)
    elif conflicts!=0 and execution_ended==True:
        plt.title(f"Soluzione non trovata in {step} passi con {conflicts} conflitti rimanenti", color="red", fontsize=14)
    plt.pause(0.5)

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
    plt.ion() 
    plt.show()

    for i in range(max_steps+1):
        for point in csp["extended_points"]: #reset degli elementi prima di ogni iterazione
            point["is_in_conflict"] = False  
            point["neighbors"] = [0] * len(point["neighbors"])  

        is_solution = CheckSolution(csp["connections"], current, csp["extended_points"])
        conflicts = sum(1 for edge in csp["connections"] if current[edge[0]] == current[edge[1]])  #numero di conflitti (archi in conflitto) 

        plot_solution([p["coordinates"] for p in csp["extended_points"]], csp["connections"],current,colours,step=i,conflicts=conflicts,execution_ended=False)

        if is_solution:
            print("Soluzione trovata!")
            break  

        conflicts = sum(1 for edge in csp["connections"] if current[edge[0]] == current[edge[1]])
        print(f"Numero di archi conflittuali: {conflicts}") #per il numero di conflitti non si contano le variabili, ma gli archi in conflitto

        index_to_change = IndextoChange(csp["extended_points"])

        min_value = min(csp["extended_points"][index_to_change]["neighbors"])#cerco tra i neighbor quello con il valore minore, ovvero il colore che compare meno volte tra i vicini e che quindi comporterà meno conflitti
        min_index = csp["extended_points"][index_to_change]["neighbors"].index(min_value) #cerco l'indice di tale colore,ovvero il colore che andrà sostituito alla variabile da modificare
        current[index_to_change] = min_index
       
        n_steps+=1
        time.sleep(1) 

    is_solution = CheckSolution(csp["connections"], current, csp["extended_points"]) #aggiungo iterazione finale per controllare ultimo passaggio
    conflicts = sum(1 for edge in csp["connections"] if current[edge[0]] == current[edge[1]]) 
    plot_solution([p["coordinates"] for p in csp["extended_points"]], csp["connections"],current,colours,step=i,conflicts=conflicts,execution_ended=False)
    plt.ioff()

    return current,n_steps,conflicts





#Funzione main
if __name__ == "__main__":
    n = 1000
    coloursNumbers = [0, 1, 2, 3]
    colours = ["Yellow", "Green", "Blue","Purple"]
    correct_execution,points, connections = RandomMapGeneration.generate_map_coloring_problem(n,len(coloursNumbers))
    if correct_execution:
        extended_points = []
        for i, point in enumerate(points): #ho creato dei punti "estesi" che contengono informazioni sui colori dei propri vicini(quanti vicini per ogni colore), e sul proprio stato di conflitto
            new_extended_point = { 
                "coordinates": point,  
                "neighbors": [0] * len(colours),  
                "is_in_conflict": False  
            }
            extended_points.append(new_extended_point)

        csp ={
        "extended_points":extended_points,
        "connections":connections,
        "coloursNumbers":coloursNumbers
        }
        
        print("Inizio algoritmo MinConflicts")
        n_steps=0
        final_conflicts = 0
        solution,n_steps,final_conflicts = MinConflicts(csp, max_steps=50, colours=colours)
        if final_conflicts == 0:
            print("Soluzione trovata:", solution)
            plot_solution([p["coordinates"] for p in csp["extended_points"]],csp["connections"],solution=solution,colours=colours,step=n_steps,conflicts=final_conflicts,execution_ended=True)
        else:
            print("Soluzione non trovata dopo il numero massimo di passi")
            plot_solution([p["coordinates"] for p in extended_points], connections, solution, colours, step=n_steps, conflicts=final_conflicts,execution_ended=True)
            
        plt.show()
    else:
        print("algoritmo non eseguito")
