''' FK Guide Element'''

from guides.base.guide import guide

class fk(guide):
    def __init__(self, name, module, submodule=None, side=None, parent=None):
        super().__init__(name, module, submodule, side, parent)
