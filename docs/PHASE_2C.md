# Phase 2c — Metadata Schema Documentation

Supplement to [`PROGRESS.md`](../PROGRESS.md). Phase 2b complete; you are here.

---

## Goal

Write the **single source of truth** for RigBox metadata: what attributes exist on guides vs built nodes, what values they hold, and how `metadata/query.py` reads them.

Phase 2c is mostly **documentation**. A small amount of code alignment is recommended so docs and code stay in sync.

---

## Deliverable

Create **`docs/METADATA_SCHEMA.md`** — the canonical schema reference for agents and future phases.

Optionally add brief module docstrings pointing to that file (one line each; no long comments in code).

---

## Step 1 — Document guide attributes

Already implemented in `guides/base/guide.py`. Document in the schema file:

| Attribute | Type | Example | Required | Purpose |
|-----------|------|---------|----------|---------|
| `componentType` | string | `guide` | yes | Identifies RigBox guide transforms |
| `module` | string | `fk` | yes | Maps to `templates.json` rig entry |
| `subModule` | string | `""` | yes | Sub-type within module (limbs, spine segments) |
| `side` | string | `""` | yes | Laterality: `L`, `R`, or empty |

**Rules to document:**
- Tags live on the **transform**, never the shape.
- `tag.create` stores `None` as empty string `""`.
- All guide attrs are locked string attributes.

---

## Step 2 — Document built-node attributes

Implemented in `modules/base/module.py` → `_tag_node()`. Document:

| Attribute | Type | Example | On | Purpose |
|-----------|------|---------|-----|---------|
| `componentType` | string | `joint` / `control` / `constraint` | built nodes | Identifies rig output type |
| `guideNode` | string | `fk_guide` | built nodes | Source guide transform name |
| `module` | string | `fk` | built nodes | Copied from guide |

**`componentType` values (current + planned):**

| Value | Phase | Created by |
|-------|-------|------------|
| `guide` | 1 | `guides/base/guide.py` |
| `joint` | 2b | `module._create_joint()` |
| `control` | 3 | `module._create_control()` |
| `constraint` | 5+ | future modules |

**Gap to note in docs:** guides have `subModule` and `side`; built nodes do **not** yet. Document as *planned* — Phase 5 limb modules will likely need them on joints/controls for filtering.

---

## Step 3 — Document naming conventions

From `module` base class:

| Pattern | Example | Constant |
|---------|---------|----------|
| Guide | `{name}_guide` | — |
| Joint | `{module}_jnt` or `{module}_{part}_jnt` | `JOINT_SUFFIX` |
| Control | `{module}_ctrl` or `{module}_{part}_ctrl` | `CONTROL_SUFFIX` |
| Rig group | `rig_GRP` | `RIG_GROUP` |

Document that `_joint_name(part)` / future `_control_name(part)` are the preferred naming API for subclasses.

---

## Step 4 — Document query API contract

Document what `metadata/query.py` provides and what each function returns.

**Existing:**

| Function | Returns | Notes |
|----------|---------|-------|
| `is_guide(node)` | `bool` | `componentType == 'guide'` |
| `find_guides(module=None)` | `list[str]` | All guide transform names |
| `read_guide_data(node)` | `dict` | Raises if not a guide |

**`read_guide_data` shape:**
```python
{
    'node': str,
    'module': str,
    'subModule': str,
    'side': str,
    'xform': {
        'translation': [x, y, z],
        'rotation': [rx, ry, rz],
    }
}
```

**Recommended additions (implement + document):**

| Function | Returns | Notes |
|----------|---------|-------|
| `is_joint(node)` | `bool` | `componentType == 'joint'` |
| `is_control(node)` | `bool` | `componentType == 'control'` |
| `find_joints(module=None)` | `list[str]` | Replace stub; mirror `find_guides` |
| `read_node_data(node)` | `dict` | Generic reader for any tagged rig node (optional) |

Add `ATTR_GUIDE_NODE = 'guideNode'` alongside existing `ATTR_*` constants.

---

## Step 5 — Code alignment (recommended, small)

Keep docs honest — these changes match what you document:

### `metadata/query.py`

1. Add `ATTR_GUIDE_NODE = 'guideNode'`
2. Implement `is_joint(node)` / `is_control(node)` — copy `is_guide` pattern, change value check
3. Implement `find_joints(module=None)` — scan `cmds.ls(type='joint')`, filter with `is_joint`
4. Remove `find_joints` stub `pass`

### `modules/base/module.py` (optional)

One-line module docstring:
```python
'''Base module — see docs/METADATA_SCHEMA.md for tagging contract.'''
```

### `guides/base/guide.py` (optional)

Same one-line pointer to schema doc.

**Do not** extend `_tag_node` with `subModule`/`side` unless you want parity now — documenting as *planned* is enough for 2c.

---

## Step 6 — Cross-reference other docs

Update these lightly (one paragraph or link each):

| File | Change |
|------|--------|
| `docs/PHASE_1_ARCHIVE.md` | Add link to `METADATA_SCHEMA.md`; note built-node section superseded by schema doc |
| `PROGRESS.md` | Mark 2c complete when done |

---

## `METADATA_SCHEMA.md` suggested outline

```markdown
# RigBox Metadata Schema

## Overview
## Guide nodes
## Built nodes (joint, control, constraint)
## Naming conventions
## Query API
## templates.json linkage
## Future (subModule/side on built nodes, constraints)
```

Include a small diagram or table showing data flow:

```
templates.json → guide spawn → guide attrs
                              ↓
                         Build Joints/Controls
                              ↓
                    built node attrs (guideNode links back)
```

---

## How to test

Documentation phase — verify accuracy in Maya:

```python
from metadata.query import query

# After spawning fk_guide + Build Joints:
query.is_guide('fk_guide')      # True
query.is_joint('fk_jnt')        # True (after you implement is_joint)
query.find_joints()             # ['fk_jnt']
query.find_joints('fk')         # ['fk_jnt']

cmds.getAttr('fk_jnt.guideNode')  # 'fk_guide'
```

Walk through `METADATA_SCHEMA.md` line by line against Attribute Editor — every documented attr should exist on the right node type.

---

## 2c exit criteria

- [ ] `docs/METADATA_SCHEMA.md` exists and covers guides + built nodes + naming + query API
- [ ] `is_joint` / `is_control` / `find_joints` implemented (stub replaced)
- [ ] `ATTR_GUIDE_NODE` constant added
- [ ] `PHASE_1_ARCHIVE.md` links to schema doc
- [ ] Schema matches live Maya scene after FK build

---

## After 2c

**Phase 2 complete** — base class, naming, tagging, and schema documented.

**Phase 3 — Build Controls:** `_create_control`, parent under `rig_GRP`, Build Controls button, `find_joints` used to pair controls to guides.
