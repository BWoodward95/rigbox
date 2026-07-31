''' Build Module for RigBox AutoRigging System '''
# Standard Imports
import os
import json
import importlib

# Rigbox Imports
import guides
from metadata.query import query

class build():
    def __init__(self):
        self._load_templates()

    def _load_templates(self):
        with open (os.path.join(guides.__path__[0], 'templates.json'), 'r') as f:
            self.template_data = json.load(f)

    def _rig_lookup(self):
        lookup = {}

        for template in self.template_data['templates'].values():
            rig_call = template['tool call']['rig']
            lookup[rig_call['args']['module']] = rig_call
        
        return lookup
    
    def build_joints(self):
        guides_in_scene = query.find_guides()
        rig_lookup = self._rig_lookup()

        if not guides_in_scene:
            print('RigBox: No Guides Found in Scene')
            return

        for guide_node in guides_in_scene:
            module_name = query.read_guide_data(guide_node)['module']
            rig_call = rig_lookup.get(module_name)
            if not rig_call:
                print(f'RigBox: No Rig Call Found for "{module_name}" ({guide_node})')
                continue

            rig_module = importlib.import_module(rig_call['module'])
            rig_cls = getattr(rig_module, rig_call['class'])

            joint = rig_cls(guide_node).build()
            print(f'RigBox: Built {joint} from {guide_node}')