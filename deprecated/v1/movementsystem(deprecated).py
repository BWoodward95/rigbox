'''
RigBox_MovementSystem Module v1.0
Connect to RigBox_Main Module

by Broderick Woodward-Crackower

To-Do:
    Create IK/FK for Spine
    Create IK/FK for Fingers
    Create Foot roll system for IK legs
    
'''    
import maya.cmds as cmds

class MovementSystem():
    
    def __init__(self):
        pass
    
    def create_hierarchy(self):
        pass

class IKFK_System():

    def __init__(self):    
        self.selection = cmds.ls(sl=True)
        
        self.fk_list = []
        self.ik_list = []
          
    def create_chains(self, jointType, listType):    
        for joint in self.selection:
            joint_pos = cmds.xform(joint, q=True, ws=True, t=True)
            joint_rot = cmds.xform(joint, q=True, ws=True, ro=True)

            new_joint = cmds.createNode("joint", n=f"{jointType}_{joint}")
            cmds.xform(new_joint, t=joint_pos, ro=joint_rot)
            cmds.makeIdentity(new_joint, apply=True, r=True)
            
            listType.append(new_joint)
            
        for i in range(len(listType)-1):
            cmds.parent(listType[i+1],listType[i])
                    
        group = cmds.group(listType[0], n=jointType)

    def link_FK(self):        
        self.create_chains(jointType="FK", listType=self.fk_list)
                    
    def link_IK(self, name, polevector):
        self.create_chains(jointType="IK", listType=self.ik_list)
    
        ikHandle = cmds.ikHandle(sj=self.ik_list[0], ee=self.ik_list[-1], n=f"{name}_ikHandle", solver="ikRPsolver") 
        ik_group = cmds.group(self.ik_list[0], ikHandle, n="IK")
        
        if polevector == True:
            self.pole_vector(name, distance = 0)
            
    def createSwitch(self, name):
        for joint in self.selection:
            switch = cmds.createNode("blendColors", n=f"IKFKSwitch_{name}")
            cmds.setAttr(f"{switch}.blender", 0)
            cmds.connectAttr(f"{switch}.output", f"{joint}.rotate")
            cmds.connectAttr(f"FK_{joint}.rotate", f"{switch}.color1")
            cmds.connectAttr(f"IK_{joint}.rotate", f"{switch}.color2")
            