'''Base Module for RigBox AutoRigging System'''

# Maya Imports
import maya.cmds as cmds

class joint():
    def __init__(self, name, xform, parent=None):
        self.joint = cmds.createNode('joint')
        self.joint = cmds.rename(self.joint, name)

        cmds.xform(self.joint, worldSpace=True, translation=xform['translation'], rotation=xform['rotation'])

        if parent:
            cmds.parent(self.joint, parent)

class control():
    def __init__(self, name, xform, parent=None):
        self.control = cmds.circle(constructionHistory=False)[0]
        self.control = cmds.rename(self.control, name)

        cmds.xform(self.control, worldSpace=True, translation=xform['translation'], rotation=xform['rotation'])