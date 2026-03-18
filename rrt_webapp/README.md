# PHREEQC Flask webapp

### edited by rowanterra

Minimal Flask app in a separate folder: upload PHREEQC input files, optionally run phreeqc, and view USER_GRAPH JSON as charts.

## Build phreeqc first (so "Run after upload" works)

**Install CMake** (if needed):

```bash
brew install cmake
```

From the **repo root** (the folder that contains `og/` and `rrt_webapp/`):

```bash
cd /path/to/phreeqc3_rrt
cmake -S og -B build
cmake --build build
```
(The source tree is in `og/`; the binary is written to `build/phreeqc`.)

The app looks for `phreeqc` in `../build/phreeqc` (relative to rrt_webapp). If you build elsewhere, either copy the `phreeqc` binary to `phreeqc3_rrt/build/phreeqc` or add it to your PATH.

**View charts without running from the app:** Run phreeqc yourself (e.g. `./build/phreeqc rrt_webapp/example_input.pqi` from repo root), then copy the generated `phreeqc_user_graph_*.json` into `rrt_webapp/data/output/` (e.g. `rrt_webapp/data/output/my_run/`). Click **Refresh** in the app to list and show them.

The app runs examples from **`og/examples/`** (ex1, ex2, ex5, ex21, etc.). At repo root, `examples` is a symlink to `og/examples` so the build and CTest still find them. Optional manual-extracted inputs live in `manual_examples/files/`; to run the combined “all USER_GRAPH types” demo: `./rrt_webapp/run_all_manual_graphics.sh` from repo root (writes charts to `manual_examples/output/`; the app only lists charts from repo example runs under `rrt_webapp/data/output/`).

## Reconciling manual figures (e.g. Figure 24, 26)

Many figures in the PHREEQC manual (e.g. **Figure 24** – mass outflow and flux for HTO, 36Cl-, 22Na+, Cs+; **Figure 26** – Cs+ with interlayer diffusion) come from **Example 21** (radial diffusion through Opalinus Clay). That example is built to run **three separate transport calculations** by uncommenting different tracers in `SOLUTION 3`:

1. **HTO only** (default in repo) → one set of charts.
2. **36Cl-** → uncomment `Cl_tr ... -water 0.502`, comment others.
3. **22Na+ and Cs+ together** → uncomment `Cs 1; Na_tr 1.87e-7; -water 1.02`, comment others.

So **Figure 24 (A–D)** is the combination of runs (1) + (2) + (3). The repo’s `ex21` as shipped runs only (1). To get all panels you can:

- Run **Ex. 21** once in the app (you get the HTO charts), then
- Edit `og/examples/ex21` (or `examples/ex21` via the symlink): uncomment the next tracer block, run again from the app (or from the shell), then
- Repeat for the third run.

**Figure 26** (Cs+ with interlayer diffusion) uses the same input with **interlayer diffusion** turned on: in `ex21`, set `interlayer_D$ = 'true'` (around line 430) and run with Cs (and Na_tr) uncommented.

So the “missing” graphics are not missing from PHREEQC; they correspond to **different runs or options** of the same example. The webapp runs each example once as-is; for ex21, that gives one subset. To match the manual exactly, run ex21 multiple times with the tracer and `interlayer_D$` options above.

**K-Feldspar reaction path (manual Figure 7, repo Ex. 6):** The manual figure adds stability-field names (K-mica, Gibbsite, Kaolinite, K-feldspar) and point letters (A–F) by hand. The webapp adds the four **stability-field labels** automatically when displaying the "K-Feldspar Reaction Path" chart; boundary curves without a USER_GRAPH heading appear in the legend as "Phase boundary" after rebuilding phreeqc with the dump change.

## Setup

```bash
cd rrt_webapp
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
flask --app app run
# or
python app.py
```

Open http://127.0.0.1:5000

## What it does

- **Upload**: Drop a `.pqi` / `.dat` / `.inp` file. Optionally tick “Run phreeqc after upload” to run the built or PATH `phreeqc` with that file (output goes to `rrt_webapp/data/output/<basename>/`).
- **Charts**: Lists any `phreeqc_user_graph_*.json` under `rrt_webapp/data/` (e.g. from a Mac/Linux run with USER_GRAPH_DUMP). Click “Show” to plot series with Chart.js.

Data lives under `rrt_webapp/data/` (uploads in `data/uploads/`, run output in `data/output/`) so it stays out of the main PHREEQC tree.
