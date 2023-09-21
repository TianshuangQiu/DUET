import numpy as np
import kinpy as kp
from urdfpy import URDF
import pdb

# robot = kp.build_chain_from_urdf(open("ur5/ur_with_gripper.xacro").read())
robot = URDF.load("ur5/ur_with_gripper.xacro")
# print(robot.get_joint_parameter_names())
fk = robot.link_fk(
    np.array(
        [
            0,
            0,
            0,
            0,
            0,
            0.5,
            0,
        ]
    )
)
print(list(fk))
k = list(fk.keys())
for kk in k:
    print(kk.name)
# pdb.set_trace()

# robot.animate(
#     cfg_trajectory={
#         "shoulder_pan_joint": [-np.pi / 4, np.pi / 4],
#         "shoulder_lift_joint": [0.0, -np.pi / 2.0],
#         "elbow_joint": [0.0, np.pi / 2.0],
#     }
# )
