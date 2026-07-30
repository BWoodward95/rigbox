''' Base Guide Element'''

import maya.cmds as cmds

from metadata.tag import tag

class guide():
    def __init__(self, name, module=None, submodule=None, side=None):
        self.name = f'{name}_guide'
        self.module = module
        self.submodule = submodule
        self.side = side

        self.create()

    def create(self):    
        guide = cmds.createNode('locator')
        guide_transform = cmds.listRelatives(guide, parent=True)[0]

        tag.create(guide_transform, 'componentType', 'guide', locked=True)
        tag.create(guide_transform, 'module', self.module, locked=True)
        tag.create(guide_transform, 'subModule', self.submodule, locked=True)
        tag.create(guide_transform, 'side', self.side, locked=True)
        
        cmds.rename(guide_transform, self.name)
        
        self.guide = guide_transform
        return guide_transform