from duet.execute.g_motifs import *
import json
from copy import deepcopy
import numpy as np
from glob import glob
import datetime
import cowsay
import pandas as pd
import pdb

material_path = "save/Breathless Motif Sequences DUET - Material.csv"
material_df = pd.read_csv(material_path)

sequence_path = "save/Breathless Motif Sequences DUET - Sequence-Evening.csv"
sequence_df = pd.read_csv(sequence_path)

with open("config/robot_ready.json", "r") as r:
    RBT_MOTIFS = json.load(r)
    MOTIF_FUNCS = {}
    for k in RBT_MOTIFS.keys():
        MOTIF_FUNCS[k] = locals()[k]

robot_ready_funcs = {}

# PUT FUNCS IN DICT
for index, row in material_df.iterrows():
    args_str = row["Args"]
    kwargs = {}
    # pdb.set_trace()
    if args_str != "None":
        for args in args_str.split(","):
            k, a = args.split(":")
            kwargs[k] = a
    robot_ready_funcs[row["Name"]] = MOTIF_FUNCS[row["Motif"]](**kwargs)

try:
    with open("save/exec_idx.txt", "r") as r:
        idx = int(r.readline())
except:
    idx = 0

robot = UR5Robot(gripper=2)
robot.set_playload(1)
pdb.set_trace()
sequence_df = sequence_df[idx:]
# PUT FUNCS IN DICT
for index, row in sequence_df.iterrows():
    # pdb.set_trace()
    material_name = row["Material"]
    duration = float(row["Duration"])
    if duration < 0:
        duration = float("inf")
    if index - idx + 1 < len(sequence_df):
        next_material = sequence_df.iloc[index - idx + 1]
    else:
        next_material = "END"
    print(
        f"\n\n\n Currently playing: \n{row}, \n\n the next one is \n{next_material} \n"
    )
    with open("save/exec_idx.txt", "w") as w:
        w.write(str(index))
    robot_ready_funcs[material_name](robot, duration)
