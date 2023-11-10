from .motifs import *
import numpy as np
import time
from ur5py.ur5 import UR5Robot

# beat_timestamps = [] #suppose the ground truth has a timestamp for each beat

start_time = time.time()

# while True:
#    elapsed_time = time.time() - start_time
#    if elapsed_time in beat_timestamps:
#        index = beat_timestamps.index(elapsed_time)
#        interval = beat_timestamps[index + 1] - beat_timestamps[index]
#        waving(wrist_flip=?, time_interval=interval)

# take care of case where if beat too short double/triple it until threashold. \
# Preprocess beat_timestamps
# threashold = 0.5
# for timestamp in beat_timestamps:
#    ind = beat_timestamps.index(timestamp)
#    while beat_timestamps[ind+1] - beat_timestamps[ind] < threashold:
#        del beat_timestamps[ind + 1]


# #If we have frequency instead of timestamps:
# music_time = ?
# pose_freq = ?
# for i in np.arange(pose_freq):
#     waving(wrist_flip = ?, time_interval = music_time / pose_freq)


def waving_1(wrist_flip: bool, time_interval, default_curve: bool = False):
    temp = []
    final_array = []

    all_start = np.array(
        [
            np.pi,
            -np.pi / 4,
            -np.pi / 2,
            1.25 * np.pi,
            1.5 * np.pi,
            -0.5 * np.pi,
        ]
    )
    all_end = np.array(
        [
            np.pi,
            -0.75 * np.pi,
            0.5 * np.pi,
            0.75 * np.pi,
            1.5 * np.pi,
            0.5 * np.pi,
        ]
    )
    sub_start = np.array(
        [
            # wrist 2:
            -0.5
            * np.pi
        ]
    )
    sub_end = np.array([0.5 * np.pi])

    # supposing that the robot does not take time moving to starting position
    num_points = int(time_interval / 0.002)
    sub_num_points = int(num_points / 2)

    sub_array = np.linspace(sub_start, sub_end, sub_num_points)
    sub_array = np.concatenate((sub_array, sub_array[::-1]), axis=0)
    sub_array = np.repeat(sub_array, 2)

    final_array = np.linspace(all_start, all_end, num_points)
    final_array = np.concatenate((final_array, final_array[::-1]), axis=0)

    final_array[:, -1] = sub_array
    # adding path back to initial position

    def run_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        for i, arr in enumerate(tqdm(final_array)):
            robot.servo_joint(arr, time=0.002, lookahead_time=0.2, gain=1000)
            current_time = time.time()
            while time.time() - current_time < 0.002:
                pass
        robot.stop_joint(5)

    def run_default_on_robot(robot: UR5Robot):
        move_to_start(robot, final_array[0], wrist_flip)
        robot.move_joint(all_end)
        robot.move_joint(all_start)
        robot.stop_joint(5)

    if default_curve:
        return run_default_on_robot
    else:
        return run_on_robot
