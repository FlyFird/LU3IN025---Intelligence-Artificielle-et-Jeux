import random
from robot import *
import robot_ga_fixed as ga_mod

nb_robots = 0

class Robot_player(Robot):
    """
    Challenger arbre de comportement:
    1. Eviter les enemies (si n'importe quel enemies detecter tourner dans l'autre directon)
    2. Longer un mur si il est latéral avec une proba de 0.9, sinon avoider
    3. Eviter les murs
    4. GA optimisé
    """
    team_name = "LesKabyles"
    robot_id = -1

    # sensor groups
    LATERAL_SENSORS     = [sensor_front_left, sensor_left, sensor_front_right, sensor_right]
    NON_LATERAL_SENSORS = [sensor_front, sensor_rear_left, sensor_rear, sensor_rear_right]

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="A"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        # GA fixed agent
        self.ga_agent = ga_mod.Robot_player(x_0, y_0, theta_0,
                                            name=team, team=self.team_name)
        super().__init__(x_0, y_0, theta_0, name=name, team=self.team_name)

    def reset(self):
        super().reset()
        self.ga_agent.reset()

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        
         # 1) Single robot detection -> opposite direction
        if any(view == 2 for view in sensor_view):
            return 1.0, 1.0, False
            
            
        # 2) Lateral wall detection
        if sensor_view and any(sensor_view[i] == 1 for i in self.LATERAL_SENSORS):
            if random.random() < 0.9:
                # SideWall hugging
                thr = sensors[sensor_front]
                translation = thr * 0.5
                rot_left  = sensors[sensor_left] + sensors[sensor_front_left]
                rot_right = sensors[sensor_right] + sensors[sensor_front_right]
                rotation  = (rot_left - rot_right) * 0.2
                rotation  = max(min(rotation, 1.0), -1.0)
                return translation, rotation, False
            else:
                # RandomDirectionAvoider for walls
                free_dirs = [i for i in range(8)
                             if not (sensor_view and sensor_view[i] == 1)]
                if not free_dirs:
                    return 1.0, random.uniform(-1.0, 1.0), False
                dir_idx = random.choice(free_dirs)
                angle   = dir_idx * 45 if dir_idx <= 4 else (dir_idx - 8) * 45
                if angle > 180:
                    angle -= 360
                rotation = angle / 180.0
                return 1.0, rotation, False

        # 3) Non-lateral wall detection
        if sensor_view and any(sensor_view[i] == 1 for i in self.NON_LATERAL_SENSORS):
            free_dirs = [i for i in range(8)
                         if not (sensor_view and sensor_view[i] == 1)]
            if not free_dirs:
                return 1.0, random.uniform(-1.0, 1.0), False
            dir_idx = random.choice(free_dirs)
            angle   = dir_idx * 45 if dir_idx <= 4 else (dir_idx - 8) * 45
            if angle > 180:
                angle -= 360
            rotation = angle / 180.0
            return 1.0, rotation, False

        # 4) Otherwise: GA fixed navigation
        return self.ga_agent.step(sensors, sensor_view, sensor_robot, sensor_team)
