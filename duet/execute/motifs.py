from ur5py.ur5 import UR5Robot
import numpy as np
import time
import math
import pdb
from tqdm import tqdm
import cowsay
import os
import sympy
import time
import datetime
from random import choice, uniform


def get_line(x1, y1, x2, y2):
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1
    return slope, intercept


def round_nearest(x, base, offset=0):
    return base * round((x - offset) / base) + offset


def move_to_start(robot: UR5Robot, next_pose, wrist_flip=False):
    robot.gripper.close()
    # pdb.set_trace()
    prev_pose = np.array(robot.get_joints())
    next_pose = np.array(next_pose)
    # Set to neutral pose for wrist 1

    # Collision detection
    interpolated_wrist = np.linspace(prev_pose, next_pose, 100)
    potential_collision = np.logical_and(
        interpolated_wrist[:, 3] <= np.pi * 0.75,
        interpolated_wrist[:, 3] >= np.pi * 0.25,
    )
    tmp_coll = np.logical_and(
        interpolated_wrist[:, 4] <= 1.25 * np.pi,
        interpolated_wrist[:, 4] >= 0.75 * np.pi,
    )
    potential_collision = np.logical_and(potential_collision, tmp_coll)
    poses = np.array(
        [
            [np.pi, 1.5 * np.pi, 0.5 * np.pi],
            [0, 1.5 * np.pi, 0.5 * np.pi],
            [0, 1.5 * np.pi, 0],
            [0, 0.5 * np.pi, 0],
        ]
    )
    if np.any(potential_collision):
        # Move to closer one
        inv = np.linalg.norm(poses[0] - prev_pose[3:]) > np.linalg.norm(
            poses[-1] - prev_pose[3:]
        )
        if inv:
            poses = poses[::-1]
        for p in poses:
            prev_pose[3:] = p
            robot.move_joint(prev_pose)
    # robot.move_pose(robot.get_fk(next_pose))
    robot.move_joint(next_pose)


def painter_vertical(wrist_flip: bool):
    final_array = []
    temp = []
    for x in np.arange(0, 120 * np.pi, np.pi / 40):
        temp.append(np.pi)
        temp.append(np.pi / 8 * math.cos(x - np.pi) - np.pi / 6)
        temp.append(np.pi / 20 * math.cos(x))
        temp.append(np.pi / 6 * math.cos(x) + 8 * np.pi / 7)
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.1)
            current_time = time.time()
            while time.time() - current_time < 0.1:
                pass
        robot.stop_joint()

    return run_on_robot


def cleaner_horizontal(wrist_flip: bool):
    temp = []
    final_array = []
    for x in np.arange(0, 20 * np.pi, np.pi / 8):
        temp.append(np.pi / 8 * math.cos(x) + np.pi)
        temp.append(np.pi / 14 * math.cos(2 * x) - 19 * np.pi / 60)
        temp.append(np.pi / 12 * math.cos(2 * x - np.pi) + np.pi / 3.5)
        temp.append(np.pi)
        temp.append(np.pi / 12 * math.cos(x + np.pi) + 3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.1)
            current_time = time.time()
            while time.time() - current_time < 0.1:
                pass
        robot.stop_joint()

    return run_on_robot


def circle_horizontal(wrist_flip: bool):
    temp = []
    final_array = []
    for x in np.arange(0, 32 * np.pi, np.pi / 40):
        temp.append(np.pi / 6 * math.cos(x) + np.pi)
        temp.append(np.pi / 10 * math.cos(x - np.pi / 2) - np.pi / 4)
        temp.append(np.pi / 4 * math.cos(x + np.pi / 2) + 7 * np.pi / 12)
        temp.append(np.pi / 12 * math.cos(x - np.pi / 2) + 1.15 * np.pi)
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.05)
            current_time = time.time()
            while time.time() - current_time < 0.05:
                pass
        robot.stop_joint()

    return run_on_robot


def hammer_wall(wrist_flip: bool):
    temp = []
    final_array = []
    for x in np.arange(0, 8 * np.pi, np.pi / 8):
        temp.append(np.pi)
        temp.append(np.pi / 8)
        temp.append(np.pi / 6 * math.cos(x) - np.pi / 2)
        temp.append(5 * np.pi / 4)
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.15)
            current_time = time.time()
            while time.time() - current_time < 0.15:
                pass
        robot.stop_joint()

    return run_on_robot


def hammer_floor(wrist_flip: bool):
    temp = []
    final_array = []
    grace = False
    prev_x = 0
    rewind_shift = 0
    hammer_shift = 0
    for x in np.arange(0, 116 * np.pi, np.pi / 10):
        temp.append(np.pi)
        temp.append(0)
        # if x - prev_x == np.pi:
        #     grace = True
        #     prev_x = x
        #     rewind_shift += np.pi / 2
        #     hammer_shift += np.pi
        # if grace and x - prev_x == 2 * np.pi:
        #     grace = False
        #     prev_x = x
        # if not grace:
        temp.append(np.pi / 6 * math.cos(x - np.pi) - np.pi / 6)
        # else:
        #     temp.append(np.pi / 6 * math.cos(0.5 * x - np.pi / 2) - np.pi / 6)
        # temp.append(np.pi / 6 * math.cos(0.5*x-np.pi/2) - np.pi / 6)
        temp.append(3 * np.pi / 2)
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.15)
            current_time = time.time()
            while time.time() - current_time < 0.15:
                pass
        robot.stop_joint()

    return run_on_robot


def screw_lightbulb(wrist_flip: bool):
    offset = 0
    temp = []
    final_array = []
    for x in np.arange(0, 64 * np.pi, np.pi / 8):
        temp.append(np.pi)
        temp.append(-np.pi / 8)
        temp.append(-np.pi / 2.7)
        temp.append(np.pi)
        temp.append(3 * np.pi / 2)
        temp.append(np.pi / 6 * math.cos(x - offset))
        # gripper.append(0.25*math.cos(x-offset))
        if x % np.pi == 0:
            offset += np.pi
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.1)
            current_time = time.time()
            while time.time() - current_time < 0.1:
                pass
        robot.stop_joint()

    return run_on_robot


