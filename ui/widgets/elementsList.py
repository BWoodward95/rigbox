''' Elements List Widget '''

# Maya Imports
import maya.cmds as cmds

# Qt Imports
from PySide6 import QtWidgets, QtCore, QtGui

# Rigbox Imports
from metadata.query import query, ATTR_GUIDE_NODE

ROLE_NODE = QtCore.Qt.ItemDataRole.UserRole
ROLE_KIND = QtCore.Qt.ItemDataRole.UserRole + 1

class widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self._block_item_changed = False
        self._block_tree_move = False

        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.refresh()

    def create_widgets(self):
        self.title_label = QtWidgets.QLabel('Elements')
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.tree_view = QtWidgets.QTreeWidget()
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.InternalMove)
        self.tree_view.setDefaultDropAction(QtCore.Qt.DropAction.MoveAction)

        self.refresh_button = QtWidgets.QPushButton('Refresh')

    def create_layout(self):
        frame = QtWidgets.QFrame()
        frame.setFrameStyle(QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Sunken)
        frame.setLineWidth(1)

        frame_layout = QtWidgets.QVBoxLayout(frame)
        frame_layout.addWidget(self.title_label)
        frame_layout.addWidget(self.tree_view)
        frame_layout.addWidget(self.refresh_button)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(frame)

    def create_connections(self):
        self.tree_view.itemSelectionChanged.connect(self._on_tree_selection_changed)
        self.tree_view.itemChanged.connect(self._on_item_changed)
        self.tree_view.model().rowsMoved.connect(self._on_rows_moved)

        self.refresh_button.clicked.connect(self.on_refresh_button_clicked)
        
    def refresh(self):
        self._block_item_changed = True
        self._block_tree_move = True
        self.tree_view.blockSignals(True)
        self.tree_view.clear()

        guides = query.find_guides()
        guide_set = set(guides)
        item_map = {}

        for guide in guides:
            item = QtWidgets.QTreeWidgetItem([guide])
            item.setData(0, ROLE_NODE, guide)
            item.setData(0, ROLE_KIND, 'guide')
            item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable | QtCore.Qt.ItemFlag.ItemIsDragEnabled | QtCore.Qt.ItemFlag.ItemIsDropEnabled)
            item_map[guide] = item

            joint = query.find_joint_for_guide(guide)
            if joint:
                joint_item = QtWidgets.QTreeWidgetItem([joint])
                joint_item.setData(0, ROLE_NODE, joint)
                joint_item.setData(0, ROLE_KIND, 'joint')
                joint_item.setFlags(joint_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable & ~QtCore.Qt.ItemFlag.ItemIsDragEnabled & ~QtCore.Qt.ItemFlag.ItemIsDropEnabled)
                item.addChild(joint_item)
            
            control = query.find_control_for_guide(guide)
            if control:
                control_item = QtWidgets.QTreeWidgetItem([control])
                control_item.setData(0, ROLE_NODE, control)
                control_item.setData(0, ROLE_KIND, 'control')
                control_item.setFlags(control_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable & ~QtCore.Qt.ItemFlag.ItemIsDragEnabled & ~QtCore.Qt.ItemFlag.ItemIsDropEnabled)
                item.addChild(control_item)
        
        roots = []
        for guide in guides:
            parents = cmds.listRelatives(guide, parent=True) or []
            parent_guide = next((p for p in parents if p in guide_set), None)
            if parent_guide:
                item_map[parent_guide].addChild(item_map[guide])
            else:
                roots.append(item_map[guide])
        
        for root in roots:
            self.tree_view.addTopLevelItem(root)

        self.tree_view.expandAll()
        self.tree_view.blockSignals(False)

        self._block_item_changed = False
        self._block_tree_move = False

    def on_refresh_button_clicked(self):
        self.refresh()

    def _on_tree_selection_changed(self):
        items = self.tree_view.selectedItems()
        if not items:
            return
        node = items[0].data(0, ROLE_NODE)
        if node and cmds.objExists(node):
            cmds.select(node, replace=True)

    def _on_item_changed(self, item, column):
        if self._block_item_changed:
            return
        if item.data(0, ROLE_KIND) != 'guide':
            return
        
        old_name = item.data(0, ROLE_NODE)
        new_name = item.text(0).strip()

        if not old_name or not new_name or old_name == new_name:
            return

        if not cmds.objExists(old_name):
            return

        actual_name = cmds.rename(old_name, new_name)

        self._block_item_changed = True
        item.setData(0, ROLE_NODE, actual_name)
        item.setText(0, actual_name)
        self._block_item_changed = False

        self._update_guide_node_refs(old_name, actual_name)

    def _update_guide_node_refs(self, old_name, new_name):
        for node in query.find_joints() + query.find_controls():
            attr = f'{node}.{ATTR_GUIDE_NODE}'
            if not cmds.attributeQuery(ATTR_GUIDE_NODE, node=node, exists=True):
                continue
            if cmds.getAttr(attr) != old_name:
                continue

            cmds.setAttr(attr, lock=False)
            cmds.setAttr(attr, new_name, type='string')
            cmds.setAttr(attr, lock=True)
        
    def _on_rows_moved(self, parent, start, end, destination, row):
        if self._block_tree_move:
            return
        self._sync_guides_from_tree()
    
    def _sync_guides_from_tree(self):
        for i in range(self.tree_view.topLevelItemCount()):
            self._sync_guide_item(self.tree_view.topLevelItem(i), parent_guide=None)

    def _sync_guide_item(self, item, parent_guide):
        if item is None or item.data(0, ROLE_KIND) != 'guide':
            return
        
        guide = item.data(0, ROLE_NODE)
        if not guide or not cmds.objExists(guide):
            return
        
        self._parent_guide_in_maya(guide, parent_guide)

        for i in range(item.childCount()):
            child = item.child(i)
            if child.data(0, ROLE_KIND) == 'guide':
                self._sync_guide_item(child, guide)
    
    def _parent_guide_in_maya(self, guide, parent_guide):
        if parent_guide:
            if not query.is_guide(parent_guide):
                print(f'RigBox: Invalid parent "{parent_guide}" - not a guide')
                self.refresh()
                return
            if self._would_create_cycle(guide, parent_guide):
                print(f'RigBox: Cannot parent "{guide}" under "{parent_guide}" - (cycle)')
                self.refresh()
                return
            cmds.parent(guide, parent_guide)
        else:
            cmds.parent(guide, world=True)

    def _would_create_cycle(self, guide, new_parent):
        current = new_parent
        while current:
            if current == guide:
                return True
            parents = cmds.listRelatives(current, parent=True) or []
            current = next((p for p in parents if query.is_guide(p)), None)
        return False