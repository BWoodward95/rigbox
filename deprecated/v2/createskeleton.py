import maya.cmds as cmds

from rigbox import labels, root, spine, neck, legs, arms, hands

class AssembleSkeleton():
    
    def __init__(self):
        self.importroot = root.ImportRoot()
        self.importspine = spine.ImportSpine()
        self.importneck = neck.ImportNeck()
        self.importlegs = legs.ImportLegs()
        self.importarms = arms.ImportArms()        
        self.importhands = hands.ImportHands()
        
        self.DeformJoints_Set = None
        
    def import_skeleton(self):
        self.importroot.create_root()
        self.importspine.create_spine()
        self.importneck.create_neck()
        self.importlegs.create_leftLeg()
        self.importlegs.create_rightLeg()
        self.importarms.create_leftArm()
        self.importarms.create_rightArm()
        self.importhands.create_leftHand()
        self.importhands.create_rightHand()
        
    def assemble_skeleton(self):
        cmds.parent(self.importspine.hips, self.importroot.root)
        cmds.parent(self.importneck.neck, self.importspine.spine2)
        cmds.parent(self.importlegs.upperLeg_L, self.importspine.hips)
        cmds.parent(self.importlegs.upperLeg_R, self.importspine.hips)
        cmds.parent(self.importarms.clavicle_L, self.importspine.spine2)
        cmds.parent(self.importarms.clavicle_R, self.importspine.spine2)
        cmds.parent(self.importhands.index_L, self.importhands.middle_L, self.importhands.ring_L, self.importhands.pinky_L, self.importhands.thumb_L, self.importarms.wrist_L)
        cmds.parent(self.importhands.index_R, self.importhands.middle_R, self.importhands.ring_R, self.importhands.pinky_R, self.importhands.thumb_R, self.importarms.wrist_R)
    
    def finalize_skeleton(self):
        cmds.select(d=True)
        
        self.DeformJoints_Set = cmds.sets(n="DeformJoints_Set")
        
    def arm_roll(self):
        self.importarms.apply_roll_jnts()
        self.importarms.setup_roll_sys()

    def leg_roll(self):
        self.importlegs.apply_roll_jnts()
        self.importlegs.setup_roll_sys()
             
    def deform_set(self):        
        print(type(self.DeformJoints_Set))
        for each in labels.deformJoint_list:
            cmds.sets(self.DeformJoints_Set, edit=True, add=each)
        
    def base_skeleton_main(self):
        self.import_skeleton()
        self.assemble_skeleton()
        self.finalize_skeleton()
        # self.deform_set()
        
    def roll_system_main(self):
        self.leg_roll()
        self.arm_roll()
        # self.deform_set()           
         
if __name__ == "__main__":
    skeleton = AssembleSkeleton()
    skeleton.main()