''' Build Joints Button Widget '''

# Qt Imports
from PySide6 import QtWidgets, QtCore, QtGui

# Rigbox Imports
from modules.build import build

class widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.builder = build()

        self.create_widgets()   
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.build_joints_button = QtWidgets.QPushButton('Build Joints')

    def create_layout(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.build_joints_button)
        self.setLayout(self.layout)

    def create_connections(self):
        self.build_joints_button.clicked.connect(self.on_build_joints_button_clicked)

    def on_build_joints_button_clicked(self):
        self.builder.build_joints()