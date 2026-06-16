# Importation des differents bibliotheques et fichiers necessaires
from pulp import*

from lecture_pref import *
from gale_shapley import *
from paire_instable import *
from fonctions_utiles import *
from temps import *
from programme_lin import *



def lancement():
    # Partie 1 : Gale-Shapley

    print("Affectation Gale-Shapley : ")

    matrix_pref_etu, agent_etu = read_pref_etu("data/PrefEtu.txt")
    matrix_pref_spe, capacite, agent_spe = read_pref_spe("data/PrefSpe.txt")

    # Question 5
    # Affectation avec Gale-Shapley cote etudiant et cote parcours
    affectation_cote_etu = gale_shapley_etu(matrix_pref_etu, matrix_pref_spe, agent_etu, agent_spe, capacite)
    affectation_cote_spe = gale_shapley_spe(matrix_pref_spe, matrix_pref_etu, agent_spe, agent_etu, capacite)

    print("Affectation cote etudiant : ", affectation_cote_etu)
    print("Affectation cote parcours (master) : ", affectation_cote_spe)

    # Question 6
    # Verification de la stabilite des affectations
    paires_instables_etu = paire_instable(affectation_cote_etu, matrix_pref_spe, matrix_pref_etu)
    paires_instables_spe = paire_instable(affectation_cote_spe, matrix_pref_etu, matrix_pref_spe)

    print("Liste des paires instables cote etudiant : ", paires_instables_etu)
    print("Liste des paires instables cote parcours (master) : ", paires_instables_spe)

    # Calcul des utilites
    result_etu_gale = gale_shapley_etu(matrix_pref_etu, matrix_pref_spe, agent_etu, agent_spe, capacite)
    result_spe_gale = gale_shapley_spe(matrix_pref_spe, matrix_pref_etu, agent_spe, agent_etu, capacite)

    utilite_moyenne, utilite_minimale = moyenne_et_min(result_etu_gale, matrix_pref_etu)
    print(f"Utilité moyenne : {utilite_moyenne}")
    print(f"Utilité minimale : {utilite_minimale}")

    utilite_moyenne, utilite_minimale = moyenne_et_min_spe(result_spe_gale, matrix_pref_spe)
    print(f"Utilité moyenne : {utilite_moyenne}")
    print(f"Utilité minimale : {utilite_minimale}")


    # Partie 2 : calcul des temps moyens

    print("Calcul du temps moyen : ")
    calcul_temps()


    # Partie 3 : PL(NE)

    print("Calcul du PLNE : ")


    # Question 12
    n_etud = 11
    n_parcours = 9
    k = 3
    result = solve_assignment(n_etud, n_parcours, capacite, matrix_pref_etu, k)
    print("Affectation:", result)

    # Question 13
    find_min_k(n_etud,n_parcours,matrix_pref_etu,capacite)

    result = solve_max_utile(n_etud, n_parcours, capacite, matrix_pref_etu,matrix_pref_spe)
    print("Affectation:", result)

    # Recuperation des resultats
    result1 = find_min_k(n_etud,n_parcours,matrix_pref_etu,capacite)
    print("Affectation:", result1)

    result2 = solve_max_utile(n_etud, n_parcours, capacite, matrix_pref_etu,matrix_pref_spe)
    print("Affectation:", result2)

    result3=solve_max_utile_k(n_etud, n_parcours, capacite, matrix_pref_etu,matrix_pref_spe,5)
    print("Affectation:", result3)

    affectation4 = convertir(result1)
    print(affectation4)
    affectation5 = convertir(result2)
    print(affectation5)
    affectation6 = convertir(result3)
    print(affectation6)

    print("Liste des paires instables Q13  :", paire_instable(affectation4, matrix_pref_spe,matrix_pref_etu))
    print("Liste des paires instables Q14 :", paire_instables(affectation4, matrix_pref_spe,matrix_pref_etu))
    print("Liste des paires instables Q15 :", paire_instable(affectation6, matrix_pref_spe,matrix_pref_etu))


if __name__ == "__main__":
    # Lancement du programme principal
    print("Exécution de main : ")

    lancement()

    print("Fin main")