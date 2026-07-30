import maya.cmds as cmds

from rigbox import tools, labels, spine

class ImportNeck():
    
    def __init__(self):
        # Declare variables
        self.neck = None
        self.neck1 = None
        self.head = None
        self.headEnd = None
        
        # Initialize joint positions
        self.neck_pos = (0,145,0)
        self.neck1_pos = (0,155,0)
        self.head_pos = (0,165,0)
        self.headEnd_pos = (0,175,0)       
        
    def create_neck(self):
        neck_list = [] # Carries around neck joint variables
        
        self.neck = cmds.createNode("joint", n=labels.JNT[5] + labels.SIDE[0] + labels.SUF[0])    # Create Joints
        self.neck1 = cmds.createNode("joint", n=labels.JNT[6] + labels.SIDE[0] + labels.SUF[0])   #              |
        self.head = cmds.createNode("joint", n=labels.JNT[7] + labels.SIDE[0] + labels.SUF[0])    #              |
        self.headEnd = cmds.createNode("joint", n=labels.JNT[8] + labels.SIDE[0] + labels.SUF[0]) #              V
        
        cmds.xform(self.neck, ws=True, t=self.neck_pos)       # Place joints
        cmds.xform(self.neck1, ws=True, t=self.neck1_pos)     #             |
        cmds.xform(self.head, ws=True, t=self.head_pos)       #             |
        cmds.xform(self.headEnd, ws=True, t=self.headEnd_pos) #             V
        
        neck_list.append(self.neck)    # Append to list
        neck_list.append(self.neck1)   #               |
        neck_list.append(self.head)    #               |
        neck_list.append(self.headEnd) #               V
        
        tools.create_joint_chain("X", "Y",  neck_list) # Create chain
        
        head_rot = tools.query_rotation(self.head)
        cmds.xform(self.headEnd, ro=head_rot)
        
        labels.deformJoint_list.extend(neck_list) # Add to selection set