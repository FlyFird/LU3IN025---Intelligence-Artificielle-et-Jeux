# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : Iarina Nistor 21210925
#  Prénom Nom No_étudiant/e : Elise Thomas 21234701
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import * 
import math

nb_robots = 0

class Robot_player(Robot):

    team_name = "NistorThomas"  # vous pouvez modifier le nom de votre équipe
    robot_id = -1             # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory = 0                # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)
    
    # Braitenberg avoider
    def avoider_comportement(self, sensors, sensor_to_robot, sensor_to_wall):
        translation = sensors[sensor_front]*1.0
        rotation = - 1.0*sensor_to_wall[sensor_front_right]*sensor_to_robot[sensor_front_right] + 1.0*sensor_to_wall[sensor_front_left]*sensor_to_robot[sensor_front_left] - 1.0*sensor_to_wall[sensor_right]*sensor_to_robot[sensor_right] + 1.0*sensor_to_wall[sensor_left]*sensor_to_robot[sensor_left] - 1.0*sensor_to_wall[sensor_rear_right]*sensor_to_robot[sensor_rear_right] + 1.0*sensor_to_wall[sensor_rear_left]*sensor_to_robot[sensor_rear_left]  
        return translation, rotation, False
    
    # Fonctions pour la stratégie de subsomption (explore, lovebot, hatebot, hatewall)
    def lovebot_comportement(self, sensors, sensor_to_robot):
        translation = sensors[sensor_front]*0.5
        rotation = 1.0*sensor_to_robot[sensor_front_right] - 1.0*sensor_to_robot[sensor_front_left] - 1.0*sensor_to_robot[sensor_rear_left] + 1.0*sensor_to_robot[sensor_rear_right] + 1.0*sensor_to_robot[sensor_right] - 1.0*sensor_to_robot[sensor_left]
        return translation, rotation, False
    
    def hatebot_comportement(self, sensors, sensor_to_robot):
        translation = sensors[sensor_front]*0.5
        rotation = - 1.0*sensor_to_robot[sensor_front_right] + 1.0*sensor_to_robot[sensor_front_left] - 1.0*sensor_to_robot[sensor_right] + 1.0*sensor_to_robot[sensor_left] - 1.0*sensor_to_robot[sensor_rear_right] + 1.0*sensor_to_robot[sensor_rear_left]
        return translation, rotation, False
    
    def hatewall_comportement(self, sensors, sensor_to_wall):
        translation = sensors[sensor_front]*0.5
        rotation = - 1.0*sensor_to_wall[sensor_front_right] + 1.0*sensor_to_wall[sensor_front_left] - 1.0*sensor_to_wall[sensor_right] + 1.0*sensor_to_wall[sensor_left] - 1.0*sensor_to_wall[sensor_rear_right] + 1.0*sensor_to_wall[sensor_rear_left]
        return translation, rotation, False
    
    def explore_comportement(self, sensors):
        translation = sensors[sensor_front]*1.0
        rotation = (random.random() - 0.5)*0.5 # Légère rotation aléatoire
        return translation, rotation, False
    
    # Génétique + Braitenberg
    def genetique_plus_braitenberg(self, sensors, sensor_to_robot, sensor_to_wall):
        # Vecteur de poids optimisé génétiquement
        param = [0, 0, 1, 1, 1, 0, 0, -1]

        # Comportement génétique de base
        t = math.tanh(
            param[0]
            + param[1] * sensors[sensor_front_left]
            + param[2] * sensors[sensor_front]
            + param[3] * sensors[sensor_front_right]
        )
        r = math.tanh(
            param[4]
            + param[5] * sensors[sensor_front_left]
            + param[6] * sensors[sensor_front]
            + param[7] * sensors[sensor_front_right]
        )

        # Comportement Braitenberg avoider
        t_b, r_b, _ = self.avoider_comportement(sensors, sensor_to_robot, sensor_to_wall)

        # Combinaison pondérée
        alpha = 0.7  # poids du comportement génétique
        beta = 0.3   # poids du comportement Braitenberg

        translation = alpha * t + beta * t_b
        rotation = alpha * r + beta * r_b

        return translation, rotation, False

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):   
        sensor_to_wall = []
        sensor_to_robot = []
        for i in range (0,8):
            if  sensor_view[i] == 1:
                sensor_to_wall.append( sensors[i] )
                sensor_to_robot.append(1.0)
            elif  sensor_view[i] == 2:
                sensor_to_wall.append( 1.0 )
                sensor_to_robot.append( sensors[i] )
            else:
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(1.0)
        
        # 4 robots : 2 Braitenberg et 1 Subsomption et 1 Génétique
        if self.robot_id == 0 or self.robot_id == 1 or self.robot_id == 2 or self.robot_id == 3:
            # Stratégie d'évitement des blocages
            capteurs = [sensor_front, sensor_front_left, sensor_front_right, sensor_left, sensor_right] # A considérer ici
            # Si au moins 2 senseurs détectent un obstacle à moins de 0.1 de distance, alors on estime que le robot est bloqué
            blocked = sum(1 for i in capteurs if(sensor_view[i] == 2 or sensor_view[i] == 1) and sensors[i] < 0.1) >= 2

            # Avoid being blocked (la mémoire va permettre au robot de changer de rotation d'une action à l'autre afin d'éviter au possible d'être bloqué)
            # Chaque stratégie (gauche ou droite) restera durant quelques itérations (5, ici) pour prendre effet
            if blocked:
                translation = -0.5 # Reculer légèrement
                
                # Strat 0 : tourner à gauche
                if self.memory <= 5:
                    rotation = 1.0
                    self.memory += 1
                    
                # Strat 1 : tourner à droite
                elif self.memory > 5 and self.memory < 10:
                    rotation = -1.0
                    self.memory += 1

                # Dernière itération de strat 1 : remise à 0 de la mémoire
                else:
                    rotation = -1.0
                    self.memory = 0 # Reset
                    
                return translation, rotation, False
            
            # Braitenberg
            if self.robot_id == 0 or self.robot_id == 1:
                translation, rotation, _ = self.avoider_comportement(sensors, sensor_to_robot, sensor_to_wall)
              
            # Subsomption
            if self.robot_id == 2:
                wall_detected = any(sensor_view[i] == 1 and sensors[i] < 0.7 for i in capteurs)
                ally_robot_detected = any(sensor_view[i] == 2 and sensor_team[i] == self.team_name and sensors[i] < 0.7 for i in capteurs)
                ennemy_robot_detected = any(sensor_view[i] == 2 and sensor_team[i] != self.team_name and sensors[i] < 0.7 for i in capteurs)
                             
                # Priority order : wall detected -> ally robot detected -> ennemy robot detected -> explore
                if wall_detected:           # Avoid
                    translation, rotation, _ = self.avoider_comportement(sensors, sensor_to_robot, sensor_to_wall)
                elif ally_robot_detected:   # Avoid (pour éviter de rentrer en collision avec ses alliés et de repasser inutilement sa propre peinture)
                    translation, rotation, _ = self.hatebot_comportement(sensors, sensor_to_robot)
                elif ennemy_robot_detected: # Follow (pour repasser la peinture adverse par la sienne)
                    translation, rotation, _ = self.lovebot_comportement(sensors, sensor_to_robot)
                else:
                    translation, rotation,_ = self.explore_comportement(sensors)
                    
            # Génétique
            if self.robot_id == 3:
                translation,rotation,_ = self.genetique_plus_braitenberg(sensors, sensor_to_robot, sensor_to_wall)
            
        
        return translation, rotation, False

