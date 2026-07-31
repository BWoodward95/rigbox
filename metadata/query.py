# Maya Imports
import maya.cmds as cmds

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

