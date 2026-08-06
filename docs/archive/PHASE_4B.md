# Phase 4b — Guide Rename + guideNode Sync

Supplement to [`PHASE_4A.md`](PHASE_4A.md). Phase 4a complete; you are here.

---

## Goal

Rename **guides** inline in the Elements tree. When a guide is renamed in Maya, update the locked `guideNode` attribute on linked joints and controls so `find_joint_for_guide` / `find_control_for_guide` keep working.

**Scope:** guides only — joints and controls stay read-only in the tree.

---

## Files to touch

| File | Edit? | What |
|------|-------|------|
| [`ui/widgets/elementsList.py`](../ui/widgets/elementsList.py) | **Yes** | All Phase 4b work lives here |
| `metadata/query.py` | No | Read-only — import `ATTR_GUIDE_NODE` |
| `ui/mainWindowUI.py` | No | Already wired from 4a |
| `modules/` | No | — |

---

## Why this matters

Built nodes store the guide name as a string:

```
fk_jnt.guideNode  →  "fk_guide"
fk_ctrl.guideNode →  "fk_guide"
```

If you rename `fk_guide` → `arm_fk_guide` in the tree but don't update `guideNode`, Build Controls and the Elements tree break the link.

---

## Step 1 — Module constants and import

**File:** `ui/widgets/elementsList.py` — top of file (after existing imports)

Add `ATTR_GUIDE_NODE` to the import from `metadata.query`:

```python
from metadata.query import query, ATTR_GUIDE_NODE
```

Below `ROLE_NODE`, add:

```python
ROLE_KIND = QtCore.Qt.ItemDataRole.UserRole + 1  # 'guide', 'joint', 'control'
```

---

## Step 2 — Guard flag in `__init__`

**File:** `ui/widgets/elementsList.py` — class `widget`, method `__init__`

After `super().__init__()`, add:

```python
self._block_item_changed = False
```

This prevents rename logic from firing during `refresh()` or when you update item text after a rename.

---

## Step 3 — Editable flags in `refresh()`

**File:** `ui/widgets/elementsList.py` — class `widget`, method `refresh()`

### 3a — Block item-changed at start/end of `refresh()`

At the **start** of `refresh()` (before `self.tree_view.clear()`), add:

```python
self._block_item_changed = True
```

At the **end** of `refresh()` (after `blockSignals(False)`), add:

```python
self._block_item_changed = False
```

### 3b — Guide items (inside the `for guide in guides:` loop)

After `item.setData(0, ROLE_NODE, guide)`:

```python
item.setData(0, ROLE_KIND, 'guide')
item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)
```

### 3c — Joint items (inside the `if joint:` block)

After `joint_item.setData(0, ROLE_NODE, joint)`:

```python
joint_item.setData(0, ROLE_KIND, 'joint')
joint_item.setFlags(joint_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
```

### 3d — Control items (inside the `if control:` block)

After `control_item.setData(0, ROLE_NODE, control)`:

```python
control_item.setData(0, ROLE_KIND, 'control')
control_item.setFlags(control_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
```

---

## Step 4 — Connect `itemChanged`

**File:** `ui/widgets/elementsList.py` — class `widget`, method `create_connections()`

Add:

```python
self.tree_view.itemChanged.connect(self._on_item_changed)
```

---

## Step 5 — Add `_on_item_changed`

**File:** `ui/widgets/elementsList.py` — class `widget`, **new method** (e.g. after `_on_tree_selection_changed`)

```python
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
```

**Notes:**
- `cmds.rename` may return a suffixed name (`fk_guide1`) if `new_name` collides — always use `actual_name`.
- `strip()` avoids whitespace-only renames.

---

## Step 6 — Add `_update_guide_node_refs`

**File:** `ui/widgets/elementsList.py` — class `widget`, **new method** (below `_on_item_changed`)

```python
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
```

Uses `ATTR_GUIDE_NODE` imported in Step 1 — no edits to `metadata/query.py`.

---

## Change map (quick reference)

| Step | File | Method / location |
|------|------|-------------------|
| 1 | `ui/widgets/elementsList.py` | Imports + `ROLE_KIND` constant |
| 2 | `ui/widgets/elementsList.py` | `__init__` |
| 3 | `ui/widgets/elementsList.py` | `refresh()` |
| 4 | `ui/widgets/elementsList.py` | `create_connections()` |
| 5 | `ui/widgets/elementsList.py` | `_on_item_changed()` (new) |
| 6 | `ui/widgets/elementsList.py` | `_update_guide_node_refs()` (new) |

---

## How to test in Maya

| Step | Action | Expected |
|------|--------|----------|
| 1 | Spawn `fk_guide`, Build Joints + Controls | Tree shows guide + jnt + ctrl |
| 2 | F2 / slow-double-click guide name in tree | Edit mode |
| 3 | Rename to `arm_fk_guide`, Enter | Maya node renamed; tree shows new name |
| 4 | Script Editor | `cmds.getAttr('fk_jnt.guideNode')` → `'arm_fk_guide'` |
| 5 | Script Editor | `query.find_joint_for_guide('arm_fk_guide')` → `'fk_jnt'` |
| 6 | Try renaming a **joint** row | Should not enter edit mode |
| 7 | Click **Refresh** | No errors; tree still correct |

---

## Edge cases

| Case | Behavior |
|------|----------|
| Empty rename / same name | Ignore |
| Invalid Maya name | `cmds.rename` errors — let Maya warn |
| Guide deleted in Outliner | `cmds.objExists` fails — skip or Refresh |
| `itemChanged` during `refresh()` | Blocked by `_block_item_changed` |
| Name collision | Maya suffixes; use `actual_name` from rename |

---

## 4b exit criteria

- [ ] Only guide rows are editable in the tree
- [ ] Renaming a guide renames the Maya transform
- [ ] `guideNode` on linked joint(s) and control(s) updated to new name
- [ ] `find_joint_for_guide` / `find_control_for_guide` work after rename
- [ ] Joint/control rows cannot be renamed from the tree
- [ ] No errors when clicking Refresh after rename

---

## After 4b

**Phase 4c** — drag-drop reparent guides (`ui/widgets/elementsList.py` only).

Check in with *"Phase 4b done — please review"*.
