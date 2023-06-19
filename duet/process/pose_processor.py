import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt
from tqdm import tqdm
from duet.const import const
import glob


class PoseProcessor:

    def __init__(self, raw_json_folder: str) -> None:
        self.prev_hand_kp = {'left': [0, 0], 'right': [0, 0]}
        self.prev_thumb_kp = [0, 0]
        self.folder = raw_json_folder
        self.frame_count = len(glob.glob(raw_json_folder+"/*.json"))
        self.theta_list = []

    def process_angle(self):
        for n in range(0, self.frame_count):
            d = self._readfile(n)["people"][0]
            series = d['pose_keypoints_2d']
            frame_angles = []

            def get_point(value):
                if type(value) == int:
                    return series[value*3], series[value*3+1]
                else:
                    name = value.split("_")
                    return self.get_hand_kpt(d, name[0]) if name[1] == 'hand' else self.get_thumb_kpt(d, name[0])

            for combo in const.POINT_COMBO:
                frame_angles.append(
                    self.get_angle(get_point(combo[0]), get_point(combo[1])))

            # hand_pt = get_hand_kpt(d)
            # thumb_pt = get_thumb_kpt(d)

            # thetas = extract_angles(pt2, pt3, pt4, hand_pt, thumb_pt)
            thetas = frame_angles
            self.theta_list.append(frame_angles)
        self.theta_list = np.array(self.theta_list)

    def construct(self):
        tl = self.theta_list
        tl[tl < 0] = tl[tl < 0] + 2 * np.pi
        tl[tl < 0] = tl[tl < 0] + 2 * np.pi
        kernel = np.array([1, 2, 4, 6, 10, 14, 17, 19, 17, 14, 10, 6, 4, 2, 1])
        kernel = kernel / np.sum(kernel)

        if len(tl) % 2 != 0:
            tl = tl[:-1]

        for i in range(len(tl) - 1):
            for j in range(len(tl[i])):
                if np.abs(tl[i, j] - tl[i + 1, j]) > np.abs(tl[i, j] - tl[i + 1, j] - 2 * np.pi):
                    tl[i + 1, j] += 2 * np.pi
                if np.abs(tl[i, j] - tl[i + 1, j]) > np.abs(tl[i, j] - tl[i + 1, j] + 2 * np.pi):
                    tl[i + 1, j] -= 2 * np.pi

        smoothed_thetas = []
        for i in range(len(tl[0])):
            smoothed_thetas.append(np.convolve(tl[:, i], kernel, mode='same'))

        smoothed_thetas = np.vstack(smoothed_thetas)
        print(smoothed_thetas.shape)
        data = smoothed_thetas[:]

        t = np.arange(len(data[0])) / const.FRAMERATE

    def _read_files(self, n: int):

        numstring = f"{n:04d}"
        strp_folder = self.folder.split("/")[-1]
        filename = self.folder + \
            f"/{strp_folder}_" + numstring + "_keypoints.json"
        item = pd.read_json(filename)
        return item

    def _get_angle(self, first, second):
        xdiff1 = first[0] - second[0]
        ydiff1 = first[1] - second[1]
        return np.arctan2(ydiff1, xdiff1)

    def extract_angles(self, shoulder, elbow, wrist, fingertip, thumbtip):
        """
        Given the positions of the shoulder, elbow, wrist, 
        and fingertip, extract the three desired angles.
        """

        theta1 = self._get_angle(elbow, shoulder)
        theta2 = self._get_angle(wrist, elbow)
        theta3 = self._get_angle(fingertip, wrist)
        theta4 = self._get_angle(thumbtip, wrist)

        return [theta1, theta2, theta3, theta4]

    def get_hand_kpt(self, d, side='right'):
        """
        Hand keypoint detection is extremely noisy, so we do 
        the best we can and allow for lots of smoothing later.
        """
        keypoints = d[f'hand_{side}_keypoints_2d']
        for i in [12, 16, 8, 20, 11, 15, 7, 19]:
            p = keypoints[3 * i: 3 * i + 2]
            if p[0] != 0 and p[1] != 0:
                self.prev_hand_kp[side] = p
                return p
        return self.prev_hand_kp[side]

    def get_thumb_kpt(self, d, side='right'):
        """
        Get the thumb detection in order to find the rotation angle of the wrist.
        """
        thumb = None

        keypoints = d[f'hand_{side}_keypoints_2d']
        for i in [4, 3, 2, 1]:
            p = keypoints[3 * i: 3 * i + 2]
            if p[0] != 0 and p[1] != 0:
                thumb = p
                break
        if thumb == None:
            return self.prev_thumb_kp
        else:
            return thumb

    def linear_interp(self, array, num):
        interpolated = array[0]
        for i in range(len(array) - 1):
            interp = np.linspace(array[i], array[i + 1], num, endpoint=False)
            interpolated = np.vstack([interpolated, interp])

        return interpolated[1:]

    def fourier_filter(self, array, thresh):
        fourier = np.fft.rfft(array)
        fourier[np.abs(fourier) < thresh] = 0
        filtered = np.fft.irfft(fourier)
        return filtered

    def num_deriv(self, array, t):
        stack = None
        for a in array.T:
            grad = np.gradient(a, t, axis=0)
            stack = (grad if stack is None else np.vstack([stack, grad]))
        return stack.T

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))
