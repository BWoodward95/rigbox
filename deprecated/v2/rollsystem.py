import maya.cmds as cmds

from rigbox import tools, labels, arms, legs

class RollSystem():
    
    def __init__(self):
        self.import_arms = arms.ImportArms()
        self.import_legs = legs.ImportLegs()
    
    def arm_roll(self):
        self.import_arms.apply_roll_jnts()
        self.import_arms.setup_roll_sys()
    
    def leg_roll(self):
        self.import_legs.apply_roll_jnts()
        self.import_legs.setup_roll_sys()