import numpy as np
import kinpy as kp

robot = kp.build_chain_from_urdf(open("ur5/ur5.urdf").read())
print(robot)
print(robot.forward_kinematics(np.array([0, 0, 0, 0, 0, 0.5])))
# robot.animate(
#     cfg_trajectory={
#         "shoulder_pan_joint": [-np.pi / 4, np.pi / 4],
#         "shoulder_lift_joint": [0.0, -np.pi / 2.0],
#         "elbow_joint": [0.0, np.pi / 2.0],
#     }
# )
