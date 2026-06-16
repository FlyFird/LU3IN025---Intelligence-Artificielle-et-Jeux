# Partie 1 : Probleme et affectation

# Question 1

def read_pref_etu(f):
    fichier = open(f, "r")           # Ouverture du fichier en mode lecture "r"
    contenu = fichier.readlines()    # Liste contenant chaque ligne du fichier
    fichier.close()                  # Fermeture du fichier

    nbEtu = int(contenu[0])
    matrix = [[] for i in range(nbEtu)]

    contenu = contenu[1:]            # On retire la 1ere ligne (nombre d'etudiants)

    for ligne in contenu:
        l = ligne.split()            # Liste contenant chaque element de la ligne separe par un espace
        numEtu = int(l[0])
        nomEtu = l[1]
        l = l[2:]                    # On retire les 2 premiers elements (numero + nom)
        matrix[numEtu] = l
        matrix[numEtu] = [int(s) for s in matrix[numEtu]]   # On convertit les string en int

    return matrix

#print(read_pref_etu("PrefEtu.txt"))


def read_pref_spe(f):
    fichier = open(f, "r")           # Ouverture du fichier en mode lecture "r"
    contenu = fichier.readlines()    # Liste contenant chaque ligne du fichier
    fichier.close()                  # Fermeture du fichier

    contenu = contenu[1:]            # On retire la 1ere ligne (nombre d'etudiants)

    # On met la capacite de chaque parcours dans une liste
    capacite = contenu[0].split()
    capacite = capacite[1:]              # On retire "Cap" de la liste
    for i in range(len(capacite)):
        capacite[i] = int(capacite[i])

    nbSpe = len(capacite)            # On recupere le nombre total de spe

    matrix = [[] for i in range(nbSpe)]

    contenu = contenu[1:]            # On retire la 1ere ligne (capacite des spe)

    for ligne in contenu:
        l = ligne.split()            # Liste contenant chaque element de la ligne separe par un espace
        numSpe = int(l[0])
        nomSpe = l[1]
        l = l[2:]                    # On retire les 2 premiers elements (numero + nom)
        matrix[numSpe] = l
        matrix[numSpe] = [int(s) for s in matrix[numSpe]]   # On convertit les string en int

    return matrix, capacite

#print(read_pref_spe("PrefSpe.txt"))


# Question 2

"""
On peut utiliser les structures de donnees suivantes :
    - file
    - liste
    - dictionnaire

1. 0(1) avec une structure de file
2. O(1) avec un dictionnaire contenant l'indice du prochain parcours a proposer dans la case de l'etudiant i
3. O(n) avec une liste et en faisant des comparaisons successives pour trouver la position de l'etudiant
4. O(m) avec une liste ou m est le nombre d'etudiants affectes au parcours j
5. O(m + c) avec une liste contenant les etudiants affectes au parcours avec c la taille de la solution finale
"""


# Question 3

def Gale_Shapley_etu(matrix_pref_etu, matrix_pref_spe, capacite):
    nbEtu = len(matrix_pref_etu)
    nbSpe = len(matrix_pref_spe)

    # dictionnaire des mariages
    mariages_cote_etu = dict()
    mariages_cote_parcours = dict()

    # Au debut, tous les etudiants sont libres
    file_etu_libre = []
    for i in range(nbEtu):
        file_etu_libre.append(i)
        mariages_cote_etu[i] = -1

    for i in range(nbSpe):
        mariages_cote_parcours[i] = -1

    liste_proposition = [0 for i in range(nbEtu)]
    liste_max = [nbSpe for i in range(nbEtu)]
    liste_places_spe = capacite

    while(len(file_etu_libre) != 0):
        etudiant = file_etu_libre.pop(0)
        prochain_parcours_etu = liste_proposition[etudiant]
        parcours = int(matrix_pref_etu[etudiant][prochain_parcours_etu])

        ind_pref_parcours = -1

        for i in range(len(matrix_pref_spe[parcours])):
            if (matrix_pref_spe[parcours][i] == etudiant):
                ind_pref_parcours = i

        # Cas libre :
        if (mariages_cote_etu[etudiant] == -1):
            # On verifie que le parcours a encore de la place
            while (liste_places_spe[parcours] == 0):
                liste_proposition[etudiant] += 1

            mariages_cote_etu[etudiant] = parcours
            liste_proposition[etudiant] += 1
            liste_places_spe[parcours] -= 1


        # Cas nouveau parcours prefere a l'ancien
        elif (ind_pref_parcours < mariages_cote_parcours[parcours]):
            mariages_cote_etu[etudiant] = parcours                      # On affecte l'etudiant avec le parcours
            mariages_cote_parcours[parcours] = etudiant                 # On affecte le parcours avec l'etudiant
            mariages_cote_etu[mariages_cote_parcours[parcours]] = -1    # On libere l'autre etudiant
            file_etu_libre.append(mariages_cote_parcours[parcours])     # Et on l'ajoute a la liste des etudiants libres

        liste_proposition[etudiant] += 1

    return mariages_cote_etu

