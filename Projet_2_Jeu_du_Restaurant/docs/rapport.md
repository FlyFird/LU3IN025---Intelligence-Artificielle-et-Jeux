# Rapport de projet

## Groupe
* Zhou Jérémy 21126962
* Chen Florent 21101813

## Description des choix importants d'implémentation

### Structures de données utilisées :  
* Liste : Stocker les restaurants et les joueurs 
* Dictionnaire : Associer les joueurs avec leurs regrets et comptage des configurations
* Tuple : Structure immuable pour gérer les configurations
  
### Algorithme de recherche de chemin :  
Utilisation de A* afin de trouver le chemin optimal entre le joueur et le restaurant qu'il a choisi en minimisant le coût total des déplacements  
("manhattan" car on est sur un plateau où on peut se déplacer horizontalement ou verticalement seulement)  

### Gestion des fichiers et stockage des données :  
On écrit les résultats des tests dans des fichiers texte afin de pouvoir tracer les courbes associées.  
=> Solution simple et facile d'utilisation.  

### Gestion des erreurs et contraintes :  
On fait beaucoup de structures if then else pour pouvoir gérer les potentielles erreurs.  
De plus, on fait aussi des try catch pour gérer les erreurs du type DivisionByZero afin de gérer les cas dans la stratégie Regret-matching.  

## Description des stratégies proposées

On a implémenté au total 9 stratégies.  

* Les stratégies non-informées :  
  - **Têtu** : Le joueur choisi un restaurant avant le début de la simulation et va dans ce restaurant tous les jours  
  - **Stochastique** : Le joueur choisi aléatoirement un restaurant chaque jour  
  - **Coupe-file** : Le joueur va dans le restaurant le plus proche et cherche un coupe-file à proximité (dans un certain rayon autour de lui)
* Les stratégies basées sur l'observation :  
  - **Greedy** : Le joueur visite les restaurants (du plus proche au plus éloigné) et va dans celui où il y a un nombre de personnes inférieur à un certain seuil  
* Les stratégies basées sur l'historique :  
  - **Fictitious-play** : le 1er jour, le joueur choisit un restaurant aléatoirement, puis il regarde l'historique des restaurants visités tous les jours d'avant et choisit un restaurant où il est peu probable qu'il y ait plus d'un certain nombre de joueurs  
  - **Regret-matching** : le 1er jour, le joueur il choisit un restaurant aléatoirement, puis il regarde les regrets qu'il a pour chaque restaurant les jours précédent et choisit avec une probabilité dépendant du regret sur ce restaurant (plus son regret pour un restaurant est élevé, plus il a de chances d'y aller)  
* Les stratégies complexes :  
  - **Greedy Coupe-file** : Le joueur suit une stratégie greedy mais le joueur va d'abord chercher un coupe-file (si il est assez proche de lui) 
  - **Adaptative** : Le joueur suit une stratégie Greedy Coupe-file pendant la 1ère moitié des jours, puis il fait une moyenne du nombre de personnes dans le restaurant et il décide d'aller dans celui ou il y en a le moins   
  - **Fictitious-play Coupe-file** : Le joueur suis une stratégie fictitious-play mais le joueur va d'abord chercher un coupe-file (si il est assez proche de lui)  

## Description des résultats
Comparaison entre les stratégies. Bien indiquer les cartes utilisées.  

* Tests toutes les stratégies entre eux :  
    ![Courbe_un_chaque](../graphiques/graphe_un_chaque.png)

* Tests de la stratégie **Têtu** contre les autres :  
    - Têtu contre Stochastique :  
    ![Courbe_tetu_vs_stochastique](../graphiques/graphe_tetu_vs_stochastique.png)
    
    - Têtu contre Greedy :  
    ![Courbe_tetu_vs_greedy](../graphiques/graphe_tetu_vs_greedy.png)
    
    - Têtu contre Fictitious-play :  
    ![Courbe_tetu_vs_fictitious_play](../graphiques/graphe_tetu_vs_fictitious_play.png)
    
    - Têtu contre Regret-matching :  
    ![Courbe_tetu_vs_regret_matching](../graphiques/graphe_tetu_vs_regret_matching.png)
    
    - Têtu contre Coupe-file :  
    ![Courbe_tetu_vs_coupe_file](../graphiques/graphe_tetu_vs_coupe_file.png)
    
    - Têtu contre Greedy Coupe-file :  
    ![Courbe_tetu_vs_greedy_coupe_file](../graphiques/graphe_tetu_vs_greedy_coupe_file.png)
    
    - Têtu contre Adaptative :  
    ![Courbe_tetu_vs_adaptative](../graphiques/graphe_tetu_vs_adaptative.png)
    
    - Têtu contre Fictitious-play Coupe-file :  
    ![Courbe_tetu_vs_fictitious-play_coupe_file](../graphiques/graphe_tetu_vs_fictitious_play_coupe_file.png)
    

