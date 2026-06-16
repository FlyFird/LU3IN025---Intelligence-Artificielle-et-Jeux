# Importation des differents bibliotheques et fichiers necessaires
from lecture_pref import *
from gale_shapley import *
from paire_instable import *
from fonctions_utiles import *
from temps import *
from programme_lin import *


# Recuperation des matrices de preferences des etudiants et des parcours
matrix_pref_etu, agent_etu = read_pref_etu("data/PrefEtu.txt")
matrix_pref_spe, capacite, agent_spe = read_pref_spe("data/PrefSpe.txt")

print("--------------------")
print("Affichage des matrices de preferences :\n")
print(matrix_pref_etu)
print(matrix_pref_spe)
print("\nFin affichage des matrices de preferences")
print("--------------------\n")

# Affectation avec Gale-Shapley cote etudiant et cote parcours
affectation_cote_etu = gale_shapley_etu(matrix_pref_etu, matrix_pref_spe, agent_etu, agent_spe, capacite)
affectation_cote_spe = gale_shapley_spe(matrix_pref_spe, matrix_pref_etu, agent_spe, agent_etu, capacite)

print("--------------------")
print("Affichage des affectations par Gale-Shapley :\n")
print(affectation_cote_etu)
print(affectation_cote_spe)
print("\nFin affichage des affectations par Gale-Shapley")
print("--------------------\n")

# Verification des paires instables
paires_instables_etu = paire_instable(affectation_cote_etu, matrix_pref_spe, matrix_pref_etu)
paires_instables_spe = paire_instable(affectation_cote_spe, matrix_pref_etu, matrix_pref_spe)

print("--------------------")
print("Affichage des paires instables :\n")
print(paires_instables_etu)
print(paires_instables_spe)
print("\nFin affichage des paires instables")
print("--------------------\n")

# Calcul du temps moyen
temps_moyen = calcul_temps()

print("--------------------")
print("Affichage calcul temps moyen :\n")
print(temps_moyen)
print("\nFin affichage calcul temps moyen")
print("--------------------\n")