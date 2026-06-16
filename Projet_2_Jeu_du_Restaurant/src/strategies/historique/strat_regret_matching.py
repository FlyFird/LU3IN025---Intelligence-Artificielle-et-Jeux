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


def strat_regret_matching(p, x_init, y_init, nb_lignes, nb_cols, pos_restaurants, nb_restos, nb_jours, regret_player, resto_prec):
    """
        Cette fonction calcule et retourne le chemin que le joueur p va parcourir pour aller a un restaurant avec la strategie regret-matching

        Parametres :
            - p (Object) : Joueur
            - x_init (int) : Position x du joueur
            - y_init (list->int) : Liste des positions y des joueurs
            - nb_lignes (int) : Nombre de lignes du plateau
            - nb_cols (int) : Nombre de colonnes du plateau
            - pos_restaurants (list -> (int, int)) : Liste des positions des restaurants
            - nb_restos (int) : Nombre de restaurants
            - nb_jours (int) : Nombre de jours passes
            - regret_player (list->int) : Liste representant le regret du joueur par rapport a chaque restaurant au fil des jours
            - resto_prec (int, int) : Position du restaurant visite le jour precedent

        Return :
            choix_resto (int) : Numero du restaurant choisi
            path (list->(int, int)) : Liste contenant le chemin que le joueur p va parcourir pour aller au restaurant
    """
    path = []

    # Prediction initiale (jour 0) : choix aleatoire du restaurant
    if (nb_jours == 0):
        return strat_stochastique(p, x_init, y_init, nb_lignes, nb_cols, pos_restaurants, nb_restos)

    proba_resto = [0 for i in range(nb_restos)]
    choix_resto = None

    # Calcul de la somme des regrets
    somme_regrets = sum(max(0, regret) for regret in regret_player)
    if somme_regrets == 0:
        proba_resto = [1 / nb_restos] * nb_restos
    else:
        proba_resto = [max(0, regret_player[r]) / somme_regrets for r in range(nb_restos)]

    try:
        choix_index = np.random.choice(range(nb_restos), p=proba_resto)
        choix_resto = pos_restaurants[choix_index]
    except ValueError:
        # Sécurité si un problème survient
        choix_resto = random.choice(pos_restaurants)

    pos_player = (x_init,y_init[p])
    print("Le client :", p, "avec la stratégie regret matching et il commence en :", pos_player)
    print("Il décide d'aller dans le restaurant : ", choix_resto)
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

    prob = ProblemeGrid2D(pos_player, choix_resto, g, 'manhattan')
    path = probleme.astar(prob, verbose=False)
    print("Chemin trouvé:", path)

    return choix_resto, path