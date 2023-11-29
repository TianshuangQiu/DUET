from .motifs import *
import numpy as np
import time
from ur5py.ur5 import UR5Robot
from roboticstoolbox.tools.trajectory import quintic
from roboticstoolbox.tools.trajectory import trapezoidal
import librosa


start_time = time.time()

def waving_1(wrist_flip: bool, time_interval, default_curve: bool = False):
    temp = []
    final_array = []

    all_start = np.array(
        [
            np.pi,
            -np.pi / 4,
            -np.pi / 2,
            1.25 * np.pi,
            #1.5 * np.pi,
            1.3 * np.pi,
            -0.5 * np.pi,
        ]
    )
    all_end = np.array(
        [
            np.pi,
            -0.75 * np.pi,
            0.5 * np.pi,
            0.75 * np.pi,
            #1.5 * np.pi,
            1.7 * np.pi,
            0.5 * np.pi,
        ]
    )
    sub_start = np.array(
        [
            # wrist 2:
            1.3
            * np.pi
        ]
    )
    sub_end = np.array([1.7 * np.pi])

    # NON-LINEAR
    num_points = int(time_interval / 0.002)

    final_array = np.zeros((num_points * 2, 6))
    for i in range(6):
        full_cycle_pos = helper_sine(all_start[i], all_end[i], num_points)
        final_array[:, i] = full_cycle_pos
    
    sub_array = helper_sine(all_start[-2], all_end[-2], int(num_points / 2))
    sub_array = np.concatenate((sub_array, sub_array), axis=0)
    final_array[:, -2] = sub_array

    def helper_sine(ini_start, ini_end, num):
        time = np.linspace(0, 1, num)
        speed = np.sin(np.pi * time)
        position = np.cumsum(speed)
        scaled_position = position - position[0]
        scaled_position = scaled_position / scaled_position[-1]
        scaled_position = ini_start + (ini_end - ini_start)*scaled_position
        full_cycle_pos = np.concatenate((scaled_position, scaled_position[::-1]), axis=0)
        return full_cycle_pos
    
    def helper_quintic(ini_start, ini_end, num):
        time = np.linspace(0, 1, num)
        trajectory = quintic(ini_start, ini_end, time)
        #positions = trajectory.y[:, 0]
        positions = trajectory.q
        full_cycle_pos = np.concatenate((positions, positions[::-1]), axis=0)
        return full_cycle_pos

    def helper_trapezoidal(ini_start, ini_end, num):
        time = np.linspace(0, 1, num)
        trajectory = trapezoidal(ini_start, ini_end, time)
        #positions = trajectory.y[:, 0]
        positions = trajectory.q
        full_cycle_pos = np.concatenate((positions, positions[::-1]), axis=0)
        return full_cycle_pos
        

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

# For dancing to a song (with a file input)
def get_bpm(file):
    y, sr = librosa.load(file, duration = None)
    tempo, beats = librosa.beat.beat_track(y, sr)
    timestamps = librosa.frames_to_time(beats, sr = sr)
    intervals = np.diff(timestamps)
    return intervals
    #return tempo (if just want to use global beat)
def safe_interval(intervals, threshold):
    safe_interval = []
    i = 0
    while i < len(intervals):
        curr_interval = intervals[i]
        while i + 1 < len(intervals) and curr_interval < threshold:
            i += 1
            curr_interval += intervals[i]
        safe_interval.append(curr_interval)
        i += 1
    return safe_interval

def waving_1_song(wrist_flip: bool, file, default_curve: bool = False):
    intervals = get_bpm(file)
    safe_interval = safe_interval(interval, 2)
    for interval in safe_interval:
        waving_1(wrist_flip, interval, default_curve)


    # # LINEAR INTERPOLATION
    # num_points = int(time_interval / 0.002)
    # sub_num_points = int(num_points / 2)

    # sub_array = np.linspace(sub_start, sub_end, sub_num_points)
    # sub_array = np.concatenate((sub_array, sub_array[::-1]), axis=0)
    # sub_array = np.concatenate((sub_array, sub_array), axis=0)

    # final_array = np.linspace(all_start, all_end, num_points)
    # final_array = np.concatenate((final_array, final_array[::-1]), axis=0)

    # final_array[:, -2] = sub_array