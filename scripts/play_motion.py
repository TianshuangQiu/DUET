from duet.execute.motifs import *
from ur5py import UR5Robot

robot = UR5Robot(gripper=True)
yes(True, 0.5, False, 1)
run_recording("IMG_4010.txt", True)[0](robot)  # run python3 scripts/play_motion.py
# run_recording("jump4_120.txt", False)[0](robot)  # run python3 scripts/play_motion.py