def waving(wrist_flip: bool):
    temp = []
    final_array = []
    for x in np.arange(0, 18 * np.pi, np.pi / 400):
        temp.append(np.pi / 2)
        temp.append(np.pi / 8 * math.cos(x) - np.pi / 2)
        temp.append(np.pi / 6 * math.cos(x - 0.5))
        temp.append(np.pi / 4 * math.cos(x) - np.pi / 2 + 3 * np.pi / 2)
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.01)
            current_time = time.time()
            while time.time() - current_time < 0.01:
                pass
        robot.stop_joint()

    return run_on_robot


def metronome(wrist_flip: bool):
    temp = []
    final_array = []
    for x in np.arange(0, 300 * np.pi, np.pi / 40):
        temp.append(np.pi / 2)
        temp.append(-np.pi / 2)
        temp.append(np.pi / 20 * math.cos(x) - np.pi / 3)
        temp.append(np.pi)
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.1)
            current_time = time.time()
            while time.time() - current_time < 0.1:
                pass
        robot.stop_joint()

    return run_on_robot


def circle_vertical(wrist_flip: bool):
    final_array = []
    temp = []
    for x in np.arange(0, 32 * np.pi, np.pi / 40):
        temp.append(np.pi / 10 * math.cos(x) + np.pi)
        temp.append(np.pi / 12 * math.cos(x - np.pi / 2) - np.pi / 4)
        temp.append(np.pi / 12 * math.cos(x - np.pi / 2) + np.pi / 6)
        temp.append(np.pi / 10 * math.cos(x - 3 * np.pi / 2) + 7 * np.pi / 6)
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.05)
            current_time = time.time()
            while time.time() - current_time < 0.05:
                pass
        robot.stop_joint()

    return run_on_robot


# Copied-
def circle_vertical_gradual_increase(wrist_flip):
    final_array = []
    temp = []
    for x in np.arange(0, 170 * np.pi, np.pi / 40):
        temp.append(np.pi / 10 * math.e ** (0.01 * x - 5) * math.cos(x) + np.pi)
        temp.append(
            np.pi / 12 * math.e ** (0.01 * x - 5) * math.cos(x - np.pi / 2) - np.pi / 4
        )
        temp.append(
            np.pi / 12 * math.e ** (0.01 * x - 5) * math.cos(x - np.pi / 2) + np.pi / 6
        )
        temp.append(
            np.pi / 10 * math.e ** (0.01 * x - 5) * math.cos(x - 3 * np.pi / 2)
            + 7 * np.pi / 6
        )
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []
    for x in np.arange(0, 20 * np.pi, np.pi / 40):
        temp.append(
            np.pi / 10 * math.e ** (0.01 * 170 * np.pi - 5) * math.cos(x) + np.pi
        )
        temp.append(
            np.pi / 12 * math.e ** (0.01 * 170 * np.pi - 5) * math.cos(x - np.pi / 2)
            - np.pi / 4
        )
        temp.append(
            np.pi / 12 * math.e ** (0.01 * 170 * np.pi - 5) * math.cos(x - np.pi / 2)
            + np.pi / 6
        )
        temp.append(
            np.pi
            / 10
            * math.e ** (0.01 * 170 * np.pi - 5)
            * math.cos(x - 3 * np.pi / 2)
            + 7 * np.pi / 6
        )
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        robot.move_joint(final_array[0], vel=0.5)
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.05)
            current_time = time.time()
            while time.time() - current_time < 0.05:
                pass
        robot.stop_joint()

    return run_on_robot


def circle_vertical_gradual_decrease(wrist_flip):
    final_array = []
    temp = []
    for x in np.arange(0, 20 * np.pi, np.pi / 40):
        temp.append(
            np.pi / 10 * math.e ** (0.01 * 170 * np.pi - 5) * math.cos(x) + np.pi
        )
        temp.append(
            np.pi / 12 * math.e ** (0.01 * 170 * np.pi - 5) * math.cos(x - np.pi / 2)
            - np.pi / 4
        )
        temp.append(
            np.pi / 12 * math.e ** (0.01 * 170 * np.pi - 5) * math.cos(x - np.pi / 2)
            + np.pi / 6
        )
        temp.append(
            np.pi
            / 10
            * math.e ** (0.01 * 170 * np.pi - 5)
            * math.cos(x - 3 * np.pi / 2)
            + 7 * np.pi / 6
        )
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []
    for x in np.arange(170 * np.pi, 0, -np.pi / 40):
        temp.append(np.pi / 10 * math.e ** (0.01 * x - 5) * math.cos(x) + np.pi)
        temp.append(
            np.pi / 12 * math.e ** (0.01 * x - 5) * math.cos(x - np.pi / 2) - np.pi / 4
        )
        temp.append(
            np.pi / 12 * math.e ** (0.01 * x - 5) * math.cos(x - np.pi / 2) + np.pi / 6
        )
        temp.append(
            np.pi / 10 * math.e ** (0.01 * x - 5) * math.cos(x - 3 * np.pi / 2)
            + 7 * np.pi / 6
        )
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        robot.move_joint(final_array[0], vel=0.5)
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.05)
            current_time = time.time()
            while time.time() - current_time < 0.05:
                pass
        robot.stop_joint()

    return run_on_robot


def sweep_floor(wrist_flip: bool):
    final_array = []
    temp = []
    for x in np.arange(0, 32 * np.pi, np.pi / 40):
        temp.append(np.pi / 6 * math.cos(x) + np.pi)
        temp.append(np.pi / 14 * math.cos(x - np.pi / 2) - np.pi / 3)
        temp.append(np.pi / 14 * math.cos(x + np.pi / 2) + 7 * np.pi / 12)
        temp.append(7 * np.pi / 6)
        temp.append(np.pi / 7 * math.cos(x) + 4 * np.pi / 3)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], True)
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.05)
            current_time = time.time()
            while time.time() - current_time < 0.05:
                pass
        # robot.move_joint_path(final_array[::20], 0.7, 0.5, 0.5)
        robot.stop_joint()

    return run_on_robot


