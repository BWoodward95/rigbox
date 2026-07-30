import maya.cmds as cmds

from rigbox import tools, labels, arms

class ImportHands():
    
    def __init__(self):
        # Declare variables
        self.index_L = None
        self.index1_L = None
        self.index2_L = None
        self.indexEnd_L = None
        
        self.middle_L = None
        self.middle1_L = None
        self.middle2_L = None
        self.middleEnd_L = None
        
        self.ring_L = None
        self.ring1_L = None
        self.ring2_L = None
        self.ringEnd_L = None
        
        self.pinky_L = None
        self.pinky1_L = None
        self.pinky2_L = None
        self.pinkyEnd_L = None
        
        self.thumb_L = None
        self.thumb1_L = None
        self.thumb2_L = None
        self.thumbEnd_L = None
        
        self.index_R = None
        self.index1_R = None
        self.index2_R = None
        self.indexEnd_R = None
        
        self.middle_R = None
        self.middle1_R = None
        self.middle2_R = None
        self.middleEnd_R = None
        
        self.ring_R = None
        self.ring1_R = None
        self.ring2_R = None
        self.ringEnd_R = None
        
        self.pinky_R = None
        self.pinky1_R = None
        self.pinky2_R = None
        self.pinkyEnd_R = None
        
        self.thumb_R = None
        self.thumb1_R = None
        self.thumb2_R = None
        self.thumbEnd_R = None      
        
        # Initialize joint positions
        self.index_L_pos = (80,147,3)
        self.index1_L_pos = (85,147,3)
        self.index2_L_pos = (88,147,3)
        self.indexEnd_L_pos = (90,147,3)
        
        self.middle_L_pos = (80,147,1)
        self.middle1_L_pos = (85,147,1)
        self.middle2_L_pos = (88,147,1)
        self.middleEnd_L_pos = (90,147,1)
        
        self.ring_L_pos = (80,147,-1)
        self.ring1_L_pos = (85,147,-1)
        self.ring2_L_pos = (88,147,-1)
        self.ringEnd_L_pos = (90,147,-1)
        
        self.pinky_L_pos = (80,147,-3)
        self.pinky1_L_pos = (85,147,-3)
        self.pinky2_L_pos = (88,147,-3)
        self.pinkyEnd_L_pos = (90,147,-3)
        
        self.thumb_L_pos = (76,145,4)
        self.thumb1_L_pos = (78,145,5)
        self.thumb2_L_pos = (81,145,5)
        self.thumbEnd_L_pos = (84,145,5)
        
        self.index_R_pos = (-80,147,3)
        self.index1_R_pos = (-85,147,3)
        self.index2_R_pos = (-88,147,3)
        self.indexEnd_R_pos = (-90,147,3)
        
        self.middle_R_pos = (-80,147,1)
        self.middle1_R_pos = (-85,147,1)
        self.middle2_R_pos = (-88,147,1)
        self.middleEnd_R_pos = (-90,147,1)
        
        self.ring_R_pos = (-80,147,-1)
        self.ring1_R_pos = (-85,147,-1)
        self.ring2_R_pos = (-88,147,-1)
        self.ringEnd_R_pos = (-90,147,-1)
        
        self.pinky_R_pos = (-80,147,-3)
        self.pinky1_R_pos = (-85,147,-3)
        self.pinky2_R_pos = (-88,147,-3)
        self.pinkyEnd_R_pos = (-90,147,-3)
        
        self.thumb_R_pos = (-76,145,4)
        self.thumb1_R_pos = (-78,145,5)
        self.thumb2_R_pos = (-81,145,5)
        self.thumbEnd_R_pos = (-84,145,5)        
        
    def create_leftHand(self):
        index_list = []
        middle_list = []
        ring_list = []
        pinky_list = []
        thumb_list = []
        
        # Index Finger
        self.index_L = cmds.createNode("joint", n=labels.JNT[17] + labels.SIDE[1] + labels.SUF[0])
        self.index1_L = cmds.createNode("joint", n=labels.JNT[18] + labels.SIDE[1] + labels.SUF[0])
        self.index2_L = cmds.createNode("joint", n=labels.JNT[19] + labels.SIDE[1] + labels.SUF[0])
        self.indexEnd_L = cmds.createNode("joint", n=labels.JNT[20] + labels.SIDE[1] + labels.SUF[0])
        
        cmds.xform(self.index_L, ws=True, t=self.index_L_pos)
        cmds.xform(self.index1_L, ws=True, t=self.index1_L_pos)
        cmds.xform(self.index2_L, ws=True, t=self.index2_L_pos)
        cmds.xform(self.indexEnd_L, ws=True, t=self.indexEnd_L_pos)
        
        index_list.append(self.index_L)
        index_list.append(self.index1_L)
        index_list.append(self.index2_L)
        index_list.append(self.indexEnd_L)
        
        index2_L_rot = tools.query_rotation(self.index2_L)
        cmds.xform(self.indexEnd_L, ro=index2_L_rot)
        
        # Middle Finger
        self.middle_L = cmds.createNode("joint", n=labels.JNT[21] + labels.SIDE[1] + labels.SUF[0])
        self.middle1_L = cmds.createNode("joint", n=labels.JNT[22] + labels.SIDE[1] + labels.SUF[0])
        self.middle2_L = cmds.createNode("joint", n=labels.JNT[23] + labels.SIDE[1] + labels.SUF[0])
        self.middleEnd_L = cmds.createNode("joint", n=labels.JNT[24] + labels.SIDE[1] + labels.SUF[0])
        
        cmds.xform(self.middle_L, ws=True, t=self.middle_L_pos)
        cmds.xform(self.middle1_L, ws=True, t=self.middle1_L_pos)
        cmds.xform(self.middle2_L, ws=True, t=self.middle2_L_pos)
        cmds.xform(self.middleEnd_L, ws=True, t=self.middleEnd_L_pos)
        
        middle_list.append(self.middle_L)
        middle_list.append(self.middle1_L)
        middle_list.append(self.middle2_L)
        middle_list.append(self.middleEnd_L)

        middle2_L_rot = tools.query_rotation(self.middle2_L)
        cmds.xform(self.middleEnd_L, ro=middle2_L_rot)
        
        # Ring Finger
        self.ring_L = cmds.createNode("joint", n=labels.JNT[25] + labels.SIDE[1] + labels.SUF[0])
        self.ring1_L = cmds.createNode("joint", n=labels.JNT[26] + labels.SIDE[1] + labels.SUF[0])
        self.ring2_L = cmds.createNode("joint", n=labels.JNT[27] + labels.SIDE[1] + labels.SUF[0])
        self.ringEnd_L = cmds.createNode("joint", n=labels.JNT[28] + labels.SIDE[1] + labels.SUF[0])
        
        cmds.xform(self.ring_L, ws=True, t=self.ring_L_pos)
        cmds.xform(self.ring1_L, ws=True, t=self.ring1_L_pos)
        cmds.xform(self.ring2_L, ws=True, t=self.ring2_L_pos)
        cmds.xform(self.ringEnd_L, ws=True, t=self.ringEnd_L_pos)
        
        ring_list.append(self.ring_L)
        ring_list.append(self.ring1_L)
        ring_list.append(self.ring2_L)
        ring_list.append(self.ringEnd_L)

        ring2_L_rot = tools.query_rotation(self.ring2_L)
        cmds.xform(self.ringEnd_L, ro=ring2_L_rot)
        
        # Pinky Finger
        self.pinky_L = cmds.createNode("joint", n=labels.JNT[29] + labels.SIDE[1] + labels.SUF[0])
        self.pinky1_L = cmds.createNode("joint", n=labels.JNT[30] + labels.SIDE[1] + labels.SUF[0])
        self.pinky2_L = cmds.createNode("joint", n=labels.JNT[31] + labels.SIDE[1] + labels.SUF[0])
        self.pinkyEnd_L = cmds.createNode("joint", n=labels.JNT[32] + labels.SIDE[1] + labels.SUF[0])
        
        cmds.xform(self.pinky_L, ws=True, t=self.pinky_L_pos)
        cmds.xform(self.pinky1_L, ws=True, t=self.pinky1_L_pos)
        cmds.xform(self.pinky2_L, ws=True, t=self.pinky2_L_pos)
        cmds.xform(self.pinkyEnd_L, ws=True, t=self.pinkyEnd_L_pos)
        
        pinky_list.append(self.pinky_L)
        pinky_list.append(self.pinky1_L)
        pinky_list.append(self.pinky2_L)
        pinky_list.append(self.pinkyEnd_L)

        pinky2_L_rot = tools.query_rotation(self.pinky2_L)
        cmds.xform(self.pinkyEnd_L, ro=pinky2_L_rot)
        
        # Thumb
        self.thumb_L = cmds.createNode("joint", n=labels.JNT[13] + labels.SIDE[1] + labels.SUF[0])
        self.thumb1_L = cmds.createNode("joint", n=labels.JNT[14] + labels.SIDE[1] + labels.SUF[0])
        self.thumb2_L = cmds.createNode("joint", n=labels.JNT[15] + labels.SIDE[1] + labels.SUF[0])
        self.thumbEnd_L = cmds.createNode("joint", n=labels.JNT[16] + labels.SIDE[1] + labels.SUF[0])
        
        cmds.xform(self.thumb_L, ws=True, t=self.thumb_L_pos)
        cmds.xform(self.thumb1_L, ws=True, t=self.thumb1_L_pos)
        cmds.xform(self.thumb2_L, ws=True, t=self.thumb2_L_pos)
        cmds.xform(self.thumbEnd_L, ws=True, t=self.thumbEnd_L_pos)
        
        thumb_list.append(self.thumb_L)
        thumb_list.append(self.thumb1_L)
        thumb_list.append(self.thumb2_L)
        thumb_list.append(self.thumbEnd_L)
        
        thumb2_L_rot = tools.query_rotation(self.thumb2_L)
        cmds.xform(self.thumbEnd_L, ro=thumb2_L_rot)        
        
        tools.create_joint_chain("X", "Y", index_list)
        tools.create_joint_chain("X", "Y", middle_list)
        tools.create_joint_chain("X", "Y", ring_list)
        tools.create_joint_chain("X", "Y", pinky_list)
        tools.create_joint_chain("X", "Y", thumb_list)
            
        labels.deformJoint_list.extend(index_list)
        labels.deformJoint_list.extend(middle_list)
        labels.deformJoint_list.extend(ring_list)
        labels.deformJoint_list.extend(pinky_list)
        labels.deformJoint_list.extend(thumb_list)
        
    def create_rightHand(self):
        index_list = []
        middle_list = []
        ring_list = []
        pinky_list = []
        thumb_list = []
        
        # Index Finger
        self.index_R = cmds.createNode("joint", n=labels.JNT[17] + labels.SIDE[2] + labels.SUF[0])
        self.index1_R = cmds.createNode("joint", n=labels.JNT[18] + labels.SIDE[2] + labels.SUF[0])
        self.index2_R = cmds.createNode("joint", n=labels.JNT[19] + labels.SIDE[2] + labels.SUF[0])
        self.indexEnd_R = cmds.createNode("joint", n=labels.JNT[20] + labels.SIDE[2] + labels.SUF[0])
        
        cmds.xform(self.index_R, ws=True, t=self.index_R_pos)
        cmds.xform(self.index1_R, ws=True, t=self.index1_R_pos)
        cmds.xform(self.index2_R, ws=True, t=self.index2_R_pos)
        cmds.xform(self.indexEnd_R, ws=True, t=self.indexEnd_R_pos)
        
        index_list.append(self.index_R)
        index_list.append(self.index1_R)
        index_list.append(self.index2_R)
        index_list.append(self.indexEnd_R)

        index2_R_rot = tools.query_rotation(self.index2_R)
        cmds.xform(self.indexEnd_R, ro=index2_R_rot)
        
        # Middle Finger
        self.middle_R = cmds.createNode("joint", n=labels.JNT[21] + labels.SIDE[2] + labels.SUF[0])
        self.middle1_R = cmds.createNode("joint", n=labels.JNT[22] + labels.SIDE[2] + labels.SUF[0])
        self.middle2_R = cmds.createNode("joint", n=labels.JNT[23] + labels.SIDE[2] + labels.SUF[0])
        self.middleEnd_R = cmds.createNode("joint", n=labels.JNT[24] + labels.SIDE[2] + labels.SUF[0])
        
        cmds.xform(self.middle_R, ws=True, t=self.middle_R_pos)
        cmds.xform(self.middle1_R, ws=True, t=self.middle1_R_pos)
        cmds.xform(self.middle2_R, ws=True, t=self.middle2_R_pos)
        cmds.xform(self.middleEnd_R, ws=True, t=self.middleEnd_R_pos)
        
        middle_list.append(self.middle_R)
        middle_list.append(self.middle1_R)
        middle_list.append(self.middle2_R)
        middle_list.append(self.middleEnd_R)

        middle2_R_rot = tools.query_rotation(self.middle2_R)
        cmds.xform(self.middleEnd_R, ro=middle2_R_rot)
        
        # Ring Finger
        self.ring_R = cmds.createNode("joint", n=labels.JNT[25] + labels.SIDE[2] + labels.SUF[0])
        self.ring1_R = cmds.createNode("joint", n=labels.JNT[26] + labels.SIDE[2] + labels.SUF[0])
        self.ring2_R = cmds.createNode("joint", n=labels.JNT[27] + labels.SIDE[2] + labels.SUF[0])
        self.ringEnd_R = cmds.createNode("joint", n=labels.JNT[28] + labels.SIDE[2] + labels.SUF[0])
        
        cmds.xform(self.ring_R, ws=True, t=self.ring_R_pos)
        cmds.xform(self.ring1_R, ws=True, t=self.ring1_R_pos)
        cmds.xform(self.ring2_R, ws=True, t=self.ring2_R_pos)
        cmds.xform(self.ringEnd_R, ws=True, t=self.ringEnd_R_pos)
        
        ring_list.append(self.ring_R)
        ring_list.append(self.ring1_R)
        ring_list.append(self.ring2_R)
        ring_list.append(self.ringEnd_R)

        ring2_R_rot = tools.query_rotation(self.ring2_R)
        cmds.xform(self.ringEnd_R, ro=ring2_R_rot)
        
        # Pinky Finger
        self.pinky_R = cmds.createNode("joint", n=labels.JNT[29] + labels.SIDE[2] + labels.SUF[0])
        self.pinky1_R = cmds.createNode("joint", n=labels.JNT[30] + labels.SIDE[2] + labels.SUF[0])
        self.pinky2_R = cmds.createNode("joint", n=labels.JNT[31] + labels.SIDE[2] + labels.SUF[0])
        self.pinkyEnd_R = cmds.createNode("joint", n=labels.JNT[32] + labels.SIDE[2] + labels.SUF[0])
        
        cmds.xform(self.pinky_R, ws=True, t=self.pinky_R_pos)
        cmds.xform(self.pinky1_R, ws=True, t=self.pinky1_R_pos)
        cmds.xform(self.pinky2_R, ws=True, t=self.pinky2_R_pos)
        cmds.xform(self.pinkyEnd_R, ws=True, t=self.pinkyEnd_R_pos)
        
        pinky_list.append(self.pinky_R)
        pinky_list.append(self.pinky1_R)
        pinky_list.append(self.pinky2_R)
        pinky_list.append(self.pinkyEnd_R)

        pinky2_R_rot = tools.query_rotation(self.pinky2_R)
        cmds.xform(self.pinkyEnd_R, ro=pinky2_R_rot)
        
        # Thumb
        self.thumb_R = cmds.createNode("joint", n=labels.JNT[13] + labels.SIDE[2] + labels.SUF[0])
        self.thumb1_R = cmds.createNode("joint", n=labels.JNT[14] + labels.SIDE[2] + labels.SUF[0])
        self.thumb2_R = cmds.createNode("joint", n=labels.JNT[15] + labels.SIDE[2] + labels.SUF[0])
        self.thumbEnd_R = cmds.createNode("joint", n=labels.JNT[16] + labels.SIDE[2] + labels.SUF[0])
        
        cmds.xform(self.thumb_R, ws=True, t=self.thumb_R_pos)
        cmds.xform(self.thumb1_R, ws=True, t=self.thumb1_R_pos)
        cmds.xform(self.thumb2_R, ws=True, t=self.thumb2_R_pos)
        cmds.xform(self.thumbEnd_R, ws=True, t=self.thumbEnd_R_pos)
        
        thumb_list.append(self.thumb_R)
        thumb_list.append(self.thumb1_R)
        thumb_list.append(self.thumb2_R)
        thumb_list.append(self.thumbEnd_R)
        
        thumb2_R_rot = tools.query_rotation(self.thumb2_R)
        cmds.xform(self.thumbEnd_R, ro=thumb2_R_rot)        
        
        tools.create_joint_chain("-X", "-Y", index_list)
        tools.create_joint_chain("-X", "-Y", middle_list)
        tools.create_joint_chain("-X", "-Y", ring_list)
        tools.create_joint_chain("-X", "-Y", pinky_list)
        tools.create_joint_chain("-X", "-Y", thumb_list)
        
        labels.deformJoint_list.extend(index_list)
        labels.deformJoint_list.extend(middle_list)
        labels.deformJoint_list.extend(ring_list)
        labels.deformJoint_list.extend(pinky_list)
        labels.deformJoint_list.extend(thumb_list)               
        
    
        