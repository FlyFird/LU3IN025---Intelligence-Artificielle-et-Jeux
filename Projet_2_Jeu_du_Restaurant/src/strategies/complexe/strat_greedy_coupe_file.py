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
from strategies.non_informee.strat_coupe_file import strat_coupe_file,recherche_objet

def strat_greedy_coupe_file(p, x_init, y_init, nb_lignes, nb_cols, pos_restaurants, seuil,choix_resto,iterations,liste_objet):
    """
    Stratégie où le joueur explore les restaurants un par un et s'arrête dès qu'il en trouve un en dessous du seuil d'occupation.
    avec l'option coupe file

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
        - liste_objet (dict) : liste de position des objets

    Retour :
        - choix_resto (int), path (list->int) : Tuple contenant le restaurant choisi et le chemin parcouru
    """
    path = []
    pos_player = (x_init, y_init[p])
    print("Le client :", p, "avec la stratégie coupe file et il commence en :", pos_player)
    #décroissant
    pos_restaurants.sort(key=lambda r: abs(r[0] - pos_player[0]) + abs(r[1] - pos_player[1]))
    dic_resto={}
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
        #cherche des objets avant de rejoindre le restaurant
        pos_init,new_chemin=strat_coupe_file(p, x_init, y_init, nb_lignes, nb_cols, pos_restaurants,iterations,liste_objet,pos_restaurants[resto],pos_init)
        if len(path+new_chemin)>iterations:# vérifie s'il a assez d'itérations pour aller aux resto
            print(f"Decide d'aller dans ce restaurant {resto}")
            return pos_restaurants[resto], path
        path+=new_chemin

        #vérifie s'il n'a pas dépassé le seuil
        for i in choix_resto:
            if i==pos_restaurants[resto]:
                tmp+=1
        if tmp < (seuil):
            print(f"Decide d'aller dans ce restaurant {resto}")
            return pos_restaurants[resto], path
        dic_resto[pos_restaurants[resto]]=tmp
    cle_min = min(dic_resto, key=dic_resto.get)
    prob_last = ProblemeGrid2D(pos_init,cle_min, g, 'manhattan')
    chemin_last = probleme.astar(prob_last, verbose=False)
    if (len(chemin_last)+len(path))<iterations:
        return cle_min,path+chemin_last
    return pos_init, path