# Copied-
def sweep_floor_increasing(wrist_flip):
    final_array = []
    temp = []
    for x in np.arange(0, 192 * np.pi, np.pi / 100):
        temp.append(np.pi / 6 * math.e ** (-0.004 * x + 0.5) * math.cos(x) + np.pi)
        temp.append(
            np.pi / 7 * math.e ** (-0.004 * x + 0.5) * math.cos(x - np.pi / 2)
            - np.pi / 3.2
        )
        temp.append(
            np.pi / 6 * math.e ** (-0.004 * x + 0.5) * math.cos(x + np.pi / 2)
            + 6 * np.pi / 12
        )
        temp.append(7 * np.pi / 6)
        temp.append(np.pi / 7 * math.cos(x) + 4 * np.pi / 3)
        temp.append(0)
        final_array.append(temp)
        temp = []

        def run_on_robot(robot: UR5Robot):
            robot.move_joint(final_array[0], vel=0.5)
            count = 0
            for i, arr in enumerate(tqdm(final_array)):
                robot.servo_joint(arr, time=0.03, gain=500)
                current_time = time.time()
                while time.time() - current_time < 0.03:
                    pass
                if count == 2304:
                    robot.stop_joint()
                    robot.gripper.open()
                    robot.gripper.close()
                count += 1
            robot.stop_joint()

    return run_on_robot


def yes(wrist_flip: bool, amp, pan, length):
    final_array = []
    temp = []
    for x in np.arange(0, length + np.pi / 40, np.pi / 40):
        temp.append(pan)
        temp.append(-np.pi / 3)
        temp.append(np.pi / 4)
        temp.append(amp * math.cos(x) + 8 * np.pi / 7)
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []
    for x in np.arange(0, 2 * np.pi, np.pi / 40):
        temp.append(pan)
        temp.append(-np.pi / 3)
        temp.append(np.pi / 4)
        temp.append(amp * math.cos(length) + 8 * np.pi / 7)
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        t = 0.04
        if amp < np.pi / 8:
            t = 0.01
        for i, arr in enumerate(final_array):
            robot.servo_joint(arr, time=t)
            current_time = time.time()
            while time.time() - current_time < t:
                pass
        robot.stop_joint()

    return run_on_robot


def pointing(wrist_flip: bool):  # 0.01
    final_array = []
    temp = []
    for x in np.arange(0, 4 * np.pi, np.pi / 40):
        temp.append(np.pi)
        temp.append(np.pi / 48 * math.cos(x - np.pi) - np.pi / 3)
        temp.append(np.pi / 48 * math.cos(x) + np.pi / 4)
        temp.append(7 * np.pi / 6)
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.01)
            current_time = time.time()
            while time.time() - current_time < 0.01:
                pass
        robot.stop_joint()

    return run_on_robot


def no(wrist_flip: bool, amp, pan, length):
    final_array = []
    temp = []
    for x in np.arange(0, length + np.pi / 40, np.pi / 40):
        temp.append(pan)
        temp.append(-np.pi / 3)
        temp.append(np.pi / 4)
        temp.append(8 * np.pi / 7)
        temp.append(amp * math.cos(x) + 3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []
    for x in np.arange(0, 2 * np.pi, np.pi / 40):
        temp.append(pan)
        temp.append(-np.pi / 3)
        temp.append(np.pi / 4)
        temp.append(8 * np.pi / 7)
        temp.append(amp * math.cos(length) + 3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        t = 0.04
        if amp < np.pi / 8:
            t = 0.01
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=t)
            current_time = time.time()
            while time.time() - current_time < t:
                pass
        robot.stop_joint()

    return run_on_robot


def random_yes_no(wrist_flip: bool, amount: int, in_place: int):
    amp_range = [0.2617, 1.047]
    if in_place == 1:
        pan_range = [np.pi, np.pi]
    else:
        pan_range = [0, 2 * np.pi]
    length_range = [2 * np.pi, 14 * np.pi]
    funcs = []
    rand = np.random.random(amount)
    for i in range(amount):
        wf = i == 0 and wrist_flip
        if rand[i] < 0.5:
            funcs.append(
                yes(
                    wf,
                    np.random.uniform(amp_range[0], amp_range[1]),
                    np.random.uniform(pan_range[0], pan_range[1]),
                    np.random.uniform(length_range[0], length_range[1]),
                )
            )
        else:
            funcs.append(
                no(
                    wf,
                    np.random.uniform(
                        amp_range[0],
                        amp_range[1],
                    ),
                    np.random.uniform(pan_range[0], pan_range[1]),
                    np.random.uniform(length_range[0], length_range[1]),
                )
            )

    def run_on_robot(robot: UR5Robot):
        for i, f in enumerate(tqdm(funcs)):
            f(robot)

    return run_on_robot, amount * 8


def horizontal_tag(wrist_flip: bool, speed: float):
    final_array = []
    temp = []
    for x in np.arange(0, 10 * np.pi, np.pi / 50):
        temp.append(np.pi / 2 * math.cos(x) + np.pi)
        temp.append(-2 * np.pi / 9)
        temp.append(np.pi / 6)
        temp.append(np.pi)
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=speed, lookahead_time=0.2, gain=500)
            current_time = time.time()
            while time.time() - current_time < speed:
                pass
        robot.stop_joint()

    return run_on_robot


