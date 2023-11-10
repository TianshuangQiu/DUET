from duet.execute.motifs import *
from duet.execute.closed_loop import *
from ur5py import UR5Robot

robot = UR5Robot(gripper=2)
robot.set_playload(1.5)
robot.set_tcp([0, 0.0, 0.07, 0, 0, 0], False)
robot.move_joint(
    [
        1.496670961380004883e00,
        -1.375702683125631154e00,
        -5.044615904437463882e-01,
        -1.337908093129293263e00,
        1.725960969924926758e00,
        3.530181646347045898e00,
    ]
)
move_to_start(robot, [np.pi / 2, -np.pi / 2, 0, np.pi, 1.5 * np.pi, np.pi / 6])
# teach_mode(1, False, True)[0](robot)
# pdb.set_trace()
# waving_1(True, 2, False)(robot)
# hammer_floor(False)(robot)
# circle_horizontal(True)(robot)
# run_recording("IMG_4010.txt", False)[0](robot)
# circle_horizontal(True)(robot)
# hair_whip(False)(robot)
# horizontal_tag(False, 0.1)(robot)
# horizontal_tag(False, 0.05)(robot)
# locals["horizontal_tag"](**{"wrist_flip": 1, "speed": 0.1})(robot)
# teach_mode(10, 0, False)[0](robot)
