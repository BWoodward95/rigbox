''' Build Controls Button Widget '''

# Qt Imports
from PySide6 import QtWidgets, QtCore, QtGui

# Rigbox Imports
from modules.build import build

class widget(QtWidgets.QWidget):
    def __init__(self, on_complete=None):
        super().__init__()
        self.on_complete = on_complete
        self.builder = build()

        self.create_widgets()
        self.create_layout()
        self.create_connections()
    
    def create_widgets(self):
        self.build_controls_button = QtWidgets.QPushButton('Build Controls')

    def create_layout(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.build_controls_button)
        self.setLayout(self.layout)

    def create_connections(self):
        self.build_controls_button.clicked.connect(self.on_build_controls_button_clicked)

    def on_build_controls_button_clicked(self):
        self.builder.build_controls()

        if self.on_complete:
            self.on_complete()