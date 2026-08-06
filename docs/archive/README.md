# Archive

Superseded RigBox documentation, retained for history only. **Do not use these as a source of truth.**

Archived on **2026-08-06** when the project plan was reset against the revised module goals in
[`.cursor/rules/rigbox-project.mdc`](../../.cursor/rules/rigbox-project.mdc).

| File | Was | Superseded by |
|------|-----|---------------|
| `rigbox_project_plan_b609042b.plan.md` | Original Phases 0–8 roadmap | [`docs/RIGBOX_PROJECT_PLAN.md`](../RIGBOX_PROJECT_PLAN.md) |
| `PROGRESS_pre_reset.md` | Progress tracker for old numbering | [`PROGRESS.md`](../../PROGRESS.md) |
| `METADATA_SCHEMA.md` | 4-attribute string-only schema | [`docs/METADATA_SCHEMA.md`](../METADATA_SCHEMA.md) |
| `PHASE_1_ARCHIVE.md` | Old Phase 0–1 detail | `docs/PHASE_*.md` (new numbering) |
| `PHASE_2B.md`, `PHASE_2C.md` | Old module base / schema phases | `docs/PHASE_*.md` (new numbering) |
| `PHASE_3.md` | Old Build Controls phase | `docs/PHASE_*.md` (new numbering) |
| `PHASE_4.md`, `PHASE_4A.md`, `PHASE_4B.md`, `PHASE_4C.md` | Old Elements UI phases | `docs/PHASE_*.md` (new numbering) |

## Why the reset

The original plan predated these requirements:

- Six metadata attributes with mixed types (`deform` boolean, `side` / `kinematics` enums) rather than four string attributes
- A four-step pipeline with explicit scene groups (`guides_GRP`, `joints_GRP`, `deform_GRP`, `rig_GRP`) and selection sets (`deform_skeleton`, `controls`)
- `effector` as a first-class `componentType`
- A control curve library backed by `curves/curve_library.json`
- A concrete module list (fk, fk chain, root, spine, head/neck, shoulder, arm, finger, leg, foot)

Phase numbering restarts at **Phase 1** under the new plan. Old phase numbers in these files do not map onto the new ones.

## Note on Cursor plan files

Three Cursor plan documents in `.cursor/plans/` also predate the reset and use the old numbering
(`rig_build_stabilization_*`, `phase_4.5_stabilization_*`, `rigbox_phases_4.5-8_*`).
Their content is folded into Phase 2 of the new plan. Treat them as obsolete.
