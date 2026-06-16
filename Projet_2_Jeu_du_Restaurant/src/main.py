# -*- coding: utf-8 -*-

# Nicolas, 2024-02-09
from __future__ import absolute_import, print_function, unicode_literals

import random 
import numpy as np
import sys
from itertools import chain
from pathlib import Path

import pygame

from pySpriteWorld.gameclass import Game,check_init_game_done
from pySpriteWorld.spritebuilder import SpriteBuilder
from pySpriteWorld.players import Player
from pySpriteWorld.sprite import MovingSprite
from pySpriteWorld.ontology import Ontology
import pySpriteWorld.glo

from search.grid2D import ProblemeGrid2D
from search import probleme


# Importation des strategies
from strategies.non_informee.strat_tetu import strat_tetu
from strategies.non_informee.strat_stochastique import strat_stochastique
from strategies.non_informee.strat_coupe_file import strat_coupe_file
from strategies.observation.strat_greedy import strat_greedy
from strategies.historique.strat_fictitious_play import strat_fictitious_play
from strategies.historique.strat_regret_matching import strat_regret_matching
from strategies.complexe.strat_greedy_coupe_file import strat_greedy_coupe_file
from strategies.complexe.strat_adaptive import strat_adaptive
from strategies.complexe.strat_fictitious_play_coupe_file import strat_fictitious_play_coupe_file


# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'restaurant-map2'
    #game = Game('./Cartes/' + name + '.json', SpriteBuilder)
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 50 # nb de pas max par episode
    nb_jours = 30    # nombre de jours dans la simulation
    if len(sys.argv) == 3:
        iterations = int(sys.argv[1])
        nb_jours = int(sys.argv[2])
    print ("Iterations: ")
    print (iterations)
    print ("Nombre de jours: ")
    print (nb_jours)

    init()
    

    
    #-------------------------------
    # Initialisation
    #-------------------------------
    
    nb_lignes = game.spriteBuilder.rowsize
    nb_cols = game.spriteBuilder.colsize
    assert nb_lignes == nb_cols # a priori on souhaite un plateau carre
    lMin=2  # les limites du plateau de jeu (2 premieres lignes utilisees pour stocker les objets)
    lMax=nb_lignes-2
    cMin=2
    cMax=nb_cols-2
    
    seuil = 2       # Seuil a fixer pour la strategie greedy
   
    
    players = [o for o in game.layers['joueur']]
    nb_players = len(players)

    pos_restaurants = [(3,4),(3,7),(3,10),(3,13),(3,16)] # 5 restaurants positionnes
    nb_restos = len(pos_restaurants)
    capacity = [1]*nb_restos

    coupe_files = [o for o in game.layers["ramassable"]] # a utiliser dans le cas de la variante coupe-file
    nb_coupe_files= len(coupe_files)
    historique={i:[] for i in pos_restaurants}
    players_points = {j: 0 for j in range(nb_players)} # Initialisation des points de chaque joueur

    #-------------------------------
    # Fonctions permettant de récupérer les listes des coordonnées
    # d'un ensemble d'objets ou de joueurs
    #-------------------------------
    
    def item_states(items):
        # donne la liste des coordonnees des items
        return [o.get_rowcol() for o in items]
    
    def player_states(players):
        # donne la liste des coordonnees des joueurs
        return [p.get_rowcol() for p in players]
    
   
    #-------------------------------
    # Rapport de ce qui est trouve sut la carte
    #-------------------------------
    print("lecture carte")
    print("-------------------------------------------")
    print('joueurs:', nb_players)
    print("restaurants:",nb_restos)
    print("lignes:", nb_lignes)
    print("colonnes:", nb_cols)
    print("coup_files:",nb_coupe_files)
    print("-------------------------------------------")

    #-------------------------------
    # Carte demo 
    # 8 joueurs
    # 5 restos
    #-------------------------------
    
        
    #-------------------------------

    #-------------------------------
    # Fonctions definissant les positions legales et placement aléatoire
    #-------------------------------

    
    def legal_position(pos):
        row,col = pos
        # une position legale est dans la carte et pas sur un objet deja pose ni sur un joueur ni sur un resto
        return ((pos not in item_states(coupe_files)) and (pos not in player_states(players)) and (pos not in pos_restaurants) and row>lMin and row<lMax-1 and col>=cMin and col<cMax)
    
    def draw_random_location():
        # tire au hasard un couple de positions permettant de placer un item
        while True:
            random_loc = (random.randint(lMin,lMax),random.randint(cMin,cMax))
            if legal_position(random_loc):
                return(random_loc)

    def players_in_resto(r):
        """
        :param r: id of the resto
        :return: id of players in resto
        """
        are_here = []
        pos = pos_restaurants[r]
        for i in range(0,nb_players):
            if players[i].get_rowcol() == pos:
                are_here.append(i)
        return are_here

    def nb_players_in_resto(r):
        """
        :param r: id of resto
        :return: int number of players currently here
        """
        return len(players_in_resto(r))
        
    
    # Fonctions de generations des configurations possibles (nombre de joueurs dans chaque restaurant)
    def genere_config(nb_joueurs_restants, current_config, num_resto, nb_restos, liste_config):
        # Si tous les joueurs sont répartis, ajoute la configuration a la liste des configurations
        if num_resto == nb_restos:
            if nb_joueurs_restants == 0:
                liste_config.append(tuple(current_config))
            return

        # Pour chaque restaurant, on essaye de mettre un nombre de joueurs
        for i in range(nb_joueurs_restants + 1):
            current_config[num_resto] = i
            genere_config(nb_joueurs_restants - i, current_config, num_resto + 1, nb_restos, liste_config)
        
    def genere_all_config(nb_restos, nb_players):
        liste_config = []
        
        genere_config(nb_players, [0]*nb_restos, 0, nb_restos, liste_config)
        
        return liste_config
    
    
    # Definition des strategies possibles
    liste_strategies = [strat_tetu, strat_stochastique, strat_greedy, strat_fictitious_play, strat_regret_matching, strat_coupe_file, strat_greedy_coupe_file, strat_adaptive, strat_fictitious_play_coupe_file]
          
    nb_strategies = len(liste_strategies)
    
    # Restaurant fixe attribue a chaque joueur (strat tetu)
    resto_fixe = [random.randint(0,nb_restos-1) for i in range(nb_players)]
    
    # Liste des configurations possibles de joueurs dans les restaurants
    liste_configurations = genere_all_config(nb_restos, nb_players)
    
    # Initialisation de l'historique des configurations
    historique_config = {}
    for config in liste_configurations:
        historique_config[config] = 0
    
    # Initialisation des regrets de chaque joueur
    score_player = [0 for i in range(nb_players)]
    score_player_autre = [[0 for i in range(nb_restos)] for j in range(nb_players)]
    regrets_players = {}
    for p in range(nb_players):
        regrets_players[p] = [0 for i in range(nb_restos)]
    
    resto_prec = [None for i in range(nb_players)]
    
    # Boucle principale
    for k in range(nb_jours):
        #-------------------------------
        # On place tous les coupe_files du bord au hasard
        #-------------------------------
                        
        for o in coupe_files:
            (x1,y1) = draw_random_location()
            o.set_rowcol(x1,y1)
            game.mainiteration()

        pos_objet={i.get_rowcol():i for i in coupe_files} # coco des objets

        #-------------------------------
        # On place tous les joueurs au hasard sur la ligne du bas
        #-------------------------------
        y_init = [3,5,7,9,11,13,15,17]
        x_init = 18
        random.shuffle(y_init)
        for i in range(0,nb_players):
            players[i].set_rowcol(x_init,y_init[i])
            game.mainiteration()
        
    
        # -------------------------------
        # Choix de la strategie de chaque joueur
        # -------------------------------
        
        choix_resto = []
        path = []
        
        for p in range(0, nb_players):                 
            
            # On choisit une strategie aleatoirement pour chaque joueur
            #strat = liste_strategies[random.randint(0, nb_strategies-1)]
            strat = liste_strategies[p]
            
            # Test 1 strategie sur 1 joueur contre une strategie sur tous les autres joueurs
            if (p == 0):
                strat = liste_strategies[0]     # Choix de la strategie du joueur 0
            else :
                strat = liste_strategies[1]     # Choix de la strategie des autres joueurs
            
            if (strat == strat_tetu):
                resto_choisi, chemin = strat(p, x_init, y_init, nb_lignes, nb_cols, pos_restaurants, nb_restos, resto_fixe[p])
            elif (strat == strat_stochastique):
                resto_choisi, chemin = strat(p, x_init, y_init, nb_lignes, nb_cols, pos_restaurants, nb_restos)
            elif (strat == strat_greedy):
                resto_choisi, chemin = strat(p, x_init, y_init, nb_lignes, nb_cols, pos_restaurants, seuil, choix_resto, iterations)
            elif (strat == strat_fictitious_play):
                resto_choisi, chemin = strat(p, x_init, y_init, nb_lignes, nb_cols, pos_restaurants, nb_restos, k, historique_config)
            elif (strat == strat_regret_matching):
                resto_choisi, chemin = strat(p, x_init, y_init, nb_lignes, nb_cols, pos_restaurants, nb_restos, k, regrets_players[p], resto_prec[p])
            elif (strat == strat_coupe_file):
                resto_choisi, chemin = strat(p, x_init, y_init, nb_lignes, nb_cols, pos_restaurants, iterations, pos_objet,None,None)
            elif (strat == strat_greedy_coupe_file):
                resto_choisi, chemin = strat(p, x_init, y_init, nb_lignes, nb_cols, pos_restaurants, seuil, choix_resto, iterations, pos_objet) 
            elif (strat == strat_adaptive):
                resto_choisi, chemin = strat(p, x_init, y_init, nb_lignes, nb_cols, pos_restaurants, seuil,choix_resto,iterations,k,nb_jours/2,historique,pos_objet)
            elif (strat == strat_fictitious_play_coupe_file):
                resto_choisi, chemin = strat(p, x_init, y_init, nb_lignes, nb_cols, pos_restaurants, nb_restos, k, historique_config)
                
            choix_resto.append(resto_choisi)
            path.append(chemin)
        
    
        #-------------------------------
        # Boucle principale de déplacements 
        #-------------------------------
        
        for i in range(iterations):
            
            for j in range(0,nb_players):
    
                # on fait bouger chaque joueur jusqu'à son but
                # en suivant le chemin trouve avec A*
    
                if i<len(path[j]): # si le joueur n'est pas deja arrive
                    (row,col) = path[j][i]
                    players[j].set_rowcol(row, col)
                    #print("pos joueur:", j,  row, col)
                    if (row,col) in pos_objet:
                        players[j].ramasse(game.layers)
                        print("Inventory du joueur : ",players[j]," ; ",players[j].getInventory())
                        pos_objet.pop((row,col))
                # mise à jour du pleateau de jeu
                #game.mainiteration()
    
    
    
            # mise à jour du pleateau de jeu
            game.mainiteration()
    
        # -------------------------------
        # Calcul des scores
        # -------------------------------
    
    
        # calcul du nombre de joueurs sur chaque resto
    
        attendance = [0]*nb_restos
        for r in range(0,nb_restos):
            attendance[r]=nb_players_in_resto(r)
    
        print(attendance)
    
    
        # calcul du service et points
        #TODO
        
        for r in range(nb_restos): # le calcul des points en fonction des joueurs qui ont mangé ou non
            nb_served = min(capacity[r], len(players_in_resto(r)))
            print("Dans le resto : ",players_in_resto(r))
            if len(players_in_resto(r))==1:
                served_players = random.sample(players_in_resto(r), nb_served)
            else:
                etat_coupefile=True
                player_manger=players_in_resto(r)
                for i in players_in_resto(r):
                    if len(players[i].getInventory())>0:
                        if etat_coupefile:
                            player_manger=[]
                            etat_coupefile=False
                        player_manger.append(i)
                        players[i].depose(game.layers)
                served_players = random.sample(player_manger, nb_served)
            historique[pos_restaurants[r]].append(players_in_resto(r))
            for j in served_players:
                players_points[j] += 1

        fichier = open("donnee_resultat/resultat_test.txt", "a")
        fichier.write(str(players_points)+"\n")
        fichier.close()
        
        print("points : ", players_points)
        #print("points : ", points)
        
    
        # -------------------------------
        # Mise a jour du restaurant visite par les joueurs
        # -------------------------------
        
        for p in range(nb_players):
            resto_prec[p] = path[p][-1]
    
        # -------------------------------
        # Mise a jour de l'historique
        # -------------------------------
        
        config_jour = []
        for r in range(nb_restos):
            config_jour.append(nb_players_in_resto(r))
        
        for c in historique_config.keys():
            config_corresp = []
            for i in c:
                config_corresp.append(i)
            
            if (config_jour == config_corresp):
                historique_config[c] += 1
        
        # -------------------------------
        # Mise a jour des regrets
        # -------------------------------
        
        # On met a jour les scores de chaque joueur pour le resto choisi ce tour ainsi les autres
        for r in range(nb_restos):
            for p in range(nb_players):
                if (nb_players_in_resto(r) == 0):
                    proba = 1
                else :
                    proba = capacity[r] / nb_players_in_resto(r)
                    
                if (pos_restaurants[r] == path[p][-1]):
                    score_player[p] += proba
                
                score_player_autre[p][r] += proba
        
        for p in range(nb_players):
            players[p].depose(game.layers)#vide son inventaire avant le jour suivant
            for r in range(nb_restos):
                score_t = score_player[p]
                score_ts = score_player_autre[p][r]
                
                regrets_players[p][r] += (score_t - score_ts)
        
        
    pygame.quit()

    
    #-------------------------------

    
   

if __name__ == '__main__':
    for i in range(5):
        main()
        fichier = open("donnee_resultat/resultat_test.txt", "a")
        fichier.write("\n")
        fichier.close()


