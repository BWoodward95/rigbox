# Phase 4a — Elements Tree (display + selection + refresh)

Supplement to [`PHASE_4.md`](PHASE_4.md). Scope: **read-only** tree — no rename, no drag-drop (that's 4b/4c).

---

## Goal

Add an **Elements** panel that:

1. Shows guide hierarchy (Maya parenting)
2. Shows joint + control under each guide
3. Selects the Maya node when you click a tree item
4. Refreshes manually and after spawn / build actions

---

## What you are NOT building in 4a

- Guide rename
- Drag-drop reparent
- Maya → tree selection sync (scriptJob)
- Showing `rig_GRP` as its own branch

---

## Step 1 — Create `ui/widgets/elementsList.py`

### File skeleton

```python
''' Elements tree widget '''

import maya.cmds as cmds
from PySide6 import QtCore, QtWidgets

from metadata.query import query

ROLE_NODE = QtCore.Qt.ItemDataRole.UserRole


class widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.refresh()

    def create_widgets(self):
        self.title_label = QtWidgets.QLabel('Elements')
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.tree = QtWidgets.QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)

        self.refresh_button = QtWidgets.QPushButton('Refresh')

    def create_layout(self):
        frame = QtWidgets.QFrame()
        frame.setFrameStyle(QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Sunken)

        frame_layout = QtWidgets.QVBoxLayout(frame)
        frame_layout.addWidget(self.title_label)
        frame_layout.addWidget(self.tree)
        frame_layout.addWidget(self.refresh_button)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(frame)

    def create_connections(self):
        self.refresh_button.clicked.connect(self.refresh)
        self.tree.itemSelectionChanged.connect(self._on_tree_selection_changed)
```

Match the **framed layout** style of `guidetemplateList.py` (title inside sunken frame).

---

## Step 2 — Implement `refresh()`

```python
def refresh(self):
    self.tree.blockSignals(True)
    self.tree.clear()

    guides = query.find_guides()
    guide_set = set(guides)
    item_map = {}

    # 1) Create guide items
    for guide in guides:
        item = QtWidgets.QTreeWidgetItem([guide])
        item.setData(0, ROLE_NODE, guide)
        item_map[guide] = item

        # 2) Add joint / control children (read-only)
        joint = query.find_joint_for_guide(guide)
        if joint:
            j_item = QtWidgets.QTreeWidgetItem([joint])
            j_item.setData(0, ROLE_NODE, joint)
            j_item.setFlags(j_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            item.addChild(j_item)

        control = query.find_control_for_guide(guide)
        if control:
            c_item = QtWidgets.QTreeWidgetItem([control])
            c_item.setData(0, ROLE_NODE, control)
            c_item.setFlags(c_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            item.addChild(c_item)

    # 3) Build guide hierarchy from Maya parenting
    roots = []
    for guide in guides:
        parents = cmds.listRelatives(guide, parent=True) or []
        parent_guide = next((p for p in parents if p in guide_set), None)
        if parent_guide:
            item_map[parent_guide].addChild(item_map[guide])
        else:
            roots.append(item_map[guide])

    # 4) Add roots to tree (only top-level items)
    for root in roots:
        self.tree.addTopLevelItem(root)

    self.tree.expandAll()
    self.tree.blockSignals(False)
```

**Order note:** Add joint/control children **before** reparenting guide items in the tree. When a guide becomes a child of another guide, its joint/control children move with it.

**Empty scene:** `guides` is `[]` → tree stays empty. No error needed.

---

## Step 3 — Click → Maya selection

```python
def _on_tree_selection_changed(self):
    items = self.tree.selectedItems()
    if not items:
        return

    node = items[0].data(0, ROLE_NODE)
    if node and cmds.objExists(node):
        cmds.select(node, replace=True)
```

No `_updating_selection` flag needed in 4a (you are not syncing Maya → tree).

---

## Step 4 — Add `on_guide_spawned` to `guidetemplateList.py`

Change `__init__` to accept an optional callback:

```python
def __init__(self, on_guide_spawned=None):
    super().__init__()
    self.on_guide_spawned = on_guide_spawned
    # ... rest unchanged
```

At the **end** of `on_item_clicked`, after `guide_cls(**call_args)`:

```python
if self.on_guide_spawned:
    self.on_guide_spawned()
```

Default `None` keeps the widget usable without the Elements panel.

---

## Step 5 — Add `on_complete` to build buttons

Same pattern in **`buildjointsButton.py`** and **`buildcontrolsButton.py`**:

```python
def __init__(self, on_complete=None):
    super().__init__()
    self.on_complete = on_complete
    # ...
```

At end of click handler:

```python
self.builder.build_joints()  # or build_controls()
if self.on_complete:
    self.on_complete()
```

---

## Step 6 — Wire everything in `mainWindowUI.py`

**Import:**

```python
from ui.widgets import guidetemplateList, buildjointsButton, buildcontrolsButton, elementsList
```

**Create widgets** — elements first so you can pass `refresh`:

```python
def create_widgets(self):
    self.title_label = QtWidgets.QLabel(self.WINDOW_TITLE)
    self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    self.elements_widget = elementsList.widget()
    refresh = self.elements_widget.refresh

    self.guide_list_widget = guidetemplateList.widget(on_guide_spawned=refresh)
    self.build_joints_button = buildjointsButton.widget(on_complete=refresh)
    self.build_controls_button = buildcontrolsButton.widget(on_complete=refresh)
```

**Layout** — put Elements between templates and build buttons; give the tree space:

```python
def create_layout(self):
    main_layout = QtWidgets.QVBoxLayout(self)
    main_layout.setContentsMargins(8, 8, 8, 8)
    main_layout.setSpacing(6)

    main_layout.addWidget(self.title_label)
    main_layout.addWidget(self.guide_list_widget)
    main_layout.addWidget(self.elements_widget, stretch=1)  # tree grows
    main_layout.addWidget(self.build_joints_button)
    main_layout.addWidget(self.build_controls_button)
```

Remove `main_layout.addStretch()` above templates — it was pushing everything down and leaves no room for the tree.

**Optional:** `self.tree.setMinimumHeight(120)` in `elementsList` so the panel is usable when docked.

---

## Files to touch (4a only)

| File | Change |
|------|--------|
| `ui/widgets/elementsList.py` | **new** |
| `ui/widgets/guidetemplateList.py` | `on_guide_spawned` callback |
| `ui/widgets/buildjointsButton.py` | `on_complete` callback |
| `ui/widgets/buildcontrolsButton.py` | `on_complete` callback |
| `ui/mainWindowUI.py` | import, create, layout |

---

## How to test in Maya

| Step | Action | Expected |
|------|--------|----------|
| 1 | `show()` | Elements panel visible with empty tree |
| 2 | Double-click **fk** | `fk_guide` appears in tree |
| 3 | Select `fk_guide`, spawn second FK | `fk_guide1` nested under `fk_guide` |
| 4 | **Build Joints** | `fk_jnt` / `fk_jnt1` under respective guides |
| 5 | **Build Controls** | `fk_ctrl` / `fk_ctrl1` under respective guides |
| 6 | Click `fk_jnt` in tree | Joint selected in viewport |
| 7 | Delete a node in Outliner, click **Refresh** | Tree updates |

**Script Editor spot-check:**

```python
from metadata.query import query
query.find_guides()
query.find_joint_for_guide('fk_guide')
query.find_control_for_guide('fk_guide')
```

---

## 4a exit criteria

- [ ] `elementsList.py` exists with tree + Refresh button
- [ ] Guide hierarchy matches Maya parenting
- [ ] Joint and control appear under correct guide
- [ ] Clicking any item selects it in Maya
- [ ] Refresh button rebuilds tree
- [ ] Tree auto-updates after guide spawn, Build Joints, Build Controls
- [ ] No changes to `modules/` or `metadata/`

---

## Common pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| Tree empty after spawn | Forgot `on_guide_spawned` callback | Wire `refresh` in `mainWindowUI` |
| Joint under wrong guide | `guideNode` mismatch | Verify attrs on built nodes |
| `find_joint_for_guide` raises | Passing non-guide node | Only call with guide names from `find_guides()` |
| Tree squashed / tiny | `addStretch()` eating space | Remove stretch above templates; use `stretch=1` on elements widget |
| Duplicate top-level + nested guide | Added all guides as roots AND children | Only `addTopLevelItem` for `roots` list |

---

## After 4a

**4b** — rename guides from tree (+ update locked `guideNode` attrs).

**4c** — drag-drop reparent guides.

Check in with *"Phase 4a done — please review"*.