* Tests de la stratégie **Stochastique** contre les autres :  
    - Stochastique contre Têtu :  
    ![Courbe_stochastique_vs_tetu](../graphiques/graphe_stochastique_vs_tetu.png)
    
    - Stochastique contre Greedy :  
    ![Courbe_stochastique_vs_greedy](../graphiques/graphe_stochastique_vs_greedy.png)
    
    - Stochastique contre Fictitious-play :  
    ![Courbe_stochastique_vs_fictitious_play](../graphiques/graphe_stochastique_vs_fictitious_play.png)
    
    - Stochastique contre Regret-matching :  
    ![Courbe_stochastique_vs_regret_matching](../graphiques/graphe_stochastique_vs_regret_matching.png)
    
    - Stochastique contre Coupe-file :  
    ![Courbe_stochastique_vs_coupe_file](../graphiques/graphe_stochastique_vs_coupe_file.png)
    
    - Stochastique contre Greedy Coupe-file :  
    ![Courbe_stochastique_vs_greedy_coupe_file](../graphiques/graphe_stochastique_vs_greedy_coupe_file.png)
    
    - Stochastique contre Adaptative :  
    ![Courbe_stochastique_vs_adaptative](../graphiques/graphe_stochastique_vs_adaptative.png)
    
    - Stochastique contre Fictitious-play Coupe-file :  
    ![Courbe_stochastique_vs_fictitious-play_coupe_file](../graphiques/graphe_stochastique_vs_fictitious_play_coupe_file.png)
        

* Tests de la stratégie **Greedy** contre les autres :  
    - Greedy contre Têtu :  
    ![Courbe_greedy_vs_tetu](../graphiques/graphe_greedy_vs_tetu.png)
    
    - Greedy contre Stochastique :  
    ![Courbe_greedy_vs_stochastique](../graphiques/graphe_greedy_vs_stochastique.png)
    
    - Greedy contre Fictitious-play :  
    ![Courbe_greedy_vs_fictitious_play](../graphiques/graphe_greedy_vs_fictitious_play.png)
    
    - Greedy contre Regret-matching :  
    ![Courbe_greedy_vs_regret_matching](../graphiques/graphe_greedy_vs_regret_matching.png)
    
    - Greedy contre Coupe-file :  
    ![Courbe_greedy_vs_coupe_file](../graphiques/graphe_greedy_vs_coupe_file.png)
    
    - Greedy contre Greedy Coupe-file :  
    ![Courbe_greedy_vs_greedy_coupe_file](../graphiques/graphe_greedy_vs_greedy_coupe_file.png)
    
    - Greedy contre Adaptative :  
    ![Courbe_greedy_vs_adaptative](../graphiques/graphe_greedy_vs_adaptative.png)
    
    - Greedy contre Fictitious-play Coupe-file :  
    ![Courbe_greedy_vs_fictitious-play_coupe_file](../graphiques/graphe_greedy_vs_fictitious_play_coupe_file.png)
        

* Tests de la stratégie **Fictitious-play** contre les autres :  
    - Fictitious-play contre Têtu :  
    ![Courbe_fictitious_play_vs_tetu](../graphiques/graphe_fictitious_play_vs_tetu.png)
    
    - Fictitious-play contre Stochastique :  
    ![Courbe_fictitious_play_vs_stochastique](../graphiques/graphe_fictitious_play_vs_stochastique.png)
    
    - Fictitious-play contre Greedy :  
    ![Courbe_fictitious_play_vs_greedy](../graphiques/graphe_fictitious_play_vs_greedy.png)
    
    - Fictitious-play contre Regret-matching :  
    ![Courbe_fictitious_play_vs_regret_matching](../graphiques/graphe_fictitious_play_vs_regret_matching.png)
    
    - Fictitious-play contre Coupe-file :  
    ![Courbe_fictitious_play_vs_coupe_file](../graphiques/graphe_fictitious_play_vs_coupe_file.png)
    
    - Fictitious-play contre Greedy Coupe-file :  
    ![Courbe_fictitious_play_vs_greedy_coupe_file](../graphiques/graphe_fictitious_play_vs_greedy_coupe_file.png)
    
    - Fictitious-play contre Adaptative :  
    ![Courbe_fictitious_play_vs_adaptative](../graphiques/graphe_fictitious_play_vs_adaptative.png)
    
    - Fictitious-play contre Fictitious-play Coupe-file :  
    ![Courbe_fictitious_play_vs_fictitious-play_coupe_file](../graphiques/graphe_fictitious_play_vs_fictitious_play_coupe_file.png)
  

