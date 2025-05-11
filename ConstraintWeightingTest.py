import time
import RandomMapGeneration
import random
import math
import matplotlib.pyplot as plt
import time
import random

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
    n_steps=0
    current = RandomSolution(len(csp["points"]), csp["coloursNumbers"])  
    for step in range(max_steps):
        for connection in csp["extended_connections"]:
            connection["is_in_conflict"] = False 
        sum_weights = CheckSolution(csp["extended_connections"], current)
        conflicts = sum(c['is_in_conflict'] for c in csp['extended_connections'])  
        
        if sum_weights==0:
            print("\033[92mSoluzione trovata!\033[0m") 
            break  
        
        max_edge=max(csp['extended_connections'], key=lambda c: c['weight']) #seleziono l'arco che ha più peso
        index_to_change =random.choice(max_edge['connected_points'])  #seleziono un punto a caso nell'arco che ha più peso(per evitare di bloccarsi in minimi locali)

        new_colour=NewColour(csp['extended_connections'],index_to_change,current,csp['coloursNumbers'])
        current[index_to_change]=new_colour
        n_steps+=1
        
    sum_weights = CheckSolution(csp["extended_connections"], current) #aggiungo iterazione finale per controllare ultimo passaggio
    conflicts = sum(c['is_in_conflict'] for c in csp['extended_connections'])  # Numero di conflitti al termine
    if conflicts > 0:
        print("Soluzione non trovata entro il limite massimo di passi")
    return current,n_steps,conflicts 

#Funzione che esta l'algoritmo per vari input
def test_performance(max_n, step, max_steps):
    n_values = []
    times = []

    for n in range(step, max_n + 1, step):
        # Generazione del problema
        coloursNumbers = [0, 1, 2]
        colours = ["Yellow", "Green", "Blue"]
        correct_execution,points, connections = RandomMapGeneration.generate_map_coloring_problem(n,len(coloursNumbers))
        extended_connections = []

        for i, point in enumerate(connections):
            new_extended_connection = {
                "connected_points": connections[i],
                "weight": 1,
                "is_in_conflict": False
            }
            extended_connections.append(new_extended_connection)

        csp = {
            "points": points,
            "extended_connections": extended_connections,
            "coloursNumbers": coloursNumbers
        }

        if correct_execution:
            #si calcola quanto tempo si impiega per ogni esecuzione
            start_time = time.time()
            solution, n_steps, final_conflicts = ConstraintWeighting(csp, max_steps=max_steps, colours=["Yellow", "Green", "Blue"])
            end_time = time.time()

            
            elapsed_time = end_time - start_time

        
            n_values.append(n)
            times.append(elapsed_time)

            print(f"n: {n}, tempo: {elapsed_time:.4f} secondi, conflitti finali: {final_conflicts}")
        else:
            print("Esecuzione non riuscita")

    #al termine si produce un grafico
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, times, marker="o", linestyle="-", color="blue", label="Tempo di esecuzione")
    plt.xlabel("Numero di nodi (n)")
    plt.ylabel("Tempo di esecuzione (secondi)")
    plt.title("Prestazioni di ConstraintWeighting al crescere di n")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    #configurazione dei parametri del test
    max_n = 1000  #numero massimo di nodi da testare
    step = 100  #incremento del numero di nodi
    max_steps = 100  #numero massimo di passi per l'algoritmo

    print("Esecuzione dei test...")
    test_performance(max_n, step, max_steps)
