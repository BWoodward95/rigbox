import maya.cmds as cmds

from rigbox import tools, labels, spine

class ImportLegs():
    
    def __init__(self):
        # Declare variables
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
        
        self.upperLeg_roll_L = None
        self.lowerLeg_roll_L = None
        
        self.upperLeg_roll_R = None
        self.lowerLeg_roll_R = None
        
        self.upperLeg_roll_L_sys = None
        self.lowerLeg_roll_L_sys = None
        
        self.upperLeg_roll_R_sys = None
        self.lowerLeg_roll_R_sys = None
        
        # Initialize joint positions
        self.upperLeg_L_pos = (9,94,0)
        self.lowerLeg_L_pos = (9,49,0)
        self.foot_L_pos = (9,8,0)
        self.toe_L_pos = (9,2,13)
        self.toeEnd_L_pos = (9,2,20)
        
        self.upperLeg_R_pos = (-9,94,0)
        self.lowerLeg_R_pos = (-9,49,0)
        self.foot_R_pos = (-9,8,0)
        self.toe_R_pos = (-9,2,13)
        self.toeEnd_R_pos = (-9,2,20)
                
    def create_leftLeg(self):
        leg_list = []
                
        self.upperLeg_L = cmds.createNode("joint", n=labels.JNT[33] + labels.SIDE[1] + labels.SUF[0]) # Create Joints
        self.lowerLeg_L = cmds.createNode("joint", n=labels.JNT[34] + labels.SIDE[1] + labels.SUF[0]) #              |
        self.foot_L = cmds.createNode("joint", n=labels.JNT[35] + labels.SIDE[1] + labels.SUF[0])     #              |
        self.toe_L = cmds.createNode("joint", n=labels.JNT[36] + labels.SIDE[1] + labels.SUF[0])      #              |
        self.toeEnd_L = cmds.createNode("joint", n=labels.JNT[37] + labels.SIDE[1] + labels.SUF[0])   #              V
    
        cmds.xform(self.upperLeg_L, ws=True, t=self.upperLeg_L_pos) # Place Joints
        cmds.xform(self.lowerLeg_L, ws=True, t=self.lowerLeg_L_pos) #             |
        cmds.xform(self.foot_L, ws=True, t=self.foot_L_pos)         #             |
        cmds.xform(self.toe_L, ws=True, t=self.toe_L_pos)           #             | 
        cmds.xform(self.toeEnd_L, ws=True, t=self.toeEnd_L_pos)     #             V
        
        leg_list.append(self.upperLeg_L) # Append to list
        leg_list.append(self.lowerLeg_L) #               |
        leg_list.append(self.foot_L)     #               | 
        leg_list.append(self.toe_L)      #               |
        leg_list.append(self.toeEnd_L)   #               V
        
        tools.create_joint_chain("X", "Z", leg_list) # Create chain
        
        toe_L_rot = tools.query_rotation(self.toe_L)
        cmds.xform(self.toeEnd_L, ro=toe_L_rot)
                        
        labels.deformJoint_list.extend(leg_list) # Add to selection set
        
    def create_rightLeg(self):
        leg_list = []
                
        self.upperLeg_R = cmds.createNode("joint", n=labels.JNT[33] + labels.SIDE[2] + labels.SUF[0])
        self.lowerLeg_R = cmds.createNode("joint", n=labels.JNT[34] + labels.SIDE[2] + labels.SUF[0])
        self.foot_R = cmds.createNode("joint", n=labels.JNT[35] + labels.SIDE[2] + labels.SUF[0])
        self.toe_R = cmds.createNode("joint", n=labels.JNT[36] + labels.SIDE[2] + labels.SUF[0])
        self.toeEnd_R = cmds.createNode("joint", n=labels.JNT[37] + labels.SIDE[2] + labels.SUF[0])
    
        cmds.xform(self.upperLeg_R, ws=True, t=self.upperLeg_R_pos)
        cmds.xform(self.lowerLeg_R, ws=True, t=self.lowerLeg_R_pos)
        cmds.xform(self.foot_R, ws=True, t=self.foot_R_pos)
        cmds.xform(self.toe_R, ws=True, t=self.toe_R_pos)
        cmds.xform(self.toeEnd_R, ws=True, t=self.toeEnd_R_pos)
        
        leg_list.append(self.upperLeg_R)
        leg_list.append(self.lowerLeg_R)
        leg_list.append(self.foot_R)
        leg_list.append(self.toe_R)
        leg_list.append(self.toeEnd_R)
            
        tools.create_joint_chain("-X", "-Z", leg_list)

        toe_R_rot = tools.query_rotation(self.toe_R)
        cmds.xform(self.toeEnd_R, ro=toe_R_rot)
                        
        labels.deformJoint_list.extend(leg_list)          
        
    def apply_roll_jnts(self):
        self.upperLeg_roll_L = tools.create_roll_jnt(f"{labels.JNT[33]}_roll{labels.SIDE[1]}{labels.SUF[0]}", self.upperLeg_L, self.lowerLeg_L)
        labels.deformJoint_list.append(self.upperLeg_roll_L)
             
        self.lowerLeg_roll_L = tools.create_roll_jnt(f"{labels.JNT[34]}_roll{labels.SIDE[1]}{labels.SUF[0]}", self.lowerLeg_L, self.foot_L)
        labels.deformJoint_list.append(self.lowerLeg_roll_L)
        
        self.upperLeg_roll_R = tools.create_roll_jnt(f"{labels.JNT[33]}_roll{labels.SIDE[2]}{labels.SUF[0]}", self.upperLeg_R, self.lowerLeg_R)
        labels.deformJoint_list.append(self.upperLeg_roll_R)
             
        self.lowerLeg_roll_R = tools.create_roll_jnt(f"{labels.JNT[34]}_roll{labels.SIDE[2]}{labels.SUF[0]}", self.lowerLeg_R, self.foot_R)
        labels.deformJoint_list.append(self.lowerLeg_roll_R)
            
    def setup_roll_sys(self):    
        self.upperLeg_roll_L_sys = tools.create_roll_sys(f"{labels.JNT[33]}{labels.SIDE[1]}{labels.SUF[1]}", self.upperLeg_L, self.upperLeg_roll_L, "X", 0.5)
        labels.node_list.append(self.upperLeg_roll_L_sys)
        
        self.lowerLeg_roll_L_sys = tools.create_roll_sys(f"{labels.JNT[34]}{labels.SIDE[1]}{labels.SUF[1]}", self.lowerLeg_L, self.lowerLeg_roll_L, "X", 0.5)      
        labels.node_list.append(self.lowerLeg_roll_L_sys)
        
        self.upperLeg_roll_R_sys = tools.create_roll_sys(f"{labels.JNT[33]}{labels.SIDE[2]}{labels.SUF[1]}", self.upperLeg_R, self.upperLeg_roll_R, "X", 0.5)
        labels.node_list.append(self.upperLeg_roll_R_sys)
        
        self.lowerLeg_roll_R_sys = tools.create_roll_sys(f"{labels.JNT[34]}{labels.SIDE[2]}{labels.SUF[1]}", self.lowerLeg_R, self.lowerLeg_roll_R, "X", 0.5)      
        labels.node_list.append(self.lowerLeg_roll_R_sys)          