def random_pointing(
    wrist_flip: bool, in_plane, start_pause, end_pause
):  # gripper CLOSED
    final_array = []
    temp = []
    w2s, w2i = get_line(2 * np.pi / 3, 5.63, 4 * np.pi / 3, 3.78)
    speed_up = False
    if in_plane == 1:
        in_plane = True
    else:
        in_plane = False
    if start_pause != end_pause:
        speed_up = True
    pause = start_pause
    # first pose
    if in_plane:
        prev_pan = pan_angle = uniform(2 * np.pi / 3, 4 * np.pi / 3)
        prev_w2 = wrist2_angle = w2s * pan_angle + w2i
    else:
        prev_pan = pan_angle = uniform(0, 2 * np.pi)
        prev_w2 = wrist2_angle = 3 * np.pi / 2
    prev_lift = lift_angle = uniform(-np.pi / 3, -np.pi / 7)
    if lift_angle < -np.pi / 4:
        prev_elbow = elbow_angle = uniform(np.pi / 10, np.pi / 3)
    else:
        prev_elbow = elbow_angle = uniform(-np.pi / 4, np.pi / 10)
    prev_w1 = wrist1_angle = uniform(np.pi - np.pi / 4, np.pi + np.pi / 4)
    # go to first pose
    temp.append(pan_angle)
    temp.append(lift_angle)
    temp.append(elbow_angle)
    temp.append(wrist1_angle)
    temp.append(wrist2_angle)
    temp.append(0)
    final_array.append(temp)
    temp = []
    # point
    if wrist1_angle > -np.pi:
        lift_delta = 0.2
    else:
        lift_delta = -0.2
    for x in np.arange(0, pause, np.pi / 40):
        temp.append(pan_angle)
        if x > 2 * np.pi:
            temp.append(lift_angle)
        else:
            temp.append(lift_angle)
        temp.append(elbow_angle)
        temp.append(wrist1_angle)
        temp.append(wrist2_angle)
        temp.append(0)
        final_array.append(temp)
        temp = []

    for x in range(9):
        # new pos
        if speed_up:
            pause -= (start_pause - end_pause) / 10
        if in_plane:
            pan_angle = uniform(2 * np.pi / 3, 4 * np.pi / 3)
            wrist2_angle = w2s * pan_angle + w2i
        else:
            pan_angle = uniform(0, 2 * np.pi)
            wrist2_angle = 3 * np.pi / 2
        lift_angle = uniform(-np.pi / 3, -np.pi / 4)
        if lift_angle < -np.pi / 4:
            elbow_angle = uniform(np.pi / 10, np.pi / 4)
        else:
            elbow_angle = uniform(-np.pi / 4, np.pi / 10)
        wrist1_angle = uniform(np.pi - np.pi / 4, np.pi + np.pi / 4)
        if wrist1_angle > -np.pi:
            lift_delta = 0.2
        else:
            lift_delta = -0.2

        # transition
        pan_slope, pan_intercept = get_line(0, prev_pan, 2 * np.pi, pan_angle)
        lift_slope, lift_intercept = get_line(0, prev_lift, 2 * np.pi, lift_angle)
        elbow_slope, elbow_intercept = get_line(0, prev_elbow, 2 * np.pi, elbow_angle)
        w1_slope, w1_intercept = get_line(0, prev_w1, 2 * np.pi, wrist1_angle)
        w2_slope, w2_intercept = get_line(0, prev_w2, 2 * np.pi, wrist2_angle)

        prev_pan = pan_angle
        prev_lift = lift_angle
        prev_elbow = elbow_angle
        prev_w1 = wrist1_angle
        prev_w2 = wrist2_angle

        for x in np.arange(0, 2 * np.pi, np.pi / 40):
            temp.append(pan_slope * x + pan_intercept)
            temp.append(lift_slope * x + lift_intercept)
            temp.append(elbow_slope * x + elbow_intercept)
            temp.append(w1_slope * x + w1_intercept)
            temp.append(w2_slope * x + w2_intercept)
            temp.append(0)
            final_array.append(temp)
            temp = []

        # point
        for x in np.arange(0, pause, np.pi / 40):
            temp.append(pan_angle)
            if x > 2 * np.pi:
                temp.append(lift_angle)
            else:
                temp.append(lift_angle)
            temp.append(elbow_angle)
            temp.append(wrist1_angle)
            temp.append(wrist2_angle)
            temp.append(0)
            final_array.append(temp)
            temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.05, gain=500)
            current_time = time.time()
            while time.time() - current_time < 0.05:
                pass
        robot.stop_joint()

    return run_on_robot


def hair_whip(wrist_flip: bool):  # add wrist flick up at each end
    final_array = []
    temp = []
    for x in np.arange(0, 10 * np.pi, np.pi / 100):
        temp.append(np.pi / 3 * math.cos(x) + np.pi)
        temp.append(np.pi / 12 * math.cos(2 * x - np.pi) - np.pi / 5)
        temp.append(np.pi / 4 * math.cos(2 * x - np.pi - 0.5))
        temp.append(np.pi)
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.05)
            current_time = time.time()
            while time.time() - current_time < 0.05:
                pass
        time.sleep(0.1)
        robot.stop_joint()

    return run_on_robot


# def move_and_pose():
#     pan_angle = uniform(3 * np.pi / 4, 5 * np.pi / 4)
#     lift_angle = uniform(-np.pi / 3, -np.pi / 4)
#     elbow_angle = uniform(np.pi / 10, np.pi / 4)
#     elbow_angle = uniform(-np.pi / 4, np.pi / 10)
#     wrist1_angle = uniform(-np.pi / 4 - np.pi, -np.pi + np.pi / 4)
#     final_array = []
#     temp = []
#     for x in np.arange(0, 9 * np.pi / 2, np.pi / 40):
#         temp.append(np.pi / 6 * math.cos(x) + np.pi)
#         temp.append(-0.08)
#         temp.append(0)
#         temp.append(np.pi)
#         temp.append(3 * np.pi / 2)
#         temp.append(0)
#         final_array.append(temp)
#         temp = []
#     def run_on_robot(robot: UR5Robot):
#     for i, arr in enumerate(tqdm(final_array)):
#         robot.servo_joint(arr, time=0.02)
#     time.sleep(0.02)

# return run_on_robot


