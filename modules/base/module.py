'''Base Module for RigBox AutoRigging System

Refer to METADATA_SCHEMA.md for more information.
'''

# Maya Imports
import maya.cmds as cmds

# RigBox Imports
from metadata.tag import tag


RIG_GROUP = 'rig_GRP'
JOINT_SUFFIX = '_jnt'
CONTROL_SUFFIX = '_ctrl'

class module():
    def __init__(self, guide_node, metadata: dict):
        self.guide = guide_node
        self.metadata = metadata
        self.xform = self._read_xform()
    
    def build(self):
        raise NotImplementedError('build method not implemented')

    def _tag_node(self, node, component_type):
        tag.create(node, 'componentType', component_type, locked=True)
        tag.create(node, 'guideNode', self.guide, locked=True)
        tag.create(node, 'module', self.metadata['module'], locked=True)

    def _read_xform(self):
        return {
            'translation': cmds.xform(self.guide, query=True, worldSpace=True, translation=True),
            'rotation': cmds.xform(self.guide, query=True, worldSpace=True, rotation=True)
        }
    
    def _create_joint(self, name, xform=None, parent=None):
        joint = cmds.createNode('joint')
        joint = cmds.rename(joint, name)
 
        if not xform:
            xform = self.xform

        cmds.xform(joint, worldSpace=True, translation=xform['translation'], rotation=xform['rotation'])

        if parent:
            cmds.parent(joint, parent)

        self._tag_node(joint, 'joint')

        return joint
    
    def _joint_name(self, part=''):
        base = self.metadata['module']
        if part:
            return f'{base}_{part}{JOINT_SUFFIX}'
        return f'{base}{JOINT_SUFFIX}'

    def _create_control(self, name, xform=None, parent=None):
        control = cmds.circle(constructionHistory=False)[0]
        control = cmds.rename(control, name)
        
        if not xform:
            xform = self.xform

        cmds.xform(control, worldSpace=True, translation=xform['translation'], rotation=xform['rotation'])

        if parent:
            cmds.parent(control, parent)

        self._tag_node(control, 'control')

        return control
        
    def _control_name(self, part=''):
        base = self.metadata['module']
        if part:
            return f'{base}_{part}{CONTROL_SUFFIX}'
        return f'{base}{CONTROL_SUFFIX}'

    def _rig_group(self):
        if not cmds.objExists(RIG_GROUP):
            cmds.group(empty=True, name=RIG_GROUP)
        return RIG_GROUP

    def build_joints(self):
        raise NotImplementedError('RigBox: Joints are not implemented yet')

    def build_controls(self):
        raise NotImplementedError('RigBox: Controls are not implemented yet')

