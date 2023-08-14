from urdfpy import URDF
import numpy as np

robot = URDF.load("ur5/ur_with_gripper.xacro")
robot.show()
# robot.animate(
#     cfg_trajectory={
#         "shoulder_pan_joint": [-np.pi / 4, np.pi / 4],
#         "shoulder_lift_joint": [0.0, -np.pi / 2.0],
#         "elbow_joint": [0.0, np.pi / 2.0],
#     }
# )
