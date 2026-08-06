# RigBox Progress

**Last updated:** 2026-08-06
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

Breakdowns are written one phase at a time as `docs/PHASE_N.md`. Current: [`docs/PHASE_1.md`](docs/PHASE_1.md).

---

## What already works

Written before the reset and still valid. **Do not rebuild these** — later phases extend them.

| Capability | Files |
|------------|-------|
| String metadata tagging and removal | [`metadata/tag.py`](metadata/tag.py) |
| Scene queries for guides, joints, controls | [`metadata/query.py`](metadata/query.py) |
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
| `tag.py` writes only string attributes; no boolean or enum | Phase 1 |
| `deform` and `kinematics` attributes do not exist | Phase 1 |
| `side` is a string rather than an enum | Phase 1 |
| `effector` is not a recognized `componentType` | Phase 1 |
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

## Open design questions

Answer before the owning phase begins. Detail in [`RIGBOX_PROJECT_PLAN.md`](docs/RIGBOX_PROJECT_PLAN.md) section 5.

| Question | Blocks |
|----------|--------|
| Is `deform_GRP` a child of `joints_GRP` or a sibling? | Phase 2 |
| Does `side` appear in guide names, or only in metadata? | Phase 2 |
| Should guides use a custom drawn shape instead of a plain locator? | Phase 6 |

---

## Resume here

**Phase 1 — Metadata Foundation.** Read [`docs/PHASE_1.md`](docs/PHASE_1.md) for the step-by-step breakdown.

Check in with *"Phase 1 done — please review"*, or per step, for example *"Phase 1a done — please review"*.

---

## Notes

- Phases were once bulk-implemented by an agent and reverted. Do not repeat that. The agent writes Python only when explicitly asked.
- The agent maintains this file, `docs/*.md`, and `.cursor/rules/`; source directories are the user's.
- [`deprecated/`](deprecated) holds v1 and v2 RigBox code. Useful precedent for the reverse foot, roll system, and curve library, but reference only.
