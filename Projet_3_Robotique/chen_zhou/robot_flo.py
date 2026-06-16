from robot import * 

nb_robots = 0
debug = True

class Robot_player(Robot):

    team_name = "JadoreLesMurs"  # vous pouvez modifier le nom de votre équipe
    robot_id = -1             # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory = 0                # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def get_extended_sensors(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        tmp = []
        for key in range(len(sensors)):
            d = {
                "distance_to_robot": 1.0,
                "distance_to_wall": 1.0,
                "distance_to_ally": 1.0,
                "distance_to_enemy": 1.0,
                "distance": sensors[key]
            }
            if sensor_view[key] == 2:
                d["distance_to_robot"] = sensors[key]
                if sensor_robot[key] != 'n/a' and sensor_team[key] != 'n/a':
                    d["distance_to_ally"] = sensors[key]
                else:
                    d["distance_to_enemy"] = sensors[key]
            else:
                d["distance_to_wall"] = sensors[key]
            tmp.append(d)
        return tmp

    def detecteur_wall(self,sensors) :
        # comportement : il detecte si il y a un mur proche de lui
        # renvoie true si il y a un mur sinon false
        if (sensors[0]["distance_to_wall"] < 0.7 or
            sensors[1]["distance_to_wall"] < 0.7 or
            sensors[6]["distance_to_wall"] < 0.7 or
            sensors[2]["distance_to_wall"] < 0.7 or
            sensors[5]["distance_to_wall"] < 0.7 or
            sensors[3]["distance_to_wall"] < 0.7 or
            sensors[4]["distance_to_wall"] < 0.7 or
            sensors[7]["distance_to_wall"] < 0.7
            ):
            return True
        return False
    
    def ally_around(self,sensors) :
        # savoir s'il y a un allie autour : 'left' -> a gauche , 'right' -> a droite
        # return true s'il y a un allie autour, false sinon avec l'endroit ou il a detecté
        if sensors[0]["distance_to_ally"] < 1.0 :
            return True
        if sensors[1]["distance_to_ally"] < 1.0 :
            return True
        if sensors[2]["distance_to_ally"] < 1.0 :
            return True
        if sensors[7]["distance_to_ally"] < 1.0 :
            return True
        if sensors[6]["distance_to_ally"] < 1.0 :
            return True

        return False
    def tourne_right(self,sensors):
        near = sensors[4]["distance_to_wall"]
        near_right = sensors[5]["distance_to_wall"]
        right = sensors[6]["distance_to_wall"]
        front_right = sensors[7]["distance_to_wall"]
        if near<1.0 and front_right<1.0 and near_right<1.0 and right>0.7 or right<0.1 or near_right<0.1 and right<0.1:
            return False
        if near<1.0 and front_right<1.0 and sensors[3]["distance_to_wall"]<1.0:
            return False
        if right>0.7:
            return True
        if front_right>0.5:
            return True
        return False
        
    def tourne_left(self,sensors):

        near = sensors[4]["distance_to_wall"]
        near_left = sensors[3]["distance_to_wall"]
        left = sensors[2]["distance_to_wall"]
        front_left = sensors[1]["distance_to_wall"]
        if near<1.0 and front_left<1.0 and near_left<1.0 and left>0.7 or left<0.1 or near_left<0.1 and left<0.1:
            return False
        if near<1.0 and front_left<1.0 and sensors[5]["distance_to_wall"]<1.0:
            return False
        if left>0.7:
            return True
        if front_left>0.5:
            return True
        return False
    
    def enemy_following(self,sensors) :
        # savoir s'il y a un enemi en train de me suivre
        # return true s'il y a un enemi en train de me suivre, false sinon

        if sensors[4]["distance_to_enemy"] < 1.0 or sensors[3]["distance_to_enemy"] < 1.0 or sensors[5]["distance_to_enemy"] < 1.0 :
            return True
        return False
    
    def enemy_before(self,sensors) :
        # savoir s'il y a un ennemi devant
        # return true s'il y a un ennemi devant, false sinon

        if sensors[7]["distance_to_enemy"] < 1.0 or sensors[1]["distance_to_enemy"] < 1.0 or sensors[0]["distance_to_enemy"] < 1.0:
            return True
        return False
    
    def follow_enemy(sensors) :
        # comportement : suit les ennemis
        # renvoie les valeurs de translation et de rotation : pos -> tourne a droite, neg -> tourne a gauche 

        return sensors[0]["distance_to_enemy"], sensors[1]["distance_to_enemy"] + (-1) * sensors[7]["distance_to_enemy"],False
    
    def spirale(self):
        #Comportement : bouge en spirale

        spiral= (self.memory % 100) / 100 
        return 1.0, 0.3 if spiral < 0.5 else -0.3, False
    
    def evite_obstacle_front(self, sensors):
        # Comportement : evite les obstacles

        front = sensors[0]["distance"]
        left = sensors[2]["distance"]
        right = sensors[6]["distance"]
        front_left = sensors[1]["distance"]
        front_right = sensors[7]["distance"]
        print(f"Position: x={self.x:.2f}, y={self.y:.2f}, theta={self.theta:.2f}")

        if front < 0.15:
            print("Obstacle frontal proche")
            diff = (right+front_right) - (left+front_left)
            print(diff)
            if (right<0.3 and left<0.3) or sensors[4]["distance"]<0.3 or front<0.1 or front<0.3 and sensors[4]["distance"]<0.3:
                print("Fait demi-tour")
                return 0.1,-1,False
            if right > 0.5 and diff >0 and front_right-front_left>0.15:
                return 0,-0.8,False
            if left>0.5 and diff <0 and front_left-front_right>0.15:
                return 0,0.8,False
            if diff <0 and front_left<front_right:
                return 0, -0.8, False
            if diff <0 and front_left>front_right:
                return 0, 0.8, False
            if diff > 0 and front_left>front_right:
                return 0, 0.8, False
            if diff > 0 and front_left<front_right:
                return 0, -0.8, False
            else:
                return 0, -0.8, False
        if front<0.35:
            if front_right-front_left>0.15:
                return 0.2, -0.7, False
            if front_left-front_right>0.15:
                return 0.2,0.7,False
            if sensors[5]["distance"]>sensors[3]["distance"] and right>0.7 and left>0.7:
                return 0.3,-0.1,False
            if sensors[5]["distance"]<sensors[3]["distance"] and right>0.7 and left>0.7:
                return 0.3,0.1,False
            else:
                return 0.2,-0.7, False
        if front_right<0.3:
            return 0.3,0.3,False
        if front_left<0.3:
            return 0.3,-0.3,False
        if right < 0.22 and front<0.7:
            return 0.7,0.3,False
        if left < 0.22 and front < 0.7:
            return 0.7,-0.3,False
        if right<0.15:
            return 0.7,0.1,False
        if left<0.15:
            return 0.7,-0.1,False
        if sensors[5]["distance"]>sensors[3]["distance"]:
            return 0.3,-0.1,False
        if sensors[5]["distance"]<sensors[3]["distance"]:
            return 0.3,0.1,False
        return 1.0, 0, False
    
    def hate_wall(self, sensors):
        #Comportement : Évite les murs + détecte s'il y a un obstacle directement devant.
        #Retourne : (vitesse_translation, vitesse_rotation, arrêt)
        diff=(sensors[1]["distance_to_wall"]+sensors[2]["distance_to_wall"])-(sensors[7]["distance_to_wall"]+sensors[6]["distance_to_wall"])
        if sensors[0]["distance_to_wall"] < 0.8:
            return self.evite_obstacle_front(sensors)
        speed=min(sensors[0]["distance_to_wall"],sensors[7]["distance_to_wall"],sensors[6]["distance_to_wall"],sensors[1]["distance_to_wall"],sensors[2]["distance_to_wall"])
        return speed, 0.2 * diff, False
    
    def hate_all(self,sensors):
        # Comportement : deteste tous 
        diff=(sensors[1]["distance"]+sensors[2]["distance"])-(sensors[7]["distance"]+sensors[6]["distance"])
        if sensors[0]["distance"] < 0.8:
            return self.evite_obstacle_front(sensors)
        speed=min(sensors[0]["distance"],sensors[7]["distance"],sensors[6]["distance"],sensors[1]["distance"],sensors[2]["distance"])
        return speed, 0.2 * diff, False

    def love_wall(self,sensors,mode="right"):
        # comportement : suit les murs droit ou gauche
        #[1.0, 0.20545290915602604, 0.1111111111111111, 0.05039373708911317, 0.0, 0.05039373708911317, 0.2222222222222222, 0.36436232732482077]
        left = sensors[2]["distance_to_wall"]
        right = sensors[6]["distance_to_wall"]
        front_left = sensors[1]["distance_to_wall"]
        front_right = sensors[7]["distance_to_wall"]
        match mode :
            case "right":
                if right<0.15:
                    return 0.5,0.1,False
                if front_right<0.25:
                    return 0.4,0.1,False
                if right>0.25 and right<0.9:
                    return 0.5,-0.1,False
                if front_right>0.35 and front_right<0.9:
                    return 0.4,-0.1,False
            case "left":
                if left<0.07:
                    print('trop proche')
                    return 0.1,-0.5,False
                if left<0.15:
                    return 0.5,-0.1,False
                if front_left<0.22:
                    return 0.4,-0.1,False
                if left>0.25:
                    return 0.5,0.1,False
                if front_left>0.35:
                    return 0.4,0.1,False
        return 1,0,False
    
    def strat_love_wall(self,sensors):
        #comportement principale : chercher les murs , puis les suit
        # option : follow enemy, stop enemy
        # manque detection allier, mettre un cas pour le labyrinthe, Longer les murs faut l'amémliorer
        if self.enemy_before(sensors):
            return self.follow_enemy(sensors)
        if self.enemy_following(sensors):
            return 0,0,False
        if self.ally_around(sensors) :
            print("lpl")
            return self.hate_all(sensors)
        if self.detecteur_wall(sensors):
            if sensors[0]["distance"]<0.8:
                return self.evite_obstacle_front(sensors)
            tmp=0
            for i in range(len(sensors)):
                if sensors[i]["distance"]<0.9:
                    tmp+=1
            if tmp>=4:
                return self.evite_obstacle_front(sensors)
            if (sensors[2]["distance"]<1.0 and sensors[6]["distance"]<1.0 or
                sensors[3]["distance"]<1.0 and (sensors[4]["distance"]<1.0) and
                sensors[5]["distance"]<1.0 and (sensors[1]["distance"]<1.0 or sensors[7]["distance"]<1.0)):#pas fini
                return self.evite_obstacle_front(sensors)
            else:
                if sensors[2]["distance"]<sensors[6]["distance"] or (sensors[2]["distance"]==sensors[6]["distance"] and (sensors[1]["distance"]<sensors[7]["distance"] or sensors[3]["distance"]<sensors[5]["distance"] )):
                    if sensors[4]["distance"] < 1.0 and sensors[3]["distance"] <1.0 and sensors[1]["distance"] <1.0 and sensors[2]["distance"] >0.7:
                        return 0.2,-0.5,False
                    if self.tourne_left(sensors):
                        if sensors[2]["distance"] < 0.3 and sensors[3]["distance"] >0.45 and sensors[1]["distance"] >0.6:
                            return 0.2,-0.8,False
                        if sensors[2]["distance"] < 0.14 and sensors[3]["distance"] <0.21:
                            return 0.1,-0.8,False
                        if sensors[1]["distance"] < 1 and sensors[7]["distance"] <1 and sensors[5]["distance"] <1 and sensors[3]["distance"] <1:
                            return self.evite_obstacle_front(sensors)
                        if ((sensors[3]["distance"] < 1 and sensors[0]["distance"] >0.7 and sensors[2]["distance"] >0.7 and 
                            sensors[4]["distance"] >0.7 and sensors[5]["distance"] >0.7 and sensors[6]["distance"] >0.7 and sensors[7]["distance"] >0.7) or
                            (sensors[5]["distance"] < 1 and sensors[0]["distance"] >0.7 and sensors[2]["distance"] >0.7 and 
                            sensors[4]["distance"] >0.7 and sensors[3]["distance"] >0.7 and sensors[6]["distance"] >0.7 and sensors[7]["distance"] >0.7)):
                            return self.hate_all(sensors)
                        return 0,1,False
                    return self.love_wall(sensors,"left")
                else:
                    if sensors[4]["distance"] < 1.0 and sensors[5]["distance"] <1.0 and sensors[7]["distance"] <1.0 and sensors[6]["distance"] >0.7:
                        return 0.2,0.5,False
                    if self.tourne_right(sensors):
                        if sensors[6]["distance"] < 0.3 and sensors[7]["distance"] >0.6 and sensors[5]["distance"] >0.45:
                            return 0.2,0.8,False
                        if sensors[6]["distance"] < 0.14 and sensors[7]["distance"] <0.21:
                            return 0.1,0.8,False
                        if sensors[1]["distance"] < 1 and sensors[7]["distance"] <1 and sensors[5]["distance"] <1 and sensors[3]["distance"] <1:
                            return self.evite_obstacle_front(sensors)
                        if ((sensors[5]["distance"] < 1 and sensors[0]["distance"] >0.7 and sensors[2]["distance"] >0.7 and 
                            sensors[4]["distance"] >0.7 and sensors[3]["distance"] >0.7 and sensors[6]["distance"] >0.7 and sensors[7]["distance"] >0.7) or
                            (sensors[3]["distance"] < 1 and sensors[0]["distance"] >0.7 and sensors[2]["distance"] >0.7 and 
                            sensors[4]["distance"] >0.7 and sensors[5]["distance"] >0.7 and sensors[6]["distance"] >0.7 and sensors[7]["distance"] >0.7)):
                            return self.hate_all(sensors)
                        return 0,-1,False
                    return self.love_wall(sensors,"right")
        return self.spirale()
    
    def walker(self,sensors) :
        # Comportement : se deplace en esquivant tout
        # renvoie les valeurs de translation et de rotation : pos -> tourne a droite, neg -> tourne a gauche

        if self.enemy_before(sensors):
            return self.follow_enemy(sensors)
        if self.enemy_following(sensors):
            return 0,0,False
        if self.ally_around(sensors) :
            return self.hate_all(sensors)
        if (sensors[2]["distance"]<1.0 and sensors[6]["distance"]<1.0 or
            sensors[3]["distance"]<1.0 and (sensors[4]["distance"]<1.0 or sensors[0]["distance"]<1.0) and
            sensors[5]["distance"]<1.0 and (sensors[1]["distance"]<1.0 or sensors[7]["distance"]<1.0)):#pas fini
            return self.evite_obstacle_front(sensors)
        return self.hate_all(sensors)
    
    def give_strat(self,sensors,liste_strat, modif_job) : 
        # Comportement : attributs une strat a chaque robot
        # return les valeurs de translation et rotation du job

        match modif_job :
            case 0 :
                return liste_strat[0](sensors)
            
            case 1 :
                return liste_strat[1](sensors)
            
            case _ :
                return liste_strat[0](sensors)
    
    def init_strat(self,num,nb_tour):
        if nb_tour > 0 and nb_tour < 500 :
            return 0+num
        
        if nb_tour > 500 and nb_tour < 1000 :
            return 1+num
        
        if nb_tour > 1000 and nb_tour < 1500 :
            return 2+num
        
        if nb_tour > 1500 and nb_tour < 2000 :
            return 3+num
        
        return 4+num

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        self.memory+=1
        list_strat = [self.strat_love_wall,self.hate_all]
        list_sensors=self.get_extended_sensors(sensors, sensor_view, sensor_robot, sensor_team)
        print(sensors)
        return self.strat_love_wall(list_sensors)