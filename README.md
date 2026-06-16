# LU3IN025---Intelligence-Artificielle-et-Jeux

Dossier contenant les 3 projets réalisés durant le cours d'Intelligence Artificielle et Jeux

--------------------------------------------------

# 1er Projet : Implémentation des algorithmes de Gale-Shapley

Dans ce projet, on s'intéresse au problème d'affectation des étudiants dans un master informatique de Sorbonne Université.  
Pour cela, nous devons coder l'algorithme de Gale-Shapley pour trouver des affectations stables des étudiants dans les parcours.  
Nous mesurons ensuite le temps de calcul nécessaire avec l'algorithme, ainsi que la complexité de celui-ci.  
Enfin, à l'aide d'un PLNE (Programmation Linéaire en Nombres Entiers), nous devons chercher s'il existe une affectation où tout étudiant a un de ses k premiers choix (pour k fixé).

--------------------------------------------------

# 2ème Projet : Jeu du Restaurant

Dans ce projet, on s'intéresse aux différentes stratégies qu'un joueur peut adopter pour atteindre un restaurant sur une carte prédéfinie (normale sans coupe-file ou avec coupe-file).  
Nous avons donc implémenté plusieurs stratégies différentes :  

### Stratégies non informées
- tétu : toujours aller dans le même restaurant
- stochastique : choisir selon une distribution de probabilité fixe (généralisation de la stratégie aléatoire)

### Stratégies basées sur l'observation (pendant la phase de délibération)
- greedy : tester les restaurants dans un ordre donné, et s'arrêter dans le premier qui ait une occupation en dessous d'un seuil donné

### Stratégies basées sur l'historique (s'appuient sur les expériences des tours précédents)
- fictitious play
- regret-matching

--------------------------------------------------

# 3ème Projet : Robotique

Dans ce projet, on s'intéresse aux différents comportement que peut adopter un robot pour peindre le maximum de cases dans différentes arènes.  
Nous avons donc implémenté plusieurs comportement différents :

### Comportements de base (Braitenberg)
- Avoider : évite les obstacles (murs et robots)
- LoveWall : va vers les murs et ignore les robots
- HateWall : évite les murs et ignore les robots
- LoveBot : va vers les robots et ignore les murs
- HateBot : évite les autres robots et ignore les murs

### Architecture de subsomption
Robot qui va poursuivre les autres robots

### Recherche aléatoire
Robot qui va se déplacer de manière aléatoire

### Algorithme génétique
Implémentation d'un algorithme génétique que l'on va entraîner.  
Pour une génération donnée, on crée un seul enfant à partir d'un parent en modifiant la valeur d'un seul paramètre. Si l'enfant est meilleur que le parent, alors l'enfant remplace le parent, sinon on garde le parent.  
