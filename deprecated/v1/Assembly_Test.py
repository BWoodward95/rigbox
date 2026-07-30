import maya.cmds as cmds

from rigbox import root, spine, neck, legs, arms, hands

class AssembleSkeleton():
    
    def __init__(self):
        self.importroot = root.ImportRoot()
        self.importspine = spine.ImportSpine()
        self.importneck = neck.ImportNeck()
        self.importlegs = legs.ImportLegs()
        self.importarms = arms.ImportArms()        
        self.importhands = hands.ImportHands()
        
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
        
    def main(self):
        self.import_skeleton()
        self.assemble_skeleton()
         
if __name__ == "__main__":
    skeleton = AssembleSkeleton()
    skeleton.main()