from urdfpy import URDF
import numpy as np
import pdb
import trimesh

robot = URDF.load("ur5/ur_with_gripper.xacro")
# print(robot.actuated_joint_names)
robot.show(np.array([0, 0, 0, 0, 0, 0, 0.5]))
# component_array = robot.visual_trimesh_fk()
# list(component_array.keys())[0].show()
