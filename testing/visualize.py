from urdfpy import URDF
import numpy as np
import math

#robot = URDF.load('/home/shreyaganti/urdfpy/tests/data/ur5/ur5.urdf')
# for link in robot.links:
#     print(link.name)
#for joint in robot.joints:
#    print('{} connects {} to {}'.format(joint.name, joint.parent, joint.child))

#painting (vertical line)
def painter_vertical(robot):
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	for x in np.arange(0,8*np.pi, np.pi/8):
		lift.append(np.pi/4*math.cos(x-np.pi))
		elbow.append(np.pi/6*math.cos(x))
		wrist1.append(np.pi/10*math.cos(x) + np.pi)
		wrist2.append(3*np.pi/2)
	robot.animate(cfg_trajectory={
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_2_joint' : wrist2,
		'wrist_1_joint' : wrist1}, loop_time=7)


def painter_dip_brush(robot):
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	for x in np.arange(0,8*np.pi, np.pi/8):
		lift.append(np.pi/24*math.cos(x) - np.pi/2.25)
		elbow.append(17*np.pi/24)
		wrist1.append(5*np.pi/4)
		wrist2.append(3*np.pi/2)
	robot.animate(cfg_trajectory={
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_2_joint' : wrist2,
		'wrist_1_joint' : wrist1}, loop_time=7)

#painting and dipping brush(vertical line)
def painter_vertical_dip(robot):
	pan = []
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	for x in np.arange(0,15*np.pi/2, np.pi/8):
		pan.append(np.pi/4*math.cos(x/5 - np.pi/2))
		lift.append(np.pi/4*math.cos(x-np.pi))
		elbow.append(np.pi/6*math.cos(x))
		wrist1.append(np.pi/10*math.cos(x) + np.pi)
		wrist2.append(np.pi/8*math.cos(x/5 - 3*np.pi/2) - np.pi/2)
	for x in np.arange(15*np.pi/2,17*np.pi/2, np.pi/8):
		pan.append(-np.pi/4)
		lift.append(-4*x/9 + 10*np.pi/3)
		elbow.append(17*x/24 - 255*np.pi/48)
		wrist1.append(x/4 -7*np.pi/8)
		wrist2.append(3*np.pi/2)
	for x in np.arange(17*np.pi/2,10*np.pi, np.pi/8):
		pan.append(-np.pi/4)
		lift.append(np.pi/24*math.cos(2*x) - np.pi/2.25)
		elbow.append(17*np.pi/24)
		wrist1.append(5*np.pi/4)
		wrist2.append(3*np.pi/2)
	robot.animate(cfg_trajectory={
		'shoulder_pan_joint' : pan,
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_2_joint' : wrist2,
		'wrist_1_joint' : wrist1}, loop_time=9)
	

#newspaper delivery (throwing)
def newspaper_delivery(robot):
	pan = []
	lift = []
	elbow = []
	wrist3 = []
	wrist2 = []
	for x in np.arange(0,8*np.pi, np.pi/8):
		pan.append(np.pi/4*math.cos(x-np.pi) + np.pi/4)
		lift.append(np.pi/24*math.cos(x) - 7*np.pi/24)
		elbow.append(np.pi/6*math.cos(x) + 5*np.pi/12)
		wrist3.append(np.pi/9*math.cos(x) + np.pi)
		wrist2.append(np.pi/4*math.cos(x) + 3*np.pi/4)

	robot.animate(cfg_trajectory={
		'shoulder_pan_joint' : pan,
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_2_joint' : wrist2,
		'wrist_3_joint' : wrist3}, loop_time=6)


#cleaner (vacuuming)
def cleaner_vacuum(robot):
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	for x in np.arange(0,8*np.pi, np.pi/8):
		lift.append(np.pi/12*math.cos(x) + np.pi/4)
		elbow.append(5*np.pi/24*math.cos(x-np.pi) - 13*np.pi/24)
		wrist1.append(np.pi/20*math.cos(x-np.pi) - 11*np.pi/20)
		wrist2.append(3*np.pi/2)
	robot.animate(cfg_trajectory={
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_2_joint' : wrist2,
		'wrist_1_joint' : wrist1}, loop_time=7)

