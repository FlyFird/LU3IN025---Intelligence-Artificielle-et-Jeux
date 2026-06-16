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


# Question 6

def paire_instables(affectation, matrix_pref_etu, matrix_pref_spe):
    liste_paires_instables = []

    # On parcourt l'ensemble des parcours pour trouver un/des paires instables
    for parcours1, liste_etudiants in affectation.items():
        # On parcourt l'ensemble des etudiants affectes au parcours (si il en accepte plusieurs)
        for etudiant in liste_etudiants:
            liste_pref_etu = matrix_pref_etu[int(etudiant)]

            ind_etu_pref1 = 0   # Indice du 1er parcours dans la liste de preference de l'etudiant
            for i in range(len(liste_pref_etu)):
                if (liste_pref_etu[i] == parcours1):
                    ind_etu_pref1 = i

            ind_etu_pref2 = 0   # Indice du 2eme parcours dans la liste de preference de l'etudiant

            # On parcourt l'ensemble des parcours pour comparer les preferences
            for parcours2 in affectation.keys():
                # On doit comparer 2 parcours differents
                if (parcours2 != parcours1):

                    # On recupere l'indice de parcours2 dans les preferences de l'etudiant
                    for i in range(len(liste_pref_etu)):
                        if (liste_pref_etu[i] == parcours2):
                            ind_etu_pref2 = i

                    # Si le parcours affecte est moins bien classe que l'autre parcours
                    if (ind_etu_pref2 < ind_etu_pref1):
                        liste_pref_parcours = matrix_pref_spe[int(parcours2)]

                        # On verifie si le nouveau parcours prefere aussi cet etudiant a ceux deja affectes
                        ind_etu_parcours2 = 0  # Indice de l'etudiant dans la liste de preference de parcours2
                        ind_etu_affecte_parcours2 = 0  # Indice de l'etudiant deja affecte a parcours2

                        # On parcourt l'ensemble des etudiants affectes a parcours2
                        for etudiant_affecte in affectation[parcours2]:
                            # On recupere la position des etudiants de parcours2
                            for i in range(len(liste_pref_parcours)):
                                if (liste_pref_parcours[i] == etudiant):
                                    ind_etu_parcours2 = i
                                elif (liste_pref_parcours[i] == etudiant_affecte):
                                    ind_etu_affecte_parcours2 = i

                            # Si le parcours2 prefere aussi l'etudiant
                            if (ind_etu_parcours2 < ind_etu_affecte_parcours2):
                                liste_paires_instables.append((parcours2, etudiant))

    return liste_paires_instables

affectation = {'0': ['5', '3'], '1': ['4'], '2': ['9'], '3': ['8'], '4': ['10'], '5': ['1'], '6': ['0'], '7': ['7'], '8': ['6', '2']}
#affectation2 = {'0': ['5', '3'], '1': ['4'], '2': ['9'], '3': ['8'], '4': ['10'], '5': ['1'], '6': ['0'], '7': ['6'], '8': ['7', '2']}
affectation2 = {'0': ['0', '1'], '1': ['2'], '2': ['3'], '3': ['4'], '4': ['5'], '5': ['6'], '6': ['7'], '7': ['8'], '8': ['9', '10']}
matrix_pref_etu = read_pref_etu("PrefEtu.txt")
matrix_pref_spe, capacite = read_pref_spe("PrefSpe.txt")

print("Liste des paires instables :", paire_instables(affectation, matrix_pref_etu, matrix_pref_spe))
print("Liste des paires instables :", paire_instables(affectation2, matrix_pref_etu, matrix_pref_spe))


### Test

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
affectation2 = {'0': ['5', '3'], '1': ['4'], '2': ['9'], '3': ['8'], '4': ['10'], '5': ['1'], '6': ['0'], '7': ['6'], '8': ['7', '2']}
affectation3 = {'0': ['0', '1'], '1': ['2'], '2': ['3'], '3': ['4'], '4': ['5'], '5': ['6'], '6': ['7'], '7': ['8'], '8': ['9', '10']}
matrix_pref_etu = read_pref_etu("PrefEtu.txt")
matrix_pref_spe, capacite = read_pref_spe("PrefSpe.txt")

print("Liste des paires instables :", paire_instables(affectation, matrix_pref_etu, matrix_pref_spe))
print("Liste des paires instables :", paire_instables(affectation2, matrix_pref_etu, matrix_pref_spe))
print("Liste des paires instables :", paire_instables(affectation3, matrix_pref_etu, matrix_pref_spe))