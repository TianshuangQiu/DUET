from ur5py.ur5 import UR5Robot
import numpy as np
import time
import math
import pdb
from tqdm import tqdm
import cowsay
from random import choice, uniform


def get_line(x1, y1, x2, y2):
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1
    return slope, intercept


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
            robot.move_joint(intermediate_pose, vel=0.5)

            # move to wrist 2 goal
            intermediate_pose[-3] = next_pose[-3]
            robot.move_joint(intermediate_pose, vel=0.5)

            # move to neutral position for wrist 2
            intermediate_pose[-1] = round_nearest(intermediate_pose[-2], np.pi)
            robot.move_joint(intermediate_pose, vel=0.5)

            # move to wrist 2 goal
            intermediate_pose[-2] = next_pose[-2]
            robot.move_joint(intermediate_pose, vel=0.5)

            # move to wrist 3 goal
            intermediate_pose[-1] = next_pose[-1]
            robot.move_joint(intermediate_pose, vel=0.5)

    robot.move_joint(next_pose)


def painter_vertical():
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
        move_to_start(robot, final_array[0])
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.02)
            time.sleep(0.02)
        robot.stop_joint()

    return run_on_robot


def cleaner_horizontal():
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
        move_to_start(robot, final_array[0])
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.02)
            time.sleep(0.02)
        robot.stop_joint()

    return run_on_robot


def circle_horizontal():
    temp = []
    final_array = []
    for x in np.arange(0, 120 * np.pi, np.pi / 40):
        temp.append(np.pi / 6 * math.cos(x) + np.pi)
        temp.append(np.pi / 10 * math.cos(x - np.pi / 2) - np.pi / 4)
        temp.append(
            np.pi / 4 * math.cos(x + np.pi / 2) - 7 * np.pi / 12
        )  # + 7*np.pi/12
        temp.append(np.pi / 12 * math.cos(x - np.pi / 2) + 1.15 * np.pi)
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0])
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.02)
            time.sleep(0.02)
        robot.stop_joint()

    return run_on_robot


def hammer_wall():
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
        move_to_start(robot, final_array[0])
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.02)
            time.sleep(0.02)
        robot.stop_joint()

    return run_on_robot


def hammer_floor():
    temp = []
    final_array = []
    grace = False
    prev_x = 0
    rewind_shift = 0
    hammer_shift = 0
    for x in np.arange(0, 100 * np.pi, np.pi / 8):
        temp.append(np.pi)
        temp.append(0)
        if x - prev_x == np.pi:
            grace = True
            prev_x = x
            rewind_shift += np.pi / 2
            hammer_shift += np.pi
        if grace and x - prev_x == 2 * np.pi:
            grace = False
            prev_x = x
        if not grace:
            temp.append(np.pi / 6 * math.cos(x - np.pi) - np.pi / 6)
        else:
            temp.append(np.pi / 6 * math.cos(0.5 * x - np.pi / 2) - np.pi / 6)
        # temp.append(np.pi / 6 * math.cos(0.5*x-np.pi/2) - np.pi / 6)
        temp.append(3 * np.pi / 2)
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0])
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.02)
            time.sleep(0.02)
        robot.stop_joint()

    return run_on_robot


def screw_lightbulb():
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
        move_to_start(robot, final_array[0])
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.1)
            time.sleep(0.1)
        robot.stop_joint()

    return run_on_robot


def waving():
    temp = []
    final_array = []
    for x in np.arange(0, 8 * np.pi, np.pi / 40):
        temp.append(np.pi / 2)
        temp.append(np.pi / 8 * math.cos(x) - np.pi / 2)
        temp.append(np.pi / 6 * math.cos(x - 0.5))
        temp.append(np.pi / 4 * math.cos(x) - np.pi / 2 + 3 * np.pi / 2)
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0])
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.02)
            time.sleep(0.02)
        robot.stop_joint()

    return run_on_robot


def metronome():
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
        move_to_start(robot, final_array[0])
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.02)
            time.sleep(0.02)
        robot.stop_joint()

    return run_on_robot


def circle_vertical():
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
        move_to_start(robot, final_array[0])
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.02)
            time.sleep(0.02)
        robot.stop_joint()

    return run_on_robot


def sweep_floor():
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
        # for i, arr in enumerate(tqdm(final_array)):
        #     robot.servo_joint(arr, time=0.05)
        #     time.sleep(0.05)
        robot.move_joint_path(final_array[::20], 0.7, 0.5, 0.5)
        robot.stop_joint()

    return run_on_robot


def yes(amp):
    final_array = []
    temp = []
    for x in np.arange(0, 9 * np.pi / 2, np.pi / 40):
        temp.append(np.pi)
        temp.append(-np.pi / 3)
        temp.append(np.pi / 4)
        temp.append(amp * math.cos(x) + 7 * np.pi / 6)
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0])
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.02)
            time.sleep(0.02)
        robot.stop_joint()

    return run_on_robot


def pointing():  # 0.01
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
        move_to_start(robot, final_array[0])
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.02)
            time.sleep(0.02)
        robot.stop_joint()

    return run_on_robot