#cleaner (vacuuming and panning)
def cleaner_vacuum_panning(robot):
	pan = []
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	for x in np.arange(0,8*np.pi, np.pi/8):
		pan.append(np.pi/4*math.cos(x/12))
		lift.append(np.pi/12*math.cos(x) + np.pi/4)
		elbow.append(5*np.pi/24*math.cos(x-np.pi) - 13*np.pi/24)
		wrist1.append(np.pi/20*math.cos(x-np.pi) - 11*np.pi/20)
		wrist2.append(3*np.pi/2)
	robot.animate(cfg_trajectory={
		'shoulder_pan_joint' : pan,
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_2_joint' : wrist2,
		'wrist_1_joint' : wrist1}, loop_time=7)


#cleaner (wiping horizontally)
def cleaner_horizontal(robot):
	pan = []
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	for x in np.arange(0,8*np.pi, np.pi/8):
		pan.append(np.pi/4*math.cos(x))
		lift.append(np.pi/60*math.cos(x-np.pi) + 11*np.pi/60)
		elbow.append(np.pi/12*math.cos(2*x) - 11*np.pi/30)
		wrist1.append(-5*np.pi/6)
		wrist2.append(np.pi/6*math.cos(x + np.pi) - np.pi/2)

	robot.animate(cfg_trajectory={
		'shoulder_pan_joint' : pan,
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_2_joint' : wrist2,
		'wrist_1_joint' : wrist1}, loop_time=7)


#cleaner (horizontally down a wall)
def cleaner_horizontal_wall(robot):
	pan = []
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	lift_count = 0
	lift_const = 0
	lift_grace_prd = False
	lift_grace_const = 0
	wrist1_num = 3.2
	wrist1_den = 2.2
	for x in np.arange(0,16*np.pi, np.pi/8):
		pan.append(np.pi/4*math.cos(x))
		elbow.append(np.pi/12*math.cos(2*x) - 11*np.pi/30)
		wrist2.append(np.pi/6*math.cos(x-np.pi) - np.pi/2)
		if lift_count == 12:
			lift_count = 0
			lift_grace_const = np.pi/60*math.cos(2*x-np.pi) + lift_const
			lift_const += np.pi/30
			wrist1_num += 0.75
			wrist1_den += 0.75
			lift_grace_prd = True
		if lift_grace_prd and x%np.pi!=0:
			lift.append(lift_grace_const)
		else:
			lift_grace_prd = False
			lift.append(np.pi/60*math.cos(2*x-np.pi) + lift_const)
			lift_count += 1
		wrist1.append(wrist1_num*np.pi/wrist1_den)	

	robot.animate(cfg_trajectory={
		'shoulder_pan_joint' : pan,
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_2_joint' : wrist2,
		'wrist_1_joint' : wrist1}, loop_time=10)

	
#farmer raking
def farmer_raking(robot):
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	for x in np.arange(0,8*np.pi, np.pi/8):
		lift.append(np.pi/5*math.cos(x) - np.pi/6)
		elbow.append(np.pi/3*math.cos(x- 3*np.pi/4) +np.pi/3)
		wrist2.append(3*np.pi/2)
		wrist1.append(7*np.pi/6)
	robot.animate(cfg_trajectory={
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_2_joint' : wrist2,
		'wrist_1_joint' : wrist1}, loop_time=7)

#farmer raking (panning and random)
def farmer_raking_panning(robot):
	pan = []
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	for x in np.arange(0,8*np.pi, np.pi/8):
		pan.append(np.pi/6*math.cos(1/(4*np.pi)*x))
		wrist2.append(3*np.pi/2)
		wrist1.append(7*np.pi/6)
	decay = 0.07
	for x in np.arange(0,4*np.pi, np.pi/8):
		lift.append(np.pi/12*math.e**(-decay*(x-4*np.pi))*math.cos(2*x) - np.pi/6)
		elbow.append(np.pi/8*math.e**(-decay*(x-4*np.pi))*math.cos(2*x - 3*np.pi/4) +np.pi/3)
	for x in np.arange(4*np.pi,8*np.pi, np.pi/8):
			lift.append(np.pi/12*math.e**(decay*(x-4*np.pi))*math.cos(2*x) - np.pi/6)
			elbow.append(np.pi/8*math.e**(decay*(x-4*np.pi))*math.cos(2*x - 3*np.pi/4) +np.pi/3)
	robot.animate(cfg_trajectory={
		'shoulder_pan_joint' : pan,
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_2_joint' : wrist2,
		'wrist_1_joint' : wrist1}, loop_time=9)
		

