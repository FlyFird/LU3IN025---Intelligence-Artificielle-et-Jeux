# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : Moustapha Diaby/21208806
#  Prénom Nom No_étudiant/e : _________
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import * 
import math
nb_robots = 0

class Robot_player(Robot):

    team_name = "Challenger_arjdal_diaby"  # vous pouvez modifier le nom de votre équipe
    robot_id = -1             # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory = 0                # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier
    debug=True
    iteration=0
    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        sensor_to_wall = []
        sensor_to_robot = []
        sensor_to_robot_ops = []
        sensor_to_robot_al = []
        
        for i in range (0,8):
            if  sensor_view[i] == 1:
                sensor_to_wall.append(sensors[i])
                sensor_to_robot_ops.append(1.0)
                sensor_to_robot_al.append(1.0)
                sensor_to_robot.append(1.0)
            elif  sensor_view[i] == 2:
                sensor_to_wall.append( 1.0 )
                if sensor_team[i]!=self.team:
                    sensor_to_robot_ops.append(sensors[i])
                    sensor_to_robot_al.append(1.0)
                    sensor_to_robot.append(sensors[i])
                else:
                    sensor_to_robot_ops.append(1.0)
                    sensor_to_robot_al.append(sensors[i])
                    sensor_to_robot.append(sensors[i])
            else:
                sensor_to_wall.append( 1.0 )
                sensor_to_robot_ops.append(1.0)
                sensor_to_robot_al.append(1.0)
                sensor_to_robot.append(1.0)

        self.iteration+=1
        ################################

        #PRIORITE

        #1 debuggage
        #2 si robot ennemie devant soit -> id 1 le suit les autres le fuis
        #3 si mur devant fuir
        #4 si un allié autour de soit le fuir
        #5 avancer droit a l'aide des poids genetic

        ################################



        if min (sensor_to_robot_al) <= 0.45 or min(sensor_to_robot_ops) <= 0.45: # sauf si on est bloqué
            translation=0
            droit = (sensor_to_robot_al[1]+sensor_to_robot_al[2] +sensor_to_robot_al[3] )*1.5
            gauche = sensor_to_robot_al[5] +sensor_to_robot_al[6] +sensor_to_robot_al[7] 
            rotation = (droit-gauche)*0.4
            if sensor_to_robot_ops[1] >= 0.5 and sensor_to_robot_ops[7] >= 0.5 and sensor_to_robot_al[1] >= 0.5 and sensor_to_robot_al[7] >= 0.5 and sensor_to_wall[1] >= 0.2 and sensor_to_wall[7] >= 0.2 :
                translation = sum(sensor_to_robot)

        
        elif sensor_to_robot_ops[1] < 1.0 or sensor_to_robot_ops[7] <1.0 or sensor_to_robot_ops[0] < 1.0 :     #si un ennemi devant soit
                                       #les autres robot le fuis 
                translation = sum(sensor_to_robot)
                droit = (sensor_to_robot_ops[1]+sensor_to_robot_ops[2] +sensor_to_robot_ops[3] )*1.01
                gauche = sensor_to_robot_ops[5] +sensor_to_robot_ops[6] +sensor_to_robot_ops[7] 
                rotation = (droit-gauche)*0.8
            

        elif sensor_to_wall[1] < 1.0 or sensor_to_wall[7] <1.0 or sensor_to_wall[0] < 1.0 :        # si un mur devant toi fuis
            translation = sum(sensor_to_wall) 
            droit = (sensor_to_wall[1]+sensor_to_wall[2] +sensor_to_wall[3] )*1.01
            gauche = sensor_to_wall[5] +sensor_to_wall[6] +sensor_to_wall[7] 
            rotation = (droit-gauche)*0.8 

        elif min(sensor_to_robot_al) < 1.0:    # si un allié au tour de toi il se fuis entre eux
            if self.robot_id == 0 :
                translation = sum(sensor_to_robot_al)
                droit = (sensor_to_robot_al[1]+sensor_to_robot_al[2] +sensor_to_robot_al[3] )*1.01
                gauche = sensor_to_robot_al[5] +sensor_to_robot_al[6] +sensor_to_robot_al[7] 
                rotation = (droit-gauche)
            if self.robot_id == 1 :
                translation = sum(sensor_to_robot_al) 
                droit = (sensor_to_robot_al[1]+sensor_to_robot_al[2] +sensor_to_robot_al[3] )*1.01
                gauche = sensor_to_robot_al[5] +sensor_to_robot_al[6] +sensor_to_robot_al[7] 
                rotation = (droit-gauche)*0.4
            if self.robot_id == 2 :
                translation = sum(sensor_to_robot_al) 
                droit = (sensor_to_robot_al[1]+sensor_to_robot_al[2] +sensor_to_robot_al[3] )*1.01
                gauche = sensor_to_robot_al[5] +sensor_to_robot_al[6] +sensor_to_robot_al[7] 
                rotation = (droit-gauche)*0.6
            else:
                translation = sum(sensor_to_robot_al) 
                droit = (sensor_to_robot_al[1]+sensor_to_robot_al[2] +sensor_to_robot_al[3] )*1.01
                gauche = sensor_to_robot_al[5] +sensor_to_robot_al[6] +sensor_to_robot_al[7] 
                rotation = (droit-gauche)*0.8


        else:                                  #on utilise les poids genetic
            weights = [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, -1, 1, 0, -1, 0, 1]

            z_t = sum(weights[i] * sensors[i] for i in range(8))
            z_r = sum(weights[i+8] * sensors[i] for i in range(8))

            translation = math.tanh(z_t)
            rotation = math.tanh(z_r) *0.5


        return translation, rotation, False
