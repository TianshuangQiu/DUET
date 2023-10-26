import ur5py
import numpy as np
import pandas as pd
import time
from tqdm import tqdm
import pdb
from ur5py.ur5 import UR5Robot


def round_nearest(x, base, offset=0):
    return base * round((x - offset) / base) + offset


def move_to_start(robot: UR5Robot, next_pose, wrist_flip=False):
    if wrist_flip:
        prev_pose = np.array(robot.get_joints())
        next_pose = np.array(next_pose)
        if np.any(np.abs(prev_pose[-3:] - next_pose[-3]) > np.pi / 2):
            # Set to neutral pose for wrist 1
            intermediate_pose = prev_pose
            intermediate_pose[-3] = round_nearest(prev_pose[-3], np.pi / 2)
            intermediate_pose[-2] = round_nearest(
                prev_pose[-2], np.pi, offset=np.pi / 2
            )
            intermediate_pose[-1] = round_nearest(
                prev_pose[-1], np.pi, offset=np.pi / 2
            )
            if intermediate_pose[-1] == 2 * np.pi:
                intermediate_pose[-1] -= np.pi
            robot.move_joint(intermediate_pose, vel=1)

            # move to wrist 2 goal
            intermediate_pose[-3] = next_pose[-3]
            robot.move_joint(intermediate_pose, vel=1)

            # move to neutral position for wrist 2
            intermediate_pose[-1] = round_nearest(intermediate_pose[-2], np.pi)
            robot.move_joint(intermediate_pose, vel=1)

            # move to wrist 2 goal
            intermediate_pose[-2] = next_pose[-2]
            robot.move_joint(intermediate_pose, vel=1)

            # move to wrist 3 goal
            intermediate_pose[-1] = next_pose[-1]
            robot.move_joint(intermediate_pose, vel=1)

    robot.move_joint(next_pose)


robot = ur5py.UR5Robot("172.22.22.3")

# path = [
#     "drive/IMG_4010.txt",
#     "drive/IMG_4013.txt",
#     "drive/IMG_4014.txt",
#     "drive/IMG_4015.txt",
#     "drive/IMG_4015.txt",
# ]
path = ["drive/wave1.txt"]
for i, p in enumerate(path):
    plan = np.loadtxt(p)[:, :]
    # plan[:, 1] *= -1
    # plan[:, 1] = plan[:, 1][0]
    # pdb.set_trace()

    move_to_start(robot, plan[0], i == 0)
    # robot.move_joint_path(plan, 1, 0.7, 0.5)

    # for p in tqdm(plan):
    #     robot.servo_joint(p, time=0.004)
    #     time.sleep(0.004)

    for p in tqdm(plan):
        last_time = time.time()
        robot.servo_joint(p, time=0.004)
        while time.time() - last_time < 0.004:
            pass
    robot.stop_joint()
