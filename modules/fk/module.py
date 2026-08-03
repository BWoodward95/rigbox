# Rigbox Imports
from metadata.query import query
from modules.base.module import module

class fk(module):
    def __init__(self, guide_node):
        data = query.read_guide_data(guide_node)
        super().__init__(guide_node, data)
        self.joint = None

    def build_joints(self):
        self.joint = self._create_joint(self._joint_name())
        return self.joint

    def build_controls(self):
        self.joint = query.find_joint_for_guide(self.guide_node)
        if not self.joint:
            print(f'RigBox: No Joint Found for "{self.guide_node}"')
            return
        
        self.control = self._create_control(self._control_name(), parent=self._rig_group())
        cmds.parentConstraint(self.control, self.joint, mo=True)
        cmds.orientConstraint(self.control, self.joint, mo=True)

        return self.control