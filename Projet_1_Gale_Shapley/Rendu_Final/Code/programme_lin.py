from gale_shapley import *


# Programme Lineaire


from pulp import*


def solve_assignment(n_etud, n_parcours, capacities, matrice_prefs_etud, k):
    """
    n_etud -> list*int : nombre d etudiant
    n_parcours -> list*int : nombre d option
    matrice_prefs_etud -> list*list*str : les preferences des etudiants
    k -> k premiers choix : k premiers choix

    La fonction permet de savoir s il existe une affctation ou tout etudiant a un de ses k premiers choix ou non

    Return : la solution , si il est trouve sinon None
    """
    model = LpProblem("Assignement des etudiants", LpMinimize)

    # Variables de decision : x[i, j] = 1 si l etudiant i est affecte a l'option j
    #creation d un dictionnaire pour stocker le nom de la variable x_i,j, et declation des variables
    x = {(i, j): LpVariable(f"x_{int(i)},{j}", cat=LpBinary) for i in range(n_etud) for j in range(n_parcours)}
    #print(x)
    # Chaque etudiant est affecté a une seule option
    #Definition de la fonction objectif :x_i,j + ...+ x_i+n,j+m = 1
    for i in range(n_etud):
        model += lpSum(x[i, j] for j in range(n_parcours)) == 1
    # Chaque option respecte sa capacité maximale
    for j in range(n_parcours):
        model += lpSum(x[i, j] for i in range(n_etud)) <= capacities[j]
    #print(model)
    # Chaque etudiant doit etre affecte a l une de ses k premieres options
    for i in range(n_etud):
        allouer_options = matrice_prefs_etud[i][:k]  # On prend les k premieres options preferees
        model += lpSum(x[i, int(j)] for j in allouer_options) == 1
    #print(model)
    # Resolution du probleme
    model.solve(solver=GLPK(msg=True,keepFiles=True))
    if model.status == 1:
        print("Solution trouvée")
        return {(i, int(j)): x[i, int(j)].varValue for i in range(n_etud) for j in range(n_parcours) if x[i, int(j)].varValue > 0.5}
    else:
        print("Aucune solution trouvée")
        return None
def find_min_k(n_etud, n_parcours, matrice_pref_etud,capacite):
    """
    n_students -> list*int : nombre d etudiant
    n_options -> list*int : nombre d option
    matrice_prefs -> list*list*str : les preferences des etudiants

    Fonction qui troue le plus petit k

    Return : une solution maximsant l utilite minimale des etudiants
    """
    for k in range(1, n_parcours + 1):# k+1
        solution= solve_assignment(n_etud, n_parcours, capacite, matrice_pref_etud, k)
        if solution:#si la reponse est different de None alors cest le plus petit k, mais si on ne trouve aucune solution a la fin de la boucle alors il ny a pas de solution
            print(f"Le plus petit k permettant de trouver une solution est de {k}")
            return solution
    print("Aucune solution possible")
    return None


#Meme principe
def solve_max_utile(n_etud, n_parcours, capacities, matrice_prefs_etud, matrice_prefs_parcours):
    """
    n_etud -> list*int : nombre d etudiant
    n_parcours -> list*int : nombre de parcours
    matrice_prefs -> list*list*str : les preferences des etudiants
    k -> k premiers choix : k premiers choix

    La fonction permet de trouver une solution qui maximise la somme des utilites(etudiant et parcours) avec glpk
    En plus il donne la moyenne et le minimun de l utilite des etudiants

    Return : la solution
    """
    model = LpProblem("Maximum Assignement des etudiants",LpMaximize)

     # Variables de decision : x[i, j] = 1 si l etudiant i est affecte a l'option j
    #creation d un dictionnaire pour stocker le nom de la variable x_i,j, et declation des variables
    x = {(i, j): LpVariable(f"x_{int(i)},{j}", cat=LpBinary) for i in range(n_etud) for j in range(n_parcours)}
    #print(x)
    # Chaque etudiant est affecté a une seule option
    #Definition de la fonction objectif :x_i,j + ...+ x_i+n,j+m = 1
    for i in range(n_etud):
        model += lpSum(x[i, j] for j in range(n_parcours)) == 1
    # Chaque option respecte sa capacité maximale
    for j in range(n_parcours):
        model += lpSum(x[i, j] for i in range(n_etud)) <= capacities[j]
    #print(model)
    # Definition de l objectif : maximiser la somme des utilites (etudiants et parcours)
    model += lpSum(int(matrice_prefs_etud[i][j]) * x[i, j] for i in range(n_etud) for j in range(n_parcours)) + \
             lpSum(int(matrice_prefs_parcours[j][i]) * x[i, j] for i in range(n_etud) for j in range(n_parcours))

    # Resolution du problème
    model.solve(solver=GLPK(msg=True,keepFiles=True))

    values = [sum(int(matrice_prefs_etud[i][j]) * x[i, j].varValue for j in range(n_parcours)) for i in range(n_etud)]
    print(f"On obtient l'utilité minimale des étudiants : {min(values)}")
    print(f"On obtient l'utilité moyenne des étudiants : {sum(values) / n_etud}")

    return {(i, j): x[i, j].varValue for i in range(n_etud) for j in range(n_parcours) if x[i, j].varValue > 0.5}


def solve_max_utile_k(n_etud, n_parcours, capacities, matrice_prefs_etud, matrice_prefs_parcours,k):
    """
    n_etud -> list*int : nombre d etudiant
    n_parcours -> list*int : nombre de parcours
    matrice_prefs -> list*list*str : les preferences des etudiants
    k -> k premiers choix : k premiers choix

    La fonction permet de trouver une solution qui maximise la somme des utilites(etudiant et parcours) avec glpk
    En plus il donne la moyenne et le minimun de l utilite des etudiants

    Return : la solution
    """
    model = LpProblem("Maximum Assignement des etudiants",LpMaximize)

     # Variables de decision : x[i, j] = 1 si l etudiant i est affecte a l'option j
    #creation d un dictionnaire pour stocker le nom de la variable x_i,j, et declation des variables
    x = {(i, j): LpVariable(f"x_{int(i)},{j}", cat=LpBinary) for i in range(n_etud) for j in range(n_parcours)}
    #print(x)
    # Chaque etudiant est affecté a une seule option
    #Definition de la fonction objectif :x_i,j + ...+ x_i+n,j+m = 1
    for i in range(n_etud):
        model += lpSum(x[i, int(j)] for j in matrice_prefs_etud[i][:k]) == 1
    # Chaque option respecte sa capacité maximale
    for j in range(n_parcours):
        model += lpSum(x[i, j] for i in range(n_etud)) <= capacities[j]
    #print(model)
    # Definition de l objectif : maximiser la somme des utilites (etudiants et parcours)
    model += lpSum(int(matrice_prefs_etud[i][j]) * x[i, j] for i in range(n_etud) for j in range(n_parcours)) + \
             lpSum(int(matrice_prefs_parcours[j][i]) * x[i, j] for i in range(n_etud) for j in range(n_parcours))

    # Resolution du problème
    model.solve(solver=GLPK(msg=True,keepFiles=True))

    values = [sum(int(matrice_prefs_etud[i][j]) * x[i, j].varValue for j in range(n_parcours)) for i in range(n_etud)]
    print(f"On obtient l'utilité minimale des étudiants : {min(values)}")
    print(f"On obtient l'utilité moyenne des étudiants : {sum(values) / n_etud}")

    return {(i, j): x[i, j].varValue for i in range(n_etud) for j in range(n_parcours) if x[i, j].varValue > 0.5}
