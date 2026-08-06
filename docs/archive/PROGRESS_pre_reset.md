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
| **3** | Build Controls pipeline | Complete |
| **4** | Elements UI widget | Complete |
| **4c** | Drag-drop reparent guides | Complete |
| **5** | Humanoid guides/modules (Root, Spine, limbs, etc.) | **Next** |
| **6** | Skin workflow | Pending |
| **7** | Camera + Metahuman | Pending |
| **8** | Distribution + polish | Pending |

---

## What works (verified through Phase 4)

- Full FK pipeline: guides → Build Joints → Build Controls
- **Elements** tree: hierarchy, joint/control children, click-to-select, Refresh
- Guide rename in tree + `guideNode` sync on built nodes
- Drag-drop reparent guides (cycle guard, `query.is_guide` on parent)
- Auto-refresh after guide spawn and build actions

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

**Phase 5** — Humanoid guides/modules (Root, Spine, limbs).

1. Ask agent for Phase 5 breakdown or implement manually.
2. Check in with *"Phase 5 done — please review"* (or per sub-phase).

**Phase 4 (complete):** Elements UI — tree (4a), rename (4b), drag-drop reparent (4c).

---

## Notes

- Phases 2–8 were once auto-implemented and **reverted** — do not re-apply bulk agent implementation; follow manual workflow.
- Agent default: guide-only for Python source; may update this file and `.cursor/rules/` for behavior/progress.
