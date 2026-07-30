'''
RigBox_BaseSkeleton Module v1.0
Connect to RigBox_Main Module

by Broderick Woodward-Crackower

To-Do:
    Convert joint position coordinates to variables
    Generate Shoulder and Hip rolls
    Add parameters for single/double roll joints per-limb
    Add COG joint
'''  

import maya.cmds as cmds

from rigbox import tools

class CreateBaseSkeleton(object):
    
    def __init__(self):
        # Joint Labels:
        self.JNT = [
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
        self.SUF = ["_jnt", "_sys", "_ctrl"] # [0], [1], [2]
        
        # Orientation Labels
        self.SIDE = ["_M", "_L", "_R"] # [0], [1], [2]
        
        # Lists for carrying variables around
        self.deformJoint_list = []
        self.node_list = []
        
        # Joint Variables
        self.root = None
        self.hips = None
        self.spine = None
        self.spine1 = None
        self.spine2 = None
        
        self.neck = None
        self.neck1 = None
        self.head = None
        self.headEnd = None
        
        self.upperLeg_L = None
        self.lowerLeg_L = None
        self.foot_L = None
        self.toe_L = None
        self.toeEnd_L = None
        
        self.upperLeg_R = None
        self.lowerLeg_R = None
        self.foot_R = None
        self.toe_R = None
        self.toeEnd_R = None
            
        self.clavicle_L = None
        self.upperArm_L = None
        self.lowerArm_L = None
        self.wrist_L = None
        
        self.clavicle_R = None
        self.upperArm_R = None
        self.lowerArm_R = None
        self.wrist_R = None
        
        self.index_L = None
        self.index2_L = None
        self.index3_L = None
        self.indexEnd_L = None
        
        self.middle_L = None
        self.middle2_L = None
        self.middle3_L = None
        self.middleEnd_L = None
        
        self.ring_L = None
        self.ring2_L = None
        self.ring3_L = None
        self.ringEnd_L = None
        
        self.pinky_L = None
        self.pinky2_L = None
        self.pinky3_L = None
        self.pinkyEnd_L = None
        
        self.thumb_L = None
        self.thumb2_L = None
        self.thumb3_L = None
        self.thumbEnd_L = None
        
        self.index_R = None
        self.index2_R = None
        self.index3_R = None
        self.indexEnd_R = None
        
        self.middle_R = None
        self.middle2_R = None
        self.middle3_R = None
        self.middleEnd_R = None
        
        self.ring_R = None
        self.ring2_R = None
        self.ring3_R = None
        self.ringEnd_R = None
        
        self.pinky_R = None
        self.pinky2_R = None
        self.pinky3_R = None
        self.pinkyEnd_R = None
        
        self.thumb_R = None
        self.thumb2_R = None
        self.thumb3_R = None
        self.thumbEnd_R = None
        
        # Joint Initialization Variables
        self.root_pos = (0,0,0)
        
        self.hips_pos = (0,100,0)
        self.spine_pos = (0,107,0)
        self.spine1_pos = (0,120,0)
        self.spine2_pos = (0,132,0)
        
        self.neck_pos = (0,145,0)
        self.neck1_pos = (0,155,0)
        self.head_pos = (0,165,0)
        self.headEnd_pos = (0,175,0)
        
        self.upperLeg_L_pos = (9,94,0)
        self.lowerLeg_L_pos = (9,49,0)
        self.foot_L_pos = (9,8,0)
        self.toe_L_pos = (9,2,13)
        self.toeEnd_L_pos = (9,2,20)
 
        self.clavicle_L_pos = (7,147,0)
        self.upperArm_L_pos = (17,147,0)
        self.lowerArm_L_pos = (45,147,0)
        self.wrist_L_pos = (72,147,0)
                  
    def create_root(self):
        self.root = cmds.createNode("joint", n=self.JNT[0] + self.SUF[0]) # Create root node at world origin
            
    def create_spine(self):
        spine_list = [] # Carries around spine joint variables
        
        self.hips = cmds.createNode("joint", n=self.JNT[1] + self.SIDE[0] + self.SUF[0])   # Create Joints
        self.spine = cmds.createNode("joint", n=self.JNT[2] + self.SIDE[0] + self.SUF[0])  #              |
        self.spine1 = cmds.createNode("joint", n=self.JNT[3] + self.SIDE[0] + self.SUF[0]) #              |
        self.spine2 = cmds.createNode("joint", n=self.JNT[4] + self.SIDE[0] + self.SUF[0]) #              V
       
        cmds.xform(self.hips, ws=True, t=(0,100,0))   # Place Joints
        cmds.xform(self.spine, ws=True, t=(0,107,0))  #             |
        cmds.xform(self.spine1, ws=True, t=(0,120,0)) #             |
        cmds.xform(self.spine2, ws=True, t=(0,132,0)) #             V
        
        spine_list.append(self.hips)   # Append to list
        spine_list.append(self.spine)  #               |
        spine_list.append(self.spine1) #               |
        spine_list.append(self.spine2) #               V
        
        tools.create_joint_chain("X", "Y", spine_list) # Create chain
        
        cmds.parent(self.hips, self.root) # Attach to Root
        
        self.deformJoint_list.extend(spine_list) # Add to the basket
        
    def create_neck(self):
        neck_list = [] # Carries around neck joint variables
        
        self.neck = cmds.createNode("joint", n=self.JNT[5] + self.SIDE[0] + self.SUF[0])    # Create Joints
        self.neck1 = cmds.createNode("joint", n=self.JNT[6] + self.SIDE[0] + self.SUF[0])   #
        self.head = cmds.createNode("joint", n=self.JNT[7] + self.SIDE[0] + self.SUF[0])    #
        self.headEnd = cmds.createNode("joint", n=self.JNT[8] + self.SIDE[0] + self.SUF[0]) #
        
        cmds.xform(self.neck, ws=True, t=(0,145,0))    # Place joints
        cmds.xform(self.neck1, ws=True, t=(0,155,0))   #
        cmds.xform(self.head, ws=True, t=(0,165,0))    #
        cmds.xform(self.headEnd, ws=True, t=(0,175,0)) #
        
        neck_list.append(self.neck)    # Append to list
        neck_list.append(self.neck1)   #
        neck_list.append(self.head)    #
        neck_list.append(self.headEnd) #
        
        tools.create_joint_chain("X", "Y",  neck_list) # Create chain
        
        cmds.parent(self.neck, self.spine2) # Attach to Spine2
        
        self.deformJoint_list.extend(neck_list) # Add to the basket
        
    def create_leftLeg(self):
        leg_list = []
                
        self.upperLeg_L = cmds.createNode("joint", n=self.JNT[33] + self.SIDE[1] + self.SUF[0])
        self.lowerLeg_L = cmds.createNode("joint", n=self.JNT[34] + self.SIDE[1] + self.SUF[0])
        self.foot_L = cmds.createNode("joint", n=self.JNT[35] + self.SIDE[1] + self.SUF[0])
        self.toe_L = cmds.createNode("joint", n=self.JNT[36] + self.SIDE[1] + self.SUF[0])
        self.toeEnd_L = cmds.createNode("joint", n=self.JNT[37] + self.SIDE[1] + self.SUF[0])
    
        cmds.xform(self.upperLeg_L, ws=True, t=(9,94,0))
        cmds.xform(self.lowerLeg_L, ws=True, t=(9,49,0))
        cmds.xform(self.foot_L, ws=True, t=(9,8,0))
        cmds.xform(self.toe_L, ws=True, t=(9,2,13))
        cmds.xform(self.toeEnd_L, ws=True, t=(9,2,20))
        
        leg_list.append(self.upperLeg_L)
        leg_list.append(self.lowerLeg_L)
        leg_list.append(self.foot_L)
        leg_list.append(self.toe_L)
        leg_list.append(self.toeEnd_L)
        
        tools.create_joint_chain("X", "Z", leg_list)
    
        cmds.parent(self.upperLeg_L, self.hips)
                        
        self.deformJoint_list.extend(leg_list)   
        
    def create_rightLeg(self):
        leg_list = []
                
        self.upperLeg_R = cmds.createNode("joint", n=self.JNT[33] + self.SIDE[2] + self.SUF[0])
        self.lowerLeg_R = cmds.createNode("joint", n=self.JNT[34] + self.SIDE[2] + self.SUF[0])
        self.foot_R = cmds.createNode("joint", n=self.JNT[35] + self.SIDE[2] + self.SUF[0])
        self.toe_R = cmds.createNode("joint", n=self.JNT[36] + self.SIDE[2] + self.SUF[0])
        self.toeEnd_R = cmds.createNode("joint", n=self.JNT[37] + self.SIDE[2] + self.SUF[0])
    
        cmds.xform(self.upperLeg_R, ws=True, t=(-9,94,0))
        cmds.xform(self.lowerLeg_R, ws=True, t=(-9,49,0))
        cmds.xform(self.foot_R, ws=True, t=(-9,8,0))
        cmds.xform(self.toe_R, ws=True, t=(-9,2,13))
        cmds.xform(self.toeEnd_R, ws=True, t=(-9,2,20))
        
        leg_list.append(self.upperLeg_R)
        leg_list.append(self.lowerLeg_R)
        leg_list.append(self.foot_R)
        leg_list.append(self.toe_R)
        leg_list.append(self.toeEnd_R)
            
        tools.create_joint_chain("-X", "-Z", leg_list)
    
        cmds.parent(self.upperLeg_R, self.hips)
                        
        self.deformJoint_list.extend(leg_list)           
        
    def create_leftArm(self, hand=False):
        arm_list = []
        
        self.clavicle_L = cmds.createNode("joint", n=self.JNT[9] + self.SIDE[1] + self.SUF[0])
        self.upperArm_L = cmds.createNode("joint", n=self.JNT[10] + self.SIDE[1] + self.SUF[0])
        self.lowerArm_L = cmds.createNode("joint", n=self.JNT[11] + self.SIDE[1] + self.SUF[0])
        self.wrist_L = cmds.createNode("joint", n=self.JNT[12] + self.SIDE[1] + self.SUF[0])
            
        cmds.xform(self.clavicle_L, ws=True, t=(7,147,0))
        cmds.xform(self.upperArm_L, ws=True, t=(17,147,0))
        cmds.xform(self.lowerArm_L, ws=True, t=(45,147,0))
        cmds.xform(self.wrist_L, ws=True, t=(72,147,0))
                
        arm_list.append(self.clavicle_L)
        arm_list.append(self.upperArm_L)
        arm_list.append(self.lowerArm_L)
        arm_list.append(self.wrist_L)
        
        tools.create_joint_chain("X", "Y", arm_list)
        
        lowerArm_rot = tools.query_rotation(self.lowerArm_L)
        cmds.xform(self.wrist_L, ro=lowerArm_rot)        
        
        if hand:
            self.create_leftHand()
               
        cmds.parent(self.clavicle_L, self.spine2)
    
        self.deformJoint_list.extend(arm_list)
        
    def create_rightArm(self, hand=False):
        arm_list = []
        
        self.clavicle_R = cmds.createNode("joint", n=self.JNT[9] + self.SIDE[2] + self.SUF[0])
        self.upperArm_R = cmds.createNode("joint", n=self.JNT[10] + self.SIDE[2] + self.SUF[0])
        self.lowerArm_R = cmds.createNode("joint", n=self.JNT[11] + self.SIDE[2] + self.SUF[0])
        self.wrist_R = cmds.createNode("joint", n=self.JNT[12] + self.SIDE[2] + self.SUF[0])
            
        cmds.xform(self.clavicle_R, ws=True, t=(-7,147,0))
        cmds.xform(self.upperArm_R, ws=True, t=(-17,147,0))
        cmds.xform(self.lowerArm_R, ws=True, t=(-45,147,0))
        cmds.xform(self.wrist_R, ws=True, t=(-72,147,0))
                
        arm_list.append(self.clavicle_R)
        arm_list.append(self.upperArm_R)
        arm_list.append(self.lowerArm_R)
        arm_list.append(self.wrist_R)
        
        tools.create_joint_chain("-X", "-Y", arm_list)
        
        lowerArm_rot = tools.query_rotation(self.lowerArm_R)
        cmds.xform(self.wrist_R, ro=lowerArm_rot)        
        
        if hand:
            self.create_rightHand()
               
        cmds.parent(self.clavicle_R, self.spine2)
    
        self.deformJoint_list.extend(arm_list)
       
    def create_leftHand(self):
        index_list = []
        middle_list = []
        ring_list = []
        pinky_list = []
        thumb_list = []
        
        # Index Finger
        self.index_L = cmds.createNode("joint", n=self.JNT[17] + self.SIDE[1] + self.SUF[0])
        self.index1_L = cmds.createNode("joint", n=self.JNT[18] + self.SIDE[1] + self.SUF[0])
        self.index2_L = cmds.createNode("joint", n=self.JNT[19] + self.SIDE[1] + self.SUF[0])
        self.indexEnd_L = cmds.createNode("joint", n=self.JNT[20] + self.SIDE[1] + self.SUF[0])
        
        cmds.xform(self.index_L, ws=True, t=(80,147,3))
        cmds.xform(self.index1_L, ws=True, t=(85,147,3))
        cmds.xform(self.index2_L, ws=True, t=(88,147,3))
        cmds.xform(self.indexEnd_L, ws=True, t=(90,147,3))
        
        index_list.append(self.index_L)
        index_list.append(self.index1_L)
        index_list.append(self.index2_L)
        index_list.append(self.indexEnd_L)
        
        # Middle Finger
        self.middle_L = cmds.createNode("joint", n=self.JNT[21] + self.SIDE[1] + self.SUF[0])
        self.middle1_L = cmds.createNode("joint", n=self.JNT[22] + self.SIDE[1] + self.SUF[0])
        self.middle2_L = cmds.createNode("joint", n=self.JNT[23] + self.SIDE[1] + self.SUF[0])
        self.middleEnd_L = cmds.createNode("joint", n=self.JNT[24] + self.SIDE[1] + self.SUF[0])
        
        cmds.xform(self.middle_L, ws=True, t=(80,147,1))
        cmds.xform(self.middle1_L, ws=True, t=(85,147,1))
        cmds.xform(self.middle2_L, ws=True, t=(88,147,1))
        cmds.xform(self.middleEnd_L, ws=True, t=(90,147,1))
        
        middle_list.append(self.middle_L)
        middle_list.append(self.middle1_L)
        middle_list.append(self.middle2_L)
        middle_list.append(self.middleEnd_L)
        
        # Ring Finger
        self.ring_L = cmds.createNode("joint", n=self.JNT[25] + self.SIDE[1] + self.SUF[0])
        self.ring1_L = cmds.createNode("joint", n=self.JNT[26] + self.SIDE[1] + self.SUF[0])
        self.ring2_L = cmds.createNode("joint", n=self.JNT[27] + self.SIDE[1] + self.SUF[0])
        self.ringEnd_L = cmds.createNode("joint", n=self.JNT[28] + self.SIDE[1] + self.SUF[0])
        
        cmds.xform(self.ring_L, ws=True, t=(80,147,-1))
        cmds.xform(self.ring1_L, ws=True, t=(85,147,-1))
        cmds.xform(self.ring2_L, ws=True, t=(88,147,-1))
        cmds.xform(self.ringEnd_L, ws=True, t=(90,147,-1))
        
        ring_list.append(self.ring_L)
        ring_list.append(self.ring1_L)
        ring_list.append(self.ring2_L)
        ring_list.append(self.ringEnd_L)
        
        # Pinky Finger
        self.pinky_L = cmds.createNode("joint", n=self.JNT[29] + self.SIDE[1] + self.SUF[0])
        self.pinky1_L = cmds.createNode("joint", n=self.JNT[30] + self.SIDE[1] + self.SUF[0])
        self.pinky2_L = cmds.createNode("joint", n=self.JNT[31] + self.SIDE[1] + self.SUF[0])
        self.pinkyEnd_L = cmds.createNode("joint", n=self.JNT[32] + self.SIDE[1] + self.SUF[0])
        
        cmds.xform(self.pinky_L, ws=True, t=(80,147,-3))
        cmds.xform(self.pinky1_L, ws=True, t=(85,147,-3))
        cmds.xform(self.pinky2_L, ws=True, t=(88,147,-3))
        cmds.xform(self.pinkyEnd_L, ws=True, t=(90,147,-3))
        
        pinky_list.append(self.pinky_L)
        pinky_list.append(self.pinky1_L)
        pinky_list.append(self.pinky2_L)
        pinky_list.append(self.pinkyEnd_L)
        
        # Thumb
        self.thumb_L = cmds.createNode("joint", n=self.JNT[13] + self.SIDE[1] + self.SUF[0])
        self.thumb1_L = cmds.createNode("joint", n=self.JNT[14] + self.SIDE[1] + self.SUF[0])
        self.thumb2_L = cmds.createNode("joint", n=self.JNT[15] + self.SIDE[1] + self.SUF[0])
        self.thumbEnd_L = cmds.createNode("joint", n=self.JNT[16] + self.SIDE[1] + self.SUF[0])
        
        cmds.xform(self.thumb_L, ws=True, t=(76,145,4))
        cmds.xform(self.thumb1_L, ws=True, t=(78,145,5))
        cmds.xform(self.thumb2_L, ws=True, t=(81,145,5))
        cmds.xform(self.thumbEnd_L, ws=True, t=(84,145,5))
        
        thumb_list.append(self.thumb_L)
        thumb_list.append(self.thumb1_L)
        thumb_list.append(self.thumb2_L)
        thumb_list.append(self.thumbEnd_L)
        
        tools.create_joint_chain("X", "Y", index_list)
        tools.create_joint_chain("X", "Y", middle_list)
        tools.create_joint_chain("X", "Y", ring_list)
        tools.create_joint_chain("X", "Y", pinky_list)
        tools.create_joint_chain("X", "Y", thumb_list)
        
        cmds.parent(self.index_L, self.middle_L, self.ring_L, self.pinky_L, self.thumb_L, self.wrist_L)
        
        self.deformJoint_list.extend(index_list)
        self.deformJoint_list.extend(middle_list)
        self.deformJoint_list.extend(ring_list)
        self.deformJoint_list.extend(pinky_list)
        self.deformJoint_list.extend(thumb_list)
        
    def create_rightHand(self):
        index_list = []
        middle_list = []
        ring_list = []
        pinky_list = []
        thumb_list = []
        
        # Index Finger
        self.index_R = cmds.createNode("joint", n=self.JNT[17] + self.SIDE[2] + self.SUF[0])
        self.index1_R = cmds.createNode("joint", n=self.JNT[18] + self.SIDE[2] + self.SUF[0])
        self.index2_R = cmds.createNode("joint", n=self.JNT[19] + self.SIDE[2] + self.SUF[0])
        self.indexEnd_R = cmds.createNode("joint", n=self.JNT[20] + self.SIDE[2] + self.SUF[0])
        
        cmds.xform(self.index_R, ws=True, t=(-80,147,3))
        cmds.xform(self.index1_R, ws=True, t=(-85,147,3))
        cmds.xform(self.index2_R, ws=True, t=(-88,147,3))
        cmds.xform(self.indexEnd_R, ws=True, t=(-90,147,3))
        
        index_list.append(self.index_R)
        index_list.append(self.index1_R)
        index_list.append(self.index2_R)
        index_list.append(self.indexEnd_R)
        
        # Middle Finger
        self.middle_R = cmds.createNode("joint", n=self.JNT[21] + self.SIDE[2] + self.SUF[0])
        self.middle1_R = cmds.createNode("joint", n=self.JNT[22] + self.SIDE[2] + self.SUF[0])
        self.middle2_R = cmds.createNode("joint", n=self.JNT[23] + self.SIDE[2] + self.SUF[0])
        self.middleEnd_R = cmds.createNode("joint", n=self.JNT[24] + self.SIDE[2] + self.SUF[0])
        
        cmds.xform(self.middle_R, ws=True, t=(-80,147,1))
        cmds.xform(self.middle1_R, ws=True, t=(-85,147,1))
        cmds.xform(self.middle2_R, ws=True, t=(-88,147,1))
        cmds.xform(self.middleEnd_R, ws=True, t=(-90,147,1))
        
        middle_list.append(self.middle_R)
        middle_list.append(self.middle1_R)
        middle_list.append(self.middle2_R)
        middle_list.append(self.middleEnd_R)
        
        # Ring Finger
        self.ring_R = cmds.createNode("joint", n=self.JNT[25] + self.SIDE[2] + self.SUF[0])
        self.ring1_R = cmds.createNode("joint", n=self.JNT[26] + self.SIDE[2] + self.SUF[0])
        self.ring2_R = cmds.createNode("joint", n=self.JNT[27] + self.SIDE[2] + self.SUF[0])
        self.ringEnd_R = cmds.createNode("joint", n=self.JNT[28] + self.SIDE[2] + self.SUF[0])
        
        cmds.xform(self.ring_R, ws=True, t=(-80,147,-1))
        cmds.xform(self.ring1_R, ws=True, t=(-85,147,-1))
        cmds.xform(self.ring2_R, ws=True, t=(-88,147,-1))
        cmds.xform(self.ringEnd_R, ws=True, t=(-90,147,-1))
        
        ring_list.append(self.ring_R)
        ring_list.append(self.ring1_R)
        ring_list.append(self.ring2_R)
        ring_list.append(self.ringEnd_R)
        
        # Pinky Finger
        self.pinky_R = cmds.createNode("joint", n=self.JNT[29] + self.SIDE[2] + self.SUF[0])
        self.pinky1_R = cmds.createNode("joint", n=self.JNT[30] + self.SIDE[2] + self.SUF[0])
        self.pinky2_R = cmds.createNode("joint", n=self.JNT[31] + self.SIDE[2] + self.SUF[0])
        self.pinkyEnd_R = cmds.createNode("joint", n=self.JNT[32] + self.SIDE[2] + self.SUF[0])
        
        cmds.xform(self.pinky_R, ws=True, t=(-80,147,-3))
        cmds.xform(self.pinky1_R, ws=True, t=(-85,147,-3))
        cmds.xform(self.pinky2_R, ws=True, t=(-88,147,-3))
        cmds.xform(self.pinkyEnd_R, ws=True, t=(-90,147,-3))
        
        pinky_list.append(self.pinky_R)
        pinky_list.append(self.pinky1_R)
        pinky_list.append(self.pinky2_R)
        pinky_list.append(self.pinkyEnd_R)
        
        # Thumb
        self.thumb_R = cmds.createNode("joint", n=self.JNT[13] + self.SIDE[2] + self.SUF[0])
        self.thumb1_R = cmds.createNode("joint", n=self.JNT[14] + self.SIDE[2] + self.SUF[0])
        self.thumb2_R = cmds.createNode("joint", n=self.JNT[15] + self.SIDE[2] + self.SUF[0])
        self.thumbEnd_R = cmds.createNode("joint", n=self.JNT[16] + self.SIDE[2] + self.SUF[0])
        
        cmds.xform(self.thumb_R, ws=True, t=(-76,145,4))
        cmds.xform(self.thumb1_R, ws=True, t=(-78,145,5))
        cmds.xform(self.thumb2_R, ws=True, t=(-81,145,5))
        cmds.xform(self.thumbEnd_R, ws=True, t=(-84,145,5))
        
        thumb_list.append(self.thumb_R)
        thumb_list.append(self.thumb1_R)
        thumb_list.append(self.thumb2_R)
        thumb_list.append(self.thumbEnd_R)
        
        tools.create_joint_chain("-X", "-Y", index_list)
        tools.create_joint_chain("-X", "-Y", middle_list)
        tools.create_joint_chain("-X", "-Y", ring_list)
        tools.create_joint_chain("-X", "-Y", pinky_list)
        tools.create_joint_chain("-X", "-Y", thumb_list)
        
        cmds.parent(self.index_R, self.middle_R, self.ring_R, self.pinky_R, self.thumb_R, self.wrist_R)
        
        self.deformJoint_list.extend(index_list)
        self.deformJoint_list.extend(middle_list)
        self.deformJoint_list.extend(ring_list)
        self.deformJoint_list.extend(pinky_list)
        self.deformJoint_list.extend(thumb_list)        
    
    def finalize(self):
        cmds.select(d=True)
        
        for each in self.deformJoint_list:
            cmds.select(each, add=True)
            
        cmds.sets(n="DeformJoints_Set")
        
        cmds.select(d=True)

# Create Deform System        
    def create_roll_jnt(self, name, first, last):
        cmds.select(first)
        self.roll_jnt = cmds.joint(n=name)

        self.roll_jnt_pos = tools.average_location("X", last)
                        
        cmds.xform(self.roll_jnt, t=self.roll_jnt_pos)
        
        self.deformJoint_list.append(self.roll_jnt)    
        
    def apply_roll_jnts(self, mirror=False):
        self.create_roll_jnt(f"{self.JNT[33]}_roll{self.SIDE[1]}{self.SUF[0]}", self.upperLeg_L, self.lowerLeg_L)
             
        self.create_roll_jnt(f"{self.JNT[34]}_roll{self.SIDE[1]}{self.SUF[0]}", self.lowerLeg_L, self.foot_L)
        
        self.create_roll_jnt(f"{self.JNT[10]}_roll{self.SIDE[1]}{self.SUF[0]}", self.upperArm_L, self.lowerArm_L)

        self.create_roll_jnt(f"{self.JNT[11]}_roll{self.SIDE[1]}{self.SUF[0]}", self.lowerArm_L, self.wrist_L)   
        
        if mirror:
            self.create_roll_jnt(f"{self.JNT[33]}_roll{self.SIDE[2]}{self.SUF[0]}", self.upperLeg_R, self.lowerLeg_R)
                 
            self.create_roll_jnt(f"{self.JNT[34]}_roll{self.SIDE[2]}{self.SUF[0]}", self.lowerLeg_R, self.foot_R)
            
            self.create_roll_jnt(f"{self.JNT[10]}_roll{self.SIDE[2]}{self.SUF[0]}", self.upperArm_R, self.lowerArm_R)

            self.create_roll_jnt(f"{self.JNT[11]}_roll{self.SIDE[2]}{self.SUF[0]}", self.lowerArm_R, self.wrist_R)       
            
    def create_roll_sys(self, name, inJoint, outJoint):    
        sys_node = cmds.createNode("multiplyDivide", n=name)
        cmds.connectAttr(f"{inJoint}.ry", f"{sys_node}.input1X")
        cmds.connectAttr(f"{sys_node}.outputX", f"{outJoint}.ry")
        cmds.setAttr(f"{sys_node}.input2X", 0.5)
        self.node_list.append(sys_node)        
    
    def setup_roll_sys(self, mirror):
        # upperArm roll
        self.create_roll_sys(f"{self.JNT[10]}{self.SIDE[1]}{self.SUF[1]}", f"{self.JNT[10]}{self.SIDE[1]}{self.SUF[0]}", f"{self.JNT[10]}_roll{self.SIDE[1]}{self.SUF[0]}")
    
        # lowerArm roll
        self.create_roll_sys(f"{self.JNT[11]}{self.SIDE[1]}{self.SUF[1]}", f"{self.JNT[12]}{self.SIDE[1]}{self.SUF[0]}", f"{self.JNT[11]}_roll{self.SIDE[1]}{self.SUF[0]}")
        
        # upperLeg roll
        self.create_roll_sys(f"{self.JNT[33]}{self.SIDE[1]}{self.SUF[1]}", f"{self.JNT[33]}{self.SIDE[1]}{self.SUF[0]}", f"{self.JNT[33]}_roll{self.SIDE[1]}{self.SUF[0]}")
        
        # lowerLeg roll
        self.create_roll_sys(f"{self.JNT[34]}{self.SIDE[1]}{self.SUF[1]}", f"{self.JNT[35]}{self.SIDE[1]}{self.SUF[0]}", f"{self.JNT[34]}_roll{self.SIDE[1]}{self.SUF[0]}")
        
        if mirror:       
            # upperArm roll
            self.create_roll_sys(f"{self.JNT[10]}{self.SIDE[2]}{self.SUF[1]}", f"{self.JNT[10]}{self.SIDE[2]}{self.SUF[0]}", f"{self.JNT[10]}_roll{self.SIDE[2]}{self.SUF[0]}")
           
            # lowerArm roll
            self.create_roll_sys(f"{self.JNT[11]}{self.SIDE[2]}{self.SUF[1]}", f"{self.JNT[12]}{self.SIDE[2]}{self.SUF[0]}", f"{self.JNT[11]}_roll{self.SIDE[2]}{self.SUF[0]}")

            # upperLeg roll
            self.create_roll_sys(f"{self.JNT[33]}{self.SIDE[2]}{self.SUF[1]}", f"{self.JNT[33]}{self.SIDE[2]}{self.SUF[0]}", f"{self.JNT[33]}_roll{self.SIDE[2]}{self.SUF[0]}")
            
            # lowerLeg roll
            self.create_roll_sys(f"{self.JNT[34]}{self.SIDE[2]}{self.SUF[1]}", f"{self.JNT[35]}{self.SIDE[2]}{self.SUF[0]}", f"{self.JNT[34]}_roll{self.SIDE[2]}{self.SUF[0]}")                     
                    
    def main(self):
        try:
            cmds.delete("root_jnt")
            cmds.delete(self.node_list)
            cmds.delete(self.deformJoint_list)
        except:
            pass
        self.create_root()
        self.create_spine()
        self.create_neck()
        self.create_leftLeg()
        self.create_rightLeg()
        self.create_leftArm(hand=True)
        self.create_rightArm(hand=True)
        cmds.makeIdentity(self.root, apply=True, r=True)
        
        cmds.select(d=True)
        
        for each in self.deformJoint_list:
            cmds.select(each, add=True)
            
        cmds.sets(n="DeformJoints_Set")
        
        cmds.select(d=True)
                       
if __name__ == "__main__":
    bskel = CreateBaseSkeleton()
    bskel.main()
                
        