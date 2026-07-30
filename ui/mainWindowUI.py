'''Dockable RigBox main window.'''

# Maya Imports
import maya.cmds as cmds
from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

# Qt Imports
from PySide6 import QtCore, QtWidgets
from shiboken6 import wrapInstance

# Rigbox Imports
from ui.widgets import guidetemplateList, buildjointsButton

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class mainWindowUI(MayaQWidgetDockableMixin, QtWidgets.QWidget):
    OBJECT_NAME = 'rigboxMainWindow'
    WINDOW_TITLE = 'RigBox'
    WORKSPACE_CONTROL = f'{OBJECT_NAME}WorkspaceControl'

    _instance = None

    def __init__(self, parent=None):
        super().__init__(parent=parent or maya_main_window())

        self.setObjectName(self.OBJECT_NAME)
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumWidth(280)

        self.create_widgets()
        self.create_layout()
        # self.create_connections()

    def create_widgets(self):
        self.title_label = QtWidgets.QLabel(self.WINDOW_TITLE)
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.guide_list_widget = guidetemplateList.widget()
        self.build_joints_button = buildjointsButton.widget()

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(6)

        main_layout.addWidget(self.title_label)
        main_layout.addStretch()
        main_layout.addWidget(self.guide_list_widget)
        main_layout.addWidget(self.build_joints_button)

    @classmethod
    def show_ui(cls, dockable=True):
        cls.close_ui()

        cls._instance = cls()
        cls._instance.show(dockable=dockable)
        return cls._instance

    @classmethod
    def close_ui(cls):
        if cls._instance is not None:
            try:
                cls._instance.close()
                cls._instance.deleteLater()
            except RuntimeError:
                pass
            cls._instance = None

        if cmds.workspaceControl(cls.WORKSPACE_CONTROL, exists=True):
            cmds.deleteUI(cls.WORKSPACE_CONTROL, control=True)


def show(dockable=True):
    return mainWindowUI.show_ui(dockable=dockable)


if __name__ == '__main__':
    show()
