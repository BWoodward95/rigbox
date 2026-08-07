# Phase 1 — Metadata Foundation

**Goal:** Every RigBox node carries the full six-attribute metadata set, written with the correct Maya attribute types and readable through a typed query API.

**Contract:** [`METADATA_SCHEMA.md`](METADATA_SCHEMA.md) sections 2 and 3 define what this phase must produce.

**Why this is Phase 1:** Every later phase queries these attributes. `deform` gates skinning in Phase 6 and decides whether a joint joins the exported deform skeleton, `kinematics` gates IK/FK switching in Phase 9, and `side` drives naming and mirroring. Adding attributes after ten modules exist would mean retagging all of them.

**Scope boundary:** this phase changes *what is written and read*. It does **not** change naming, grouping, hierarchy, or build idempotency — that is Phase 2. Joints will still collide by name when you finish Phase 1, and that is expected.

**Note on existing work:** [`modules/base/module.py`](../modules/base/module.py) already carries the group constants (`GUIDE_GROUP`, `JOINTS_GROUP`, `RIG_GROUP`), `_joints_group()`, and guide-derived `_joint_name()` / `_control_name()`. That is Phase 2 groundwork you have already written. Leave it alone in Phase 1; step 1d only touches `_tag_node` and the two create helpers.

---

## Files to touch

| Step | File | Work |
|------|------|------|
| 1a | [`metadata/tag.py`](../metadata/tag.py) | Add boolean and enum attribute support |
| 1b | [`metadata/query.py`](../metadata/query.py) | Attribute and enum constants, typed readers, effector and deform helpers |
| 1c | [`guides/base/guide.py`](../guides/base/guide.py) | Write `side` as an enum |
| 1d | [`modules/base/module.py`](../modules/base/module.py) | Write the full attribute set on built nodes |
| 1e | [`guides/templates.json`](../guides/templates.json) | Pass `side` and `subModule` through template args |
| 1f | — | Verify in Maya |

---

## Step 1a — Typed attributes in `tag.py`

**File:** [`metadata/tag.py`](../metadata/tag.py)

### The problem

`tag.create` hardcodes `dataType="string"` and always calls `setAttr(..., type="string")`. Two of the six attributes are not strings:

- `deform` is a **boolean**
- `side` and `kinematics` are **enums**

### Maya background

Maya splits custom attributes into two families, and they take different `addAttr` flags:

| Family | `addAttr` flag | Types | `setAttr` |
|--------|----------------|-------|-----------|
| Data | `dataType='string'` | string, matrix, arrays | needs `type='string'` |
| Numeric / typed | `attributeType='bool'`, `'enum'`, `'float'`, … | bool, enum, numbers | no `type` flag |

An enum also needs its labels declared at creation time via the `enumName` flag, as a colon-delimited string:

```python
cmds.addAttr(node, ln='side', at='enum', en='none:center:left:right')
```

The label order **is** the index order. `none` is 0, `center` is 1, `left` is 2, `right` is 3. Reordering the labels later silently reinterprets every existing node, so treat the order as frozen once written into the schema.

### What to change

Give `create` an attribute-type parameter and branch on it. Suggested shape:

```python
def create(target, longname, data=None, attr_type='string',
           enum_names=None, shortname=None, nicename=None, locked=True):
```

Branching:

| `attr_type` | Creation | Value write |
|-------------|----------|-------------|
| `'string'` | `addAttr(..., dataType='string')` | `setAttr(attr, data, type='string')` |
| `'bool'` | `addAttr(..., attributeType='bool')` | `setAttr(attr, bool(data))` |
| `'enum'` | `addAttr(..., attributeType='enum', enumName=enum_names)` | `setAttr(attr, index)` |

### Two bugs to fix while you are in here

**1. The falsy-default bug.** The current line

```python
if not data:
    data = ''
```

collapses `False` and `0` to an empty string. Once `deform` exists, `tag.create(jnt, 'deform', False, attr_type='bool')` would write `''`. Guard on `None` instead:

```python
if data is None:
    data = '' if attr_type == 'string' else 0
```

