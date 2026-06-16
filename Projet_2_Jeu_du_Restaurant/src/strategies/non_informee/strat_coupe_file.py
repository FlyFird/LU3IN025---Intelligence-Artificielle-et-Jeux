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

def recherche_objet(position, list_objet, g, iterations_restantes):
    #recherche d'un objet, autour du client 
    if position in list_objet:
        return None,[]
    for obj in list_objet:
        distance = abs(obj[0] - position[0]) + abs(obj[1] - position[1])
        if distance <= 4 and distance <= iterations_restantes:
            prob_objet = ProblemeGrid2D(position, obj, g, 'manhattan')
            chemin = probleme.astar(prob_objet, verbose=False)
            return obj, chemin
    return None, []

def strat_coupe_file(p, x_init, y_init, nb_lignes, nb_cols, pos_restaurants,iterations,liste_objet,resto,pos_player):
    """
    Stratégie où le joueur explore pour trouver les objets puis il va dans le resto

    Paramètres :
        - p (Object) : Joueur
        - x_init (int) : Position x du jou
        - y_init (list->int) : Liste des positions y des joueurs
        - nb_lignes (int) : Nombre de lignes du plateau
        - nb_cols (int) : Nombre de colonnes du plateau
        - pos_restaurants (list -> (int, int)) : Liste des positions des restaurants
        - iterations (int) : nombre d'iteration max que le client peut faire
        - liste_objet (dict) : liste d'objet
        - resto ((x,y)) : le resto que le client veut visiter
        - pos_player ((x,y)) : position du client

    
    Retour :
        - choix_resto (int), path (list->int) : Tuple contenant le restaurant choisi et le chemin parcouru
    """
    if pos_player==None:
        pos_player = (x_init, y_init[p])
        print("Le client :", p, "avec la stratégie coupe file et il commence en :", pos_player)
    path = []
    if resto==None:
        pos_restaurants.sort(key=lambda r: abs(r[0] - pos_player[0]) + abs(r[1] - pos_player[1]))
        resto=pos_restaurants[0]
    
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
    iterations_restantes = iterations
    objet_int_inv=True
    
    prob = ProblemeGrid2D(pos_player, resto, g, 'manhattan')
    chemin = probleme.astar(prob, verbose=False)
    
    if len(chemin) > iterations_restantes:
        return resto, path
    
    #recherche d'objet autour du client (la recherche se lance pour chaque coordonnée)
    nouveau_chemin = []
    for step in chemin:
        objet_proche, chemin_objet = recherche_objet(step, liste_objet, g, iterations_restantes)
        if objet_proche is None:
            nouveau_chemin.append(step)
            iterations_restantes -= 1
        else:
            if objet_int_inv:
                prob_tmp = ProblemeGrid2D(objet_proche, resto, g, 'manhattan')
                chemin_tmp = probleme.astar(prob_tmp, verbose=False)
                if ((len(path)+len(nouveau_chemin)+len(chemin_objet)+len(chemin_tmp)) <= iterations_restantes):
                    objet_int_inv=False
                    nouveau_chemin.extend(chemin_objet)
                    nouveau_chemin.extend(chemin_tmp)
                    pos_player = objet_proche
                    iterations_restantes -= len(chemin_objet)
                    break
    if iterations_restantes<0:
        return resto,path
    path.extend(nouveau_chemin)
    pos_player = resto 
    print(f"Le client {p} va au restaurant {resto} et le chemin: {path}")
    return resto, path