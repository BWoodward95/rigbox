# Joint Labels:
JNT = [
    "root", # [0] 
    "hips", "spine", "spine1", "spine2", # [1], [2], [3], [4]
    "neck", "neck1", "head", "headEnd", # [5], [6], [7], [8]
    "clavicle", "upperArm", "lowerArm", "wrist", # [9], [10], [11], [12]
    "thumb", "thumb1", "thumb2", "thumbEnd", # [13], [14], [15], [16]
    "index", "index1", "index2", "indexEnd", # [17], [18], [19], [20]
    "middle", "middle1", "middle2", "middleEnd", # [21], [22], [23], [24]
    "ring", "ring1", "ring2", "ringEnd", # [25], [26], [27], [28]
    "pinky", "pinky1", "pinky2", "pinkyEnd", # [29], [30], [31], [32]
    "upperLeg", "lowerLeg", "foot", "toe", "toeEnd", # [33], [34], [35], [36], [37]
]

# Suffix Labels
SUF = ["_jnt", "_sys", "_ctrl", "_poleVector"] # [0], [1], [2], [3]

# Orientation Labels
SIDE = ["_M", "_L", "_R"] # [0], [1], [2]

# Lists for carrying variables around
deformJoint_list = []
node_list = []