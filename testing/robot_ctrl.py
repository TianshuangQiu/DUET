import ur5py
import numpy as np
import pandas as pd
import time
from tqdm import tqdm
import pdb
from ur5py.ur5 import UR5Robot


def move_to_start(robot: UR5Robot, next_pose, wrist_flip=False):
    if wrist_flip:
        prev_pose = np.array(robot.get_joints())
        next_pose = np.array(next_pose)
        if np.any(np.abs(prev_pose[-3:] - next_pose[-3]) > np.pi / 2):
            # cowsay.cow("Possible collision")
            intermediate_pose = prev_pose
            intermediate_pose[-3:] = [np.pi, 1.5 * np.pi, 0.5 * np.pi]
            robot.move_joint(intermediate_pose, vel=0.5)
            intermediate_pose[-3] = next_pose[-3]
            robot.move_joint(intermediate_pose, vel=0.5)
            intermediate_pose[-1] = 0
            robot.move_joint(intermediate_pose, vel=0.5)
            intermediate_pose[-2] = next_pose[-2]
            robot.move_joint(intermediate_pose, vel=0.5)
            intermediate_pose[-1] = next_pose[-1]
            robot.move_joint(intermediate_pose, vel=0.5)
    robot.move_joint(next_pose.tolist())


robot = ur5py.UR5Robot("172.22.22.3")
path = "drive/IMG_4014.dat"
plan = np.loadtxt(path)[::200, 1:7]
# plan[:, 1] *= -1
# plan[:, 1] = plan[:, 1][0]
# pdb.set_trace()

move_to_start(robot, plan[0], False)
robot.move_joint_path(plan, 1, 0.7, 0.5)

# for p in tqdm(plan):
#     robot.servo_joint(p, time=0.004)
#     time.sleep(0.004)

# for p in tqdm(plan):
#     last_time = time.time()
#     robot.servo_joint(p, time=0.004)
#     while time.time() - last_time < 0.004:
#         pass
# robot.stop_joint()
