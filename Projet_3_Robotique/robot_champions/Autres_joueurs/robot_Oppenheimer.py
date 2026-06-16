# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : Jules Perrin de Brichambaut 21214135
#  Prénom Nom No_étudiant/e : _________
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

import math
from robot import * 

nb_robots = 0

class Robot_player(Robot):

    team_name = "Oppenheimer"  # vous pouvez modifier le nom de votre équipe
    robot_id = -1             # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory = 0                # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        # translation = sensors[sensor_front]
        # rotation = 1.0 * sensors[sensor_front_left] - 1.0 * sensors[sensor_front_right] + (random.random()-0.5)*0.1

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

        translation = 0
        rotation = 0

        # Comportement subsomption
        if self.robot_id == 0:
            # Eviter les murs
            sens_wall = sensor_to_wall[sensor_front_left] * 1 + sensor_to_wall[sensor_front_right] * -1 + sensor_to_wall[sensor_left] * 1 + sensor_to_wall[sensor_right] * -1 + sensor_to_wall[sensor_rear_left] * -1 + sensor_to_wall[sensor_rear_right] * 1

            # Aller vers les robots
            # On ne considère que les robots de l'équipe adverse 
            sens_robot_adv = sensor_to_robot[sensor_front_left] * -int(sensor_team[1]==self.team_name) + sensor_to_robot[sensor_front_right] * int(sensor_team[7]==self.team_name) + sensor_to_robot[sensor_left] * -int(sensor_team[2]==self.team_name) + sensor_to_robot[sensor_right] * int(sensor_team[6]==self.team_name) + sensor_to_robot[sensor_rear_left] * int(sensor_team[3]==self.team_name) + sensor_to_robot[sensor_rear_right] * -int(sensor_team[5]==self.team_name)

            # Repousser les robots de son équipe
            sens_robot_team = sensor_to_robot[sensor_front_left] * int(sensor_team[1]==self.team_name) + sensor_to_robot[sensor_front_right] * -int(sensor_team[7]==self.team_name) + sensor_to_robot[sensor_left] * int(sensor_team[2]==self.team_name) + sensor_to_robot[sensor_right] * -int(sensor_team[6]==self.team_name) + sensor_to_robot[sensor_rear_left] * -int(sensor_team[3]==self.team_name) + sensor_to_robot[sensor_rear_right] * int(sensor_team[5]==self.team_name) 

            # Priorité à l'évitement des murs
            if abs(sens_wall) > abs(sens_robot_adv):
                translation = sensor_to_wall[sensor_front] * 0.6 - sensor_to_robot[sensor_front] * 0.2
                rotation = sens_wall

            # Sinon, repousser les robots de son équipe et aller vers les robots adverses, ou tout droit s'il n'y a pas de robots
            else: 
                if abs(sens_robot_team) > abs(sens_robot_adv):
                    translation = sensor_to_robot[sensor_front] * 0.5
                    rotation = sens_robot_team
                else:
                    translation = sensor_to_robot[sensor_front] * 0.3
                    rotation = sens_robot_adv 

        # Comportement optimisé par algorithme génétique
        elif self.robot_id == 1:
            comportement = [1, 1, 0, 1, -1, 1, 1, -1]
            
            translation = math.tanh ( comportement[0] + comportement[1] * sensors[sensor_front_left] + comportement[2] * sensors[sensor_front] + comportement[3] * sensors[sensor_front_right] )
            rotation = math.tanh ( comportement[4] + comportement[5] * sensors[sensor_front_left] + comportement[6] * sensors[sensor_front] + comportement[7] * sensors[sensor_front_right] )

        elif self.robot_id == 2:
            translation = sensors[sensor_front] * 0.5
            rotation = sensors[sensor_front_left] * 1.0 + sensors[sensor_front_right] * -1.0 + sensors[sensor_left] * 1.0 + sensors[sensor_right] * -1.0

            # Vérification que la position du robot est différente de la position précédente
            #if self.memory == int(str(int(self.x)) + str(int(self.y))):
                #translation = -1

        else:
            translation = sensor_to_robot[sensor_front] * 0.8
            rotation = sensor_to_robot[sensor_front_left] * -1 + sensor_to_robot[sensor_front_right] * 1 + sensor_to_robot[sensor_left] * -1 + sensor_to_robot[sensor_right] * 1 + sensor_to_robot[sensor_rear_left] * 1 + sensor_to_robot[sensor_rear_right] * -1
            
            # Vérification que la position du robot est différente de la position précédente
            #if self.memory == int(str(int(self.x)) + str(int(self.y))):
                #translation = -1
            
        # enregitrement de la position du robot en mémoire
        #self.memory = int(str(int(self.x)) + str(int(self.y)))

        return translation, rotation, False

