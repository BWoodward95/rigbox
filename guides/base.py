''' Base Guide Element'''

import maya.cmds as cmds

from metadata.tag import tag

class GuideElement():
    def __init__(self, name):
        self.name = f'{name}_guide'

        self.create()

    def create(self):    
        guide = cmds.createNode('locator')
        guide_transform = cmds.listRelatives(guide, parent=True)[0]

        tag.create(self, guide, 'componentType', 'guide', locked=False)
        
        cmds.rename(guide_transform, self.name)
        
        return guide

if __name__ == '__main__':
    guide = GuideElement('spine')