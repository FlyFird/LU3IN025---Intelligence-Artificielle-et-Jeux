# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : _________
#  Prénom Nom No_étudiant/e : Anabelle PHAM 21212689
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import * 
from robot import sensor_front, sensor_front_left, sensor_front_right, sensor_left, sensor_right
import math
import random

nb_robots = 0

class Robot_player(Robot):

    team_name = "Azouaoui_Pham"  # vous pouvez modifier le nom de votre équipe
    robot_id = -1             # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory = 0                # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        if self.robot_id == 0 :
            # Stratégie 1 : Avoider rapide optimisé
            
            # Opti par arbre genetique
            #randomeSearch2 (-1,0,1) map 0 : 
            #param = [1, 0, 0, 0.9, 1, 0, -1, -1]
            # randomeSearch2 (-1,0,1) map 1 :
            param = [0, 1, 0, 1, 1, -1, -1, 0]  # BEST FOR NOW
            # randomeSearch2 (-1,0,1) map 2 :
            # param = [-1, 0, 0, 1, -1, -1, -1, 0.5]
            # randomeSearch2 (-1,0,1) map 3 :
            #param = [-0.2, 1, 1, 0, -1, 0, 1, -1] # AUSSI 
            # randomeSearch2 (-1,0,1) map 4 :
            #param = [0.2, 0, 1, 1, 1, 0, -1, 0]
            
            # randomeSearch2 à intervalle de 0.1 map 0 :
            #param = 0
            # randomeSearch2 intervalle de 0.1 map 1 :
            #param = 0
            # randomeSearch2 intervalle de 0.1map 2 :
            #param = 0
            # randomeSearch2 intervalle de 0.1 map 3 :
            #param = 0
            # randomeSearch2 intervalle de 0.1 map 4 :
            #param = 0
            
            # selection mu=1 lambda=1 et mutation (-1, 0, 1) map 0 :
            #param =  [-0.2, 1, -0.4, 0, -0.6, 0.2, 0.7, 0]
            # selection mu=1 lambda=1 et mutation (-1, 0, 1) map 1 :
            #param =  [0, 1, -1, 1, 0, -0.6, 1, 0]
            # selection mu=1 lambda=1 et mutation (-1, 0, 1) map 2 :
            #param =  [0.5, -1, 1, -1, -1, 1, 0, 1]
            # selection mu=1 lambda=1 et mutation (-1, 0, 1) map 3 :
            #param =  
            # selection mu=1 lambda=1 et mutation (-1, 0, 1) map 4 :
            #param =  [-0.8, 1, 0.1, -1, -0.0, -1, -1, -0.1]
            
            # selection mu=1 lambda=1 et mutation à intervalle de 0.1 map 0 :
            #param =  [-0.1, 0.7, -0.0, -0.4, 0.1, -0.1, -0.1, 0.4]
            # selection mu=1 lambda=1 et mutation à intervalle de 0.1 map 1 :
            #param =  [-0.8, 0.5, 0.0, -1.0, 0.7, 0.5, 0.1, -0.3]
            # selection mu=1 lambda=1 et mutation à intervalle de 0.1 map 2 :
            #param =  [-0.9, -0.3, 0.1, 0.2, -0.3, 0.7, 0.7, -0.2]
            # selection mu=1 lambda=1 et mutation à intervalle de 0.1 map 3 :
            #param =  0
            # selection mu=1 lambda=1 et mutation à intervalle de 0.1 map 4 :
            #param =  [-0.3, 0.6, 0.6, -1.0, 1.0, -0.7, -0.4, 0.6]

            """if self.memory % 10 != 0:"""
            translation = (
                param[0]
                + param[1] * sensors[0]  # front
            )

            rotation = (
                param[2]
                + param[3] * sensors[1]  # front-left
                + param[4] * sensors[0]  # front
                + param[5] * sensors[7]  # front-right
                + param[6] * sensors[6]  # right
                + param[7] * sensors[2]  # left
                + (random.random() - 0.5)
            )
            """else : 
                # Phase "anti-bloquage" toutes les 10 steps améliorée
                
                # Si capteur gauche (6) très proche -> virer à droite fort
                if sensors[6] < 0.3:
                    translation = 0.5
                    rotation = -1.0
                # Si capteur droit (2) très proche -> virer à gauche fort
                elif sensors[2] < 0.3:
                    translation = 0.5
                    rotation = 1.0
                else:
                    # Chercher l'index du capteur avec la plus grande distance (plus éloigné du mur)
                    best_sensor_index = sensors.index(max(sensors))

                    if best_sensor_index in [0]:
                        translation = 1.0
                        rotation = 0.0
                    elif best_sensor_index in [1,2,3]:
                        translation = 0.5
                        rotation = -1.0  # Tourner à droite
                    elif best_sensor_index in [5,6,7]:
                        translation = 0.5
                        rotation = 1.0   # Tourner à gauche
                    else:  # best_sensor_index == 4
                        translation = 0.0
                        rotation = 1.0  # Demi-tour"""
            
            return translation, rotation, False

        elif self.robot_id == 1:
            # Stratégie 2 : Subsomption => Eviter les murs jusqu'a croiser un robot, si on croise un robot, le suivre
            
            sensor_to_wall = []
            sensor_to_robot = []

            for i in range(8):
                if sensor_view[i] == 1: 
                    sensor_to_wall.append(sensors[i])
                    sensor_to_robot.append(1.0)  
                elif sensor_view[i] == 2 and sensor_team[i] != self.team:  
                    sensor_to_wall.append(1.0)  
                    sensor_to_robot.append(sensors[i])
                else:  
                    sensor_to_wall.append(1.0)
                    sensor_to_robot.append(1.0)

            # Comportement de subsomption
            if sum(sensor_to_robot) < 8:  # On detecte un robot 
                # Suivre le robot détecté
                PT = [1.0, 0.8, 0.5, 0.1, 0.0, 0.1, 0.5, 0.8]
                PR = [0., 1., 1., 1., 0., -1., -1., -1.]
                translation = sum([ (1.-sensor)*p for sensor, p in zip(sensor_to_robot, PT) ]) + 0.2
                rotation = sum([ (1.-sensor)*p for sensor, p in zip(sensor_to_robot, PR) ])+ (random.random()-0.5)*1.
            else :
 
                # Éviter les murs
                param =  [0.2, 0.0, 0.8, 0.0, 0.0, 0.0 , random.random()-0.5, 0.3, 0.0, -0.3, -0.3, 0.3]

                translation = (
                    param[0]
                    + param[1] * sensors[1]  # front-left
                    + param[2] * sensors[0]  # front
                    + param[3] * sensors[7]  # front-right
                    + param[4] * sensors[6]  # right
                    + param[5] * sensors[2]  # left
                )

                rotation = (
                    param[6]
                    + param[7] * sensors[1]  # front-left
                    + param[8] * sensors[0]  # front
                    + param[9] * sensors[7]  # front-right
                    + param[10] * sensors[6]  # right
                    + param[11] * sensors[2]  # left
                )
               
            return translation, rotation, False

        elif self.robot_id == 2:
            # STRATÉGIE 3 : ARBRE DE DÉCISION 
            
            """
            |-- Capteurs avant bloqués ?
            |     |-- NON --> avancer normalement
            |     |-- OUI --> mémoire++
            |         |-- mémoire == 10 ?
            |             |-- NON --> continuer à surveiller
            |             |-- OUI --> 
            |                 |-- Mur détecté --> MODE LONGEMENT (memory=199)
            |                 |-- Robot détecté --> MODE ROTATION D'URGENCE (memory=200)
            |
            |-- En mode longement (memory 100 -> 199) ?
            |     |-- Oui : longer le mur en corrigeant
            |
            |-- En mode rotation urgence (memory==200) ?
            |     |-- Oui : rotation rapide pour fuir les robots (ou les murs si y a tjrs blocage ?)
            """
            
            
            # Étape 1 : vérifier blocage potentiel (capteurs frontaux très proches)
            bloque = sensors[sensor_front] < 0.1 and sensors[sensor_front_left] < 0.1 and sensors[sensor_front_right] < 0.1

            # Étape 2 : état normal (memory = 0), ou état de surveillance de blocage
            if self.memory < 10 :
                if bloque:
                    self.memory += 1  # On incrémente si bloqué
                    #print("Robot 3 détecte un blocage potentiel (étape de surveillance)")
                else:
                    self.memory = 0   # Reset si pas bloqué

            # Étape 3 : Blocage confirmé (memory == 4)
            elif self.memory == 10 :
                # Vérifier si on est bloqué par un mur ou un robot
                if sensor_view[sensor_front] == 1 or sensor_view[sensor_front_left] == 1 or sensor_view[sensor_front_right] == 1:
                    # Blocage par mur : c'est le mode longement : memory = 100 + n
                    self.memory = 199  #  steps de longement
        
                elif sensor_view[sensor_front] == 2 or sensor_view[sensor_front_left] == 2 or sensor_view[sensor_front_right] == 2:
                    # Blocage par robot 
                    self.memory = 200
                    #print("Robot 3 : blocage par robot détecté, rotation d'urgence")

            # Étape 4 : Longement de mur (memory entre 100 et 199)
            if 100 <= self.memory < 200:
                self.memory -= 1
                
                sensor_to_wall = []
                for i in range(8):
                    if sensor_view[i] == 1: 
                        sensor_to_wall.append(sensors[i])
                    else:  
                        sensor_to_wall.append(1.0)

                #print("Robot 3 : longement de mur en cours")

                # ----- Tentative pas foncer dans mur -----
                if sensors[sensor_front] < 0.3:
                    # Si mur devant : chercher la plus grande ouverture à gauche ou à droite
                    droite = sensors[sensor_front_right] + sensors[sensor_right]
                    gauche = sensors[sensor_front_left] + sensors[sensor_left]

                    if droite > gauche:
                        # Plus d'espace à droite : tourne à droite
                        translation = 0.0
                        rotation = -1.0
                        #print("droite")
                    elif droite < gauche:
                        # Plus d'espace à gauche :  tourne à gauche
                        translation = 0.0
                        rotation = 1.0
                        #print("gauche")
                    else :
                        # reculer
                        translation = -1.0
                        rotation = 0.
                        #print("recule")

                    return translation, rotation, False

                    if sensor_to_wall[sensor_front] < 0.5:
                        # MUR DEVANT à éviter, ne pas foncer droit devant
                        translation = 0.2
                        rotation = 1.
                        return translation, rotation, False
                    # --------------
        
                # Suit les murs
                if  sensor_to_wall[sensor_rear_right] + sensor_to_wall[sensor_front_right] + sensor_to_wall[sensor_right] < 3. :
                    droite_moyenne = (sensor_to_wall[sensor_rear_right] + sensor_to_wall[sensor_front_right] + sensor_to_wall[sensor_right]) / 3.0
                    erreur_distance = droite_moyenne - 0.5 # On veut maintenir ~0.5

                    translation = 0.8
                    rotation = -2.0 * erreur_distance  # plus l'erreur est grande, plus on corrige
                    #print("droit", rotation, droite_moyenne, erreur_distance)
                    return translation, rotation, False
                    
                else :
                    gauche_moyenne = (sensor_to_wall[sensor_rear_left] + sensor_to_wall[sensor_front_left] + sensor_to_wall[sensor_left]) / 3.0
                    erreur_distance = gauche_moyenne - 0.5 # On veut maintenir ~0.5

                    translation = 0.8
                    rotation = +2.0 * erreur_distance  # plus l'erreur est grande, plus on corrige
                    #print("gauche", rotation, gauche_moyenne, erreur_distance)
                    return translation, rotation, False
                
                
            #print(self.memory)

            # Étape 5 : Rotation si bloqué par un robot
            if self.memory == 200:
                # Détecter où se trouve exactement le robot pour tourner dans la direction opposée
                if sensor_view[sensor_front_left] == 2:
                    # Robot détecté à gauche → tourner à droite
                    translation = 0.0
                    rotation = -1.0
                    #print("Robot 3 : robot à gauche, tourne droite")
                elif sensor_view[sensor_front_right] == 2:
                    # Robot détecté à droite → tourner à gauche
                    translation = 0.0
                    rotation = 1.0
                    #print("Robot 3 : robot à droite, tourne gauche")
                else:
                    # Robot en face → choisir aléatoirement gauche ou droite
                    translation = 0.0
                    rotation = random.choice([-1.0, 1.0])
                    #print("Robot 3 : robot devant, rotation aléatoire")
                
                self.memory = 0  # Reset après rotation
                #print("Robot 3 : robot rencontre, on fuit")
                return translation, rotation, False
            
            if self.memory == 99 : 
                self.memory = 0 
            
            # Comportement par défaut : avancer avec évitement aléatoire
            translation = 0.7
            rotation = 0.5 * sensors[sensor_front_left] - 0.5 * sensors[sensor_front_right] + (random.random() - 0.5)
            #print("Robot 3 : comportement normal (exploration aléatoire)")
            return translation, rotation, False
            
        
        elif self.robot_id == 3:
            # STRATÉGIE  4 : LONGER LES MURS LORSQUE L'ON EN TROUVE PUIS ALLER EN EXPEDITION AU BOUT À CHAQUE N ITERATION
            
            sensor_to_wall = []
            for i in range(8):
                if sensor_view[i] == 1: 
                    sensor_to_wall.append(sensors[i])
                else:  
                    sensor_to_wall.append(1.0)

            phase = self.memory%110  # 110 : 100 itérations suit mur + 10 itérations avoider

            moyenne_senseurs = sum(sensors) / len(sensors)
            if moyenne_senseurs > 0.5 :
            
                if phase < 100 and sum(sensor_to_wall)<8.:

                    # ----- Tentative pas foncer dans mur -----
                    if sensors[sensor_front] < 0.3:
                        # Si mur devant : chercher la plus grande ouverture à gauche ou à droite
                        droite = sensors[sensor_front_right] + sensors[sensor_right]
                        gauche = sensors[sensor_front_left] + sensors[sensor_left]

                        if droite > gauche:
                            # Plus d'espace à droite : tourne à droite
                            translation = 0.0
                            rotation = -1.0
                            #print("droite")
                        elif droite < gauche:
                            # Plus d'espace à gauche :  tourne à gauche
                            translation = 0.0
                            rotation = 1.0
                            #print("gauche")
                        else :
                            # reculer
                            translation = -1.0
                            rotation = 0.
                            #print("recule")

                        return translation, rotation, False

                    if sensor_to_wall[sensor_front] < 0.5:
                        # MUR DEVANT à éviter, ne pas foncer droit devant
                        translation = 0.2
                        rotation = 1.
                        return translation, rotation, False
                    # --------------
        
                    # Suit les murs
                    if  sensor_to_wall[sensor_rear_right] + sensor_to_wall[sensor_front_right] + sensor_to_wall[sensor_right] < 3. :
                        droite_moyenne = (sensor_to_wall[sensor_rear_right] + sensor_to_wall[sensor_front_right] + sensor_to_wall[sensor_right]) / 3.0
                        erreur_distance = droite_moyenne - 0.5 # On veut maintenir ~0.5

                        translation = 0.8
                        rotation = -2.0 * erreur_distance  # plus l'erreur est grande, plus on corrige
                        #print("droit", rotation, droite_moyenne, erreur_distance)
                        return translation, rotation, False
                    
                    else :
                        gauche_moyenne = (sensor_to_wall[sensor_rear_left] + sensor_to_wall[sensor_front_left] + sensor_to_wall[sensor_left]) / 3.0
                        erreur_distance = gauche_moyenne - 0.5 # On veut maintenir ~0.5

                        translation = 0.8
                        rotation = +2.0 * erreur_distance  # plus l'erreur est grande, plus on corrige
                        #print("gauche", rotation, gauche_moyenne, erreur_distance)
                        return translation, rotation, False
            
            # Éviter les murs
            param =  [0.2, 0.0, 0.8, 0.0, 0.0, 0.0 , random.random()-0.5, 0.3, 0.0, -0.3, -0.3, 0.3]

            translation = (
                param[0]
                + param[1] * sensors[1]  # front-left
                + param[2] * sensors[0]  # front
                + param[3] * sensors[7]  # front-right
                + param[4] * sensors[6]  # right
                + param[5] * sensors[2]  # left
        )

            rotation = (
                param[6]
                + param[7] * sensors[1]  # front-left
                + param[8] * sensors[0]  # front
                + param[9] * sensors[7]  # front-right
                + param[10] * sensors[6]  # right
                + param[11] * sensors[2]  # left
            )
            #print("avoider", translation, rotation)    
            
        return translation, rotation, False