* Tests de la stratégie **Regret-matching** contre les autres :  
    - Regret-matching contre Têtu :  
    ![Courbe_regret_matching_vs_tetu](../graphiques/graphe_regret_matching_vs_tetu.png)
    
    - Regret-matching contre Stochastique :  
    ![Courbe_regret_matching_vs_stochastique](../graphiques/graphe_regret_matching_vs_stochastique.png)
    
    - Regret-matching contre Greedy :  
    ![Courbe_regret_matching_vs_greedy](../graphiques/graphe_regret_matching_vs_greedy.png)
    
    - Regret-matching contre Fictitious-play :  
    ![Courbe_regret_matching_vs_fictitious_play](../graphiques/graphe_regret_matching_vs_fictitious_play.png)
    
    - Regret-matching contre Coupe-file :  
    ![Courbe_regret_matching_vs_coupe_file](../graphiques/graphe_regret_matching_vs_coupe_file.png)
    
    - Regret-matching contre Greedy Coupe-file :  
    ![Courbe_regret_matching_vs_greedy_coupe_file](../graphiques/graphe_regret_matching_vs_greedy_coupe_file.png)
    
    - Regret-matching contre Adaptative :  
    ![Courbe_regret_matching_vs_adaptative](../graphiques/graphe_regret_matching_vs_adaptative.png)
    
    - Regret-matching contre Fictitious-play Coupe-file :  
    ![Courbe_regret_matching_vs_fictitious-play_coupe_file](../graphiques/graphe_regret_matching_vs_fictitious_play_coupe_file.png)
          

* Tests de la stratégie **Coupe-file** contre les autres :  
    - Coupe-file contre Têtu :  
    ![Courbe_coupe_file_vs_tetu](../graphiques/graphe_coupe_file_vs_tetu.png)
    
    - Coupe-file contre Stochastique :  
    ![Courbe_coupe_file_vs_stochastique](../graphiques/graphe_coupe_file_vs_stochastique.png)
    
    - Coupe-file contre Greedy :  
    ![Courbe_coupe_file_vs_greedy](../graphiques/graphe_coupe_file_vs_greedy.png)
    
    - Coupe-file contre Fictitious-play :  
    ![Courbe_coupe_file_vs_fictitious_play](../graphiques/graphe_coupe_file_vs_fictitious_play.png)
    
    - Coupe-file contre Regret-matching :  
    ![Courbe_coupe_file_vs_regret_matching](../graphiques/graphe_coupe_file_vs_regret_matching.png)
    
    - Coupe-file contre Greedy Coupe-file :  
    ![Courbe_coupe_file_vs_greedy_coupe_file](../graphiques/graphe_coupe_file_vs_greedy_coupe_file.png)
    
    - Coupe-file contre Adaptative :  
    ![Courbe_coupe_file_vs_adaptative](../graphiques/graphe_coupe_file_vs_adaptative.png)
    
    - Coupe-file contre Fictitious-play Coupe-file :  
    ![Courbe_coupe_file_vs_fictitious-play_coupe_file](../graphiques/graphe_coupe_file_vs_fictitious_play_coupe_file.png)
              

