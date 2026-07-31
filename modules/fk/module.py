# Rigbox Imports
from metadata.query import query
from modules.base.module import joint

class fk():
    def __init__(self, node):
        self.guide_node = node
        self.data = query.read_guide_data(node)
        self.joint = None

    def build(self):
        jnt_name = f'{self.data["module"]}_jnt'
        jnt = joint(jnt_name, self.data['xform'])
        self.joint = jnt.joint
        return self.joint
