# OG — original app from the authors

This folder holds **original repo content** (examples and any other OG files). The rrt_webapp and scripts use paths here.

**Layout**

- **`og/examples/`** — All PHREEQC example inputs (ex1, ex2, ex2b, … ex22) and sidecar files. The rrt_webapp uses this as `REPO_EXAMPLES_DIR`. At repo root, `examples` is a symlink to `og/examples` so the build and CTest still see `examples/`.
- **`og/examples/ex2b.original`** — Unchanged copy of ex2b from git (before adding `-chart_title`). The live file used by the app is `og/examples/ex2b` (edited).

**Convention:** Any file elsewhere in the repo that was edited for this project is marked at the top with:

```text
### edited by rowanterra
```

**Edited (outside og), marked as above:**

- **rrt_webapp/** — Flask app, templates, README
- **og/examples/ex2b** — added `-chart_title` (live version; original kept as ex2b.original)
- **src/ChartObjectDump.cpp** — empty curve id → "Phase boundary"

To add more originals: from repo root,  
`git show HEAD:path/to/file > og/path/to/file`
