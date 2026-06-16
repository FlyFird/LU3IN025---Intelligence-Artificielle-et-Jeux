# Importation des differents bibliotheques et fichiers necessaires
import random
import time as t

from pulp import*

import matplotlib.pyplot as plt
from fonctions_utiles import *
from gale_shapley import *


# Partie 2 : calcul des temps moyens

def calcul_temps():

    # Configuration principale
    n_values = range(200, 2001, 200)  # Valeurs de n : de 200 à 2000 par pas de 200
    num_tests = 10  # Nombre de tests par valeur de n
    average_times = []  # Temps moyen pour chaque n
    n_master=9
    for n in n_values:
        current_woman=[str(x) for x in range(n_master)]
        current_man=[str(x) for x in range(n)]
        tmp=[]
        for _ in range(num_tests):
            # Generation des preferences aleatoires
            man_liste = matrice_aleatoire(n,n_master)
            woman_liste = matrice_aleatoire(n_master,n)
            #print(test)
            # Generation des capacites equilibres
            capacites = repartir_equitablement(n,n_master)
            start_time = t.time()
            gale_shapley_etu(man_liste, woman_liste,current_man,current_woman,capacites)
            end_time = t.time()
            tmp.append(end_time - start_time)

            # Mesurer le temps de l'exécution de Gale-Shapley
        average_times.append(tmp)
    print(average_times)

    # La moyenne du temps de calcul de l'algo de Gale-Shapley
    liste_moyenne_time = ensemble_calculer_moyenne(average_times)
    print("Liste des temps moyens : ", liste_moyenne_time)


    # Trace graphique du temps moyen
    plt.plot(liste_moyenne_time, label='Courbe des valeurs', color='b', marker='o')

    # Ajout des labels et du titre
    plt.xlabel('Index')  # Axe des x (index des éléments)
    plt.ylabel('Temps')  # Axe des y (valeurs de la liste)
    plt.title('Courbe de la moyenne du temps de calcul')
    # Affichage du graphique
    plt.show()


    # Tracer les courbes pour chaque sous-liste dans 'data'
    for i, subset in enumerate(average_times):
        plt.plot(subset, label=f'Série {i+1}')

    # Ajouter des labels et un titre
    plt.xlabel('Index')
    plt.ylabel('Temps')
    plt.title('Courbe du temps de calcul')

    # Ajouter une légende
    plt.legend()

    # Afficher le graphique
    plt.show()