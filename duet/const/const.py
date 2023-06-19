DRIVE_JSON_PATH = "drive/files.json"
TIMESTEP = 0.001  # needs to evenly divide 0.04, should match input to t_toss when called
FRAMERATE = 30  # FPS in original video, should be 25 or 30
NUM_SINES = 5
POINT_COMBO = [[0, 1], [1, 2], [2, 3], [3, 4], [1, 5], [5, 6], [6, 7], [1, 8],
               [8, 9], [8, 12], [9, 10], [12, 13], [
    10, 11], [13, 14], [11, 22],
    [14, 19], [11, 24], [14, 21], [
    19, 20], [22, 23], [0, 15], [0, 16],
    [16, 18], [15, 17], [4, 'right_hand'], [4, 'right_thumb'], [7, 'left_hand'], [7, 'left_thumb']]
