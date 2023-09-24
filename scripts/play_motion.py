import ur5py
import numpy as np
import pandas as pd
import time
from tqdm import tqdm
import cowsay
import pdb

robot = ur5py.UR5Robot("172.22.22.3")
# paths = [
#     "drive/yes.txt",
#     "drive/no.txt",
#     "drive/yes2.txt",
#     "drive/yes3.txt",
#     "drive/no2.txt",
#     "drive/pointing.txt",
#     "drive/stir.txt",
#     "drive/hammer.txt",
# ]
paths = ["drive/pointing.txt"]
pdb.set_trace()
plans = [np.loadtxt(p)[:, :-1] for p in paths]

for i, plan in enumerate(plans):
    if i == 0:
        robot.move_joint(plan[0], vel=0.5)
    for p in tqdm(plan):
        robot.servo_joint(p, time=0.05)
        time.sleep(0.05)
    # robot.stop_joint(0.1)
    # cowsay.cow("stopped")
    # time.sleep(0.5)
