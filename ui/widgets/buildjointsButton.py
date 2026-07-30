''' Build Joints Button Widget '''

# Qt Imports
from PySide6 import QtWidgets, QtCore, QtGui

class widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.create_widgets()
        self.create_connections()

    def create_widgets(self):
        self.build_joints_button = QtWidgets.QPushButton('Build Joints')

    def create_connections(self):
        self.build_joints_button.clicked.connect(self.on_build_joints_button_clicked)

    def on_build_joints_button_clicked(self):
        print('Build Joints Button Clicked')
