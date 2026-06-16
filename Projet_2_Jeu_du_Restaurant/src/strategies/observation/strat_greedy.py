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




def strat_greedy(p, x_init, y_init, nb_lignes, nb_cols, pos_restaurants, seuil,choix_resto,iterations):
    """
    Stratégie où le joueur explore les restaurants un par un et s'arrête dès qu'il en trouve un en dessous du seuil d'occupation.

    Paramètres :
        - p (Object) : Joueur
        - x_init (int) : Position x du joueur
        - y_init (list->int) : Liste des positions y des joueurs
        - nb_lignes (int) : Nombre de lignes du plateau
        - nb_cols (int) : Nombre de colonnes du plateau
        - pos_restaurants (list -> (int, int)) : Liste des positions des restaurants
        - seuil (list*int) : Nombre maximum que le client accepte , pour rentrer dans le restaurant
        - choix_resto (list) : liste de restaurant prix par les clients
        - iterations (int) : nombre de iterations possible

    Retour :
        - choix_resto (int), path (list->int) : Tuple contenant le restaurant choisi et le chemin parcouru
    """
    path = []
    pos_player = (x_init, y_init[p])
    dic_resto={}
    print("Le client :", p, "avec la stratégie greedy et il commence en :", pos_player)

    pos_restaurants.sort(key=lambda r: abs(r[0] - pos_player[0]) + abs(r[1] - pos_player[1]))

    g = np.ones((nb_lignes, nb_cols), dtype=bool)  # matrice d'accessibilité
    for i in range(nb_lignes):  # on exclut aussi les bordures du plateau
        g[0][i] = False
        g[1][i] = False
        g[nb_lignes - 1][i] = False
        g[nb_lignes - 2][i] = False
        g[i][0] = False
        g[i][1] = False
        g[i][nb_lignes - 1] = False
        g[i][nb_lignes - 2] = False
    pos_init=pos_player
    for resto in range(len(pos_restaurants)):
        tmp=0
        prob = ProblemeGrid2D(pos_init, pos_restaurants[resto], g, 'manhattan')
        chemin = probleme.astar(prob, verbose=False)
        for i in choix_resto:
            if i==pos_restaurants[resto]:
                tmp+=1
        print(f"Visite le restaurant {pos_restaurants[resto]}, nombre de clients: {tmp}")
        if len(path+chemin)>iterations:
            print(f"Decide d'aller dans ce restaurant {resto}")
            return pos_restaurants[resto], path
        path+=chemin
        print(path)
        if tmp < (seuil):
            print(f"Decide d'aller dans ce restaurant {resto}")
            return pos_restaurants[resto], path
        pos_init=pos_restaurants[resto]
        dic_resto[pos_restaurants[resto]]=tmp
    cle_min = min(dic_resto, key=dic_resto.get)
    prob_last = ProblemeGrid2D(pos_init,cle_min, g, 'manhattan')
    chemin_last = probleme.astar(prob_last, verbose=False)
    if (len(chemin_last)+len(path))<iterations:
        return cle_min,path+chemin_last
    return pos_init, path