# RigBox Progress

Manual implementation workflow — user codes; agent guides and reviews.  
Full roadmap: Cursor plan **RigBox Structured Project Plan** (Phases 0–8).

**Last updated:** 2026-07-31  
**Git branch:** `main`  
**Last commit:** `b4d7037` — Add parent support to guide creation

---

## Phase status

| Phase | Description | Status |
|-------|-------------|--------|
| **0** | Stabilize refactor (UI, tags, templates) | Complete |
| **1** | FK pipeline (query API, FK module, Build Joints) | Complete |
| **1d** | FK guide pass-through + selection parenting | Complete |
| **2** | Module base class + rig naming conventions | **Next** |
| **3** | Build Controls pipeline | Pending |
| **4** | Elements UI widget | Pending |
| **5** | Humanoid guides/modules (Root, Spine, limbs, etc.) | Pending |
| **6** | Skin workflow | Pending |
| **7** | Camera + Metahuman | Pending |
| **8** | Distribution + polish | Pending |

---

## What works (verified through Phase 1d)

- `from ui.mainWindowUI import show; show()` — dockable UI
- Double-click **fk** template → tagged `fk_guide` locator
- Select `fk_guide` → spawn second FK → new guide parents under selected guide (`parent` captured in UI before spawn)
- **Build Joints** → `fk_jnt` at guide world position (template-driven via `modules/build.py`)

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

1. Read Phase 2 in the structured project plan.
2. Ask agent for **Phase 2 breakdown** or implement manually.
3. Check in with *"Phase 2 done — please review"*.

**Phase 2 goal:** Refactor `modules/base/module.py` into a `module` base class with `build()` contract; tag built nodes; naming (`_jnt`, `_ctrl`).

---

## Notes

- Phases 2–8 were once auto-implemented and **reverted** — do not re-apply bulk agent implementation; follow manual workflow.
- Agent default: guide-only for Python source; may update this file and `.cursor/rules/` for behavior/progress.
