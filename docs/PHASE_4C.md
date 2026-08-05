# Phase 4c — Drag-Drop Reparent Guides

Supplement to [`PHASE_4B.md`](PHASE_4B.md). Phase 4b complete; you are here.

---

## Goal

Drag **guide** rows in the Elements tree to reparent them in Maya — the same outcome as parenting in the Outliner. Joint and control rows stay read-only children in the tree and cannot be dragged.

---

## Files to touch

| File | Edit? | What |
|------|-------|------|
| [`ui/widgets/elementsList.py`](../ui/widgets/elementsList.py) | **Yes** | All Phase 4c work |
| [`guides/base/guide.py`](../guides/base/guide.py) | No | Reference — `query.is_guide(parent)` on spawn |
| [`metadata/query.py`](../metadata/query.py) | No | Use existing `is_guide()` |
| [`ui/mainWindowUI.py`](../ui/mainWindowUI.py) | No | Already wired in 4a |

---

## Concepts (read before coding)

| Term | What it means |
|------|----------------|
| **InternalMove** | Qt drag-drop mode where items move *within* the same tree widget (not from an external source). |
| **Item flags** | Per-row permissions in `QTreeWidget` — editable, draggable, droppable. You set these in `refresh()` per `ROLE_KIND`. |
| **rowsMoved** | Signal from the tree's *model* fired after Qt finishes an internal drag-drop. Use it to sync Maya — not `itemPressed` or `currentItem()`. |
| **_block_tree_move** | Guard flag like `_block_item_changed` — stops `rowsMoved` from calling `cmds.parent` while `refresh()` rebuilds the tree. |
| **Sync-from-tree** | After a drop, walk the Qt tree and apply `cmds.parent` for each guide row. More reliable than guessing which item moved. |
| **Cycle guard** | Prevents parenting a guide under its own descendant (e.g. parent under child), which would break the hierarchy. |

---

## Step 1 — Enable internal drag-drop on the tree

**File:** `ui/widgets/elementsList.py` → `create_widgets()`

After `self.tree_view.setHeaderHidden(True)`:

```python
self.tree_view.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.InternalMove)
self.tree_view.setDefaultDropAction(QtCore.Qt.DropAction.MoveAction)
```

**Why:** `InternalMove` tells Qt to reorder/reparent rows inside this tree only. `MoveAction` means the row is moved, not copied. Without this, drag gestures are ignored even if flags are set.

---

## Step 2 — Per-row drag/drop flags in `refresh()`

**File:** `ui/widgets/elementsList.py` → `refresh()`

Qt does not know which rows are guides vs joints — you declare that with **item flags** each time the tree is built.

### Guide items (inside `for guide in guides:`)

Replace the current `setFlags` line:

```python
item.setFlags(
    item.flags()
    | QtCore.Qt.ItemFlag.ItemIsEditable
    | QtCore.Qt.ItemFlag.ItemIsDragEnabled
    | QtCore.Qt.ItemFlag.ItemIsDropEnabled
)
```

**Why:** Guides can be renamed (4b), dragged, and act as drop targets for other guides.

### Joint items (inside `if joint:`)

```python
joint_item.setFlags(
    joint_item.flags()
    & ~QtCore.Qt.ItemFlag.ItemIsEditable
    & ~QtCore.Qt.ItemFlag.ItemIsDragEnabled
    & ~QtCore.Qt.ItemFlag.ItemIsDropEnabled
)
```

**Why:** Joints are built output — dragging them would confuse the tree/Maya link. Clearing drop flags stops a guide being nested *under* a joint row.

### Control items (inside `if control:`)

Same pattern as joint.

---

## Step 3 — Block flag during `refresh()`

**File:** `ui/widgets/elementsList.py`

### `__init__`

```python
self._block_tree_move = False
```

### `refresh()` — at the start (alongside `_block_item_changed = True`)

```python
self._block_tree_move = True
```

### `refresh()` — at the end (after `_block_item_changed = False`)

```python
self._block_tree_move = False
```

**Why:** `refresh()` clears and rebuilds the tree, which can emit `rowsMoved`. Without blocking, you'd call `cmds.parent` on a half-built tree and corrupt the Outliner.

---

## Step 4 — Connect `rowsMoved`

**File:** `ui/widgets/elementsList.py` → `create_connections()`

```python
self.tree_view.model().rowsMoved.connect(self._on_rows_moved)
```

**Why:** Connect to the **model**, not the widget — `rowsMoved` is a `QAbstractItemModel` signal that fires once Qt has applied the drop. The handler then syncs Maya to match the new tree layout.