def handing_object(wrist_flip: bool):
    final_array = []
    temp = []
    # gripper = []
    # lift = []
    # elbow = []
    # wrist1 = []
    # wrist2 = []
    # wrist3 = []
    release = False
    for i in range(5):
        for x in np.arange(0, np.pi, np.pi / 40):
            temp.append(np.pi)
            temp.append(np.pi / 8 * math.cos(x - np.pi) - np.pi / 4)
            temp.append(np.pi / 8 * math.cos(x) + np.pi / 4)
            temp.append(5 * np.pi / 4)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
            # if release:
            #     gripper.append(0.5)
            # else:
            #     gripper.append(0)
        for x in np.arange(0, np.pi / 2, np.pi / 40):
            temp.append(np.pi)
            temp.append(np.pi / 8 - np.pi / 4)
            temp.append(-np.pi / 8 + np.pi / 4)
            temp.append(5 * np.pi / 4)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
            # if release:
            #     gripper.append(0.25*math.cos(x) +0.25)
            # else:
            #     gripper.append(0.25*math.cos(x-np.pi) +0.25)
        for x in np.arange(np.pi, 2 * np.pi, np.pi / 40):
            temp.append(np.pi)
            temp.append(np.pi / 8 * math.cos(x - np.pi) - np.pi / 4)
            temp.append(np.pi / 8 * math.cos(x) + np.pi / 4)
            temp.append(5 * np.pi / 4)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        #     if release:
        #         gripper.append(0)
        #     else:
        #         gripper.append(0.5)
        # release = not release

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.07)
            current_time = time.time()
            while time.time() - current_time < 0.07:
                pass
        robot.stop_joint()

    return run_on_robot


# Copied-
def vertical_lightbulb(wrist_flip: bool):
    temp = []
    final_array = []
    offset = 0
    for x in np.arange(0, 16 * np.pi, np.pi / 8):
        temp.append(np.pi / 2)
        temp.append(-np.pi / 2)
        temp.append(0)
        temp.append(np.pi)
        temp.append(3 * np.pi / 2)
        temp.append(np.pi / 6 * math.cos(x - offset))
        final_array.append(temp)
        temp = []
        if x % np.pi == 0:
            offset += np.pi

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.1)
            time.sleep(0.1)
        robot.stop_joint()

    return run_on_robot


def stop_each_joint(
    wrist_flip: bool,
):
    temp = []
    final_array = []
    for x in np.arange(0, 24 * np.pi, np.pi / 400):
        if x >= 39.87 and x < 43.012:
            temp.append(np.pi / 2)
            temp.append(-np.pi / 2)
            temp.append(0)
            temp.append(3 * np.pi / 2)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        elif (x >= 27.304 and x < 39.87) or (x >= 43.012 and x < 52.436):
            temp.append(np.pi / 2)
            temp.append(-np.pi / 2)
            temp.append(0)
            temp.append(np.pi / 4 * math.cos(x - 0.6) + 3 * np.pi / 2)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        elif (x >= 11 * np.pi / 2 and x < 27.304) or (
            x >= 52.436 and x < 39 * np.pi / 2
        ):
            temp.append(np.pi / 2)
            temp.append(-np.pi / 2)
            temp.append(np.pi / 4 * math.cos(x - 0.6))
            temp.append(np.pi / 4 * math.cos(x - 0.6) + 3 * np.pi / 2)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        elif x < 11 * np.pi / 2 or x >= 39 * np.pi / 2:
            temp.append(np.pi / 2)
            temp.append(np.pi / 3 * math.cos(x) - np.pi / 2)
            temp.append(np.pi / 4 * math.cos(x - 0.6))
            temp.append(np.pi / 4 * math.cos(x - 0.6) + 3 * np.pi / 2)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        for i, arr in enumerate(tqdm(final_array)):
            current_time = time.time()
            robot.servo_joint(arr, time=0.01)
            while time.time() - current_time < 0.01:
                pass
        robot.stop_joint()

    return run_on_robot


def waltz(wrist_flip: bool):
    temp = []
    final_array = []
    for i in range(10):
        for x in np.arange(0, np.pi / 2, np.pi / 80):
            temp.append(np.pi / 2)
            temp.append(np.pi / 6 * math.cos(2 * x) - np.pi / 2)
            temp.append(0)
            temp.append(3 * np.pi / 2)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        for x in np.arange(0, 2 * np.pi / 3, np.pi / 80):
            temp.append(np.pi / 2)
            temp.append(np.pi / 12 * math.cos(3 * x - np.pi) - 7 * np.pi / 12)
            temp.append(0)
            temp.append(3 * np.pi / 2)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        for x in np.arange(np.pi / 2, np.pi, np.pi / 80):
            temp.append(np.pi / 2)
            temp.append(np.pi / 6 * math.cos(2 * x) - np.pi / 2)
            temp.append(0)
            temp.append(3 * np.pi / 2)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        for x in np.arange(0, 2 * np.pi / 3, np.pi / 80):
            temp.append(np.pi / 2)
            temp.append(np.pi / 12 * math.cos(3 * x) - 5 * np.pi / 12)
            temp.append(0)
            temp.append(3 * np.pi / 2)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.02)
            current_time = time.time()
            while time.time() - current_time < 0.02:
                pass
        robot.stop_joint()

    return run_on_robot


