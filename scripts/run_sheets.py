#from duet.execute.g_motifs import *
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

#################### for recovery, if robot stops start at new index
try:
    with open("save/start_time.txt", "r") as start_time_file:
        start_time = datetime.datetime.fromisoformat(start_time_file.readline().strip())
except:
    start_time = datetime.datetime.now()
    with open("save/start_time.txt", "w") as st_file:
        st_file.write(start_time.isoformat())

def calculate_current_position(sequence_df, elapsed_time):
    cumulative_time = 0
    for index, row in sequence_df.iterrows():
        cumulative_time = cumulative_time + float(row["Duration"])
        if cumulative_time > elapsed_time:
            remaining_time = cumulative_time - elapsed_time
            return index, remaining_time
    return len(sequence_df), 0  

curr_time = datetime.datetime.now()
elapsed_time = (curr_time - start_time).total_seconds()
new_idx, remaining_duration = calculate_current_position(sequence_df, elapsed_time)

if new_idx != idx:
    idx = new_idx
    sequence_df = sequence_df[idx:]

#################### Recovery-end

# PUT FUNCS IN DICT
for index, row in sequence_df.iterrows():
    # pdb.set_trace()
    material_name = row["Material"]
    if index == idx:
        duration = remaining_duration #recovery
    else:
        duration = remaining_duration

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