#sweeping the floor
def sweep_floor(robot):
	pan = []
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	for x in np.arange(0,8*np.pi, np.pi/8):
		pan.append(np.pi/6*math.cos(x))
		lift.append(np.pi/14*math.cos(x+np.pi/2) - np.pi/4)
		elbow.append(np.pi/14*math.cos(x-np.pi/2) + 7*np.pi/12)
		wrist1.append(np.pi)
		wrist2.append(np.pi/6*math.cos(x) + 4*np.pi/3)
	robot.animate(cfg_trajectory={
		'shoulder_pan_joint' : pan,
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_2_joint' : wrist2,
		'wrist_1_joint' : wrist1}, loop_time=5)
		
#circular wiping motion on horizontal surface
def circle_horizontal(robot):
	pan = []
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	for x in np.arange(0,8*np.pi, np.pi/8):
		pan.append(np.pi/6*math.cos(x))
		lift.append(np.pi/10*math.cos(x-np.pi/2) - np.pi/4)
		elbow.append(np.pi/4*math.cos(x+np.pi/2) + 7*np.pi/12)
		wrist1.append(np.pi/12*math.cos(x-np.pi/2) + 1.15*np.pi)
		wrist2.append(3*np.pi/2)
	robot.animate(cfg_trajectory={
		'shoulder_pan_joint' : pan,
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_2_joint' : wrist2,
		'wrist_1_joint' : wrist1}, loop_time=7)

#circular wiping motion on vertical surface
def circle_vertical(robot):
	pan = []
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	for x in np.arange(0,8*np.pi, np.pi/8):
		pan.append(np.pi/6*math.cos(x))
		lift.append(np.pi/6*math.cos(x-np.pi/2))
		elbow.append(np.pi/6*math.cos(x) - np.pi/6)
		wrist1.append(np.pi/10*math.cos(x + np.pi/2) + 7*np.pi/6)
		wrist2.append(3*np.pi/2)
	robot.animate(cfg_trajectory={
		'shoulder_pan_joint': pan,
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_2_joint' : wrist2,
		'wrist_1_joint' : wrist1}, loop_time=7)

#shoveling/digging action
def shoveling(robot):
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	for x in np.arange(0,8*np.pi, np.pi/8):
		lift.append(np.pi/5*math.cos(x-np.pi) - np.pi/6)
		elbow.append(np.pi/2*math.cos(x- np.pi/4) +np.pi/4)
		wrist2.append(3*np.pi/2)
		wrist1.append(np.pi/4*math.cos(x) + np.pi)
	robot.animate(cfg_trajectory={
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_2_joint' : wrist2,
		'wrist_1_joint' : wrist1}, loop_time=7)

#cook flipping an omelete
def flipping_pan(robot):
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	for x in np.arange(0,8*np.pi, np.pi/8):
		lift.append(np.pi/15*math.cos(x-np.pi) + np.pi/6)
		elbow.append(np.pi/10*math.cos(x+ np.pi/4) -np.pi/4)
		wrist2.append(3*np.pi/2)
		wrist1.append(np.pi/20*math.cos(x) + 9*np.pi/8)
	robot.animate(cfg_trajectory={
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_2_joint' : wrist2,
		'wrist_1_joint' : wrist1}, loop_time=4)

def spiral_horizontal_circle(robot):
	pan = []
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	for x in np.arange(0,8*np.pi, np.pi/8):
		pan.append(np.pi/6*math.e**(-0.05*x)*math.cos(2*x) - np.pi/8)
		lift.append(np.pi/10*math.e**(-0.05*x)*math.cos(2*x - np.pi/2) - np.pi/4)
		elbow.append(np.pi/6*math.e**(-0.05*x)*math.cos(2*x + np.pi/2) + 7*np.pi/12)
		wrist1.append(np.pi/12*math.cos(2*x-np.pi/2) + 1.15*np.pi)
		wrist2.append(3*np.pi/2)
	robot.animate(cfg_trajectory={
		'shoulder_pan_joint' : pan,
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_2_joint' : wrist2,
		'wrist_1_joint' : wrist1}, loop_time=7)