def bartender_shaking(wrist_flip: bool, is_fast: int):
    temp = []
    final_array = []
    for x in np.arange(0, 31 * np.pi / 2, np.pi / 40):
        temp.append(np.pi)
        temp.append(np.pi / 48 * math.cos(x))  # +np.pi/4
        temp.append(np.pi / 24 * math.cos(x) - np.pi / 3)
        temp.append(np.pi / 12 * math.cos(x) + 7 * np.pi / 6)
        temp.append(np.pi / 8 * math.cos(2 * x) + 3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []
    y1 = np.pi / 48 * math.cos(31 * np.pi / 2)  # +np.pi/4
    y2 = np.pi / 48 * math.cos(55 * np.pi / 2) - np.pi / 3
    lift_slope, lift_intercept = get_line(31 * np.pi / 2, y1, 55 * np.pi / 2, y2)
    y1 = np.pi / 24 * math.cos(31 * np.pi / 2) - np.pi / 3  # 2*np.pi/3
    y2 = np.pi / 24 * math.cos(55 * np.pi / 2) + np.pi / 6
    elbow_slope, elbow_intercept = get_line(31 * np.pi / 2, y1, 55 * np.pi / 2, y2)

    for x in np.arange(31 * np.pi / 2, 55 * np.pi / 2, np.pi / 40):
        temp.append(np.pi / 12 * math.cos(x - np.pi) + np.pi)
        temp.append(lift_slope * x + lift_intercept)
        temp.append(elbow_slope * x + elbow_intercept)
        temp.append(7 * np.pi / 6)
        temp.append(11 * np.pi / 8)
        temp.append(0)
        final_array.append(temp)
        temp = []

    for x in np.arange(55 * np.pi / 2, 85 * np.pi / 2, np.pi / 40):
        temp.append(np.pi)
        temp.append(np.pi / 48 * math.cos(x) - np.pi / 3)
        temp.append(np.pi / 24 * math.cos(x) + np.pi / 6)
        temp.append(np.pi / 12 * math.cos(x) + 7 * np.pi / 6)
        temp.append(np.pi / 8 * math.cos(2 * x) + 3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    y1 = np.pi / 48 * math.cos(85 * np.pi / 2) - np.pi / 3
    y2 = np.pi / 48 * math.cos(109 * np.pi / 2)  # +np.pi/4
    lift_slope, lift_intercept = get_line(85 * np.pi / 2, y1, 109 * np.pi / 2, y2)
    y1 = np.pi / 24 * math.cos(85 * np.pi / 2) + np.pi / 6
    y2 = np.pi / 24 * math.cos(109 * np.pi / 2) - np.pi / 3  # 2*np.pi/3
    elbow_slope, elbow_intercept = get_line(85 * np.pi / 2, y1, 109 * np.pi / 2, y2)

    for x in np.arange(85 * np.pi / 2, 109 * np.pi / 2, np.pi / 40):
        temp.append(np.pi / 12 * math.cos(x - np.pi) + np.pi)
        temp.append(lift_slope * x + lift_intercept)
        temp.append(elbow_slope * x + elbow_intercept)
        temp.append(7 * np.pi / 6)
        temp.append(11 * np.pi / 8)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        if is_fast == 1:
            t = 0.016
        else:
            t = 0.07
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=t)
            current_time = time.time()
            while time.time() - current_time < t:
                pass
        robot.stop_joint()

    return run_on_robot


def bartender_pouring(wrist_flip: bool, is_fast: int):
    temp = []
    final_array = []
    for x in np.arange(0, 6 * np.pi, np.pi / 40):
        temp.append(np.pi)
        temp.append(np.pi / 20 * math.cos(x) - np.pi / 2.5)
        temp.append(np.pi / 8 * math.e ** (-0.2 * x) * math.cos(x) + np.pi / 2.5)
        temp.append(7 * np.pi / 6)
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        if is_fast == 1:
            t = 0.02
        else:
            t = 0.07
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=t)
            current_time = time.time()
            while time.time() - current_time < t:
                pass
        robot.stop_joint()

    return run_on_robot


def box(wrist_flip: bool, num_repeat):
    final_array = []
    temp = []
    # looking from back of robot
    top_left = [5.23, -1.168, 0.981, 3.378, 4.236, 0]  # 3.66, 2.62
    top_right = [4.19, -1.168, 0.981, 3.378, 5.14, 0]
    bottom_right = [4.19, -0.73, 1.544, 2.36, 5.14, 0]
    bottom_left = [5.23, -0.73, 1.544, 2.36, 4.236, 0]
    final_array.append(top_left)
    final_array.append(top_right)
    final_array.append(bottom_right)
    final_array.append(bottom_left)
    final_array.append(top_left)

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        for j in tqdm(range(num_repeat)):
            for i, arr in enumerate(final_array):
                robot.move_joint(arr, interp="tcp")
        robot.stop_joint()

    return run_on_robot, num_repeat * 5


def bobbing_up_down(wrist_flip: bool):
    temp = []
    final_array = []
    for x in np.arange(0, 96 * np.pi, np.pi / 40):
        temp.append(np.pi / 3 * math.cos(0.1 * x) + np.pi)
        temp.append(np.pi / 12 * math.cos(x + np.pi) - np.pi / 6)
        temp.append(np.pi / 6 * math.cos(x))
        temp.append(np.pi / 12 * math.cos(x + np.pi) + 7 * np.pi / 6)
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.03)
            current_time = time.time()
            while time.time() - current_time < 0.03:
                pass
        robot.stop_joint()

    return run_on_robot


def sawing(amp, wrist_flip: bool):
    temp = []
    final_array = []
    i = amp
    for x in np.arange(0, 48 * np.pi, np.pi / 40):
        if x % (8 * np.pi):
            i += np.pi / 256
        temp.append(np.pi)
        temp.append(i * math.cos(x + np.pi) - np.pi / 3)
        temp.append(i * math.cos(x) + np.pi / 2)
        temp.append(np.pi)  # np.pi/48*math.cos(x) + 8*np.pi/9
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []
    for j in range(5):
        pan = uniform(np.pi / 2, 3 * np.pi / 2)
        i = amp
        for x in np.arange(0, 48 * np.pi, np.pi / 40):
            if x % (8 * np.pi):
                i += np.pi / 256
            temp.append(pan)
            temp.append(i * math.cos(x + np.pi) - np.pi / 3)
            temp.append(i * math.cos(x) + np.pi / 2)
            temp.append(np.pi)  # np.pi/48*math.cos(x) + 8*np.pi/9
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.02)
            current_time = time.time()
            while time.time() - current_time < 0.02:
                pass
        robot.stop_joint()

    return run_on_robot


