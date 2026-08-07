'''Metadata Tagging for Maya'''

# Maya Imports
import maya.cmds as cmds

class tag():
    @staticmethod
    def create(target, longname, data=None, attr_type='string', enum_names=None, shortname=None, nicename=None, locked=True):
        '''Create a string attribute with metadata.'''
        if not target or not longname:
            raise ValueError
        else:
            metadata = f"{target}.{longname}"

        if not shortname:
            shortname = longname

        if data is None:
            if attr_type == 'string':
                data = ''
            elif attr_type == 'bool':
                data = False
            else:
                data = 0

        if cmds.attributeQuery(longname, node=target, exists=True):
            cmds.setAttr(metadata, lock=False)
            if enum_names:
                labels = enum_names.split(':')
                if isinstance(data, str):
                    data = labels.index(data)
            if not nicename:
                if attr_type == 'string':
                    cmds.addAttr(target, ln=longname, sn=shortname, dataType='string')
                elif attr_type == 'enum':
                    cmds.addAttr(target, ln=longname, sn=shortname, dataType='enum', enumNames=enum_names)
                else:
                    cmds.addAttr(target, ln=longname, sn=shortname, dataType=attr_type)
            else:
                if attr_type == 'string':
                    cmds.addAttr(target, ln=longname, sn=shortname, nn=nicename, dataType='string')
                elif attr_type == 'enum':
                    cmds.addAttr(target, ln=longname, sn=shortname, nn=nicename, dataType='enum', enumNames=enum_names)
                else:
                    cmds.addAttr(target, ln=longname, sn=shortname, nn=nicename, dataType=attr_type)

            tag._set_attr_value(target, longname, data, attr_type)

            if locked:
                cmds.setAttr(metadata, lock=locked)

    @staticmethod
    def _set_attr_value(target, longname, data, attr_type):
        target_attr = f"{target}.{longname}"

        if attr_type == 'string':
            cmds.setAttr(target_attr, data, type='string')

        elif attr_type == 'enum':
            cmds.setAttr(target_attr, data)
        
        else:
            cmds.setAttr(target_attr, data)
        

    @staticmethod
    def destroy(target, longname):
        '''Destroy a string attribute with metadata.'''
        if not target or not longname:
            raise ValueError
        else:
            metadata = f"{target}.{longname}"

        cmds.deleteAttr(metadata)

    



    