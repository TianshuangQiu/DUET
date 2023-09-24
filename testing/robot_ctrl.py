import ur5py
import numpy as np
import pandas as pd
import time
from tqdm import tqdm
import pdb

robot = ur5py.UR5Robot("172.22.22.3")
path = "drive/IMG_4012.dat"
plan = np.loadtxt(path)[::2, 1:7]
# plan[:, 1] *= -1
# pdb.set_trace()

robot.move_joint(plan[0], vel=1)
for p in tqdm(plan):
    robot.servo_joint(p, time=0.002)
    time.sleep(0.002)
