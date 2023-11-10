from duet.execute.motifs import *
import json
from copy import deepcopy
import numpy as np
from glob import glob
import datetime
import cowsay
import pdb

FILE_PATH = "save/AUTOSAVE.json"

with open("config/robot_ready.json", "r") as r:
    RBT_MOTIFS = json.load(r)
    for k in list(RBT_MOTIFS.keys()):
        if RBT_MOTIFS[k].get("time", -1) == "return_on_func":
            continue
        if RBT_MOTIFS[k].get("time", -1) < 0:
            RBT_MOTIFS.pop(k)
    MOTIF_FUNCS = {}
    for k in RBT_MOTIFS.keys():
        MOTIF_FUNCS[k] = locals()[k]
with open(FILE_PATH, "r") as r:
    config, ordering = json.load(r)
robot_ready_funcs = []

# PUT FUNCS IN LIST
for o in ordering:
    curr_config = config[o]
    kwargs = curr_config["params"]
    func_type = curr_config["type"]
    func = MOTIF_FUNCS[func_type]
    func_time_predict = RBT_MOTIFS[func_type].get("time", -1)
    # if func_type == "horizontal_tag":
    #     pdb.set_trace()
    if type(func_time_predict) in [float, int]:
        robot_ready_funcs.append(func(**kwargs))

    elif func_time_predict == "return_on_func":
        # Some motifs have variable lengths depending on the parameter
        rbt_func, runtime = func(**kwargs)
        robot_ready_funcs.append(rbt_func)
try:
    with open("save/exec_idx.txt", "r") as r:
        idx = int(r.readline())
except:
    idx = 0
pdb.set_trace()
robot = UR5Robot(gripper=2)
robot.set_playload(1.5)
for i, h in enumerate(robot_ready_funcs):
    if i < idx:
        continue
    if i < len(robot_ready_funcs)-1:
        next_motif = ordering[i + 1]
    else:
        next_motif = "None"
    print(f"Currently playing {ordering[i]}, next one is {next_motif}")
    with open("save/exec_idx.txt", "w") as w:
        w.write(str(i))
    h(robot)