**2. Re-tagging a locked attribute.** `addAttr` raises if the attribute already exists, and `setAttr` raises if it is locked. Phase 2 rebuilds will retag existing nodes, so add an update path now: if the attribute exists, unlock, set, relock, and return rather than calling `addAttr`. [`ui/widgets/elementsList.py`](../ui/widgets/elementsList.py) already does this unlock-set-relock dance for `guideNode`, so mirror that pattern.

### Enum values

Accepting either a label or an index makes call sites readable. Given `enum_names='none:center:left:right'` and `data='left'`, resolve to `2` with `enum_names.split(':').index(data)`. Raise a clear `ValueError` on an unknown label rather than defaulting to 0, or a typo will silently produce a `none`-sided node.

### 1a exit criteria

- [ ] `tag.create` writes string, boolean, and enum attributes
- [ ] Enum accepts a label and stores the matching index
- [ ] `False` and `0` are stored as themselves, not as `''`
- [ ] Re-tagging an existing locked attribute updates it instead of raising
- [ ] All three types are locked when `locked=True`

---

## Step 1b — Constants and typed readers in `query.py`

**File:** [`metadata/query.py`](../metadata/query.py)

### Add the missing constants

Alongside the existing `ATTR_*` constants:

```python
ATTR_DEFORM = 'deform'
ATTR_KINEMATICS = 'kinematics'
```

Define the enum label strings in **one** place, because `tag.create` and `query` must agree exactly:

```python
SIDE_ENUM = 'none:center:left:right'
KINEMATICS_ENUM = 'none:FK:IK:IKFK'
```

Individual labels are worth naming too (`SIDE_LEFT = 'left'`, `KINEMATICS_IKFK = 'IKFK'`) so module code compares against a constant rather than a quoted string.

**Reasoning:** these constants are the schema. Anywhere a literal `'left'` appears in module code is a place a typo becomes a silently mis-sided rig.

### Reading enums

This is the one genuine trap in the phase. `cmds.getAttr` on an enum returns the **integer index**:

```python
cmds.getAttr('L_upperArm_guide.side')                  # 2
cmds.getAttr('L_upperArm_guide.side', asString=True)   # 'left'
```

Comparing the raw result against `'left'` is always false and fails silently. Add a small reader and route every enum read through it:

```python
@staticmethod
def read_enum(node, attr):
    return cmds.getAttr(f'{node}.{attr}', asString=True)
```

### New type check and finders

Mirror the existing `is_joint` / `find_joints` pattern:

| Function | Behavior |
|----------|----------|
| `is_effector(node)` | `componentType == 'effector'` |
| `find_effectors(module=None)` | Effector transforms, optionally filtered by module |
| `find_deform_joints()` | Joints where `deform` is true |
| `find_driver_joints()` | Joints where `deform` is false |

`find_deform_joints` must tolerate joints that predate the attribute. Check `cmds.attributeQuery(ATTR_DEFORM, node=node, exists=True)` before reading, and treat a missing attribute as false. Phase 6 depends on this returning a clean influence list, and Phase 2 uses the deform/driver split to decide whether a joint belongs under `deform_GRP` or `joints_GRP`.

### Fix the missing guard on `find_control_for_guide`

`find_joint_for_guide` validates its argument, but its control twin does not:

```python
@staticmethod
def find_control_for_guide(guide_node):
    module = cmds.getAttr(f'{guide_node}.{ATTR_MODULE}')
```

Passing a non-guide raises a bare Maya attribute error instead of a clear `ValueError`. Add the same `is_guide` check the joint version has. Cheap now; confusing to debug once ten modules call it.

### Update `read_guide_data`

It currently reads `side` with a plain `getAttr`, which will start returning an integer once 1c lands. Route it through `read_enum` so the returned dict still carries `'left'`.

Consider a general `read_node_data(node)` that works for any tagged node, returning whichever of the six attributes are present. Modules in Phases 7 to 10 will want it; a guide-only reader is not enough once joints and controls carry `kinematics`.

### 1b exit criteria

- [ ] `ATTR_DEFORM` and `ATTR_KINEMATICS` defined
- [ ] Enum label strings defined once and shared
- [ ] `read_enum` returns labels, not indices
- [ ] `is_effector` and `find_effectors` exist
- [ ] `find_deform_joints` returns only `deform = true` joints and tolerates untagged joints
- [ ] `find_control_for_guide` raises `ValueError` on a non-guide, matching its joint twin
- [ ] `read_guide_data` returns `side` as a label

