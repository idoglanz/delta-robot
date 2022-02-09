import numpy as np
import plotly.graph_objects as go
from tenacity import retry
from inverse_kinematics import InverseKinematics
import logging

logger = logging.getLogger(__name__)


class DeltaRobot:
    def __init__(self, base_radius, gripper_radius, active_arm, passive_arm):
        self.base_radius = base_radius
        self.gripper_radius = gripper_radius
        self.active_arm = active_arm
        self.passive_arm = passive_arm
        self.theta = [0, 120, 240]
        self.inverse_k = InverseKinematics(
            self.base_radius, self.gripper_radius, self.active_arm, self.passive_arm, theta=self.theta
        )
        self.origin = [0, 0, 0]
        self.fig = go.Figure()
        self.gripper_loc = [0, 0, 0]
        self.phi = [0, 0, 0]
        self.base_coordinates = None
        self.gripper_coordinates = None
        self.arms_coordinates = None

    def update_pose(self, xyz):
        self.fig.data = []
        if isinstance(xyz, list):
            xyz = np.array(xyz)
        _phi = self.inverse_k.inverse(xyz)
        if _phi is not None:
            self.phi = _phi
            self.gripper_loc = xyz
        return list(self.gripper_loc)

    def update_structure(self, **kwargs):
        # update the structure of the robot
        self.base_radius = kwargs.get('base_radius') if kwargs.get('base_radius') else self.base_radius
        self.gripper_radius = kwargs.get('gripper_radius') if kwargs.get('gripper_radius') else self.gripper_radius
        self.active_arm = kwargs.get('active_arm') if kwargs.get('active_arm') else self.active_arm
        self.passive_arm = kwargs.get('passive_arm') if kwargs.get('passive_arm') else self.passive_arm
        self.inverse_k = InverseKinematics(
            self.base_radius, self.gripper_radius, self.active_arm, self.passive_arm, theta=self.theta
        )

    def draw(self):
        # note order does matter
        self.draw_base()
        self.draw_gripper()
        self.draw_active_arms()
        self.draw_passive_arms()
        d = 3 * self.base_radius
        self.fig.update_layout(
            scene=dict(
                xaxis=dict(
                    nticks=4,
                    range=[-d, d],
                ),
                yaxis=dict(
                    nticks=4,
                    range=[-d, d],
                ),
                zaxis=dict(
                    nticks=4,
                    range=[-d, d],
                ),
            ),
            width=700,
            margin=dict(r=10, l=10, b=10, t=10),
        )

        self.fig.update_layout(scene_aspectmode="cube")

        return self.fig

    def draw_base(self, **kwargs):
        # draw the top static triangle
        _theta = self.theta
        _theta.append(self.theta[0])  # to get a "closed" triangle
        _theta = np.array(_theta) * np.pi / 180
        _r = np.expand_dims(np.array([self.base_radius, 0, 0]), 1)
        triangle = np.hstack([np.matmul(self.rotM(angle, "z"), _r) for angle in _theta]).T + self.origin
        self.fig.add_trace(
            go.Scatter3d(
                x=triangle[:, 0],
                y=triangle[:, 1],
                z=triangle[:, 2],
                mode="lines",
                line={"width": 2, "color": "red"},
                name="Top",
            )
        )
        self.base_coordinates = triangle

    def draw_gripper(self, **kwargs):
        _theta = self.theta
        _theta.append(self.theta[0])  # to get a "closed" triangle
        _theta = np.array(_theta) * np.pi / 180
        _r = np.expand_dims(np.array([self.gripper_radius, 0, 0]), 1)
        triangle = np.hstack([np.matmul(self.rotM(angle, "z"), _r) for angle in _theta]).T + self.gripper_loc
        self.fig.add_trace(
            go.Scatter3d(
                x=triangle[:, 0],
                y=triangle[:, 1],
                z=triangle[:, 2],
                mode="lines",
                line={"width": 2, "color": "blue"},
                name="Gripper",
            )
        )
        self.gripper_coordinates = triangle

    def draw_active_arms(self, **kwargs):
        _theta = np.array(self.theta) * np.pi / 180
        vec = [
            np.matmul(self.rotM(np.deg2rad(_phi), "y"), np.expand_dims(np.array([self.active_arm, 0, 0]), 1))
            + np.expand_dims(np.array([self.base_radius, 0, 0]), 1)
            for _phi in self.phi
        ]
        arms = np.hstack([np.matmul(self.rotM(angle, "z"), v) for angle, v in zip(_theta, vec)]).T + self.origin
        for p1, p2 in zip(arms, self.base_coordinates[:3, :]):
            self.fig.add_trace(
                go.Scatter3d(
                    x=[p1[0], p2[0]],
                    y=[p1[1], p2[1]],
                    z=[p1[2], p2[2]],
                    mode="lines",
                    line={"width": 2, "color": "green"},
                    name="active_arm",
                )
            )
        self.arms_coordinates = arms

    def draw_passive_arms(self):
        for p1, p2 in zip(self.arms_coordinates, self.gripper_coordinates[:3, :]):
            self.fig.add_trace(
                go.Scatter3d(
                    x=[p1[0], p2[0]],
                    y=[p1[1], p2[1]],
                    z=[p1[2], p2[2]],
                    mode="lines",
                    line={"width": 2, "color": "orange"},
                    name="passive_arm",
                )
            )

    @staticmethod
    def rotM(theta_rad, axis: str = "z"):

        matrices = {
            "z": np.array(
                [[np.cos(theta_rad), -np.sin(theta_rad), 0], [np.sin(theta_rad), np.cos(theta_rad), 0], [0, 0, 1]]
            ),
            "x": np.array(
                [[1, 0, 0], [0, np.cos(theta_rad), -np.sin(theta_rad)], [0, np.sin(theta_rad), np.cos(theta_rad)]]
            ),
            "y": np.array(
                [[np.cos(theta_rad), 0, np.sin(theta_rad)], [0, 1, 0], [np.sin(theta_rad), 0, -np.cos(theta_rad)]]
            ),
        }
        return matrices.get(axis)


if __name__ == "__main__":
    robot = DeltaRobot(base_radius=20, gripper_radius=10, active_arm=12, passive_arm=40)
    robot.update_pose([0,20,-40])
    robot.draw()