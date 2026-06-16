# Importation des differents bibliotheques et fichiers necessaires
import random

# Fonctions utilitaires


# Partie 2

# Question 7

def matrice_aleatoire(n_etu,n_spe):
    """
    n_etu -> nombre d etudiant
    n_spe -> nombre de spe
    Return : genere une matrice de preference -> list*list*int  : random
    """
    matrice=[]
    pref=[str(x) for x in range(n_spe)]
    for i in range(n_etu):
        random.shuffle(pref) # randomiz la liste
        matrice.append(pref.copy())
    return matrice


def repartir_equitablement(total, places):
    """
    total -> nombre total
    places -> nombre de place
    Distribue equitablement les agents
    return une liste de int
    """
    # Répartition de base
    base = total // places
    reste = total % places

    # Création de la liste
    distribution = [base] * places

    # Répartition du reste
    for i in range(reste):
        distribution[i] += 1

    return distribution


def convertir(dictionnaire):
    return {str(cle):str(valeur) for cle,valeur in dictionnaire}

def calculer_moyenne(liste):
    #Calcule la moyenne d une liste et retourne un float
    return sum(liste) / len(liste)
def ensemble_calculer_moyenne(liste):
    #calcule la moyenne d une liste de liste et retourne une liste*float
    tmp=[]
    for i in range(len(liste)):
        #print(liste[i])
        tmp.append(calculer_moyenne(liste[i]))
    return tmp


def moyenne_et_min(couple, matrice_pref):
    """Calcule l'utilité moyenne et minimale des étudiants."""
    tmp = []

    # Convertir toute la matrice des préférences en entiers
    matrice_pref = [[int(x) for x in ligne] for ligne in matrice_pref]

    for i in range(len(matrice_pref)):
        affectation = int(couple[str(i)])  # S'assurer que l'affectation est un entier

        if affectation in matrice_pref[i]:  # Vérification avant de chercher l'index
            tmp.append(matrice_pref[i].index(affectation))

    return sum(tmp) / len(tmp), min(tmp)


def moyenne_et_min_spe(couple, matrice_pref):
    """Calcule l'utilité moyenne et minimale des options par rapport aux étudiants affectés."""
    tmp = []

    # Convertir la matrice des préférences en entiers
    matrice_pref = [[int(x) for x in ligne] for ligne in matrice_pref]

    for option, students in couple.items():
        for student in students:  # Parcourir chaque étudiant affecté à cette option
            student = int(student)  # S'assurer que l'étudiant est un entier
            option = int(option)  # S'assurer que l'option est un entier

            if student in matrice_pref[option]:  # Vérifier si l'étudiant est dans la liste des préférences de l'option
                tmp.append(matrice_pref[option].index(student))

    return sum(tmp) / len(tmp), min(tmp)