# Maya Imports
from email.policy import default
import maya.cmds as cmds

ATTR_GUIDE_NODE = 'guideNode'
ATTR_COMPONENT_TYPE = 'componentType'
ATTR_MODULE = 'module'
ATTR_SUBMODULE = 'subModule'
ATTR_SIDE = 'side'
ATTR_DEFORM = 'deform'
ATTR_KINEMATICS = 'kinematics'

SIDE_ENUM = 'none:center:left:right'
KINEMATICS_ENUM = 'none:IK:FK:IKFK'

#Side Labels
SIDE_NONE = 'none'
SIDE_CENTER = 'center'
SIDE_LEFT = 'left'
SIDE_RIGHT = 'right'

# Kinematics Labels
KINEMATICS_NONE = 'none'
KINEMATICS_IK = 'IK'
KINEMATICS_FK = 'FK'
KINEMATICS_IKFK = 'IKFK'

class query():
    '''Utility class for querying Maya nodes and attributes.'''
    @staticmethod
    def read_node_data(node):
        metadata = {
            'node': node,
            'componentType': query.read_string(node, ATTR_COMPONENT_TYPE),
            'module': query.read_string(node, ATTR_MODULE),
            'subModule': query.read_string(node, ATTR_SUBMODULE),
            'side': query.read_enum(node, ATTR_SIDE),
            'guideNode': query.read_string(node, ATTR_GUIDE_NODE),
            'deform': query.read_bool(node, ATTR_DEFORM),
            'kinematics': query.read_enum(node, ATTR_KINEMATICS),
        }

        for key, value in metadata.items():
            if cmds.attributeQuery(key, node=node, exists=True):
                metadata[key] = value
            
        return metadata

    @staticmethod
    def read_string(node, attr):
        if not cmds.attributeQuery(attr, node=node, exists=True):
            return None
        return cmds.getAttr(f'{node}.{attr}')

    @staticmethod
    def read_enum(node, attr):
        if not cmds.objExists(node):
            raise ValueError(f'Node {node} does not exist')
        if not cmds.attributeQuery(attr, node=node, exists=True):
            raise ValueError(f'Node {node} has no attribute {attr}')
        return cmds.getAttr(f'{node}.{attr}', asString=True)
    
    @staticmethod
    def read_bool(node, attr, default=False):
        if not cmds.attributeQuery(attr, node=node, exists=True):
            return default
        return cmds.getAttr(f'{node}.{attr}')

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
        
        # TODO: Legacy support for old side attribute, delete later.
        if cmds.attributeQuery(ATTR_SIDE, node=node, attributeType=True) == 'enum':
            side = query.read_enum(node, ATTR_SIDE)
        else:
            side = cmds.getAttr(f'{node}.{ATTR_SIDE}')

        return {
            'node': node,
            'module': cmds.getAttr(f'{node}.{ATTR_MODULE}'),
            'subModule': cmds.getAttr(f'{node}.{ATTR_SUBMODULE}'),
            'side': side,
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
    def find_deform_joints(module=None):
        deform_joints = []
        for joint in query.find_joints(module):
            if not cmds.attributeQuery(ATTR_DEFORM, node=joint, exists=True):
                continue
            if cmds.getAttr(f'{joint}.{ATTR_DEFORM}') == True:
                deform_joints.append(joint)
        return deform_joints

    @staticmethod
    def find_driver_joints(module=None):
        driver_joints = []
        for joint in query.find_joints(module):
            if not cmds.attributeQuery(ATTR_DEFORM, node=joint, exists=True):
                continue
            if cmds.getAttr(f'{joint}.{ATTR_DEFORM}') == False:
                driver_joints.append(joint)
        return driver_joints

    @staticmethod
    def _joint_deform_value(joint):
        if not cmds.attributeQuery(ATTR_DEFORM, node=joint, exists=True):
            return None
        return cmds.getAttr(f'{joint}.{ATTR_DEFORM}')

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
        if not query.is_guide(guide_node):
            raise ValueError(f'Node {guide_node} is not a guide')

        module = cmds.getAttr(f'{guide_node}.{ATTR_MODULE}')
        for control in query.find_controls(module):
            if cmds.getAttr(f'{control}.{ATTR_GUIDE_NODE}') == guide_node:
                return control
        return None
    
    @staticmethod
    def is_effector(node):
        if node is None or not cmds.objExists(node):
            return False
        if not cmds.attributeQuery(ATTR_COMPONENT_TYPE, node=node, exists=True):
            return False
        if not cmds.getAttr(f'{node}.{ATTR_COMPONENT_TYPE}') == 'effector':
            return False
        return True
    
    @staticmethod
    def find_effectors(module=None):
        effectors = []
        for node in cmds.ls(type='transform'):
            if query.is_effector(node):
                if module is None or cmds.getAttr(f'{node}.{ATTR_MODULE}') == module:
                    effectors.append(node)
        return effectors