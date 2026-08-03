# RigBox Progress

Manual implementation workflow — user codes; agent guides and reviews.  
Full roadmap: Cursor plan **RigBox Structured Project Plan** (Phases 0–8).

**Last updated:** 2026-08-03  
**Git branch:** `main`  
**Detailed archive:** [`docs/PHASE_1_ARCHIVE.md`](docs/PHASE_1_ARCHIVE.md) — full Phase 0–1 context for agents  
**Last commit:** see `git log -1`

---

## Phase status

| Phase | Description | Status |
|-------|-------------|--------|
| **0** | Stabilize refactor (UI, tags, templates) | Complete |
| **1** | FK pipeline (query API, FK module, Build Joints) | Complete |
| **1d** | FK guide pass-through + selection parenting | Complete |
| **2** | Module base class + rig naming conventions | Complete |
| **2c** | Document metadata schema | Complete |
| **3** | Build Controls pipeline | **Next** |
| **4** | Elements UI widget | Pending |
| **5** | Humanoid guides/modules (Root, Spine, limbs, etc.) | Pending |
| **6** | Skin workflow | Pending |
| **7** | Camera + Metahuman | Pending |
| **8** | Distribution + polish | Pending |

---

## What works (verified through Phase 2c)

- `from ui.mainWindowUI import show; show()` — dockable UI
- Double-click **fk** template → tagged `fk_guide` locator
- Select `fk_guide` → spawn second FK → new guide parents under selected guide
- **Build Joints** → tagged `fk_jnt` at guide world position
- `metadata/query.py` — `is_guide`, `is_joint`, `is_control`, `find_guides`, `find_joints`, `find_controls`
- Schema reference: [`docs/METADATA_SCHEMA.md`](docs/METADATA_SCHEMA.md)

---

## Key files (Phase 1 state)

| Area | Path |
|------|------|
| Guide base + parenting | `guides/base/guide.py` |
| FK guide | `guides/fk/guide.py` |
| Template spawn | `ui/widgets/guidetemplateList.py` |
| Scene query | `metadata/query.py` |
| FK rig module | `modules/fk/module.py` |
| Build orchestrator | `modules/build.py` |
| Templates registry | `guides/templates.json` |

---

## Resume here

**Phase 3** — Build Controls pipeline.

1. Ask agent for Phase 3 breakdown or implement manually.
2. Check in with *"Phase 3 done — please review"*.

**Phase 2 (complete):** base `module` class, naming/tagging (2b), metadata schema + query API (2c).

---

## Notes

- Phases 2–8 were once auto-implemented and **reverted** — do not re-apply bulk agent implementation; follow manual workflow.
- Agent default: guide-only for Python source; may update this file and `.cursor/rules/` for behavior/progress.