matrix_pref_etu = read_pref_etu("PrefEtu.txt")
matrix_pref_spe, capacite = read_pref_spe("PrefSpe.txt")
print("Affectation cote etudiant : ")
print(Gale_Shapley_etu(matrix_pref_etu, matrix_pref_spe, capacite))


# Question 4

def Gale_Shapley_spe(matrix_pref_etu, matrix_pref_spe, capacite):
    nbEtu = len(matrix_pref_etu)
    nbSpe = len(matrix_pref_spe)

    # dictionnaire des mariages
    mariages_cote_etu = dict()
    mariages_cote_parcours = dict()

    # Au debut, tous les etudiants sont libres
    file_spe_libre = []
    for i in range(nbSpe):
        file_etu_libre.append(i)
        mariages_cote_parcours[i] = -1

    for i in range(nbSpe):
        mariages_cote_parcours[i] = -1

    liste_proposition = [0 for i in range(nbSpe)]
    liste_max = [nbEtu for i in range(nbSpe)]
    liste_places_spe = capacite

    while(len(file_etu_libre) != 0):
        parcours = file_spe_libre.pop(0)
        prochain_etu = liste_proposition[parcours]
        etudiant = int(matrix_pref_spe[parcours][prochain_etu])

        ind_pref_etu = -1

        for i in range(len(matrix_pref_etu[etudiant])):
            if (matrix_pref_etu[etudiant][i] == parcours):
                ind_pref_etu = i

        # Cas libre :
        if (mariages_cote_parcours[etudiant] == -1):
            # On verifie que le parcours a encore de la place
            while (liste_places_spe[parcours] == 0):
                liste_proposition[parcours] += 1

            mariages_cote_parcours[parcours] = etudiant
            liste_proposition[parcours] += 1
            liste_places_spe[etudiant] -= 1


        # Cas nouveau parcours prefere a l'ancien
        elif (ind_pref_etu < mariages_cote_etu[etudiant]):
            mariages_cote_parcours[parcours] =  etudiant                # On affecte le parcours avec l'etudiant
            mariages_cote_etu[etudiant] = parcours                      # On affecte l'etudiant avec le parcours
            mariages_cote_parcours[mariages_cote_etu[etudiant]] = -1    # On libere l'autre parcours
            file_spe_libre.append(mariages_cote_etudiant[etudiant])     # Et on l'ajoute a la liste des parcours libres

        liste_proposition[parcours] += 1

    return mariages_cote_parcours

print("Affectation cote parcours : ")
print(Gale_Shapley_spe(matrix_pref_etu, matrix_pref_spe, capacite))


# Question 6

def paire_instables(affectation, matrix_pref_etu, matrix_pref_spe):
    liste_paires_instables = []

    # On parcourt tous les parcours et les étudiants affectés
    for parcours1, liste_etudiants in affectation.items():
        for etudiant in liste_etudiants:
            liste_pref_etu = matrix_pref_etu[int(etudiant)]

            # Récupérer l'indice du parcours actuel dans les préférences de l'étudiant
            ind_etu_pref1 = liste_pref_etu.index(int(parcours1))

            # Comparer parcours1 avec tous les autres parcours possibles
            for parcours2 in affectation.keys():
                if parcours2 != parcours1:
                    ind_etu_pref2 = liste_pref_etu.index(int(parcours2))

                    # Si l'étudiant préfère parcours2 à parcours1
                    if ind_etu_pref2 < ind_etu_pref1:
                        liste_pref_parcours = matrix_pref_spe[int(parcours2)]

                        # Vérifier si parcours2 préfère aussi cet étudiant à ses affectés
                        for etudiant_affecte in affectation[parcours2]:
                            ind_etu_parcours2 = liste_pref_parcours.index(int(etudiant))
                            ind_etu_affecte_parcours2 = liste_pref_parcours.index(int(etudiant_affecte))

                            # Si parcours2 préfère l'étudiant à un de ses actuels affectés
                            if ind_etu_parcours2 < ind_etu_affecte_parcours2:
                                if (not((parcours2, etudiant) in liste_paires_instables)):
                                    liste_paires_instables.append((parcours2, etudiant))

    return liste_paires_instables