def brick_layer(robot): 	#rename to stacking_cans??
	pan = []
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	temp_x = 0
	lift_count = 0
	lift_grace_prd = False
	lift_const = -np.pi/3
	lift_shift = 0
	pan_shift = 0
	pan_grace_shift = -7*np.pi
	elbow_denom = 8
	elbow_const_num = 16
	for x in np.arange(0,96*np.pi, np.pi/8):
		wrist2.append(3*np.pi/2)
		
		if lift_count == 96: #when x reaches every other interval of 12pi
			temp_x = x
			lift_shift+= 14*np.pi
			pan_shift += 7*np.pi/6
			pan_grace_shift += 7*np.pi
			lift_count = 0
			lift_grace_prd = True
			y1 = np.pi/8*math.e**(-0.07*x)*math.cos(2*x) + lift_const
			y2 = y1 - np.pi/18
			lift_const -= np.pi/18
			lift_slope, lift_intercept = get_line(x, y1, x+2*np.pi, y2)
			y1 = np.pi/elbow_denom*math.cos(x) + elbow_const_num*np.pi/24
			elbow_denom -= 0.5
			elbow_const_num += 0
			y2 = np.pi/elbow_denom*math.cos(x) + elbow_const_num*np.pi/24
			elbow_slope, elbow_intercept = get_line(x, y1, x+2*np.pi,y2)
		if lift_grace_prd and abs(x-temp_x - 2*np.pi)>0.01:
			lift.append(lift_slope*x + lift_intercept)
			elbow.append(elbow_slope*x + elbow_intercept)
			wrist1.append(3.185)
			pan.append(np.pi/4*math.cos(x/2-np.pi - pan_grace_shift))
		else:
			lift_grace_prd = False
			pan.append(np.pi/4*math.cos(x/12 - pan_shift))
			elbow.append(np.pi/elbow_denom*math.cos(x) + elbow_const_num*np.pi/24)
			wrist1.append(np.pi/9*math.cos(x - np.pi) + 9*np.pi/8)
			if x % (14*np.pi) > 6*np.pi:
				lift.append(np.pi/8*math.e**(0.07*(x-lift_shift-12*np.pi))*math.cos(2*x-lift_shift - 12*np.pi) + lift_const)
			else:
				lift.append(np.pi/8*math.e**(-0.07*(x-lift_shift))*math.cos(2*x-lift_shift) + lift_const)
			lift_count += 1
			
	robot.animate(cfg_trajectory={
		'shoulder_pan_joint' : pan,
		'elbow_joint' : elbow,
		'shoulder_lift_joint' : lift,
		'wrist_1_joint' : wrist1,
		'wrist_2_joint' : wrist2}, loop_time=60)

