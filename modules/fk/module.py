''' FK Module '''

# Maya Imports
import maya.cmds as cmds

# Rigbox Imports
from metadata.query import query
from modules.base.module import module

class fk(module):
    def __init__(self, guide_node):
        data = query.read_guide_data(guide_node)
        super().__init__(guide_node, data)
        self.joint = None
        self.control = None

    def build_joints(self):
        self.joint = self._create_joint(self._joint_name())
        return self.joint

    def build_controls(self):
        self.control = query.find_control_for_guide(self.guide)
        if self.control:
            print(f'RigBox: Control Found for "{self.guide}"')
            return self.control
        
        self.joint = query.find_joint_for_guide(self.guide)
        if not self.joint:
            print(f'RigBox: No Joint Found for "{self.guide}"')
            return
        
        self.control = self._create_control(self._control_name(), parent=self._rig_group())
        cmds.parentConstraint(self.control, self.joint, mo=True)

        return self.control