def no(amp):
    final_array = []
    temp = []
    for x in np.arange(0, 9 * np.pi / 2, np.pi / 40):
        temp.append(np.pi)
        temp.append(-np.pi / 3)
        temp.append(np.pi / 4)
        temp.append(8 * np.pi / 7)
        temp.append(amp * math.cos(x) + 3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0])
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.02)
            time.sleep(0.02)
        robot.stop_joint()

    return run_on_robot


# def random_yes_no(ur):
#     funcs = [yes, no]
#     amp = uniform(np.pi / 12, np.pi / 3)
#     final_array = choice(funcs)(amp)
#     final_array = np.array(final_array)
#     # ur = UR5Robot(gripper=True)
#     ur.move_joint(final_array[0], vel=0.5)
#     # for i, arr in enumerate(final_array):
#     #     ur.servo_joint(arr.tolist(), acc=0.2, vel=0, time=0.05, lookahead_time=0.2)
#     #     time.sleep(0.05)
#     # ur.move_joint_path(
#     #     final_array,
#     #     vels=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
#     #     accs=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
#     #     blends=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05],
#     # )
#     for i, arr in enumerate(tqdm(final_array)):
#         ur.servo_joint(arr.tolist(), time=0.04)

#     time.sleep(5)

#     for i in range(28):
#         amp = uniform(np.pi / 12, np.pi / 3.5)
#         final_array = choice(funcs)(amp)
#         final_array = np.array(final_array)
#         for i, arr in enumerate(final_array):
#             # t = 0.05
#             # if i ==0:
#             #     t = 0.5
#             # ur.servo_joint(arr.tolist(), acc=0.2, vel=0, time=t, lookahead_time=0.2)
#             ur.servo_joint(arr.tolist(), time=0.04)
#             time.sleep(0.05)
#         time.sleep(5)


def horizontal_tag():  # add wrist flick up at each end
    final_array = []
    temp = []
    for x in np.arange(0, 10 * np.pi, np.pi / 40):
        temp.append(np.pi / 2 * math.cos(x) + np.pi)
        temp.append(-0.08)
        temp.append(0)
        temp.append(np.pi)
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0])
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.1)
            time.sleep(0.1)
        robot.stop_joint()

    return run_on_robot


def random_pointing():  # gripper CLOSED
    final_array = []
    temp = []

    # first pose
    prev_pan = pan_angle = uniform(0, 2 * np.pi)
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
    temp.append(3 * np.pi / 2)
    temp.append(0)
    final_array.append(temp)
    temp = []
    # point
    if wrist1_angle > -np.pi:
        lift_delta = 0.2
    else:
        lift_delta = -0.2
    for x in np.arange(0, 2 * np.pi, np.pi / 40):
        temp.append(pan_angle)
        if x > 2 * np.pi:
            temp.append(lift_angle)
        else:
            temp.append(lift_angle)
        temp.append(elbow_angle)
        temp.append(wrist1_angle)
        temp.append(3 * np.pi / 2)
        temp.append(0)
        final_array.append(temp)
        temp = []

    for x in range(25):
        # new pos
        pan_angle = uniform(0, 2 * np.pi)
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

        prev_pan = pan_angle
        prev_lift = lift_angle
        prev_elbow = elbow_angle
        prev_w1 = wrist1_angle

        for x in np.arange(0, 2 * np.pi, np.pi / 40):
            temp.append(pan_slope * x + pan_intercept)
            temp.append(lift_slope * x + lift_intercept)
            temp.append(elbow_slope * x + elbow_intercept)
            temp.append(w1_slope * x + w1_intercept)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []

        # point
        for x in np.arange(0, 2 * np.pi, np.pi / 40):
            temp.append(pan_angle)
            if x > 2 * np.pi:
                temp.append(lift_angle)
            else:
                temp.append(lift_angle)
            temp.append(elbow_angle)
            temp.append(wrist1_angle)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0])
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.05)
            time.sleep(0.05)
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


def handing_object():
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
        move_to_start(robot, final_array[0])
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.07)
            time.sleep(0.07)
        robot.stop_joint()

    return run_on_robot


def handing_object():
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
            # if release:
            #     gripper.append(0)
            # else:
            #     gripper.append(0.5)
        # release = not release

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0])
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.02)
            time.sleep(0.02)
        robot.stop_joint()

    return run_on_robot


def stop_each_joint():  # change wrist1 to be in positive values not negative
    # lift = []
    # elbow = []
    # wrist1 = []
    # wrist2 = []
    temp = []
    final_array = []
    for x in np.arange(0, 14 * np.pi, np.pi / 80):
        if x >= 39.87:
            temp.append(np.pi / 2)
            temp.append(-np.pi / 2)
            temp.append(0)
            temp.append(-np.pi / 2)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        elif x >= 27.304:
            temp.append(np.pi / 2)
            temp.append(-np.pi / 2)
            temp.append(0)
            temp.append(np.pi / 4 * math.cos(x - 0.6) - np.pi / 2)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        elif x >= 11 * np.pi / 2:
            temp.append(np.pi / 2)
            temp.append(-np.pi / 2)
            temp.append(np.pi / 4 * math.cos(x))
            temp.append(np.pi / 4 * math.cos(x - 0.6) - np.pi / 2)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        else:
            temp.append(np.pi / 2)
            temp.append(np.pi / 3 * math.cos(x) - np.pi / 2)
            temp.append(np.pi / 4 * math.cos(x - 0.6))
            temp.append(np.pi / 4 * math.cos(x - 0.6) - np.pi / 2)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0])
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.02)
            time.sleep(0.02)
        robot.stop_joint()

    return run_on_robot


