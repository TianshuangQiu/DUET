from duet.execute.motifs import *
from ur5py import UR5Robot

robot = UR5Robot()
run_recording("jump4_120.txt", False)[0](robot) #run python3 scripts/play_motion.py
