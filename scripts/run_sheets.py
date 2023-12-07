from duet.execute.g_motifs import *
import json
from copy import deepcopy
import numpy as np
from glob import glob
import datetime
import cowsay
import pandas as pd
import pdb

material_path = "/home/breath/DUET/save/Breathless Motif Sequences DUET - Material.csv"
material_df = pd.read_csv(material_path)

sequence_path = "/home/breath/DUET/save/Breathless Motif Sequences DUET - Sequence-Evening - NEW.csv"
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

robot = UR5Robot(ip="192.168.131.69", gripper=2)
robot.set_playload(1)
print("Enter to start")
input()
# PUT FUNCS IN DICT

index = idx
while index < len(sequence_df):
    row = sequence_df.iloc[index]
    material_name = row["Material"]
    duration = float(row["Duration"])
    if duration < 0:
        duration = float("inf")
    if index + 1 < len(sequence_df):
        next_material = sequence_df.iloc[index + 1]
    else:
        next_material = "END"
    print(
        f"\n\n\n Currently playing: \n{row}, \n\n the next one is \n{next_material} \n"
    )
    with open("save/exec_idx.txt", "w") as w:
        w.write(str(index))
    try:
        robot_ready_funcs[material_name](robot, duration)
        index += 1
    except:
        print("Enter manual command")
        robot.stop_joint()
        debug_msg = input()
        if debug_msg == "q":
            raise
        elif debug_msg == "c":
            pass
        elif debug_msg[0] == "+":
            index += int(debug_msg[1:])
        elif debug_msg[0] == "-":
            index -= int(debug_msg[1:])
        else:
            print("Assuming that you have entered an integer")
            index = int(debug_msg)
