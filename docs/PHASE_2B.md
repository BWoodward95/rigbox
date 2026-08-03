# Phase 2b — Naming and Tagging Built Nodes

Supplement to [`PROGRESS.md`](../PROGRESS.md). Phase 2a complete; you are here.

---

## Goal

Establish shared rig output conventions on the `module` base class so every future module (FK, Root, Spine, etc.) tags and names built nodes consistently.

From the design chart, built scene elements include **joint**, **control**, and **constraint** — each identifiable via metadata.

---

## Conventions to implement

| Item | Value | Example |
|------|-------|---------|
| Joint suffix | `_jnt` | `fk_jnt` |
| Control suffix | `_ctrl` | `fk_ctrl` |
| Top-level group | `rig_GRP` | empty group for controls |
| Built joint tag | `componentType` = `joint` | on joint transform |
| Built control tag | `componentType` = `control` | on control transform |

FK already names joints `{module}_jnt` — formalize via constants/helpers on the base class.

---

## Step 1 — Constants on `module` base

In [`modules/base/module.py`](modules/base/module.py), add module-level or class constants:

```python
RIG_GROUP = 'rig_GRP'
JOINT_SUFFIX = '_jnt'
CONTROL_SUFFIX = '_ctrl'
```

Optional: `ATTR_GUIDE_NODE = 'guideNode'` — links built node back to source guide (useful for Phase 3 Build Controls).

---

## Step 2 — `_tag_node()` helper

Add a private method on `module` that tags any built Maya node using existing [`metadata/tag.py`](metadata/tag.py):

```python
def _tag_node(self, node, component_type):
    tag.create(node, 'componentType', component_type, locked=True)
    tag.create(node, 'guideNode', self.guide, locked=True)
    tag.create(node, 'module', self.metadata['module'], locked=True)
    # optional: subModule, side if present in metadata
```

Import `tag` from `metadata.tag`.

**Tag the transform**, not the shape (same rule as guides).

---

## Step 3 — Call `_tag_node` from helpers

At the end of `_create_joint`, before `return joint`:

```python
self._tag_node(joint, 'joint')
```

At the end of `_create_control`, before `return control`:

```python
self._tag_node(control, 'control')
```

---

## Step 4 — `_rig_group()` helper (optional but recommended)

Creates top-level `rig_GRP` if it doesn't exist; returns the group name.

```python
def _rig_group(self):
    if not cmds.objExists(RIG_GROUP):
        cmds.group(empty=True, name=RIG_GROUP)
    return RIG_GROUP
```

Used in Phase 3 when controls parent under the rig group. Safe to add now even if unused.

---

## Step 5 — Naming helper (optional)

Reduce duplication in subclasses:

```python
def _joint_name(self, part=''):
    base = self.metadata['module']
    if part:
        return f'{base}_{part}{JOINT_SUFFIX}'
    return f'{base}{JOINT_SUFFIX}'
```

FK `build()` becomes:

```python
self.joint = self._create_joint(self._joint_name())
```

---

## Step 6 — Extend `metadata/query.py` (optional for 2b, needed by Phase 3/6)

Add `find_joints(module=None)` that returns transforms where `componentType == 'joint'`.

Mirror `find_guides()` pattern — scan transforms/joints with `attributeQuery`.

Can be Phase 2b or deferred to Phase 3; tagging joints in 2b makes this possible.

---

## Files to touch

| File | Changes |
|------|---------|
| `modules/base/module.py` | Constants, `_tag_node`, call from `_create_joint` / `_create_control`, optional `_rig_group` / `_joint_name` |
| `modules/fk/module.py` | Optional: use `_joint_name()` if you add it |
| `metadata/query.py` | Optional: `find_joints()` |

No UI or `build.py` changes required for 2b.

---

## How to test in Maya

1. Spawn `fk_guide`, **Build Joints**
2. Select `fk_jnt` in Attribute Editor — verify locked string attrs:
   - `componentType` = `joint`
   - `guideNode` = `fk_guide`
   - `module` = `fk`
3. `cmds.listAttr('fk_jnt', ud=True)` in Script Editor
4. Regression: joint still at guide world position

---

## 2b exit criteria

- [ ] Constants for `_jnt`, `_ctrl`, `rig_GRP` defined on base
- [ ] `_tag_node()` tags built joints and controls
- [ ] `fk_jnt` has `componentType=joint` and `guideNode` after Build Joints
- [ ] Build Joints pipeline still works end-to-end

---

## After 2b

**Phase 2c** — document the full metadata contract (guides + built nodes) in comments or archive doc.

**Phase 3** — Build Controls uses tagged joints + `_create_control` + `rig_GRP`.
