import RandomMapGeneration
import random
import math
import matplotlib.pyplot as plt
import time
import random


# Funzione per rappresentare l'esecuzione dell'algoritmo sulla mappa
def plot_solution(points, solution, colours, step, conflicts, extended_connections,execution_ended):
    plt.clf()  
    x, y = zip(*points)  #si estraggono le coordinate dei punti
    plt.scatter(x, y, c=[colours[c] for c in solution], s=200, edgecolors='black')
    for i, (x_coord, y_coord) in enumerate(points):
        plt.text(x_coord, y_coord, str(i), fontsize=12, ha='right', va='bottom', color='black')
    for connection in extended_connections:
        i, j = connection["connected_points"]
        x1, y1 = points[i]
        x2, y2 = points[j]
        color = "red" if connection["is_in_conflict"] else "black" #gli archi in conflitto vengono disegnati come rossi
        plt.plot([x1, x2], [y1, y2], color=color, lw=1)  
    plt.title(f"Step {step} - Conflicts: {conflicts}")
    if conflicts==0 and execution_ended==True:
         plt.title(f"Soluzione trovata in {step} passi con {conflicts} conflitti rimanenti", color="green", fontsize=16)
    elif conflicts!=0 and execution_ended==True:
        plt.title(f"Soluzione non trovata in {step} passi con {conflicts} conflitti rimanenti", color="red", fontsize=14)
    plt.pause(0.5) 

#Funzione per stabilire il nuovo colore della variabile selezionata per essere modificata
def NewColour(extended_connections,point,solution,coloursNumbers):
    old_colour=solution[point]  
    NewColour=solution[point]  
    NewWeight=float('inf')
    for colour in coloursNumbers: #provo tutti i colori
        if colour==old_colour:    #non provo il colore vecchio -->in questo modo non si permette di mantenere il colore originale, perché si limiterebbe lo spazio delle soluzioni
            continue
        else:
            solution[point]=colour         
            new_conflicts = sum(1 for c in extended_connections if point in c["connected_points"] and solution[c["connected_points"][0]] == solution[c["connected_points"][1]])                       
        if new_conflicts<NewWeight:    
                NewWeight=new_conflicts   
                NewColour=colour           
                
    solution[point] = old_colour  
    return NewColour

#Funzione per controllare se la soluzione corrente è una soluzione
def CheckSolution(extended_connections, solution):
    sum_weights = 0
    for c in extended_connections:
        i, j = c["connected_points"]
        if solution[i] == solution[j]:
            c["is_in_conflict"] = True
            c["weight"] += 1
        else:
            c["is_in_conflict"] = False
            c["weight"] = 0
        sum_weights += c["weight"] if c["is_in_conflict"] else 0
    return sum_weights      


#Funzione per determinare una soluzione casuale iniziale
def RandomSolution(n, coloursNumbers):
    return [random.choice(coloursNumbers) for _ in range(n)]

#Funzione che esegue algoritmo Constraint Weighting con visulaizzazione degli step
def ConstraintWeighting(csp, max_steps, colours):
    plt.ion()  
    n_steps=0
    current = RandomSolution(len(csp["points"]), csp["coloursNumbers"])  
    for step in range(max_steps):
        for connection in csp["extended_connections"]:
            connection["is_in_conflict"] = False 
        sum_weights = CheckSolution(csp["extended_connections"], current)
        conflicts = sum(c['is_in_conflict'] for c in csp['extended_connections'])  
        plot_solution(csp["points"], current, colours, step, conflicts, csp["extended_connections"],False)
        
        if sum_weights==0:
            print("\033[92mSoluzione trovata!\033[0m")
            plt.ioff()  
            break  
        
        max_edge=max(csp['extended_connections'], key=lambda c: c['weight']) #seleziono l'arco che ha più peso
        index_to_change =random.choice(max_edge['connected_points'])  #seleziono un punto a caso nell'arco che ha più peso(per evitare di bloccarsi in minimi locali)

        new_colour=NewColour(csp['extended_connections'],index_to_change,current,csp['coloursNumbers'])
        current[index_to_change]=new_colour
        n_steps+=1
        
    sum_weights = CheckSolution(csp["extended_connections"], current) #aggiungo iterazione finale per controllare ultimo passaggio
    conflicts = sum(c['is_in_conflict'] for c in csp['extended_connections'])  # Numero di conflitti al termine
    plot_solution(csp["points"], current, colours, step, conflicts, csp["extended_connections"],False)
    if conflicts > 0:
        print("Soluzione non trovata entro il limite massimo di passi")
    plt.ioff() 
    return current,n_steps,conflicts #si ritorna sempre la soluzione a cui siamo arrivati, e nel main si controlla se era una soluzione giusta

#Funzione main
if __name__ == "__main__":
    n = 500
    coloursNumbers = [0, 1, 2]
    colours = ["Yellow", "Green", "Blue"]
    correct_execution,points, connections = RandomMapGeneration.generate_map_coloring_problem(n,len(coloursNumbers))
    if correct_execution:
        extended_connections=[]
        for i, point in enumerate(connections): #ho creato un arco "esteso" che contenga informazioni sul proprio peso e sul proprio stato di conflitto
            new_extended_connection = {
                "connected_points":connections[i],
                "weight": 1,  # Lista inizializzata a 0 per ogni colore
                "is_in_conflict": False  # Flag di conflitto inizializzato a False
            }
            extended_connections.append(new_extended_connection)

    
        csp = {
            "points": points,
            "extended_connections": extended_connections,
            "coloursNumbers": coloursNumbers
        }
        
        print("Inizio algoritmo ConstraintWeighting")
        n_steps=0
        final_conflicts=0
        solution,n_steps,final_conflicts = ConstraintWeighting(csp, max_steps=50, colours=colours)
        
        if final_conflicts==0:
            plot_solution(csp["points"], solution, colours, step=n_steps, conflicts=final_conflicts, extended_connections=csp["extended_connections"],execution_ended=True)
            plt.show()
        else:
            plot_solution(csp["points"], solution, colours, step=n_steps, conflicts=final_conflicts, extended_connections=csp["extended_connections"],execution_ended=True)
            plt.show()
    else:
        print("algoritmo non eseguito")