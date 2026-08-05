# Maya Imports
import maya.cmds as cmds

ATTR_GUIDE_NODE = 'guideNode'
ATTR_COMPONENT_TYPE = 'componentType'
ATTR_MODULE = 'module'
ATTR_SUBMODULE = 'subModule'
ATTR_SIDE = 'side'

class query():
    @staticmethod
    def is_guide(node):
        if node is None or not cmds.objExists(node):
            return False
        if not cmds.attributeQuery(ATTR_COMPONENT_TYPE, node=node, exists=True):
            return False
        if not cmds.getAttr(f'{node}.{ATTR_COMPONENT_TYPE}') == 'guide':
            return False
        return True

    @staticmethod
    def find_guides(module=None):
        
        guides = []

        for node in cmds.ls(type='transform'):
            if query.is_guide(node):
                if module is None or cmds.getAttr(f'{node}.{ATTR_MODULE}') == module:
                    guides.append(node)
        return guides

    @staticmethod
    def read_guide_data(node):
        if not query.is_guide(node):
            raise ValueError(f'Node {node} is not a guide')
        
        return {
            'node': node,
            'module': cmds.getAttr(f'{node}.{ATTR_MODULE}'),
            'subModule': cmds.getAttr(f'{node}.{ATTR_SUBMODULE}'),
            'side': cmds.getAttr(f'{node}.{ATTR_SIDE}'),
            'xform': {
                'translation': cmds.xform(node, q=True, ws=True, t=True),
                'rotation': cmds.xform(node, q=True, ws=True, ro=True),
            }
        }

    @staticmethod
    def is_joint(node):
        if node is None or not cmds.objExists(node):
            return False
        if not cmds.attributeQuery(ATTR_COMPONENT_TYPE, node=node, exists=True):
            return False
        
        if not cmds.getAttr(f'{node}.{ATTR_COMPONENT_TYPE}') == 'joint':
            return False
        return True

    @staticmethod
    def find_joints(module=None):
        
        joints = []

        for node in cmds.ls(type='transform'):
            if query.is_joint(node):
                if module is None or cmds.getAttr(f'{node}.{ATTR_MODULE}') == module:
                    joints.append(node)
        return joints

    @staticmethod
    def find_joint_for_guide(guide_node):
        if not query.is_guide(guide_node):
            raise ValueError(f'Node {guide_node} is not a guide')

        module = cmds.getAttr(f'{guide_node}.{ATTR_MODULE}')
        for joint in query.find_joints(module):
            if cmds.getAttr(f'{joint}.{ATTR_GUIDE_NODE}') == guide_node:
                return joint
        return None
    
    @staticmethod
    def is_control(node):
        if node is None or not cmds.objExists(node):
            return False
        if not cmds.attributeQuery(ATTR_COMPONENT_TYPE, node=node, exists=True):
            return False
        
        if not cmds.getAttr(f'{node}.{ATTR_COMPONENT_TYPE}') == 'control':
            return False
        return True

    @staticmethod
    def find_controls(module=None):
        
        controls = []

        for node in cmds.ls(type='transform'):
            if query.is_control(node):
                if module is None or cmds.getAttr(f'{node}.{ATTR_MODULE}') == module:
                    controls.append(node)
        return controls

    @staticmethod
    def find_control_for_guide(guide_node):
        module = cmds.getAttr(f'{guide_node}.{ATTR_MODULE}')
        for control in query.find_controls(module):
            if cmds.getAttr(f'{control}.{ATTR_GUIDE_NODE}') == guide_node:
                return control
        return None