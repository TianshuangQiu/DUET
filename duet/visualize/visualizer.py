import numpy as np
import pandas as pd
import cowsay
import math
from random import uniform, choice
import kinpy as kp
import plotly.graph_objects as go
import plotly.express as px
from matplotlib import pyplot as plt


class Motifs:
    def __init__(self) -> None:
        pass

    def filler(self, config_dict):
        param_0 = config_dict["param0"]
        param_1 = config_dict["param1"]

        return np.ones((20, 6)) * param_0 + param_1

    def circle_horizontal(self, config_dict):
        test = config_dict["param0"]
        temp = []
        final_array = []
        for x in np.arange(0, 12 * np.pi, np.pi / 40):
            temp.append(np.pi / 6 * math.cos(x) + np.pi)
            temp.append(np.pi / 10 * math.cos(x - np.pi / 2) - np.pi / 4)
            temp.append(np.pi / 4 * math.cos(x + np.pi / 2) + 7 * np.pi / 12)
            temp.append(np.pi / 12 * math.cos(x - np.pi / 2) + 1.15 * np.pi)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        return final_array

    def get_line(self, x1, y1, x2, y2):
        slope = (y2 - y1) / (x2 - x1)
        intercept = y2 - slope * x2
        return slope, intercept

    def painter_vertical(self, config_dict):
        test = config_dict["param0"]
        final_array = []
        temp = []
        vels = []
        acc = []
        blends = []
        for x in np.arange(0, 12 * np.pi, np.pi / 40):
            temp.append(np.pi)
            temp.append(np.pi / 8 * math.cos(x - np.pi) - np.pi / 6)
            temp.append(np.pi / 20 * math.cos(x))
            temp.append(np.pi / 10 * math.cos(x) + 8 * np.pi / 7)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        return final_array

    def cleaner_horizontal(self, config_dict):
        test = config_dict["param0"]
        temp = []
        final_array = []
        for x in np.arange(0, 20 * np.pi, np.pi / 8):
            temp.append(np.pi / 8 * math.cos(x) + np.pi)
            temp.append(np.pi / 14 * math.cos(2 * x) - 19 * np.pi / 60)
            temp.append(np.pi / 12 * math.cos(2 * x - np.pi) + np.pi / 3.5)
            temp.append(np.pi)
            temp.append(np.pi / 12 * math.cos(x + np.pi) + 3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        return final_array

    def circle_horizontal(self, config_dict):
        temp = []
        test = config_dict["param0"]
        final_array = []
        for x in np.arange(0, 12 * np.pi, np.pi / 40):
            temp.append(np.pi / 6 * math.cos(x) + np.pi)
            temp.append(np.pi / 10 * math.cos(x - np.pi / 2) - np.pi / 4)
            temp.append(np.pi / 4 * math.cos(x + np.pi / 2) + 7 * np.pi / 12)
            temp.append(np.pi / 12 * math.cos(x - np.pi / 2) + 1.15 * np.pi)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        return final_array

    def hammer_wall(self, config_dict):
        temp = []
        test = config_dict["param0"]
        final_array = []
        for x in np.arange(0, 8 * np.pi, np.pi / 8):
            temp.append(np.pi)
            temp.append(np.pi / 8)
            temp.append(np.pi / 6 * math.cos(x) - np.pi / 2)
            temp.append(5 * np.pi / 4)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        return final_array

    def screw_lightbulb(self, config_dict):
        offset = 0
        test = config_dict["param0"]
        temp = []
        final_array = []
        for x in np.arange(0, 16 * np.pi, np.pi / 8):
            temp.append(np.pi)
            temp.append(-np.pi / 8)
            temp.append(-np.pi / 2.7)
            temp.append(np.pi)
            temp.append(3 * np.pi / 2)
            temp.append(np.pi / 6 * math.cos(x - offset))
            # gripper.append(0.25*math.cos(x-offset))
            if x % np.pi == 0:
                offset += np.pi
            final_array.append(temp)
            temp = []
        return final_array

    def waving(self, config_dict):
        temp = []
        test = config_dict["param0"]
        final_array = []
        for x in np.arange(0, 8 * np.pi, np.pi / 40):
            temp.append(np.pi / 2)
            temp.append(np.pi / 8 * math.cos(x) - np.pi / 2)
            temp.append(np.pi / 6 * math.cos(x - 0.5))
            temp.append(np.pi / 4 * math.cos(x) - np.pi / 2 + 3 * np.pi / 2)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        return final_array

    def metronome(self, config_dict):
        test = config_dict["param0"]
        temp = []
        final_array = []
        for x in np.arange(0, 300 * np.pi, np.pi / 40):
            temp.append(np.pi / 2)
            temp.append(-np.pi / 2)
            temp.append(np.pi / 20 * math.cos(x) - np.pi / 3)
            temp.append(np.pi)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        return final_array

    def circle_vertical(self, config_dict):
        test = config_dict["param0"]
        final_array = []
        temp = []
        for x in np.arange(0, 8 * np.pi, np.pi / 40):
            temp.append(np.pi / 6 * math.cos(x) + np.pi)
            temp.append(np.pi / 6 * math.cos(x - np.pi / 2))
            temp.append(np.pi / 6 * math.cos(x) - np.pi / 6)
            temp.append(np.pi / 10 * math.cos(x + np.pi / 2) + 7 * np.pi / 6)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        return final_array

    def sweep_floor(self, config_dict):
        test = config_dict["param0"]
        final_array = []
        temp = []
        for x in np.arange(0, 16 * np.pi, np.pi / 40):
            temp.append(np.pi / 6 * math.cos(x) + np.pi)
            temp.append(np.pi / 14 * math.cos(x - np.pi / 2) - np.pi / 3)
            temp.append(np.pi / 14 * math.cos(x + np.pi / 2) + 7 * np.pi / 12)
            temp.append(7 * np.pi / 6)
            temp.append(np.pi / 7 * math.cos(x) + 4 * np.pi / 3)
            temp.append(0)
            final_array.append(temp)
            temp = []
        return final_array

    def yes(self, config_dict):
        amp = config_dict["amp"]
        final_array = []
        for x in np.arange(0, 9 * np.pi / 2, np.pi / 40):
            temp = [
                np.pi,
                -np.pi / 3,
                np.pi / 4,
                amp * math.cos(x) + 7 * np.pi / 6,
                3 * np.pi / 2,
                0,
            ]
            final_array.append(temp)
        return final_array

    def pointing(self, config_dict):  # 0.01
        test = config_dict["param0"]
        final_array = []
        temp = []
        for x in np.arange(0, 4 * np.pi, np.pi / 40):
            temp.append(np.pi)
            temp.append(np.pi / 48 * math.cos(x - np.pi) - np.pi / 3)
            temp.append(np.pi / 48 * math.cos(x) + np.pi / 4)
            temp.append(7 * np.pi / 6)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        return final_array

    def no(self, config_dict):
        amp = config_dict["amp"]
        final_array = []
        temp = []
        for x in np.arange(0, 9 * np.pi / 2, np.pi / 40):
            temp.append(np.pi)
            temp.append(-np.pi / 3)
            temp.append(np.pi / 4)
            temp.append(8 * np.pi / 7)
            temp.append(amp * math.cos(x) + 3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        return final_array

    # def random_yes_no(ur):
    #     funcs = [yes, no]
    #     amp = uniform(np.pi/12, np.pi/3)
    #     final_array = choice(funcs)(amp)
    #     final_array = np.array(final_array)
    #     #ur = UR5Robot(gripper=True)
    #     ur.move_joint(final_array[0], vel=0.5)
    #     # for i, arr in enumerate(final_array):
    #     #     ur.servo_joint(arr.tolist(), acc=0.2, vel=0, time=0.05, lookahead_time=0.2)
    #     #     time.sleep(0.05)
    #     ur.move_joint_path(
    #         final_array,
    #         vels=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    #         accs=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    #         blends=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05],
    #     )

    #     time.sleep(5)

    #     for i in range(50):
    #         amp = uniform(np.pi/12, np.pi/3.5)
    #         final_array = choice(funcs)(amp)
    #         final_array = np.array(final_array)
    #         for i, arr in enumerate(final_array):
    #             # t = 0.05
    #             # if i ==0:
    #             #     t = 0.5
    #             # ur.servo_joint(arr.tolist(), acc=0.2, vel=0, time=t, lookahead_time=0.2)
    #             ur.move_joint_path(
    #                 final_array,
    #                 vels=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    #                 accs=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    #                 blends=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05],
    #             )
    #             time.sleep(0.05)
    #         time.sleep(5)

    def horizontal_tag(self, config_dict):
        test = config_dict["param0"]
        final_array = []
        temp = []
        for x in np.arange(0, 9 * np.pi / 2, np.pi / 40):
            temp.append(np.pi / 4 * math.cos(x) + np.pi)
            temp.append(0)
            temp.append(0)
            temp.append(np.pi)
            temp.append(3 * np.pi / 2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        return final_array

    # def random_pointing(self, config_dict): #gripper CLOSED
    #     final_array = []
    #     temp = []

    #     #first pose
    #     prev_pan = pan_angle = uniform(3*np.pi/4, 5*np.pi/4)
    #     prev_lift = lift_angle = uniform(-np.pi/3,-np.pi/7)
    #     if lift_angle < -np.pi/4:
    #         prev_elbow = elbow_angle = uniform(np.pi/10, np.pi/3)
    #     else:
    #         prev_elbow = elbow_angle = uniform(-np.pi/4,np.pi/10)
    #     prev_w1 = wrist1_angle = uniform(-np.pi/4, np.pi/4)
    #     #go to first pose
    #     temp.append(pan_angle)
    #     temp.append(lift_angle)
    #     temp.append(elbow_angle)
    #     temp.append(wrist1_angle)
    #     temp.append(3*np.pi/2)
    #     temp.append(0)
    #     final_array.append(temp)
    #     temp = []
    #     #point
    #     if wrist1_angle > np.pi:
    #         lift_delta = 0.2
    #     else:
    #         lift_delta = -0.2
    #     for x in np.arange(0, 9 * np.pi/2, np.pi / 40):
    #         temp.append(pan_angle)
    #         if x > 2*np.pi:
    #             temp.append(lift_angle + lift_delta)
    #         else:
    #             temp.append(lift_angle)
    #         temp.append(elbow_angle)
    #         temp.append(wrist1_angle)
    #         temp.append(3*np.pi/2)
    #         temp.append(0)
    #         final_array.append(temp)
    #         temp = []

    #     for x in range(5):
    #         #new pos
    #         pan_angle = uniform(3*np.pi/4, 5*np.pi/4)
    #         lift_angle = uniform(-np.pi/3,-np.pi/4)
    #         if lift_angle < -np.pi/4:
    #             elbow_angle = uniform(np.pi/10, np.pi/3)
    #         else:
    #             elbow_angle = uniform(-np.pi/4,np.pi/10)
    #         wrist1_angle = uniform(-np.pi/4, np.pi/4)
    #         if wrist1_angle > np.pi:
    #             lift_delta = 0.2
    #         else:
    #             lift_delta = -0.2

    #         #transition
    #         pan_slope, pan_intercept = get_line(0,prev_pan, 2*np.pi, pan_angle)
    #         lift_slope, lift_intercept = get_line(0,prev_lift, 2*np.pi, lift_angle)
    #         elbow_slope, elbow_intercept = get_line(0,prev_elbow, 2*np.pi, elbow_angle)
    #         w1_slope, w1_intercept = get_line(0,prev_w1, 2*np.pi, wrist1_angle)
    #         for x in np.arange(0, 2*np.pi, np.pi/40):
    #             temp.append(pan_slope*x + pan_intercept)
    #             temp.append(lift_slope*x + lift_intercept)
    #             temp.append(elbow_slope*x + elbow_intercept)
    #             temp.append(w1_slope*x + w1_intercept)

    #         #point
    #         for x in np.arange(0, 9 * np.pi/2, np.pi / 40):
    #             temp.append(pan_angle)
    #             if x > 2*np.pi:
    #                 temp.append(lift_angle + lift_delta)
    #             else:
    #                 temp.append(lift_angle)
    #             temp.append(elbow_angle)
    #             temp.append(wrist1_angle)
    #             temp.append(3*np.pi/2)
    #             temp.append(0)
    #             final_array.append(temp)
    #             temp = []
    #     return final_array

    def handing_object(self, config_dict):
        test = config_dict["param0"]
        final_array = []
        temp = []
        # gripper = []
        # lift = []
        # elbow = []
        # wrist1 = []
        # wrist2 = []
        # wrist3 = []
        release = False
        for i in range(5):
            for x in np.arange(0, np.pi, np.pi/40):
                temp.append(np.pi)
                temp.append(np.pi/8*math.cos(x-np.pi) - np.pi/4)
                temp.append(np.pi/8*math.cos(x) +np.pi/4)
                temp.append(5*np.pi/4)
                temp.append(3*np.pi/2)
                temp.append(0)
                final_array.append(temp)
                temp = []
                # if release:
                #     gripper.append(0.5)
                # else:
                #     gripper.append(0)
            for x in np.arange(0, np.pi, np.pi/40):
                temp.append(np.pi)
                temp.append(np.pi/8-np.pi/4)
                temp.append(-np.pi/8+np.pi/4)
                temp.append(5*np.pi/4)
                temp.append(3*np.pi/2)
                temp.append(0)
                final_array.append(temp)
                temp = []
                # if release:
                #     gripper.append(0.25*math.cos(x) +0.25)
                # else:
                #     gripper.append(0.25*math.cos(x-np.pi) +0.25)
            for x in np.arange(np.pi, 2*np.pi, np.pi/40):
                temp.append(np.pi)
                temp.append(np.pi/8*math.cos(x-np.pi) - np.pi/4)
                temp.append(np.pi/8*math.cos(x) +np.pi/4)
                temp.append(5*np.pi/4)
                temp.append(3*np.pi/2)
                temp.append(0)
                final_array.append(temp)
                temp = []
                # if release:
                #     gripper.append(0)
                # else:
                #     gripper.append(0.5)
            # release = not release
        return final_array
    
def stop_each_joint(self, config_dict):
	# lift = []
	# elbow = []
	# wrist1 = []
	# wrist2 = []
    test = config_dict["param0"]
    temp = []
    final_array = []
    for x in np.arange(0,10*np.pi, np.pi/8):
        if x >=15*np.pi/2:
            temp.append(np.pi/2)
            temp.append(-np.pi/2)
            temp.append(0)
            temp.append(-np.pi/2)
            temp.append(3*np.pi/2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        elif x >=9*np.pi/2:
            temp.append(np.pi/2)
            temp.append(-np.pi/2)
            temp.append(0)
            temp.append(np.pi/4*math.cos(x) - np.pi/2)
            temp.append(3*np.pi/2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        elif x >= 5*np.pi/2:
            temp.append(np.pi/2)
            temp.append(-np.pi/2)
            temp.append(np.pi/4*math.cos(x - 0.5))
            temp.append(np.pi/4*math.cos(x) - np.pi/2)
            temp.append(3*np.pi/2)
            temp.append(0)
            final_array.append(temp)
            temp = []
        else:
            temp.append(np.pi/2)
            temp.append(np.pi/6*math.cos(x) - np.pi/2)
            temp.append(np.pi/4*math.cos(x- 0.5))
            temp.append(np.pi/4*math.cos(x) - np.pi/2)
            temp.append(3*np.pi/2)
            temp.append(0)
            final_array.append(temp)
            temp = []
    return final_array

def waltz(self, config_dict):
    test = config_dict["param0"]
    temp = []
    final_array = []
    for i in range(10):
        for x in np.arange(0,np.pi, np.pi/40):
            temp.append(np.pi/2)
            temp.append(np.pi/6*math.cos(x) - np.pi/2)
            temp.append(0)
            temp.append(3*np.pi/2)
            temp.append(0)
            temp.append(0)
            final_array.append(temp)
            temp = []
        for x in np.arange(0,np.pi, np.pi/40):
            temp.append(np.pi/2)
            temp.append(np.pi/12*math.cos(2*x-np.pi) - 7*np.pi/12)
            temp.append(0)
            temp.append(3*np.pi/2)
            temp.append(0)
            temp.append(0)
            final_array.append(temp)
            temp = []
        for x in np.arange(0,np.pi, np.pi/40):
            temp.append(np.pi/2)
            temp.append(np.pi/6*math.cos(x-np.pi) - np.pi/2)
            temp.append(0)
            temp.append(3*np.pi/2)
            temp.append(0)
            temp.append(0)
            final_array.append(temp)
            temp = []
        for x in np.arange(0,np.pi, np.pi/40):
            temp.append(np.pi/2)
            temp.append(np.pi/12*math.cos(2*x) - 5*np.pi/12)
            temp.append(0)
            temp.append(3*np.pi/2)
            temp.append(0)
            temp.append(0)
            final_array.append(temp)
            temp = []	
    return final_array

def one_joint_at_a_time(robot):
	pan = []
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	wrist3 = []
	prev_pan = np.pi
	prev_lift = -np.pi/3
	prev_elbow = np.pi/6
	prev_w1 = np.pi
	prev_w2 = 3*np.pi/2
	prev_w3 = 0
	prev = [prev_pan, prev_lift, prev_elbow, prev_w1, prev_w2, prev_w3]
	limbs = [pan, lift, elbow, wrist1, wrist2, wrist3]
	for j in range(20):
		index = np.random.randint(0,6)
		value = np.random.uniform(-np.pi/8,np.pi/8)
		i = 0
		while i < 6:
			if i == index:
				limbs[index].append(prev[index] + value)
			else:			
				limbs[i].append(prev[i])
			i+=1
		#time.sleep(2)


class Visualizer:
    def __init__(self, robot_file="ur5/ur5.urdf") -> None:
        self.robot = kp.build_chain_from_urdf(open(robot_file).read())

    def visualize(self, waypoints):
        df = pd.DataFrame(columns=["frame", "x", "y", "z"])
        for i, w in enumerate(waypoints):
            transform_dict = self.robot.forward_kinematics(w)
            for j, k in enumerate(transform_dict.keys()):
                if j == len(transform_dict) - 1:
                    continue
                df.loc[len(df)] = [i, *transform_dict[k].pos]
        # fig = px.line_3d(
        #     df,
        #     x="x",
        #     y="y",
        #     z="z",
        #     animation_frame="frame",
        #     range_x=[-1, 1],
        #     range_y=[-1, 1],
        #     range_z=[-0.5, 1],
        # )
        frames = [
            go.Frame(
                data=go.Scatter3d(
                    x=df[df["frame"] == k]["x"],
                    y=df[df["frame"] == k]["y"],
                    z=df[df["frame"] == k]["z"],
                    marker=dict(
                        size=4,
                    ),
                    line=dict(color="darkblue", width=5),
                ),
                layout=go.Layout(
                    yaxis=dict(range=[-1, 1]),
                ),
            )
            for k in df["frame"].unique()
        ]
        fig = go.Figure(
            data=[go.Scatter3d()],
            layout=go.Layout(  # Styling
                scene=dict(),
                updatemenus=[
                    dict(
                        type="buttons",
                        buttons=[dict(label="Play", method="animate", args=[None])],
                    )
                ],
                yaxis=dict(range=[-1, 1]),
            ),
            frames=frames,
        )
        # fig.layout.updatemenus[0].buttons[0].args[0]["frame"]["duration"] = 30
        # fig.layout.updatemenus[0].buttons[0].args[0]["transition"]["duration"] = 5
        return fig
