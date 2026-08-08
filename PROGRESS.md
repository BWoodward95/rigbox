# RigBox Progress

**Last updated:** 2026-08-07
**Branch:** `main`
**Roadmap:** [`docs/RIGBOX_PROJECT_PLAN.md`](docs/RIGBOX_PROJECT_PLAN.md)
**Metadata contract:** [`docs/METADATA_SCHEMA.md`](docs/METADATA_SCHEMA.md)

Manual implementation workflow: the user writes all code; the agent breaks down phases, reviews against exit criteria, and maintains these documents.

---

## Plan reset — 2026-08-06

Phase numbering **restarted at Phase 1** when the roadmap was rewritten against the revised module goals in [`.cursor/rules/rigbox-project.mdc`](.cursor/rules/rigbox-project.mdc). Old phase numbers do not map onto the new ones.

Everything from before the reset is in [`docs/archive/`](docs/archive/README.md) and should be treated as history only. The three `.cursor/plans/` documents that use the old numbering (`rig_build_stabilization_*`, `phase_4.5_stabilization_*`, `rigbox_phases_4.5-8_*`) are obsolete; their content is folded into Phase 2.

---

## Phase status

| Phase | Name | Status |
|-------|------|--------|
| **1** | Metadata Foundation | **In progress** |
| **2** | Scene Contract | Not started |
| **3** | Control Curve Library | Not started |
| **4** | FK Reference Module | Not started |
| **5** | Skinning Step | Not started |
| **6** | Simple Modules — fk chain, root, shoulder | Not started |
| **7** | Torso Modules — spine, head/neck | Not started |
| **8** | Limb Modules — arm, leg | Not started |
| **9** | Extremity Modules — foot, finger | Not started |
| **10** | Polish and Distribution | Not started |

Breakdowns are written one phase at a time as `docs/PHASE_N.md`. Current: [`docs/PHASE_1.md`](docs/PHASE_1.md) — **1a complete**, resume at **1b**.

### Phase 1 sub-steps

| Step | Work | Status |
|------|------|--------|
| 1a | Typed `tag.create` (string, bool, enum) | **Complete** |
| 1b | Query constants and typed readers | Not started |
| 1c | Guide `side` as enum | Not started |
| 1d | Full tagging on built nodes | Not started |
| 1e | Template args | Not started |
| 1f | Maya verification | Not started |

---

## What already works

Written before the reset and still valid. **Do not rebuild these** — later phases extend them.

| Capability | Files |
|------------|-------|
| Typed metadata tagging (string, bool, enum) with create-or-update | [`metadata/tag.py`](metadata/tag.py) |
| String-only query helpers for guides, joints, controls | [`metadata/query.py`](metadata/query.py) |
| Guide spawn with metadata; parents under a selected guide | [`guides/base/guide.py`](guides/base/guide.py), [`guides/fk/guide.py`](guides/fk/guide.py) |
| Module base with joint and control creation helpers | [`modules/base/module.py`](modules/base/module.py) |
| FK module producing one joint and one control | [`modules/fk/module.py`](modules/fk/module.py) |
| Template-driven build orchestration | [`modules/build.py`](modules/build.py), [`guides/templates.json`](guides/templates.json) |
| Dockable UI: template list, Elements tree, Build Joints, Build Controls | [`ui/mainWindowUI.py`](ui/mainWindowUI.py), [`ui/widgets/`](ui/widgets) |
| Elements tree: hierarchy, click-to-select, rename with `guideNode` sync, drag-drop reparent with cycle guard | [`ui/widgets/elementsList.py`](ui/widgets/elementsList.py) |

---

## Known gaps

Each is owned by a phase. Do not fix them ad hoc.

| Gap | Owned by |
|-----|----------|
| `deform` and `kinematics` attributes do not exist on nodes | Phase 1 (1b–1d) |
| `side` is a string rather than an enum on guides | Phase 1 (1c) |
| `effector` is not a recognized `componentType` in query | Phase 1 (1b) |
| No `guides_GRP`, `joints_GRP`, or `deform_GRP` | Phase 2 |
| No `deform_skeleton` or `controls` selection sets | Phase 2 |
| Joint and control names collide across guides in the same module | Phase 2 |
| Joints and controls do not mirror the guide hierarchy | Phase 2 |
| Rebuilding duplicates nodes instead of updating them | Phase 2 |
| FK controls use `parentConstraint` only, no `orientConstraint` | Phase 2 |
| [`curves/curve_library.json`](curves/curve_library.json) is empty; no reader or capture tool | Phase 3 |
| No skinning step | Phase 5 |
| Only the `fk` module exists | Phases 6 to 9 |
| `ik chain` is registered in templates but is not a module in the current goals | Phase 4 |

---

## Resolved

**2026-08-06 — deform skeleton hierarchy.** Game export is a project requirement. `deform_GRP` is a sibling of `joints_GRP` at the scene root and holds a single contiguous deform skeleton; only the skeleton root joint is a direct child of the group. Driver joints (IK, FK, reverse foot, twist) stay under `joints_GRP` and reach the skeleton through constraints. The Joints Step in [`.cursor/rules/rigbox-project.mdc`](.cursor/rules/rigbox-project.mdc) was revised to state this; full reasoning is in [`docs/METADATA_SCHEMA.md`](docs/METADATA_SCHEMA.md) section 5.

---

## Open design questions

Answer before the owning phase begins. Detail in [`RIGBOX_PROJECT_PLAN.md`](docs/RIGBOX_PROJECT_PLAN.md) section 5.

| Question | Blocks |
|----------|--------|
| Does `side` appear in guide names, or only in metadata? | Phase 2 |
| Should guides use a custom drawn shape instead of a plain locator? | Phase 6 |

---

## Resume here

**Phase 1b — Constants and typed readers in [`metadata/query.py`](metadata/query.py).** See [`docs/PHASE_1.md`](docs/PHASE_1.md) step 1b.

---

## Notes

- Phases were once bulk-implemented by an agent and reverted. Do not repeat that. The agent writes Python only when explicitly asked.
- The agent maintains this file, `docs/*.md`, and `.cursor/rules/`; source directories are the user's.
- [`deprecated/`](deprecated) holds v1 and v2 RigBox code. Useful precedent for the reverse foot, roll system, and curve library, but reference only.
