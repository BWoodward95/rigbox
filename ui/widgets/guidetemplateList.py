''' Guide Template List Widget '''
# Standard Library Imports
import importlib
import json
import os

# Maya Imports
import maya.cmds as cmds

# Qt Imports
from PySide6 import QtWidgets, QtCore, QtGui

# Rigbox Imports
import guides 
from metadata.query import query

class widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

            # Load the template data
        with open(os.path.join(guides.__path__[0], 'templates.json'), 'r') as f:
            self.template_data = json.load(f)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):

        self.title_label = QtWidgets.QLabel('Guide Templates')
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.list_view = QtWidgets.QListWidget()
        self.list_view.addItems(self.template_data['templates'].keys())
    
    def create_layout(self):
        frame = QtWidgets.QFrame()
        frame.setFrameStyle(QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Sunken)
        frame.setLineWidth(1)

        frame_layout = QtWidgets.QVBoxLayout(frame)
        frame_layout.addWidget(self.title_label)
        frame_layout.addWidget(self.list_view)
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(frame)

    def create_connections(self):
        self.list_view.itemDoubleClicked.connect(self.on_item_clicked)

    def on_item_clicked(self, item):
        # Get the item key and template data
        item_key = item.text()
        template = self.template_data['templates'][item_key]
        tool_call_path = template['tool call']['guide']

        # Import the guide module and class
        if isinstance(tool_call_path, str):
            guide_module = importlib.import_module(tool_call_path)
            guide_cls = getattr(guide_module, item_key)
            call_args = {}
        else:
            guide_module = importlib.import_module(tool_call_path['module'])
            guide_cls = getattr(guide_module, tool_call_path['class'])
            call_args = tool_call_path.get('args', {})

        parent_guide = None
        for node in cmds.ls(sl=True, transforms=True) or []:
            if query.is_guide(node):
                parent_guide = node
                break

        call_args = tool_call_path.get('args', {})
        call_args['parent'] = parent_guide
        guide_cls(**call_args)

