# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : MANCER Samy 21217006
#  Prénom Nom No_étudiant/e : DAI Louis 21204918
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import * 
import numpy as np
import random 
nb_robots = 0

class Robot_player(Robot):

    team_name = "Sans_Personalité"  # vous pouvez modifier le nom de votre équipe
    robot_id = -1             # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory = 0                # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier
    
    SENSOR_FRONT = [sensor_front, sensor_front_left, sensor_front_right]
    
    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

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

        #Premier robot a pour Stratégie Subsomption qui suit les robots adverses
        if self.robot_id == 0 :
            
            #S'il détecte un robot adverse il va le suivre
            if any(sensor_to_robot[i] < 1 and sensor_team[i] != self.team_name for i in self.SENSOR_FRONT) :
                #Une vitesse pas trop rapide pour ne pas aller trop vite et bien suivre les mouvements du robot adverse
                translation = 0.5 
                #Rotation qui se dirige vers le robot adverse
                rotation = sensor_to_wall[sensor_front] - sensor_to_wall[sensor_rear] - sensor_to_robot[sensor_front_left] + sensor_to_robot[sensor_front_right] - sensor_to_robot[sensor_left] + sensor_to_robot[sensor_right] 
            
            #Si c'est un robot allié on se décale pour ne pas se coller
            elif any(sensor_to_robot[i] < 1 and sensor_team[i] == self.team_name for i in self.SENSOR_FRONT) : 
                #Le robot recul (Première Stratégie pour ne pas que les robots se bloquent)
                translation = -1 
                #Rotation qui va faire en sorte que les robots ne se collent pas
                rotation =  1 - sensor_to_robot[sensor_front] + sensor_to_robot[sensor_front_left] - sensor_to_robot[sensor_front_right] + sensor_to_robot[sensor_left] - sensor_to_robot[sensor_right]
            
            #Si un robot adverse suit ce robot, il se bloque
            elif sensor_to_robot[sensor_rear] < 0.3 and sensor_team[sensor_rear] != self.team_name: 
                translation = 0 
                rotation = 0
            
            #Si il y a un mur devant lui, alors il va tourner un peu pour ne pas se bloquer sur le mur
            elif any(sensor_to_wall[i] < 0.8 for i in self.SENSOR_FRONT) :
                translation = 0.5
                rotation = sensor_to_wall[sensor_front] - sensor_to_wall[sensor_rear] + sensor_to_wall[sensor_front_left] - sensor_to_wall[sensor_front_right] + sensor_to_wall[sensor_left] - sensor_to_wall[sensor_right] + (random.random()-0.5)*1.   
            #Comportement par défaut qui va explorer la carte
            else : 
                translation = sensors[sensor_front]
                rotation = (random.random()-0.5)*1.
             
        # Génétique pour un robot
        elif self.robot_id == 3 :
            #Si il y a un mur devant lui, alors il va tourner un peu pour ne pas se bloquer sur le mur
            if any(sensor_to_wall[i] < 1 for i in self.SENSOR_FRONT):
                translation = 0.5
                rotation = sensor_to_wall[sensor_front] - sensor_to_wall[sensor_rear] + sensor_to_wall[sensor_front_left] - sensor_to_wall[sensor_front_right] + sensor_to_wall[sensor_left] - sensor_to_wall[sensor_right] + (random.random()-0.5)*1.  
            #S'il détecte un robot, alors il va se décaler 
            elif any(sensor_to_robot[i] < 0.5 and sensor_team[i] == self.team_name for i in self.SENSOR_FRONT) : 
                translation = sensors[sensor_front]*0.1+0.2
                rotation = 1 - sensor_to_robot[sensor_front] + sensor_to_robot[sensor_front_left] - sensor_to_robot[sensor_front_right] + sensor_to_robot[sensor_left] - sensor_to_robot[sensor_right]
            #Sinon il va explorer avec un des paramètres trouvé dans config_TP2.py dans la carte 4
            else : 
                param = np.array([ 1,  0,  1,  0, -1, -1,  0, -1,  0, -1, -1, -1, -1,  0, -1,  1,  0,  0])
                sensors_nda = np.array(sensors)
                translation = np.tanh ( param[0] + param[1:9] @  sensors_nda )
                rotation = np.tanh ( param[9] + param[10:] @  sensors_nda )
                
        # Subsomption qui explore la carte pour 2 robots     
        else : 
            #Si il y a un robot allié devant lui, alors il va tourner un peu pour ne pas se bloquer sur le robot allié
            if any(sensor_to_robot[i] < 0.2 and sensor_team[i] == self.team_name for i in self.SENSOR_FRONT) : 
                translation = 0.5
                #Séparation des cas pour ne pas faire de collision en fonction du robot
                if self.robot_id == 1 : 
                    #Monte pour le robot d'ID 1
                    rotation = 1
                if self.robot_id == 2 :
                    #Descend pour le robot d'ID 2
                    rotation = -1
            #S'il détecte un mur, il va dévier le mur
            elif any(sensor_to_wall[i] < 1 for i in self.SENSOR_FRONT) :
                translation = 0.5
                rotation = sensor_to_wall[sensor_front] - sensor_to_wall[sensor_rear] + sensor_to_wall[sensor_front_left] - sensor_to_wall[sensor_front_right] + sensor_to_wall[sensor_left] - sensor_to_wall[sensor_right] + (random.random()-0.5)*1. 
            #S'il détecte un robot adverse, il va essayer de se dévier mais le comportement reste identique pour tous, s'il a blocage ce n'est pas un problème
            elif any(sensor_to_robot[i] < 1 for i in self.SENSOR_FRONT) : 
                translation = 0.5
                rotation = 1 - sensor_to_robot[sensor_front] + sensor_to_robot[sensor_front_left] - sensor_to_robot[sensor_front_right] + sensor_to_robot[sensor_left] - sensor_to_robot[sensor_right]
                
            #Comportement par défaut qui va explorer la carte pour maximiser les points
            else : 
                translation = sensors[sensor_front] * 0.5
                rotation = (random.random()-0.5)*0.2
              
        return translation, rotation, False

