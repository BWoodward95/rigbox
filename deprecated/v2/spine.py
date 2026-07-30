import maya.cmds as cmds

from rigbox import tools, labels, root

class ImportSpine():
    
    def __init__(self):
        # Declare variables
        self.hips = None
        self.spine = None
        self.spine1 = None
        self.spine2 = None
        
        # Initialize joint positions
        self.hips_pos = (0,100,0)
        self.spine_pos = (0,107,0)
        self.spine1_pos = (0,120,0)
        self.spine2_pos = (0,132,0)
        
    def create_spine(self):
        spine_list = [] # Carries around spine joint variables
        
        self.hips = cmds.createNode("joint", n=labels.JNT[1] + labels.SIDE[0] + labels.SUF[0])   # Create Joints
        self.spine = cmds.createNode("joint", n=labels.JNT[2] + labels.SIDE[0] + labels.SUF[0])  #              |
        self.spine1 = cmds.createNode("joint", n=labels.JNT[3] + labels.SIDE[0] + labels.SUF[0]) #              |
        self.spine2 = cmds.createNode("joint", n=labels.JNT[4] + labels.SIDE[0] + labels.SUF[0]) #              V
       
        cmds.xform(self.hips, ws=True, t=self.hips_pos)     # Place Joints
        cmds.xform(self.spine, ws=True, t=self.spine_pos)   #             |
        cmds.xform(self.spine1, ws=True, t=self.spine1_pos) #             |
        cmds.xform(self.spine2, ws=True, t=self.spine2_pos) #             V
        
        spine_list.append(self.hips)   # Append to list
        spine_list.append(self.spine)  #               |
        spine_list.append(self.spine1) #               |
        spine_list.append(self.spine2) #               V
        
        tools.create_joint_chain("X", "Y", spine_list) # Create chain
        
        spine1_rot = tools.query_rotation(self.spine1)
        cmds.xform(self.spine2, ro=spine1_rot)
        
        labels.deformJoint_list.extend(spine_list) # Add to selection set