def tutting_in_place(num_repeat: int, wrist_flip: bool):
    temp = []
    final_array = []
    # tut = lambda a: -np.pi / 20 * math.sin(a)
    # pose = [np.pi, -np.pi / 2, np.pi / 2, 7 * np.pi / 6, 3 * np.pi / 2, 0]
    # first pose
    for i in range(num_repeat):
        for x in np.arange(0, np.pi, np.pi / 80):
            temp.append(-np.pi / 20 * math.sin(x) + np.pi)
            temp.append(-np.pi / 2)
            temp.append(np.pi / 2)
            temp.append(7 * np.pi / 6)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        for x in np.arange(0, np.pi, np.pi / 80):
            temp.append(np.pi)
            temp.append(-np.pi / 20 * math.sin(x) - np.pi / 2)
            temp.append(np.pi / 2)
            temp.append(7 * np.pi / 6)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        for x in np.arange(0, np.pi, np.pi / 80):
            temp.append(np.pi)
            temp.append(-np.pi / 2)
            temp.append(-np.pi / 20 * math.sin(x) + np.pi / 2)
            temp.append(7 * np.pi / 6)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        for x in np.arange(0, np.pi, np.pi / 80):
            temp.append(np.pi)
            temp.append(-np.pi / 2)
            temp.append(np.pi / 2)
            temp.append(-np.pi / 20 * math.sin(x) + 7 * np.pi / 6)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        for x in np.arange(0, np.pi, np.pi / 80):
            temp.append(np.pi)
            temp.append(-np.pi / 2)
            temp.append(np.pi / 2)
            temp.append(7 * np.pi / 6)
            temp.append(-np.pi / 20 * math.sin(x) + 3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        for x in np.arange(0, np.pi, np.pi / 80):
            temp.append(np.pi)
            temp.append(-np.pi / 2)
            temp.append(np.pi / 2)
            temp.append(7 * np.pi / 6)
            temp.append(3 * np.pi / 2)
            temp.append(-np.pi / 20 * math.sin(x) + 0)
            final_array.append(temp)
            temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.01)
            current_time = time.time()
            while time.time() - current_time < 0.01:
                pass
        robot.stop_joint()

    return run_on_robot, num_repeat * 4


def tutting_growing(wrist_flip: bool):
    temp = []
    final_array = []
    # tut = lambda a: -np.pi / 20 * math.sin(a)
    # pose = [np.pi, -np.pi / 2, np.pi / 2, 7 * np.pi / 6, 3 * np.pi / 2, 0]
    pan_offset = 0
    lift_offset = 0
    elbow_offset = 0
    w1_offset = 0
    w2_offset = 0
    w3_offset = 0
    prev_lift = 0
    prev_w2 = 3 * np.pi / 2
    prev_elbow = np.pi / 2
    for i in range(25):
        mult = choice([-1, 1])
        amp = -np.pi / 20 * mult
        for x in np.arange(0, np.pi / 2, np.pi / 80):
            temp.append(amp * math.sin(x) + np.pi + pan_offset)
            temp.append(-np.pi / 2 + lift_offset)
            temp.append(np.pi / 2 + elbow_offset)
            temp.append(7 * np.pi / 6 + w1_offset)
            temp.append(3 * np.pi / 2 + w2_offset)
            temp.append(0 + w3_offset)
            final_array.append(temp)
            temp = []
        pan_offset += amp

        mult = choice([-1, 1])
        if prev_lift < -2 * np.pi / 3:  # need a check for value of prev_elbow
            mult = -1
        elif prev_lift > -np.pi / 4:  # need a check for value of prev_elbow
            mult = 1
        amp = -np.pi / 20 * mult
        for x in np.arange(0, np.pi / 2, np.pi / 80):
            temp.append(np.pi + pan_offset)
            temp.append(amp * math.sin(x) - np.pi / 2 + lift_offset)
            temp.append(np.pi / 2 + elbow_offset)
            temp.append(7 * np.pi / 6 + w1_offset)
            temp.append(3 * np.pi / 2 + w2_offset)
            temp.append(0 + w3_offset)
            final_array.append(temp)
            temp = []
        prev_lift = amp + np.pi / 2 + lift_offset
        lift_offset += amp

        mult = choice([-1, 1])
        if prev_lift < -2 * np.pi / 3:
            if prev_elbow > np.pi / 2:
                mult = 1
            elif prev_elbow < -np.pi / 6:
                mult = -1
        elif prev_lift > -np.pi / 4:
            if prev_elbow < -np.pi / 2:
                mult = 1
            elif prev_elbow > np.pi / 6:
                mult = -1
        amp = -np.pi / 20 * mult
        for x in np.arange(0, np.pi / 2, np.pi / 80):
            temp.append(np.pi + pan_offset)
            temp.append(-np.pi / 2 + lift_offset)
            temp.append(amp * math.sin(x) + np.pi / 2 + elbow_offset)
            temp.append(7 * np.pi / 6 + w1_offset)
            temp.append(3 * np.pi / 2 + w2_offset)
            temp.append(0 + w3_offset)
            final_array.append(temp)
            temp = []
        prev_elbow = amp - np.pi / 2 + elbow_offset
        elbow_offset += amp

        mult = choice([-1, 1])
        amp = -np.pi / 20 * mult
        for x in np.arange(0, np.pi / 2, np.pi / 80):
            temp.append(np.pi + pan_offset)
            temp.append(-np.pi / 2 + lift_offset)
            temp.append(np.pi / 2 + elbow_offset)
            temp.append(amp * math.sin(x) + 7 * np.pi / 6 + w1_offset)
            temp.append(3 * np.pi / 2 + w2_offset)
            temp.append(0 + w3_offset)
            final_array.append(temp)
            temp = []
        w1_offset += amp

        mult = choice([-1, 1])
        if prev_w2 < np.pi:
            mult = -1
        elif prev_w2 > 2 * np.pi:
            mult = 1
        amp = -np.pi / 20 * mult
        for x in np.arange(0, np.pi / 2, np.pi / 80):
            temp.append(np.pi + pan_offset)
            temp.append(-np.pi / 2 + lift_offset)
            temp.append(np.pi / 2 + elbow_offset)
            temp.append(7 * np.pi / 6 + w1_offset)
            temp.append(amp * math.sin(x) + 3 * np.pi / 2 + w2_offset)
            temp.append(0 + w3_offset)
            final_array.append(temp)
            temp = []
        prev_w2 = amp + 3 * np.pi / 2 + w2_offset
        w2_offset += amp

        mult = choice([-1, 1])
        amp = -np.pi / 20 * mult
        for x in np.arange(0, np.pi / 2, np.pi / 80):
            temp.append(np.pi + pan_offset)
            temp.append(-np.pi / 2 + lift_offset)
            temp.append(np.pi / 2 + elbow_offset)
            temp.append(7 * np.pi / 6 + w1_offset)
            temp.append(3 * np.pi / 2 + w2_offset)
            temp.append(amp * math.sin(x) + 0 + w3_offset)
            final_array.append(temp)
            temp = []
        w3_offset += amp

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.01)
            current_time = time.time()
            while time.time() - current_time < 0.01:
                pass
        robot.stop_joint()

    return run_on_robot


