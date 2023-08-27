import numpy as np
import cowsay


class Motifs:
    def __init__(self) -> None:
        pass

    def filler(self, **kwargs):
        param_0 = kwargs["param0"]
        param_1 = kwargs["param1"]

        return np.ones((20, 6)) * param_0 + param_1


class Visualizer:
    def __init__(self, waypoints, robot_file="ur5/ur_with_gripper.xacro") -> None:
        from urdfpy import URDF

        self.waypoints = waypoints
        self.robot = URDF.load(robot_file)

    def visualize(self, time=30):
        self.robot.animate(self.waypoints, loop_time=time)