* Tests de la stratégie **Greedy Coupe-file** contre les autres :  
    - Greedy Coupe-file contre Têtu :  
    ![Courbe_greedy_coupe_file_vs_tetu](../graphiques/graphe_greedy_coupe_file_vs_tetu.png)
    
    - Greedy Coupe-file contre Stochastique :  
    ![Courbe_greedy_coupe_file_vs_stochastique](../graphiques/graphe_greedy_coupe_file_vs_stochastique.png)
    
    - Greedy Coupe-file contre Greedy :  
    ![Courbe_greedy_coupe_file_vs_greedy](../graphiques/graphe_greedy_coupe_file_vs_greedy.png)
    
    - Greedy Coupe-file contre Fictitious-play :  
    ![Courbe_greedy_coupe_file_vs_fictitious_play](../graphiques/graphe_greedy_coupe_file_vs_fictitious_play.png)
    
    - Greedy Coupe-file contre Regret-matching :  
    ![Courbe_greedy_coupe_file_vs_regret_matching](../graphiques/graphe_greedy_coupe_file_vs_regret_matching.png)
    
    - Greedy Coupe-file contre Coupe-file :  
    ![Courbe_greedy_coupe_file_vs_coupe_file](../graphiques/graphe_greedy_coupe_file_vs_coupe_file.png)
    
    - Greedy Coupe-file contre Adaptative :  
    ![Courbe_greedy_coupe_file_vs_adaptative](../graphiques/graphe_greedy_coupe_file_vs_adaptative.png)
    
    - Greedy Coupe-file contre Fictitious-play Coupe-file :  
    ![Courbe_greedy_coupe_file_vs_fictitious-play_coupe_file](../graphiques/graphe_greedy_coupe_file_vs_fictitious_play_coupe_file.png)
                  

* Tests de la stratégie **Adaptative** contre les autres :  
    - Adaptative contre Têtu :  
    ![Courbe_adaptative_vs_tetu](../graphiques/graphe_adaptative_vs_tetu.png)
    
    - Adaptative contre Stochastique :  
    ![Courbe_adaptative_vs_stochastique](../graphiques/graphe_adaptative_vs_stochastique.png)
    
    - Adaptative contre Greedy :  
    ![Courbe_adaptative_vs_greedy](../graphiques/graphe_adaptative_vs_greedy.png)
    
    - Adaptative contre Fictitious-play :  
    ![Courbe_adaptative_vs_fictitious_play](../graphiques/graphe_adaptative_vs_fictitious_play.png)
    
    - Adaptative contre Regret-matching :  
    ![Courbe_adaptative_vs_regret_matching](../graphiques/graphe_adaptative_vs_regret_matching.png)
    
    - Adaptative contre Coupe-file :  
    ![Courbe_adaptative_vs_coupe_file](../graphiques/graphe_adaptative_vs_coupe_file.png)
    
    - Adaptative contre Greedy Coupe-file :  
    ![Courbe_adaptative_vs_greedy_coupe_file](../graphiques/graphe_adaptative_vs_greedy_coupe_file.png)
    
    - Adaptative contre Fictitious-play Coupe-file :  
    ![Courbe_adaptative_vs_fictitious-play_coupe_file](../graphiques/graphe_adaptative_vs_fictitious_play_coupe_file.png)
                     

* Tests de la stratégie **Fictitious-play Coupe-file** contre les autres :  
    - Fictitious-play Coupe-file contre Têtu :  
    ![Courbe_fictitious-play_coupe_file_vs_tetu](../graphiques/graphe_fictitious-play_coupe_file_vs_tetu.png)
    
    - Fictitious-play Coupe-file contre Stochastique :  
    ![Courbe_fictitious-play_coupe_file_vs_stochastique](../graphiques/graphe_fictitious-play_coupe_file_vs_stochastique.png)
    
    - Fictitious-play Coupe-file contre Greedy :  
    ![Courbe_fictitious-play_coupe_file_vs_greedy](../graphiques/graphe_fictitious-play_coupe_file_vs_greedy.png)
    
    - Fictitious-play Coupe-file contre Fictitious-play :  
    ![Courbe_fictitious-play_coupe_file_vs_fictitious_play](../graphiques/graphe_fictitious-play_coupe_file_vs_fictitious_play.png)
    
    - Fictitious-play Coupe-file contre Regret-matching :  
    ![Courbe_fictitious-play_coupe_file_vs_regret_matching](../graphiques/graphe_fictitious-play_coupe_file_vs_regret_matching.png)
    
    - Fictitious-play Coupe-file contre Coupe-file :  
    ![Courbe_fictitious-play_coupe_file_vs_coupe_file](../graphiques/graphe_fictitious-play_coupe_file_vs_coupe_file.png)
    
    - Fictitious-play Coupe-file contre Greedy Coupe-file :  
    ![Courbe_fictitious-play_coupe_file_vs_greedy_coupe_file](../graphiques/graphe_fictitious-play_coupe_file_vs_greedy_coupe_file.png)
    
    - Fictitious-play Coupe-file contre Adaptative :  
    ![Courbe_fictitious-play_coupe_file_vs_adaptative](../graphiques/graphe_fictitious-play_coupe_file_vs_adaptative.png)