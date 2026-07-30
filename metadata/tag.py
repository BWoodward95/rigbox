'''Metadata Tagging for Maya'''

# Maya Imports
import maya.cmds as cmds

class tag():
    @staticmethod
    def create(target, longname, data=None, shortname=None, nicename=None, locked=True):
        '''Create a string attribute with metadata.'''
        if not target or not longname:
            raise ValueError
        else:
            metadata = f"{target}.{longname}"

        if not shortname:
            shortname = longname
        if not data:
            data = ''

        if not nicename:
            cmds.addAttr(target, ln=longname, sn=shortname, dataType="string")
        else:
            cmds.addAttr(target, ln=longname, sn=shortname, nn=nicename, dataType="string")

        cmds.setAttr(metadata, data, type="string")

        cmds.setAttr(metadata, lock=locked)

    @staticmethod
    def destroy(target, longname):
        '''Destroy a string attribute with metadata.'''
        if not target or not longname:
            raise ValueError
        else:
            metadata = f"{target}.{longname}"

        cmds.deleteAttr(metadata)

    



    