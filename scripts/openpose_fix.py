import numpy as np
import glob
import pdb

# import
file_list = glob.glob("drive/*.txt")
fl = []
for f in file_list:
    fl.append(f[6:])
fl.sort()
print(fl)
# print(file_list)
# for f in file_list:
#     if "requirement" in f:
#         continue
#     x = np.loadtxt(f)
#     t = list(range(0, x.shape[0]))
#     x = np.hstack([np.array(t).reshape(-1, 1) * 0.002, x])
# np.savetxt("drive/" + f.split("/")[-1], x)
