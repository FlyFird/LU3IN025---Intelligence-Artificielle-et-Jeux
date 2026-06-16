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


def strat_tetu(p, x_init, y_init, nb_lignes, nb_cols, pos_restaurants, nb_restos, resto):
    """
        Cette fonction calcule et retourne le chemin que le joueur va parcourir pour aller au restaurant choisi

        Parametres :
            - p (Object) : Joueur
            - x_init (int) : Position x du joueur
            - y_init (list->int) : Liste des positions y des joueurs
            - nb_lignes (int) : Nombre de lignes du plateau
            - nb_cols (int) : Nombre de colonnes du plateau
            - pos_restaurants (list -> (int, int)) : Liste des positions des restaurants
            - nb_restos (int) : Nombre de restaurants
            - resto (int) : Numero du restaurant ou le joueur veut aller

        Return :
            choix_resto (int) : Numero du restaurant choisi
            path (list->(int, int)) : Liste contenant le chemin que le joueur p va parcourir pour aller au restaurant resto
    """
    path = []
    choix_resto = pos_restaurants[resto]
    pos_player = (x_init,y_init[p])

    print("Le client :", p, "avec la stratégie tétu et il commence en :", pos_player)
    print("Il décicde d'aller dans le restaurant : ", choix_resto)
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