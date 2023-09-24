import ur5py
import numpy as np
import pandas as pd
import time
from tqdm import tqdm
import pdb

robot = ur5py.UR5Robot("172.22.22.3")
path = "drive/IMG_4013.dat"
plan = np.loadtxt(path)[::2, 1:7]

pdb.set_trace()

robot.move_joint(plan[0], vel=0.5)
for p in tqdm(plan):
    robot.servo_joint(p, time=0.01)
    time.sleep(0.01)