affectation = {'0': ['5', '3'], '1': ['4'], '2': ['9'], '3': ['8'], '4': ['10'], '5': ['1'], '6': ['0'], '7': ['7'], '8': ['6', '2']}
#affectation2 = {'0': ['5', '3'], '1': ['4'], '2': ['9'], '3': ['8'], '4': ['10'], '5': ['1'], '6': ['0'], '7': ['6'], '8': ['7', '2']}
affectation2 = {'0': ['0', '1'], '1': ['2'], '2': ['3'], '3': ['4'], '4': ['5'], '5': ['6'], '6': ['7'], '7': ['8'], '8': ['9', '10']}
matrix_pref_etu = read_pref_etu("PrefEtu.txt")
matrix_pref_spe, capacite = read_pref_spe("PrefSpe.txt")

print("Liste des paires instables :", paire_instables(affectation, matrix_pref_etu, matrix_pref_spe))
print("Liste des paires instables :", paire_instables(affectation2, matrix_pref_etu, matrix_pref_spe))


### Version 1 Gale-Shapley

def Gale_Shapley_etu(matrix_pref_etu, matrix_pref_spe):
    nbEtu = len(matrix_pref_etu)
    nbSpe = len(matrix_pref_spe)

    # dictionnaire des mariages
    mariages_cote_etu = dict()
    mariages_cote_parcours = dict()

    # Au debut, tous les etudiants sont libres
    file_etu_libre = []
    for i in range(nbEtu):
        file_etu_libre.append(i)
        mariages_cote_etu[i] = -1

    for i in range(nbSpe):
        mariages_cote_parcours[i] = -1

    liste_proposition = [0 for i in range(nbEtu)]
    liste_max = [nbSpe for i in range(nbEtu)]

    while(len(file_etu_libre) != 0):
        etudiant = file_etu_libre.pop(0)
        prochain_parcours_etu = liste_proposition[etudiant]
        parcours = int(matrix_pref_etu[etudiant][prochain_parcours_etu])

        ind_pref_parcours = -1

        for i in range(len(matrix_pref_spe[parcours])):
            if (matrix_pref_spe[parcours][i] == etudiant):
                ind_pref_parcours = i

        # Cas libre :
        if (mariages_cote_etu[etudiant] == -1):
            mariages_cote_etu[etudiant] = parcours

        # Cas nouveau parcours prefere a l'ancien
        elif (ind_pref_parcours < mariages_cote_parcours[parcours]):
            mariages_cote_etu[etudiant] = parcours                      # On affecte l'etudiant avec le parcours
            mariages_cote_parcours[parcours] = etudiant                 # On affecte le parcours avec l'etudiant
            mariages_cote_etu[mariages_cote_parcours[parcours]] = -1    # On libere l'autre etudiant
            file_etu_libre.append(mariages_cote_parcours[parcours])               # L'autre etudiant est libre

        liste_proposition[etudiant] += 1

    return mariages_cote_etu

matrix_pref_etu = read_pref_etu("PrefEtu.txt")
matrix_pref_spe = read_pref_spe("PrefSpe.txt")
print(Gale_Shapley_etu(matrix_pref_etu, matrix_pref_spe))


###

