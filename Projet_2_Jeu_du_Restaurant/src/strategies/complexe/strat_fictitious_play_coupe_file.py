# Importation des fichiers et bibliotheques
import sys
import os
# Path pour pouvoir acceder aux fichiers de src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import random
import numpy as np

from pySpriteWorld.gameclass import Game,check_init_game_done
from pySpriteWorld.spritebuilder import SpriteBuilder
from pySpriteWorld.players import Player
from pySpriteWorld.sprite import MovingSprite
from pySpriteWorld.ontology import Ontology
import pySpriteWorld.glo

from search.grid2D import ProblemeGrid2D
from search import probleme

from strategies.non_informee.strat_stochastique import strat_stochastique


def strat_fictitious_play_coupe_file(p, x_init, y_init, nb_lignes, nb_cols, pos_restaurants, nb_restos, nb_jours, historique_config):
    """
        Cette fonction calcule et retourne le chemin que le joueur p va parcourir pour aller a un restaurant avec la strategie fictitious play

        Parametres :
            - p (Object) : Joueur
            - x_init (int) : Position x du joueur
            - y_init (list->int) : Liste des positions y des joueurs
            - nb_lignes (int) : Nombre de lignes du plateau
            - nb_cols (int) : Nombre de colonnes du plateau
            - pos_restaurants (list -> (int, int)) : Liste des positions des restaurants
            - nb_restos (int) : Nombre de restaurants
            - nb_jours (int) : Nombre de jours passes
            - historique_config (dict[tuple]->int) : Dictionnaire associant une configuration et son nombre d'apparitions au fil des jours

        Return :
            choix_resto (int) : Numero du restaurant choisi
            shortest_path (list->(int, int)) : Liste contenant le chemin que le joueur p va parcourir pour aller au restaurant
    """
    path = []


    # Prediction initiale (jour 0) : choix aleatoire du restaurant
    if (nb_jours == 0):
        return strat_stochastique(p, x_init, y_init, nb_lignes, nb_cols, pos_restaurants, nb_restos)

    # Calcul des probabilites de chaque configuration par rapport aux jours precedents
    probas = {}
    min_proba = 0
    best_config = []

    for config, val in historique_config.items():
        proba = val/nb_jours
        probas[config] = proba

        if (proba < min_proba):
            min_proba = proba
            best_config.append(config)

    pos_player = (x_init,y_init[p])
    print("Le client :", p, "avec la stratégie fictitious play file et il commence en :", pos_player)

    # calcul A* pour le joueur p

    g = np.ones((nb_lignes, nb_cols), dtype=bool)  # une matrice remplie par defaut a True

    for i in range(nb_lignes):  # on exclut aussi les bordures du plateau
        g[0][i] = False
        g[1][i] = False
        g[nb_lignes - 1][i] = False
        g[nb_lignes - 2][i] = False
        g[i][0] = False
        g[i][1] = False
        g[i][nb_lignes - 1] = False
        g[i][nb_lignes - 2] = False

    nb_choix_resto = {}
    for i in range(nb_restos):
        nb_choix_resto[i] = 0

    for config in best_config:
        nb_min_player = min(config)     # Plus petit nombre de joueurs presents dans les restaurants
        ind_min = [i for i, val in enumerate(config) if (val == nb_min_player)]

        # On compte le nombre de fois qu'un resto peut etre choisi dans les meilleures configurations
        for ind_resto in ind_min:
            nb_choix_resto[ind_resto] += 1

    # On prend les restaurants qui apparaissent le plus de fois
    nb_max = max(nb_choix_resto.values())

    best_resto = [i_resto for i_resto, val in nb_choix_resto.items() if (val == nb_max)]
    shortest_path = []

    # Choix du chemin le plus court vers les restaurants avec le moins de joueurs dans les meilleurs configurations de l'historique
    for i in best_resto:
        resto = pos_restaurants[i]

        prob = ProblemeGrid2D(pos_player, resto, g, 'manhattan')
        path = probleme.astar(prob, verbose=False)

        if (shortest_path == []) or (len(path) < len(shortest_path)):
            shortest_path = path
            choix_resto = resto

    resto_choisi,new_chemin=strat_coupe_file(p, x_init, y_init, nb_lignes, nb_cols, pos_restaurants,iterations,liste_objet,choix_resto,pos_player)
    print("Il décide d'aller dans le restaurant ", resto_choisi)
    print("Chemin trouvé:", new_chemin)

    return resto_choisi, new_chemin