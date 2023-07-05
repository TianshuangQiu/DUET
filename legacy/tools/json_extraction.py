import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

TIMESTEP = 0.001 # needs to evenly divide 0.04, should match input to t_toss when called
FRAMERATE = 25 # FPS in original video, should be 25
prev_hand_kp = [0, 0]
folder = "drive/IMG_4010"

def readfile(n):
    numstring = f"{n:012d}"
    strp_folder = folder.split("/")[-1]
    filename = folder + \
        f"/{strp_folder}_" + numstring + "_keypoints.json"
    item = pd.read_json(filename)
    return item

def extract_angles(shoulder, elbow, wrist, fingertip):
    """
    Given the positions of the shoulder, elbow, wrist, 
    and fingertip, extract the three desired angles.
    """
    xdiff1 = elbow[0] - shoulder[0]
    ydiff1 = elbow[1] - shoulder[1]
    theta1 = np.arctan2(ydiff1, xdiff1)
    
    xdiff2 = wrist[0] - elbow[0]
    ydiff2 = wrist[1] - elbow[1]
    theta2 = np.arctan2(ydiff2, xdiff2)
    
    xdiff3 = fingertip[0] - wrist[0]
    ydiff3 = fingertip[1] - wrist[1]
    theta3 = np.arctan2(ydiff3, xdiff3)

    return [theta1, theta2, theta3]

def get_hand_kpt(d):
    """
    Hand keypoint detection is extremely noisy, so we do 
    the best we can and allow for lots of smoothing later.
    """
    global prev_hand_kp
    
    keypoints = d['hand_right_keypoints_2d']
    for i in [12, 16, 8, 20]:
        p = keypoints[3 * i: 3 * i + 2]
        if p[0] != 0 and p[1] != 0:
            prev_hand_kp = p
            return p
    return prev_hand_kp

def linear_interp(array, num):
    interpolated = array[0]
    for i in range(len(array) - 1):
        interp = np.linspace(array[i], array[i + 1], num)
        interpolated = np.vstack([interpolated, interp])
        
    return interpolated[1:]

def fourier_filter(array, thresh):
    fourier = np.fft.rfft(array)
    fourier[np.abs(fourier) < thresh] = 0
    filtered = np.fft.irfft(fourier)
    return filtered

def num_deriv(array, t):
    stack = None
    for a in array.T:
        grad = np.gradient(a, t, axis=0)
        stack = (grad if stack is None else np.vstack([stack, grad]))
    return stack.T


theta_list = []

for n in range(1345):
    d = readfile(n)["people"][0]
    series = d['pose_keypoints_2d']
    pt0 = series[0:2]
    pt1 = series[3:5]
    pt2 = series[6:8]
    pt3 = series[9:11]
    pt4 = series[12:14]
    hand_pt = get_hand_kpt(d)

    thetas = extract_angles(pt2, pt3, pt4, hand_pt)
    theta_list.append(thetas)

tl = np.array(theta_list)
tl[tl < 0] = tl[tl < 0] + 2 * np.pi
kernel = np.array([1, 2, 4, 6, 10, 14, 17, 19, 17, 14, 10, 6, 4, 2, 1])
#kernel = np.ones(9)
kernel = kernel / np.sum(kernel)

smoothed_thetas = np.vstack([np.convolve(tl[:, 0], kernel, mode='same'), 
                             np.convolve(tl[:, 1], kernel, mode='same'), 
                             np.convolve(tl[:, 2], kernel, mode='same')])

data = smoothed_thetas[:, 150:560] - np.pi / 2
t = np.arange(len(data[0])) / FRAMERATE

sh = 0 - data[0]
el = data[0] - data[1]
wr = data[1] - data[2]

sh_filtered = fourier_filter(sh, 25)
el_filtered = fourier_filter(el, 15)
wr_filtered = fourier_filter(wr, 10)

plt.plot(sh, label="shoulder")
plt.plot(el, label="shoulder")
plt.plot(wr, label="shoulder")
plt.show()

position = np.vstack([np.zeros_like(t), 
                      # np.sin(np.arange(len(data[0])) * 2 * np.pi / len(data[0])) * 0.5,
                      sh_filtered, 
                      el_filtered, 
                      wr_filtered, 
                      np.ones_like(t) * np.pi / 2,
                      np.zeros_like(t)
                     ]).T

position = linear_interp(position, int(1 / FRAMERATE / TIMESTEP))
t_int = linear_interp(t[np.newaxis].T, int(1 / FRAMERATE / TIMESTEP))

velocity = num_deriv(position, TIMESTEP)
acceleration = num_deriv(velocity, TIMESTEP)
jerk = num_deriv(acceleration, TIMESTEP)

output = np.hstack([t_int, position, velocity, acceleration, jerk])
output = np.round_(output, decimals=5)
np.savetxt("sine_dance.dat", output, fmt="%10.5f", delimiter='\t')