def waving(robot):
	lift = []
	elbow = []
	wrist1 = []
	for x in np.arange(0,8*np.pi, np.pi/8):
		lift.append(np.pi/6*math.cos(x) - np.pi/2)
		elbow.append(np.pi/4*math.cos(x- 0.5))
		wrist1.append(np.pi/4*math.cos(x) - np.pi/2)
	robot.animate(cfg_trajectory={
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_1_joint' : wrist1}, loop_time=10)

def painter_ceiling(robot):
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	for x in np.arange(0,8*np.pi, np.pi/8):
		lift.append(np.pi/6*math.cos(x) - np.pi/2)
		elbow.append(np.pi/4*math.cos(x- 0.25))
		wrist1.append(np.pi/3*math.cos(x-np.pi) + np.pi)
		wrist2.append(3*np.pi/2)
	robot.animate(cfg_trajectory={
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_1_joint' : wrist1,
		'wrist_2_joint' : wrist2}, loop_time=10)

def get_line(x1,y1,x2,y2):
	slope = (y2-y1)/(x2-x1)
	intercept = y2 - slope*x2
	return slope, intercept

def bartender_shaking(robot):
	pan = []
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	for x in np.arange(0,8*np.pi, np.pi/8):
		lift.append(np.pi/48*math.cos(x)+np.pi/4)
		elbow.append(np.pi/24*math.cos(x) - 2*np.pi/3)
		wrist1.append(np.pi/8*math.cos(x) + 7*np.pi/6)
		wrist2.append(np.pi/8*math.cos(2*x) + 3*np.pi/2)
		pan.append(0)
	
	y1 = np.pi/48*math.cos(8*np.pi)+np.pi/4
	y2 = np.pi/48*math.cos(12*np.pi)-np.pi/3
	lift_slope, lift_intercept = get_line(8*np.pi, y1, 12*np.pi, y2)
	y1 = np.pi/24*math.cos(x) - 2*np.pi/3
	y2 = np.pi/24*math.cos(12*np.pi) + np.pi/6
	elbow_slope, elbow_intercept = get_line(8*np.pi, y1, 12*np.pi, y2)
	
	for x in np.arange(8*np.pi, 12*np.pi, np.pi/8):
		lift.append(lift_slope*x + lift_intercept)
		elbow.append(elbow_slope*x + elbow_intercept)
		wrist1.append(31*np.pi/24)
		wrist2.append(13*np.pi/8)
		pan.append(np.pi/12*math.cos(x-np.pi))
		
	for x in np.arange(12*np.pi, 20*np.pi, np.pi/8):
		lift.append(np.pi/48*math.cos(x)-np.pi/3)
		elbow.append(np.pi/24*math.cos(x) + np.pi/6)
		wrist1.append(np.pi/8*math.cos(x) + 7*np.pi/6)
		wrist2.append(np.pi/8*math.cos(2*x) + 3*np.pi/2)
		pan.append(0)
	
	robot.animate(cfg_trajectory={
		'shoulder_pan_joint' : pan,
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_1_joint' : wrist1,
		'wrist_2_joint' : wrist2}, loop_time=6)

def bartender_pouring(robot):
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	for x in np.arange(0,8*np.pi, np.pi/8):
		lift.append(np.pi/14*math.cos(x) - np.pi/2.5)
		elbow.append(np.pi/4*math.e**(-0.2*x)*math.cos(x) + np.pi/2.5)
		wrist1.append(7*np.pi/6)
		wrist2.append(3*np.pi/2)
	robot.animate(cfg_trajectory={
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_1_joint' : wrist1,
		'wrist_2_joint' : wrist2}, loop_time=6)


def bartender_shake_pour(robot):
	pan = []
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	
	for x in np.arange(0,8*np.pi, np.pi/8):
		lift.append(np.pi/48*math.cos(x)+np.pi/4)
		elbow.append(np.pi/24*math.cos(x) - 2*np.pi/3)
		wrist1.append(np.pi/8*math.cos(x) + 7*np.pi/6)
		wrist2.append(np.pi/8*math.cos(2*x) + 3*np.pi/2)
		pan.append(0)
	
	y1 = np.pi/48*math.cos(8*np.pi)+np.pi/4
	y2 = np.pi/48*math.cos(12*np.pi)-np.pi/3
	lift_slope, lift_intercept = get_line(8*np.pi, y1, 12*np.pi, y2)
	y1 = np.pi/24*math.cos(x) - 2*np.pi/3
	y2 = np.pi/24*math.cos(12*np.pi) + np.pi/6
	elbow_slope, elbow_intercept = get_line(8*np.pi, y1, 12*np.pi, y2)
	
	for x in np.arange(8*np.pi, 12*np.pi, np.pi/8):
		lift.append(lift_slope*x + lift_intercept)
		elbow.append(elbow_slope*x + elbow_intercept)
		wrist1.append(31*np.pi/24)
		wrist2.append(13*np.pi/8)
		pan.append(np.pi/12*math.cos(x-np.pi))
		
	for x in np.arange(12*np.pi, 20*np.pi, np.pi/8):
		lift.append(np.pi/48*math.cos(x)-np.pi/3)
		elbow.append(np.pi/24*math.cos(x) + np.pi/6)
		wrist1.append(np.pi/8*math.cos(x) + 7*np.pi/6)
		wrist2.append(np.pi/8*math.cos(2*x) + 3*np.pi/2)
		pan.append(0)
	
	#TRANSITION
	y2 = np.pi/4 + np.pi/2.5
	y1 = np.pi/24 + np.pi/6
	slope, intercept = get_line(0, y1, 3*np.pi, y2)
	for x in np.arange(0,3*np.pi, np.pi/8):
		lift.append(np.pi/14*math.cos(0) - np.pi/2.5)
		elbow.append(slope*x + intercept)
		wrist1.append(7*np.pi/6)
		wrist2.append(3*np.pi/2)
		pan.append(0)
	
	#POUR	
	for x in np.arange(0,8*np.pi, np.pi/8):
		lift.append(np.pi/14*math.cos(x) - np.pi/2.5)
		elbow.append(np.pi/4*math.e**(-0.2*x)*math.cos(x) + np.pi/2.5)
		wrist1.append(7*np.pi/6)
		wrist2.append(3*np.pi/2)
		pan.append(0)
		
	robot.animate(cfg_trajectory={
		'shoulder_pan_joint' : pan,
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_1_joint' : wrist1,
		'wrist_2_joint' : wrist2}, loop_time=7)


def bus_driver_steering(robot):
	pan = []
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	wrist3 = []
	gripper = []
	offset = 0
	for x in np.arange(0,6*np.pi, np.pi/8):
		pan.append(np.pi/10*math.cos(x) - np.pi/10)
		lift.append(np.pi/10*math.cos(x- np.pi/2 - offset) + np.pi/4)
		elbow.append(np.pi/30*math.cos(2*x - np.pi) - 2*np.pi/3)
		wrist1.append(np.pi/20*math.cos(x + np.pi) + 3*np.pi/2)
		wrist2.append(3*np.pi/2)
		wrist3.append(-np.pi/4*math.cos(x))
		gripper.append(0.5)
		if x%np.pi == 0:
			offset += np.pi
	for x in np.arange(6*np.pi, 10*np.pi, np.pi/8):
		pan.append(np.pi/10*math.cos(x) - np.pi/10)
		lift.append(np.pi/10*math.cos(x- np.pi/2) + np.pi/4)
		elbow.append(np.pi/30*math.cos(2*x - np.pi) - 2*np.pi/3)
		wrist1.append(np.pi/20*math.cos(x + np.pi/2) + 3.5*np.pi/2.5)
		wrist2.append(3*np.pi/2)
		wrist3.append(-np.pi/4*x)
		gripper.append(0.5)
	robot.animate(cfg_trajectory={
		'shoulder_pan_joint': pan,
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_2_joint' : wrist2,
		'wrist_1_joint' : wrist1,
		'wrist_3_joint' : wrist3,
		'robotiq_85_left_knuckle_joint' : gripper}, loop_time=4)

def bus_driver_lever(robot):
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	for x in np.arange(0,2*np.pi, np.pi/8):
		lift.append(np.pi/5*math.sin(x) - np.pi/6)
		elbow.append(np.pi/3*math.sin(x- 3*np.pi/4) +np.pi/4)
		wrist2.append(3*np.pi/2)
		wrist1.append(7*np.pi/6)
	robot.animate(cfg_trajectory={
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_2_joint' : wrist2,
		'wrist_1_joint' : wrist1}, loop_time=4)

def yoga_right_overhead(robot):
	gripper = []
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	for x in np.arange(0, 2*np.pi, np.pi/8):
		lift.append(np.pi/96*math.cos(x) - 3*np.pi/4)
		elbow.append(np.pi/96*math.cos(x) - np.pi/4)
		wrist1.append(np.pi)
		wrist2.append(3*np.pi/2)
		gripper.append(1)
	robot.animate(cfg_trajectory={
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_2_joint' : wrist2,
		'wrist_1_joint' : wrist1,
		'robotiq_85_left_knuckle_joint' : gripper}, loop_time=2)

def screw_lightbulb(robot):
	gripper = []
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	wrist3 = []
	offset = 0
	for x in np.arange(0, 8*np.pi, np.pi/8):
		lift.append(-np.pi/8)
		elbow.append(-np.pi/3)
		wrist1.append(np.pi)
		wrist2.append(3*np.pi/2)
		wrist3.append(np.pi/6*math.cos(x - offset))
		gripper.append(0.25*math.cos(x-offset))
		if x%np.pi == 0:
			offset += np.pi
	robot.animate(cfg_trajectory={
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_2_joint' : wrist2,
		'wrist_1_joint' : wrist1,
		'wrist_3_joint' : wrist3,
		'robotiq_85_left_knuckle_joint' : gripper}, loop_time=4)

def hammer_wall(robot):
	gripper = []
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	wrist3 = []
	for x in np.arange(0, 8*np.pi, np.pi/8):
		lift.append(np.pi/8)
		elbow.append(np.pi/6*math.cos(x)-np.pi/2)
		wrist1.append(5*np.pi/4)
		wrist2.append(3*np.pi/2)
		gripper.append(0.5)
	robot.animate(cfg_trajectory={
		'shoulder_lift_joint' : lift,
		'elbow_joint' : elbow,
		'wrist_2_joint' : wrist2,
		'wrist_1_joint' : wrist1,
		'robotiq_85_left_knuckle_joint' : gripper}, loop_time=4)

def wrench(robot):
	gripper = []
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	wrist3 = []
	pan = []
	offset = 0
	reset = False
	for x in np.arange(0, 8*np.pi, np.pi/8):
		if x!=0 and x%(2*np.pi)==0:
			offset += 2*np.pi
			reset = False
		elbow.append(np.pi/24*math.cos(x) + 2*np.pi/3)
		wrist1.append(10*np.pi/9)
		wrist2.append(3*np.pi/2)
		wrist3.append(np.pi/4*math.cos(x))
		gripper.append(0.25*math.cos(x))
		pan.append(np.pi/10*math.cos(x))
		if x!=0 and x%np.pi==0 and x%(2*np.pi)!=0:
			reset = True
		if reset:
			if x-offset - 3*np.pi/2 <0:
				lift.append(np.pi/6*math.cos(2*x) - 1.29)
			else:
				lift.append(np.pi/8*math.cos(2*x) - 1.41)
		else:
			reset = False
			lift.append(np.pi/24*math.cos(x - np.pi) - np.pi/3.5)
	robot.animate(cfg_trajectory={
		'shoulder_lift_joint' : lift,
		'shoulder_pan_joint' : pan,
		'elbow_joint' : elbow,
		'wrist_2_joint' : wrist2,
		'wrist_1_joint' : wrist1,
		'wrist_3_joint' : wrist3,
		'robotiq_85_left_knuckle_joint' : gripper}, loop_time=4)

def dust_shelf(robot):
	gripper = []
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	pan = []
	for x in np.arange(0,8*np.pi, np.pi/8):
		elbow.append(np.pi/8)
		wrist1.append(4*np.pi/3)
		wrist2.append(np.pi/6*math.cos(2*x) - np.pi/2)
		gripper.append(0.5)
		pan.append(np.pi/4*math.cos(x/12))
		lift.append(-np.pi/3)
	robot.animate(cfg_trajectory={
		'shoulder_lift_joint' : lift,
		'shoulder_pan_joint' : pan,
		'elbow_joint' : elbow,
		'wrist_2_joint' : wrist2,
		'wrist_1_joint' : wrist1,
		'robotiq_85_left_knuckle_joint' : gripper}, loop_time=2)

def pick_fruit(robot):
	gripper = []
	lift = []
	elbow = []
	wrist1 = []
	wrist2 = []
	wrist3 = []
	pan = []
	
	#FRUIT 1
	#twist
	for x in np.arange(0,np.pi, np.pi/8):
		elbow.append(np.pi/8)
		wrist1.append(np.pi)
		wrist2.append(3*np.pi/2)
		wrist3.append(np.pi/3*math.cos(2*x))
		gripper.append(0.5)
		pan.append(0)
		lift.append(-np.pi/3)
	#pluck
	for x in np.arange(0,2*np.pi, np.pi/8):
		elbow.append(-np.pi/8)
		wrist1.append(np.pi)
		wrist2.append(3*np.pi/2)
		wrist3.append(np.pi/3)
		gripper.append(0.5)
		pan.append(0)
		lift.append(-np.pi/4)
	
	#move to basket
	for x in np.arange(0,np.pi, np.pi/8):
		elbow.append(19*np.pi/48*math.cos(x-np.pi) + 13*np.pi/48)
		wrist1.append(np.pi)
		wrist2.append(3*np.pi/2)
		wrist3.append(0)
		gripper.append(0.5)
		pan.append(0)
		lift.append(np.pi/24*math.cos(x) - 7*np.pi/24)
	
	#drop in basket
	for x in np.arange(0,2*np.pi, np.pi/8):
		elbow.append(2*np.pi/3)
		wrist1.append(np.pi)
		wrist2.append(3*np.pi/2)
		wrist3.append(0)
		gripper.append(0)
		pan.append(0)
		lift.append(-np.pi/3)
	
	#FRUIT 2
	#go to fruit
	for x in np.arange(0,2*np.pi, np.pi/8):
		elbow.append(np.pi/3*math.cos(0.5*x) + np.pi/3)
		wrist1.append(np.pi)
		wrist2.append(3*np.pi/2)
		wrist3.append(0)
		gripper.append(0)
		pan.append(0)
		lift.append(np.pi/12*math.cos(0.5*x) - 5*np.pi/12)
	#twist
	for x in np.arange(0,np.pi, np.pi/8):
		elbow.append(0)
		wrist1.append(np.pi)
		wrist2.append(3*np.pi/2)
		wrist3.append(np.pi/3*math.cos(2*x))
		gripper.append(0.5)
		pan.append(0)
		lift.append(-np.pi/2)
	#pluck
	for x in np.arange(0,2*np.pi, np.pi/8):
		elbow.append(np.pi/8)
		wrist1.append(np.pi)
		wrist2.append(3*np.pi/2)
		wrist3.append(np.pi/3)
		gripper.append(0.5)
		pan.append(0)
		lift.append(-3*np.pi/5)
	
	#move to basket
	for x in np.arange(0,np.pi, np.pi/8):
		elbow.append(13*np.pi/48*math.cos(x-np.pi) + 19*np.pi/48)
		wrist1.append(np.pi)
		wrist2.append(3*np.pi/2)
		wrist3.append(0)
		gripper.append(0.5)
		pan.append(0)
		lift.append(2*np.pi/15*math.cos(x-np.pi) - 7*np.pi/15)
	
	#drop in basket
	for x in np.arange(0,2*np.pi, np.pi/8):
		elbow.append(2*np.pi/3)
		wrist1.append(np.pi)
		wrist2.append(3*np.pi/2)
		wrist3.append(0)
		gripper.append(0)
		pan.append(0)
		lift.append(-np.pi/3)
	
	#FRUIT 3
	#go to fruit
	for x in np.arange(0,2*np.pi, np.pi/8):
		elbow.append(np.pi/4*math.cos(0.5*x) + 5*np.pi/12)
		wrist1.append(np.pi)
		wrist2.append(3*np.pi/2)
		wrist3.append(0)
		gripper.append(0)
		pan.append(np.pi/4*math.cos(0.5*x))
		lift.append(np.pi/24*math.cos(0.5*x-np.pi) - 7*np.pi/24)
	#twist
	for x in np.arange(0,np.pi, np.pi/8):
		elbow.append(np.pi/6)
		wrist1.append(np.pi)
		wrist2.append(3*np.pi/2)
		wrist3.append(np.pi/3*math.cos(2*x))
		gripper.append(0.5)
		pan.append(-np.pi/4)
		lift.append(-np.pi/4)
	#pluck
	for x in np.arange(0,2*np.pi, np.pi/8):
		elbow.append(np.pi/8)
		wrist1.append(np.pi)
		wrist2.append(3*np.pi/2)
		wrist3.append(np.pi/3)
		gripper.append(0.5)
		pan.append(-np.pi/4)
		lift.append(-np.pi/3)
	
	#move to basket
	for x in np.arange(0,np.pi, np.pi/8):
		elbow.append(13*np.pi/48*math.cos(x-np.pi) + 19*np.pi/48)
		wrist1.append(np.pi)
		wrist2.append(3*np.pi/2)
		wrist3.append(0)
		gripper.append(0.5)
		pan.append(-np.pi/4)
		lift.append(-np.pi/3)
	
	#drop in basket
	for x in np.arange(0,2*np.pi, np.pi/8):
		elbow.append(2*np.pi/3)
		wrist1.append(np.pi)
		wrist2.append(3*np.pi/2)
		wrist3.append(0)
		gripper.append(0)
		pan.append(-np.pi/4)
		lift.append(-np.pi/3)
		
	robot.animate(cfg_trajectory={
		'shoulder_lift_joint' : lift,
		'shoulder_pan_joint' : pan,
		'elbow_joint' : elbow,
		'wrist_2_joint' : wrist2,
		'wrist_1_joint' : wrist1,
		'wrist_3_joint' : wrist3,
		'robotiq_85_left_knuckle_joint' : gripper}, loop_time=6)
	
	
			
def main():
    robot = URDF.load('/home/shreyaganti/DUET/ur5/ur_with_gripper.xacro')
    #painter_vertical(robot)
    #painter_dip_brush(robot)
    #painter_vertical_dip(robot)
    #painter_ceiling(robot)
    #newspaper_delivery(robot)
    #cleaner_vacuum(robot)
    #cleaner_vacuum_panning(robot)
    #cleaner_horizontal(robot)
    #cleaner_horizontal_wall(robot)
    #farmer_raking(robot)
    #farmer_raking_panning(robot)
    #sweep_floor(robot)
    #circle_horizontal(robot)
    #circle_vertical(robot)
    #shoveling(robot)
    #flipping_pan(robot)
    #spiral_horizontal_circle(robot)
    #waving(robot)
    #brick_layer(robot)
    #bartender_shaking(robot)
    #bartender_pouring(robot)
    #bartender_shake_pour(robot)
    #bus_driver_steering(robot)
    #bus_driver_lever(robot)
    #yoga_right_overhead(robot)
    #screw_lightbulb(robot)
    #hammer_wall(robot)
    #wrench(robot)
    #dust_shelf(robot)
    pick_fruit(robot)
    

if __name__ == "__main__":
    main()
	
	
