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
from strategies.complexe.strat_greedy_coupe_file import strat_greedy_coupe_file,strat_coupe_file

def strat_adaptive(p, x_init, y_init, nb_lignes, nb_cols, pos_restaurants, seuil,choix_resto,iterations,jours,fin_observ,historique,liste_objet):
    """
    Stratégie en deux phase 
    1) phase d'observation : où le joueur explore les restaurants un par un et s'arrête dès qu'il en trouve un en dessous du seuil d'occupation.
    2) phase du meilleur resto : il fait une moyenne du nombre de personne dans le resto puis il décide d'aller dans le moins pire
    Paramètres :
        - p (Object) : Joueur
        - x_init (int) : Position x du joueur
        - y_init (list->int) : Liste des positions y des joueurs
        - nb_lignes (int) : Nombre de lignes du plateau
        - nb_cols (int) : Nombre de colonnes du plateau
        - pos_restaurants (list -> (int, int)) : Liste des positions des restaurants
        - seuil (int) : Nombre maximum de clients acceptés dans un restaurant avant de le considérer comme "plein"
        - choix_resto (list) : liste de restaurant prix par les clients
        - iterations (int) : nombre de iterations possible
        - jours (int) : le combientieme jour
        - fin_obs (int) : temps d'observation
        - historique (dict) : historique de chaque restaurant 
    
    Retour :
        - choix_resto (int), path (list->int) : Tuple contenant le restaurant choisi et le chemin parcouru
    """
    #greedy_coupe_file
    if jours < fin_observ:
        print(f"Phase d'observation, jours :{jours}")
        return strat_greedy_coupe_file(p, x_init, y_init, nb_lignes, nb_cols, pos_restaurants, seuil,choix_resto,iterations,liste_objet)
    else:
        pos_player = (x_init, y_init[p])
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
        pos_restaurants.sort(key=lambda r: abs(r[0] - pos_player[0]) + abs(r[1] - pos_player[1]))
        scores = {}
        #calcule d'une moyenne du nombre de client pour chaque restaurants
        for resto in pos_restaurants:
            dist = abs(resto[0] - pos_player[0]) + abs(resto[1] - pos_player[1])
            moyen_obs=0
            if len(historique[resto])!=0:
                moyen_obs=sum([len(i) for i in historique[resto]])/len(historique[resto])
            scores[resto] = dist + moyen_obs
        resto_choix = min(scores, key=scores.get)
        new_pos,path = strat_coupe_file(p, x_init, y_init, nb_lignes, nb_cols, pos_restaurants,iterations,liste_objet,resto_choix,pos_player)
        print(f"Le client {p} choisit le restaurant {resto_choix} avec un score de {scores[resto_choix]}, vers {path}")
        return resto_choix, path