---

## Step 1c — Tag guides with the enum `side`

**File:** [`guides/base/guide.py`](../guides/base/guide.py)

`create()` currently writes four string attributes. Change the `side` call to the enum form and keep the other three as strings:

```python
tag.create(guide_transform, ATTR_SIDE, self.side,
           attr_type='enum', enum_names=SIDE_ENUM)
```

Default `self.side` to `'none'` rather than `None` when the template does not supply one, so the enum resolves to a real label instead of falling through to index 0 by accident.

Guides do **not** get `deform` or `kinematics`. A single guide can drive both IK and FK output, so the module decides at build time; storing it on the guide would be a lie.

### Decision — `side` is unlocked (confirmed 2026-08-06)

Every other metadata attribute is locked. `side` is the single exception: pass `locked=False` for it.

```python
tag.create(guide_transform, ATTR_SIDE, self.side,
           attr_type='enum', enum_names=SIDE_ENUM, locked=False)
```

**Why:** Phase 2 bakes a name prefix from this value (`left` gives `L_upperArm_guide`). If the attribute were locked, flipping a guide from left to right would mean unlocking it, renaming the guide, and updating `guideNode` on every built node that references it — in practice you would delete and respawn. Leaving it writable costs nothing and leaves room for a "flip side" action in the Elements tree later.

**Consequence for later phases:** an unlocked attribute can drift out of sync with the baked name prefix. A guide could read `side = right` while still being called `L_upperArm_guide`. Metadata stays the source of truth, so queries and mirroring are unaffected, but any future flip-side action must rename the guide and its built nodes rather than only setting the attribute.

### Ordering gotcha

`create()` tags the transform and *then* renames it. That works, but note that `tag.create` takes the node name as a string — if you move the rename earlier, the tag calls must use the post-rename name. Keep tagging and renaming adjacent so the dependency stays obvious.

### Backward compatibility

Guides in existing scene files carry a **string** `side`. There is no in-place migration in this phase. Respawn guides in a fresh scene when you test. If you have a scene worth keeping, delete the old attribute with `tag.destroy` and retag.

### Not in this step — the side prefix

Phase 2 derives a name prefix from this attribute at spawn time, using the mapping you confirmed:

| `side` | Prefix | Guide | Joint |
|--------|--------|-------|-------|
| `left` | `L_` | `L_upperArm_guide` | `L_upperArm_jnt` |
| `right` | `R_` | `R_upperArm_guide` | `R_upperArm_jnt` |
| `center` | `C_` | `C_spine_guide` | `C_spine_jnt` |
| `none` | none | `prop_guide` | `prop_jnt` |

Do **not** implement the prefix in 1c. It belongs with the rest of the naming work in Phase 2, and adding it now would leave guide names and the still-unfixed joint naming inconsistent mid-phase. The table is here so the decision is not lost; it still needs writing into [`METADATA_SCHEMA.md`](METADATA_SCHEMA.md).

### 1c exit criteria

- [ ] Spawned guides show `side` as a channel-box dropdown
- [ ] `cmds.getAttr('fk_guide.side', asString=True)` returns a label
- [ ] `componentType`, `module`, `subModule` are still strings
- [ ] `side` is editable in the channel box; the other three are locked
- [ ] Guides carry no `deform` or `kinematics`
- [ ] Guide names are unchanged — no prefix yet

---

## Step 1d — Tag built nodes with the full set

**File:** [`modules/base/module.py`](../modules/base/module.py)

`_tag_node()` currently writes three attributes: `componentType`, `guideNode`, `module`. Per [`METADATA_SCHEMA.md`](METADATA_SCHEMA.md) section 3, joints need seven and controls need six.

### Attributes to add

| Attribute | Source | Notes |
|-----------|--------|-------|
| `subModule` | `self.metadata['subModule']` | Already read by `read_guide_data`, just not written through |
| `side` | `self.metadata['side']` | Enum, copied from the guide |
| `deform` | Caller | Joints only |
| `kinematics` | Caller | Joints, controls, effectors |

