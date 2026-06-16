# Importation des bibliothèques nécessaires
import matplotlib.pyplot as plt
import sys
import ast
import numpy as np  # Pour calculer la moyenne facilement

liste_strategies = ["strat_tetu", "strat_stochastique", "strat_greedy", "strat_fictitious_play", "strat_regret_matching", "strat_coupe_file", "strat_greedy_coupe_file", "strat_adaptive", "strat_fictitious_play_coupe_file"]

def trace_graphique():
    if len(sys.argv) != 2:
        print("Il faut entrer le nom d'un fichier en argument !")
        sys.exit(1)

    fichier_path = sys.argv[1]
    iterations = []  # Stocke toutes les itérations
    current_iteration = []  # Stocke l'iteration en cours

    with open(fichier_path, 'r') as file:
        for ligne in file:
            ligne = ligne.strip()
            if ligne:  # Si la ligne contient des données
                try:
                    dico = ast.literal_eval(ligne)
                    current_iteration.append(dico)
                except Exception as e:
                    print(f"Erreur de parsing : {e}")
                    continue
            else:  # Ligne vide -> Nouvelle itération
                if current_iteration:
                    iterations.append(current_iteration)
                    current_iteration = []

    # Ajout de la dernière itération si le fichier ne se termine pas par une ligne vide
    if current_iteration:
        iterations.append(current_iteration)

    # Vérification du nombre d'itérations
    nb_iterations = len(iterations)
    if nb_iterations == 0:
        print("Aucune donnée valide trouvée.")
        sys.exit(1)

    # Nombre de jours par iteration
    nb_jours = len(iterations[0])

    # Liste des jours
    jours = list(range(nb_jours))

    # Dictionnaire pour stocker les scores par joueur sur chaque jour
    scores_par_joueur = {}

    for iteration in iterations:
        for jour, dico in enumerate(iteration):
            for id_player, score in dico.items():
                if id_player not in scores_par_joueur:
                    scores_par_joueur[id_player] = [[] for _ in range(nb_jours)]  # Initialisation

                scores_par_joueur[id_player][jour].append(score)  # Ajout du score

    # Calcul des moyennes par jour de chaque joueur
    scores_moyens_par_joueur = {id_player: [np.mean(scores) for scores in jours] for id_player, jours in scores_par_joueur.items()}

    # Tracer une courbe par joueur
    for id_player, scores in scores_moyens_par_joueur.items():
        if (id_player == 10):
            plt.plot(jours, scores, label=f'Player {id_player} - strategie : {liste_strategies[0]}', linewidth=2, linestyle='-')
        else :
            plt.plot(jours, scores, label=f'Player {id_player} - strategie : {liste_strategies[id_player]}', linewidth=2, linestyle='-')

    # Trace graphique
    #plt.plot(jours, points, label='Courbe des scores', color='b', marker='o')

    # Ajout des labels et du titre
    plt.xlabel('Nombre de jours')   # Axe des x
    plt.ylabel('Nombre de points')  # Axe des y
    plt.title('Courbe de la moyenne des points de chaque joueur en fonction des jours qui passent')

    # Ajouter une légende
    plt.legend()

    # Affichage du graphique
    plt.show()


if __name__ == '__main__':
    trace_graphique()