---

## Step 5 — Add `_on_rows_moved`

**File:** `ui/widgets/elementsList.py` → **new method** (e.g. after `_on_item_changed`)

```python
def _on_rows_moved(self, parent, start, end, destination, row):
    if self._block_tree_move:
        return
    self._sync_guides_from_tree()
```

**Why:** The signal arguments describe model indices, not Maya node names. Delegating to a full tree walk avoids tracking the dragged item manually.

---

## Step 6 — Sync tree layout → Maya

**File:** `ui/widgets/elementsList.py` → **two new methods**

```python
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
```

**Why:** Only recurse into children where `ROLE_KIND == 'guide'`. Joint/control rows stay under a guide in the tree for display but are skipped for parenting — their Maya parents are unchanged.

| Tree position | `parent_guide` passed to `_parent_guide_in_maya` |
|---------------|--------------------------------------------------|
| Top-level guide row | `None` → `cmds.parent(guide, world=True)` |
| Nested under another guide | That guide's node name |

---

## Step 7 — Parent in Maya + cycle guard

**File:** `ui/widgets/elementsList.py` → **two new methods**

```python
def _parent_guide_in_maya(self, guide, parent_guide):
    if parent_guide:
        if not query.is_guide(parent_guide):
            print(f'RigBox: Invalid parent "{parent_guide}" — not a guide')
            self.refresh()
            return
        if self._would_create_cycle(guide, parent_guide):
            print(f'RigBox: Cannot parent {guide} under {parent_guide} (cycle)')
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
```

**Why `query.is_guide`:** Same rule as [`guides/base/guide.py`](../guides/base/guide.py) on spawn — only guides can parent guides.

**Why cycle guard:** If `fk_guide` is parent of `fk_guide1`, dropping `fk_guide` onto `fk_guide1` would make the parent a child of its child. Walk *up* from `new_parent`; if you reach `guide`, block and `refresh()` to revert the tree.

**Why `refresh()` on failure:** Qt has already moved the row visually. Rebuilding from Maya restores a consistent tree.

---

## Change map

| Step | File | Method / location |
|------|------|-------------------|
| 1 | `ui/widgets/elementsList.py` | `create_widgets()` |
| 2 | `ui/widgets/elementsList.py` | `refresh()` — item flags |
| 3 | `ui/widgets/elementsList.py` | `__init__`, `refresh()` |
| 4 | `ui/widgets/elementsList.py` | `create_connections()` |
| 5 | `ui/widgets/elementsList.py` | `_on_rows_moved()` **new** |
| 6 | `ui/widgets/elementsList.py` | `_sync_guides_from_tree()`, `_sync_guide_item()` **new** |
| 7 | `ui/widgets/elementsList.py` | `_parent_guide_in_maya()`, `_would_create_cycle()` **new** |

---

## How to test in Maya

| Step | Action | Expected |
|------|--------|----------|
| 1 | Spawn two FK guides (select first, spawn second) | Child nested under parent in tree + Outliner |
| 2 | Drag child guide to root in tree | Top-level in Outliner (`world=True`) |
| 3 | Drag child onto other guide | Child parents under target in Outliner |
| 4 | Try dragging `fk_jnt` row | Row does not move |
| 5 | Build Joints on both guides | Joints still listed under correct guides |
| 6 | Drag parent under its child | Blocked; tree reverts; message in Script Editor |
| 7 | Click **Refresh** | Tree matches Outliner |

```python
import maya.cmds as cmds
cmds.listRelatives('fk_guide1', parent=True)  # verify after reparent
```

---

## Edge cases

| Case | Behavior |
|------|----------|
| Drop joint/control row | Not draggable — no-op |
| `rowsMoved` during `refresh()` | Ignored via `_block_tree_move` |
| Reparent with built joints | Joints keep world position (default Maya) — OK for 4c |
| Invalid non-guide parent | `refresh()` reverts tree |

---

## 4c exit criteria

- [ ] Guides draggable in Elements tree
- [ ] Joints/controls not draggable
- [ ] Tree reparent updates Maya Outliner
- [ ] Root-level guide uses `world=True`
- [ ] Cycle reparent blocked; tree reverts
- [ ] `query.is_guide` enforced on new parent
- [ ] Refresh still works after reparent

---

## After 4c

**Phase 4 complete** — Elements UI done.

**Phase 5** — Humanoid guides/modules (Root, Spine, limbs).

Check in with *"Phase 4c done — please review"*.
