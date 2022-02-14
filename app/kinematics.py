import numpy as np

class InverseKinematics:
    def __init__(self, base_triangle, gripper_triangle, rod_active,rod_passive, theta) -> None:
        self.base_triangle = base_triangle
        self.gripper_triangle = gripper_triangle
        self.rod_active = rod_active
        self.rod_passive = rod_passive
        self.theta = np.array(theta).T*np.pi/180

    @property
    def r(self):
        return np.vstack([self.base_triangle*(np.cos(self.theta)),self.base_triangle*(np.sin(self.theta)), np.zeros([3])]).T

    @property
    def R(self):
        return np.vstack([self.gripper_triangle*(np.cos(self.theta)),self.gripper_triangle*(np.sin(self.theta)), np.zeros([3])]).T

    def inverse(self, desired_loc_xyz:np.array):
        
        r = self.r
        R = self.R + desired_loc_xyz.T
        Cr = (R[:,0] - r[:,0])*np.cos(self.theta) + (R[:,1] - r[:,1])*np.sin(self.theta)
        Ct = -(R[:,0] - r[:,0])*np.sin(self.theta) + (R[:,1] - r[:,1])*np.cos(self.theta)
        Cz = desired_loc_xyz[-1]*np.ones([3])
        A = self.rod_active*np.ones([3])
        b = self.rod_passive*np.ones([3])
        B = np.sqrt(b**2 - Ct**2)
        C = np.sqrt(Cr**2 + Cz**2)
        alpha = -np.arctan2(Cz,Cr)*180/np.pi
        beta_rad = (A**2 + C**2 - B**2)/(2*A*C)
        if all(np.abs(beta_rad) <= 1):
            beta = np.arccos(beta_rad)*180/np.pi
            phiA = -(alpha-beta)
            return phiA
        else:
            print('Something is off with the settings or pose out of reach')
            return None
            

class ForwardKinematics:
    def __init__(self) -> None:
        raise NotImplementedError


if __name__ == "__main__":
    robot = InverseKinematics(base_triangle=75,gripper_triangle=24,rod_active=100,rod_passive=300)

    robot.inverse(np.array([0,0,-200]))
