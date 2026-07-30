'''Metadata Tagging for Maya'''

import maya.cmds as cmds

class tag():
    def __init__(self):
        pass

    def create(self, target, longname, data=None, shortname=None, nicename=None, locked=True):
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

    def destroy(self, target, longname):
        if not target or not longname:
            raise ValueError
        else:
            metadata = f"{target}.{longname}"

        cmds.deleteAttr(metadata)

    



    