def waltz():
    temp = []
    final_array = []
    for i in range(10):
        for x in np.arange(0, np.pi, np.pi / 40):
            temp.append(np.pi / 2)
            temp.append(np.pi / 6 * math.cos(x) - np.pi / 2)
            temp.append(0)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            temp.append(0)
            final_array.append(temp)
            temp = []
        for x in np.arange(0, np.pi, np.pi / 40):
            temp.append(np.pi / 2)
            temp.append(np.pi / 12 * math.cos(2 * x - np.pi) - 7 * np.pi / 12)
            temp.append(0)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            temp.append(0)
            final_array.append(temp)
            temp = []
        for x in np.arange(0, np.pi, np.pi / 40):
            temp.append(np.pi / 2)
            temp.append(np.pi / 6 * math.cos(x - np.pi) - np.pi / 2)
            temp.append(0)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            temp.append(0)
            final_array.append(temp)
            temp = []
        for x in np.arange(0, np.pi, np.pi / 40):
            temp.append(np.pi / 2)
            temp.append(np.pi / 12 * math.cos(2 * x) - 5 * np.pi / 12)
            temp.append(0)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            temp.append(0)
            final_array.append(temp)
            temp = []

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0])
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.02)
            time.sleep(0.02)
        robot.stop_joint()

    return run_on_robot


def bartender_shaking():
    # pan = []
    # lift = []
    # elbow = []
    # wrist1 = []
    # wrist2 = []
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
        move_to_start(robot, final_array[0])
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.016)
            time.sleep(0.016)
        robot.stop_joint()

    return run_on_robot


def bartender_pouring():
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
        move_to_start(robot, final_array[0])
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.02)
            time.sleep(0.02)
        robot.stop_joint()

    return run_on_robot


def box():
    final_array = []
    temp = []
    # looking from back of robot
    top_left = [3.66, -1.168, 0.981, 3.378, 4.236, 0]
    top_right = [2.62, -1.168, 0.981, 3.378, 5.14, 0]
    bottom_right = [2.62, -0.73, 1.544, 2.36, 5.14, 0]
    bottom_left = [3.66, -0.73, 1.544, 2.36, 4.236, 0]
    final_array.append(top_left)
    final_array.append(top_right)
    final_array.append(bottom_right)
    final_array.append(bottom_left)
    final_array.append(top_left)

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0])
        for i, arr in enumerate(tqdm(final_array)):
            robot.move_joint(arr, interp="tcp")
        robot.stop_joint()

    return run_on_robot


def bobbing_up_down():
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
        move_to_start(robot, final_array[0])
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.03)
            time.sleep(0.03)
        robot.stop_joint()

    return run_on_robot


def sawing(amp):
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
        move_to_start(robot, final_array[0])
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.02)
            time.sleep(0.02)
        robot.stop_joint()

    return run_on_robot

    # y1 = amp*math.cos((24*np.pi-np.pi/40)+np.pi) - np.pi/3
    # y2 = amp*math.cos((24*np.pi-np.pi/40)) + np.pi/2
    # y3 = 2*amp*math.cos(np.pi) - np.pi/3
    # y4 = 2*amp*math.cos(0) + np.pi/2
    # lift_slope, lift_intercept = get_line(0,y1, 2*np.pi, y3)
    # elbow_slope, elbow_intercept = get_line(0, y2, 2*np.pi, y4)

    # for x in np.arange(0, 2*np.pi, np.pi/40):
    #     temp.append(np.pi)
    #     temp.append(lift_slope*x + lift_intercept)
    #     temp.append(elbow_slope*x + elbow_intercept)
    #     temp.append(np.pi) #np.pi/48*math.cos(x) + 8*np.pi/9
    #     temp.append(3*np.pi/2)
    #     temp.append(0)
    #     final_array.append(temp)
    #     temp = []

    # for x in np.arange(0,24*np.pi, np.pi/40):
    #     temp.append(np.pi)
    #     temp.append(2*amp*math.cos(0.9*x+np.pi)-np.pi/3)
    #     temp.append(2*amp*math.cos(0.9*x)+np.pi/2)
    #     temp.append(np.pi) #np.pi/48*math.cos(x) + 8*np.pi/9
    #     temp.append(3*np.pi/2)
    #     temp.append(0)
    #     final_array.append(temp)
    #     temp = []
    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0])
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.02)
            time.sleep(0.02)
        robot.stop_joint()

    return run_on_robot


def tug_of_war():
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
