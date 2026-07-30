''' FK Guide Element'''

from guides.base.guide import guide

class fk(guide):
    def __init__(self, name, module, submodule=None, side=None):
        name = 'fk'
        module = 'fk'
        super().__init__(name, module, submodule, side)

        return self.guide