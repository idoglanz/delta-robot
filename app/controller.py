import numpy as np

class DeltaController:
    # all units are assumed to be in mm for loc and mm/sec for speed
    def __init__(self, initial_pose, speed) -> None:
        self.current_loc = initial_pose
        self.speed = speed    
        self.z_offset = -260

    def next_action(self, action):
        command = action['command']
        goal = list(action['value'])
        goal = [g*3 for g in goal]
        goal[-1] += self.z_offset
        if command not in ['G1','G0']:  # currently only supports G1 and G0 ('move to') commands
            return self.current_loc, 0

        _distance = self._get_distance(goal)
        if _distance:
            duration = _distance/self.speed # duration of action execution
            self.current_loc = goal
            return goal, max(duration,0.2)
            
        return self.current_loc, 0

    def _get_distance(self, goal_loc):
        return np.linalg.norm(np.array(goal_loc)-np.array(self.current_loc))
    

