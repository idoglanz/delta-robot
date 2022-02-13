import numpy as np

class DeltaController:
    # all units are assumed to be in mm for loc and mm/sec for speed
    def __init__(self, initial_pose, speed, gcode_parser) -> None:
        self.current_loc = initial_pose
        self.speed = speed
        self.gloader = gcode_parser
    
    def run(self):
        for action in self.gloader:
            pass
        
    def next_action(self, goal):
        _distance = self._get_distance(goal)
        if _distance:
            delay = _distance/self.speed # duration of action execution
            self.current_loc = goal
            return goal, delay
        return self.current_loc, 0

    def _get_distance(self, goal_loc):
        return np.linalg.norm(np.array(goal_loc)-np.array(self.current_loc))
    