def gale_shapley_parcours(maListeH,maListeF,current_man,current_women,taille_max):
    couple={j: [] for j in current_man}
    position = {j: 0 for j in current_man}
    agent=[x for x in range(len(current_man))]
    while agent!=[]:
        i=agent[0]
        if couple[current_man[i]]==[] or len(couple[current_man[i]])<taille_max[i]:
            free_man=current_man[i]
            target=maListeH[i][position[free_man]]
            if target in couple[free_man]:
                position[free_man]+=1
                continue
            if not(any(target in liste for liste in couple.values())):
                couple[free_man].append(maListeH[i][position[free_man]])
                if len(couple[current_man[i]])<taille_max[i]:
                    position[free_man]+=1
                else:
                    agent.pop(0)
            else:
                liste_cle=[free_man]
                tmp=couple.copy()
                position[free_man]+=1
                for cle,valeur in couple.items():
                    if target in valeur:
                        liste_cle.append(cle)
                        if (taille_max[int(cle)]-len(tmp[cle]))==0:
                            position[cle]+=1
                        tmp[cle].remove(target)
                        if int(cle) not in agent:
                            agent.append(int(cle))
                        break
                for x in range(len(maListeF[int(target)])):
                    if maListeF[int(target)][x] in liste_cle:
                        tmp[maListeF[int(target)][x]].append(target)
                        position[maListeF[int(target)][x]]-=1
                        if len(couple[maListeF[int(target)][x]])>=taille_max[int(maListeF[int(target)][x])]:
                            agent.remove(int(maListeF[int(target)][x]))
                        break
                couple=tmp.copy()
    return couple

matrix_pref_etu = read_pref_etu("PrefEtu.txt")
matrix_pref_spe = read_pref_spe("PrefSpe.txt")
print(Gale_Shapley_etu(matrix_pref_etu, matrix_pref_spe))


### Test code

def read_pref_etu(f):
    fichier = open(f, "r")           # Ouverture du fichier en mode lecture "r"
    contenu = fichier.readlines()    # Liste contenant chaque ligne du fichier
    fichier.close()                  # Fermeture du fichier

    nbEtu = int(contenu[0])
    matrix = [[] for i in range(nbEtu)]

    contenu = contenu[1:]            # On retire la 1ere ligne (nombre d'etudiants)

    for ligne in contenu:
        l = ligne.split()            # Liste contenant chaque element de la ligne separe par un espace
        numEtu = int(l[0])
        nomEtu = l[1]
        l = l[2:]                    # On retire les 2 premiers elements (numero + nom)
        matrix[numEtu] = l

    return matrix


def read_pref_spe(f):
    fichier = open(f, "r")           # Ouverture du fichier en mode lecture "r"
    contenu = fichier.readlines()    # Liste contenant chaque ligne du fichier
    fichier.close()                  # Fermeture du fichier

    contenu = contenu[1:]            # On retire la 1ere ligne (nombre d'etudiants)

    # On met la capacite de chaque parcours dans une liste
    capacite = contenu[0].split()
    capacite = capacite[1:]              # On retire "Cap" de la liste
    for i in range(len(capacite)):
        capacite[i] = int(capacite[i])

    nbSpe = len(capacite)            # On recupere le nombre total de spe

    matrix = [[] for i in range(nbSpe)]

    contenu = contenu[1:]            # On retire la 1ere ligne (capacite des spe)

    for ligne in contenu:
        l = ligne.split()            # Liste contenant chaque element de la ligne separe par un espace
        numSpe = int(l[0])
        nomSpe = l[1]
        l = l[2:]                    # On retire les 2 premiers elements (numero + nom)
        matrix[numSpe] = l

    return matrix, capacite


def gale_shapley(etudiants, parcours, capacites):
    nbEtu = len(etudiants)
    nbSpe = len(parcours)
    affectation = [-1] * nbEtu  # -1 signifie non affecté
    dispo_parcours = {i: [] for i in range(nbSpe)}
    file_attente = list(range(nbEtu))
    rang_preference = {i: {etu: rank for rank, etu in enumerate(parcours[i])} for i in range(nbSpe)}

    while file_attente:
        etu = file_attente.pop(0)
        for spe in etudiants[etu]:
            dispo_parcours[spe].append(etu)
            dispo_parcours[spe].sort(key=lambda x: rang_preference[spe][x])

            if len(dispo_parcours[spe]) > capacites[spe]:
                exclu = dispo_parcours[spe].pop()
                affectation[exclu] = -1
                file_attente.append(exclu)

            if affectation[etu] == -1 and etu in dispo_parcours[spe]:
                affectation[etu] = spe
                break

    return affectation


matrix_pref_etu = read_pref_etu("PrefEtu.txt")
matrix_pref_spe, capacite = read_pref_spe("PrefSpe.txt")
print(gale_shapley(matrix_pref_etu, matrix_pref_spe, capacite))