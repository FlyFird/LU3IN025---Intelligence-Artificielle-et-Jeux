# Partie 1

# Question 1

def read_pref_etu(f):
    fichier = open(f, "r")           # Ouverture du fichier en mode lecture "r"
    contenu = fichier.readlines()    # Liste contenant chaque ligne du fichier
    fichier.close()                  # Fermeture du fichier

    nbEtu = int(contenu[0])
    matrix = [[] for i in range(nbEtu)]
    agent=[]
    contenu = contenu[1:]            # On retire la 1ere ligne (nombre d'etudiants)

    for ligne in contenu:
        l = ligne.split()            # Liste contenant chaque element de la ligne separe par un espace
        numEtu = int(l[0])
        nomEtu = l[1]
        agent.append(l[0])
        l = l[2:]                    # On retire les 2 premiers elements (numero + nom)
        matrix[numEtu] = l

    return matrix, agent


def read_pref_spe(f):
    fichier = open(f, "r")           # Ouverture du fichier en mode lecture "r"
    contenu = fichier.readlines()    # Liste contenant chaque ligne du fichier
    fichier.close()                  # Fermeture du fichier
    agent=[]
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
        agent.append(l[0])
        l = l[2:]                    # On retire les 2 premiers elements (numero + nom)
        matrix[numSpe] = l

    return matrix, capacite, agent