### Signature

`deform` and `kinematics` vary per node, so they cannot be derived from guide metadata alone. In a limb the bind joint is `deform=True, kinematics='IKFK'` while its FK driver is `deform=False, kinematics='FK'` — same guide, different tags. Pass them in:

```python
def _tag_node(self, node, component_type, deform=None, kinematics=KINEMATICS_NONE):
```

Write `deform` only when `component_type == 'joint'`, so `None` means "not a joint" and `False` means "a joint that does not skin". Those are different states and collapsing them will cost you an hour in Phase 9.

Thread the parameters through `_create_joint` and `_create_control` so callers set them at creation:

```python
self._create_joint(name, deform=True, kinematics=KINEMATICS_FK)
```

Sensible defaults for the simple case: `deform=True` on joints and `kinematics=KINEMATICS_NONE` everywhere. FK modules then only override what differs.

### Why `deform` carries more weight than it looks

It is not just a skinning flag. Since game export is a project requirement, this one boolean decides which of two hierarchies a joint lives in:

- `deform = true` — joins the contiguous deform skeleton under `deform_GRP`, and is exported
- `deform = false` — a driver joint under `joints_GRP`, never exported, reaching the skeleton through constraints

Phase 2 reads this tag to route parenting. Getting it wrong later means an extra bone in the exported skeleton, which is exactly the class of defect the hierarchy rules exist to prevent. See [`METADATA_SCHEMA.md`](METADATA_SCHEMA.md) section 5.

### Add `_create_effector`

Effectors are IK handles, pole vector locators, and reverse-foot pivots — rig plumbing that is neither a joint nor an animator control. Nothing in Phase 1 creates one, but adding the tagging path now means Phase 9 is a call site rather than a refactor.

The helper does not need to create geometry. It should accept an **existing** node, since `cmds.ikHandle` returns nodes Maya has already made, and tag it with `componentType='effector'`. A thin `_tag_existing_node` used by `_create_effector` is enough.

### 1d exit criteria

- [ ] Joints carry all seven attributes
- [ ] Controls carry six and no `deform`
- [ ] `deform` and `kinematics` are settable per node, not fixed per module
- [ ] `side` and `subModule` are copied from the source guide
- [ ] An effector tagging path exists and produces `componentType = effector`

---

## Step 1e — Template arguments

**File:** [`guides/templates.json`](../guides/templates.json)

Template args currently pass only `name` and `module`. The FK entry cannot spawn a sided or sub-moduled guide, so `side` is always unset.

Add the keys to the `guide` tool-call args:

```json
"args": {
    "name": "fk",
    "module": "fk",
    "subModule": "",
    "side": "none"
}
```

[`guides/base/guide.py`](../guides/base/guide.py) already accepts `submodule` and `side` in `__init__`, and [`ui/widgets/guidetemplateList.py`](../ui/widgets/guidetemplateList.py) already splats `args` into the constructor, so no Python change is needed if the JSON key names match the parameter names.

Watch the casing: the constructor parameter is `submodule` but the Maya attribute is `subModule`. Pick one convention for the JSON and be deliberate about it — mismatched casing here produces a `TypeError` on spawn.

Leave the `ik chain`, `Root`, and `Spine` entries alone. `ik chain` is removed in Phase 3, when template definitions are reworked; `Root` and `Spine` are wired up in Phases 7 and 8.

### 1e exit criteria

- [ ] FK template passes `subModule` and `side`
- [ ] Double-clicking the FK template still spawns a guide with no traceback
- [ ] The spawned guide's `side` matches the template value

---

## Step 1f — Verify in Maya

Use a **fresh scene**. Guides from before this phase carry a string `side` and will produce misleading results.

### Test 1 — Typed attributes on a guide

Spawn an FK guide, then:

```python
import maya.cmds as cmds
from metadata.query import query, ATTR_SIDE

print(cmds.getAttr('fk_guide.side'))                 # 0  (index)
print(cmds.getAttr('fk_guide.side', asString=True))  # 'none'
print(query.read_enum('fk_guide', ATTR_SIDE))        # 'none'
print(cmds.attributeQuery('side', node='fk_guide', listEnum=True))
# ['none:center:left:right']
```