# def tutting(wrist_flip: bool):
#     temp = []
#     final_array = []
#     tut = lambda a: -np.pi / 20 * math.sin(a)
#     pose = [np.pi, -np.pi / 2, np.pi / 2, 7 * np.pi / 6, 3 * np.pi / 2, 0]
#     # first pose
#     for x in np.arange(0, np.pi, np.pi / 80):
#         temp.append(np.pi)
#         temp.append(-np.pi / 2)
#         temp.append(np.pi / 2)
#         temp.append(7 * np.pi / 6)
#         temp.append(3 * np.pi / 2)
#         temp.append(0)
#         final_array.append(temp)
#         temp = []
#     for i in range(6):
#         for x in np.arange(0, 2 * np.pi, np.pi / 80):
#             for j in range(6):
#                 if i == j:
#                     temp.append(pose[i] + tut(x))
#                 else:
#                     temp.append(pose[i])
#             final_array.append(temp)
#             temp = []
#     for i in range(36):
#         for x in np.arange(0, np.pi, np.pi / 80):
#             for j in range(6):
#                 if (i % 6) == j:
#                     temp.append(pose[i%6] + tut(x))
#                 else:
#                     temp.append(pose[i%6])
#             final_array.append(temp)
#             temp = []

#     def run_on_robot(robot: UR5Robot):
#         move_to_start(robot, final_array[0], wrist_flip)
#         for i, arr in enumerate(tqdm(final_array)):
#             robot.servo_joint(arr, time=0.5)
#             current_time = time.time()
#             while time.time() - current_time < 0.5:
#                 pass
#         robot.stop_joint()

#     return run_on_robot


def tug_of_war(wrist_flip: bool):
    def run_on_robot(robot: UR5Robot):
        robot.force_mode(
            robot.get_pose(convert=False),
            [1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            2,
            [np.pi, np.pi, np.pi, np.pi, np.pi, np.pi],
            damping=0.4,
        )
        damp_level = [0.2, 0.15, 0.1, 0.05]
        for d in damp_level:
            time.sleep(30)
            cowsay.cow(f"New damping level: {d}")
            robot.force_mode_set_damping(d)
        time.sleep(30)
        cowsay.cow("time's up")
        time.sleep(15)
        robot.end_force_mode()

    return run_on_robot


def wait_for_tap(wrist_flip: bool):
    def run_on_robot(robot: UR5Robot):
        robot.change_gripper(2)
        current_pose = robot.get_pose(convert=False)
        # print(current_pose)
        # angle = np.arctan2(current_pose[-2] ** 2, current_pose[-3] ** 2)
        # pi_2 = np.pi**2
        current_pose[-2] = 0
        current_pose[-3] = 0
        print(current_pose)
        # current_pose[-1] = round_nearest(current_pose[-1], np.pi)
        prev_force = None
        robot.move_pose(current_pose, convert=False)
        robot.gripper.open()
        time.sleep(0.5)
        while True:
            if prev_force is None:
                prev_force = np.array(robot.get_current_force()[:3])
                continue
            curr_force = np.array(robot.get_current_force()[:3])
            diff = np.linalg.norm(curr_force - prev_force)
            print(diff)
            if diff > 20:
                robot.gripper.close()
                cowsay.cow("closed")
                break
            else:
                prev_force = curr_force
                time.sleep(0.5)

    return run_on_robot


def run_recording(file_path, wrist_flip):
    final_array = np.loadtxt(os.path.join("drive", file_path))
    runtime = final_array[-1][0]

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0][1:], wrist_flip)
        for i, arr in enumerate(tqdm(final_array)):
            if i == 0:
                continue
            time_delta = final_array[i][0] - final_array[i - 1][0]
            robot.servo_joint(arr[1:], time=time_delta, gain=500)
            current_time = time.time()
            while time.time() - current_time < time_delta:
                pass
        robot.stop_joint()

    return run_on_robot, runtime


def teach_mode(num_sec: float, playback: [bool, int], wrist_flip: bool = False):
    def run_on_robot(robot: UR5Robot):
        teach_start = np.array([94, -72, 134, 117, 270, 180]) * np.pi / 180
        move_to_start(robot, teach_start, wrist_flip)
        robot.start_teach()
        poses = []
        for i in tqdm(range(int(num_sec / 0.002))):
            last_record = time.time()
            poses.append([i * 0.002, *robot.get_joints()])
            while time.time() - last_record < 0.002:
                pass
        np.savetxt("/home/ethantqiu/DUET/drive/TMP_SAVE.txt", poses)
        robot.force_mode(
            robot.get_pose(convert=False),
            [1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0],
            2,
            [np.pi, np.pi, np.pi, np.pi, np.pi, np.pi],
            damping=0.2,
        )
        time.sleep(5)
        robot.end_force_mode()
        robot.stop_teach()
        if playback:
            for i, p in enumerate(tqdm(poses)):
                if i == 0:
                    move_to_start(robot, p[1:], False)
                    continue
                last_record = time.time()
                robot.servo_joint(p[1:], time=0.002, lookahead_time=0.2, gain=150)
                while time.time() - last_record < 0.002:
                    pass
            robot.stop_joint()

    if playback:
        num_sec *= 2
    return run_on_robot, num_sec
