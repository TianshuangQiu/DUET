from duet.visualize.visualizer import Motifs, Visualizer
from yourdfpy import Robot, URDF

r = URDF.load("ur5/ur_with_gripper.xacro")
r.scene.show()
# # v = Visualizer()
# r.visualize(
#     [
#         [0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0.3],
#         [0, 0, 0, 0, 0, 0.4],
#         [0, 0, 0, 0, 0, 0.5],
#         [0, 0, 0, 0.2, 0, 0.5],
#         [0, 0, 0, 0.3, 0, 0.4],
#         [0, 0, 0, 0.4, 0, 0.3],
#     ]
# )
