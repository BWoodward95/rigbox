''' Guide Template List Widget '''
# Standard Library Imports
import importlib
import json
import os

# Qt Imports
from PySide6 import QtWidgets, QtCore, QtGui

# Rigbox Imports
import guides 

class widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        with open(os.path.join(guides.__path__[0], 'templates.json'), 'r') as f:
            self.template_data = json.load(f)

        self.list_view = QtWidgets.QListWidget()
        self.list_view.addItems(self.template_data['templates'].keys())
    
    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.list_view)

    def create_connections(self):
        self.list_view.itemDoubleClicked.connect(self.on_item_clicked)

    def on_item_clicked(self, item):
        template = self.template_data['templates'][item.text()]
        tool_call = importlib.import_module(template['tool call'])
        tool_call.create()

