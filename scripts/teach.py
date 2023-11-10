from ur5py.ur5 import UR5Robot
import numpy as np
import time
from tqdm import tqdm
import cowsay

RECORD_TIME = 120
FILE_PATH = "same_point.txt"


def play(robot: UR5Robot, poses, vel=0.5, acc=0.5, blend=0.1):
    vels = np.ones_like(poses[:, 0]) * vel
    accs = np.ones_like(poses[:, 0]) * acc
    blends = np.ones_like(poses[:, 0]) * blend
    robot.move_joint_path(poses, vels, accs, blends)


def servo(robot, poses, **kwargs):
    for i, p in enumerate(tqdm(poses)):
        if i == 0:
            robot.move_joint(p, vel=0.5)
            continue
        last_record = time.time()
        robot.servo_joint(p, time=0.002, lookahead_time=0.2, gain=150)
        while time.time() - last_record < 0.002:
            pass


if __name__ == "__main__":
    ur = UR5Robot()
    # ur.gripper.open()
    print(ur.get_pose())
    ur.start_teach()
    ur.change_gripper(2)
    ur.gripper.calibrate()
    cowsay.cow("Robot now compliant")
    poses = []

    # in seconds

    for i in tqdm(range(int(RECORD_TIME / 0.002))):
        last_record = time.time()
        poses.append([i * 0.002, *ur.get_joints()])
        while time.time() - last_record < 0.002:
            pass
        ur.gripper.open()
    cowsay.cow("time's up!")
    poses = np.array(poses)
    np.savetxt(f"/home/ethantqiu/DUET/drive/{FILE_PATH}", poses)
    ur.force_mode(
        ur.get_pose(convert=False),
        [1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        2,
        [np.pi, np.pi, np.pi, np.pi, np.pi, np.pi],
        damping=0.1,
    )
    time.sleep(5)
    ur.end_force_mode()
    ur.stop_teach()
    # # playback
    # for i in range(0, 1):
    #     # ur.gripper.open()
    #     servo(ur, poses[:, 1:], vel=0.2 * i, acc=0.2 * i)
    #     # ur.gripper.close()
