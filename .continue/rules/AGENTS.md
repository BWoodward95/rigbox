# Project Architecture
Python automated rigging system for Autodesk Maya.

## Directory layout (relative to workspace root)
- `guides/` — pre-rig guide logic
- `metadata/` — metadata tagging logic
- `modules/` — modular joint/control systems

## Tool usage
- Use workspace-relative paths (e.g. `metadata`, not `/metadata`).
- To explore folders, call `ls` with `dirPath`.
- To read files, call `read_file` with `filepath`.
- Do not ask the user to paste tool output; invoke tools directly.

## Agent behavior

- When asked about files, folders, or code, inspect the workspace with tools before answering.
- Do not guess file contents or directory listings from this document alone.
- Use `ls` to explore directories and `read_file` to read files — choose the appropriate tool yourself.
- Never ask the user to paste file contents or provide tool output.
- Never tell the user which tool to use; invoke tools directly.
- Use workspace-relative paths (`metadata`, `guides/modules/tag.py`), not leading-slash paths like `/metadata`.

# Documentation Resources
- Maya.cmds API: (https://help.autodesk.com/cloudhelp/ENU/MayaCRE-Tech-Docs/CommandsPython/)
- Pyside6: (https://doc.qt.io/qtforpython-6/index.html)