Confirm in the channel box that `side` is an editable dropdown and that `componentType`, `module`, and `subModule` are locked:

```python
for attr in ['componentType', 'module', 'subModule', 'side']:
    print(attr, cmds.getAttr(f'fk_guide.{attr}', lock=True))
# componentType True / module True / subModule True / side False
```

### Test 2 — Boolean round-trip

```python
from metadata.tag import tag

cmds.polyCube(name='tagTest')
tag.create('tagTest', 'deform', False, attr_type='bool')
print(cmds.getAttr('tagTest.deform'))   # False, not ''
print(cmds.getAttr('tagTest.deform', type=True))  # 'bool'
```

This is the falsy-default bug from 1a. If it prints an empty string, the `if not data` guard is still there.

### Test 3 — Re-tag an existing locked attribute

```python
tag.create('tagTest', 'deform', True, attr_type='bool')
print(cmds.getAttr('tagTest.deform'))   # True
```

No exception means the update path in 1a works. This is what Phase 2 rebuilds depend on.

### Test 4 — Built node tagging

Build joints and controls from the FK guide, then:

```python
for attr in ['componentType', 'module', 'subModule', 'side', 'guideNode',
             'deform', 'kinematics']:
    exists = cmds.attributeQuery(attr, node='fk_jnt', exists=True)
    print(attr, exists, cmds.getAttr(f'fk_jnt.{attr}', asString=True) if exists else '')
```

Expect all seven present on the joint. Repeat for the control and expect six, with `deform` absent.

### Test 5 — Deform query and the argument guard

```python
print(query.find_deform_joints())   # ['fk_jnt']
print(query.find_driver_joints())   # []
print(query.find_effectors())       # []

# Should raise ValueError, not a bare Maya attribute error
try:
    query.find_control_for_guide('persp')
except ValueError as e:
    print('guard ok:', e)
```

### Test 6 — Sided guide

Temporarily set the FK template's `side` to `"left"`, spawn, and confirm the guide reads back `'left'` and the built joint copies it.

---

## Phase 1 exit criteria

- [ ] `tag.create` handles string, boolean, and enum types, and updates existing locked attributes
- [ ] Enum label order is defined once in [`metadata/query.py`](../metadata/query.py) and shared with `tag.create`
- [ ] Guides carry `componentType`, `module`, `subModule`, `side`
- [ ] Joints carry those four plus `guideNode`, `deform`, `kinematics`
- [ ] Controls carry those four plus `guideNode` and `kinematics`, and no `deform`
- [ ] An effector tagging path exists
- [ ] Enums read back as labels everywhere; no code compares a raw `getAttr` result to a label string
- [ ] `find_deform_joints`, `find_driver_joints`, and `find_effectors` work
- [ ] `find_control_for_guide` guards its argument like `find_joint_for_guide` does
- [ ] `side` is unlocked on guides; every other metadata attribute is locked
- [ ] The FK template passes `subModule` and `side`
- [ ] [`METADATA_SCHEMA.md`](METADATA_SCHEMA.md) matches the code, with **planned** markers removed for anything now implemented

---

## Suggested order

Steps depend on each other in sequence. 1a and 1b can be written together since the enum constants in 1b are what 1a consumes.

1. **1a** typed `tag.create`
2. **1b** constants and typed readers
3. **1c** guide tagging
4. **1d** built node tagging
5. **1e** template args
6. **1f** verify

Check in per step (*"Phase 1a done — please review"*) or at the end of the phase.

---

## What Phase 1 does not fix

| Symptom you will still see | Owned by |
|----------------------------|----------|
| Two FK guides both target `fk_jnt` | Phase 2 |
| Nested guides produce unnested joints | Phase 2 |
| Re-pressing Build Joints duplicates nodes | Phase 2 |
| Group constants exist but nothing is parented into them | Phase 2 |
| No `deform_GRP`, no `deform_skeleton` or `controls` sets | Phase 2 |
| No side prefix on guide names | Phase 2 |
| Controls are plain circles | Phase 4 |
| Nothing consumes the `deform` tag yet | Phase 6 |
