# ### edited by rowanterra
"""
Flask app for PHREEQC workflow: upload input, view USER_GRAPH JSON charts.
Run: flask --app app run
"""
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024  # 4 MB

# Where we store uploads and run outputs (inside rrt_webapp/ by default)
DATA_DIR = Path(__file__).resolve().parent / "data"
REPO_ROOT = Path(__file__).resolve().parent.parent
REPO_EXAMPLES_DIR = REPO_ROOT / "og" / "examples"
MANUAL_EXAMPLES_DIR = REPO_ROOT / "manual_examples"
DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR = DATA_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR = DATA_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/upload", methods=["POST"])
def upload():
    """Save uploaded .pqi / .dat / .inp file and optionally run phreeqc."""
    if "file" not in request.files:
        return jsonify({"error": "No file"}), 400
    f = request.files["file"]
    if not f.filename:
        return jsonify({"error": "No filename"}), 400
    safe = os.path.basename(f.filename).replace("..", "")
    path = UPLOAD_DIR / safe
    f.save(str(path))
    run = request.form.get("run") == "true"
    out_msg = None
    if run:
        out_msg = run_phreeqc(path)
    return jsonify({
        "saved": safe,
        "run": run,
        "message": out_msg,
    })


def run_phreeqc(input_path: Path, output_dir: Optional[Path] = None) -> str:
    """Run phreeqc binary on input file; return message (output dir or error)."""
    repo_root = Path(__file__).resolve().parent.parent
    db_path = repo_root / "og" / "database" / "phreeqc.dat"
    candidates = [
        repo_root / "build" / "phreeqc",
        repo_root / "build" / "Release" / "phreeqc",
        Path("/usr/local/bin/phreeqc"),
    ]
    exe = None
    for c in candidates:
        if c.exists():
            exe = str(c)
            break
    if not exe:
        exe = "phreeqc"
    out_dir = (output_dir or OUTPUT_DIR) / input_path.stem
    out_dir.mkdir(parents=True, exist_ok=True)
    cwd = str(out_dir)
    run_input = out_dir / input_path.name
    # If running a repo example, copy all files from that example dir (e.g. ex2b.tsv, co2.dat) so phreeqc finds them
    try:
        if REPO_EXAMPLES_DIR.is_dir() and input_path.resolve().parent == REPO_EXAMPLES_DIR.resolve():
            for f in input_path.parent.iterdir():
                if f.is_file():
                    shutil.copy2(f, out_dir / f.name)
    except Exception:
        pass
    with open(input_path) as f:
        content = f.read()
    # Some repo examples require a specific database (ex15.dat, pitzer.dat, iso.dat)
    db_abs = None
    head = content[:2000]
    for pattern, path_resolver in [
        (r"must\s+use\s+database\s+([a-z0-9_.-]+\.dat)", lambda m: out_dir / m.group(1).strip()),
        (r"requires?\s+database\s+file\s+([a-z0-9_.-]+\.dat)", lambda m: out_dir / m.group(1).strip()),
        (r"database\s+file\s+([a-z0-9_.-]+\.dat)", lambda m: out_dir / m.group(1).strip()),
        (r"must\s+use\s+database\s+(pitzer\.dat)", lambda m: repo_root / "og" / "database" / m.group(1)),
        (r"must\s+use\s+database\s+(iso\.dat)", lambda m: repo_root / "og" / "database" / m.group(1)),
    ]:
        match = re.search(pattern, head, re.IGNORECASE)
        if match:
            resolved = path_resolver(match)
            if isinstance(resolved, Path) and resolved.exists():
                db_abs = str(resolved.resolve())
                break
    if db_abs is None and db_path.exists():
        db_abs = str(db_path.resolve())
    if db_abs:
        content = re.sub(
            r"^\s*DATABASE\s+[^\n]*\n?",
            "",
            content,
            flags=re.MULTILINE | re.IGNORECASE,
        )
        content = "DATABASE " + db_abs + "\n" + content.lstrip()
    with open(run_input, "w") as f:
        f.write(content)
    input_to_run = run_input
    log_stdout = out_dir / "phreeqc_stdout.txt"
    log_stderr = out_dir / "phreeqc_stderr.txt"
    print(f"[phreeqc] Running: {exe} {input_to_run} (cwd={cwd})", flush=True)
    try:
        with open(log_stdout, "w") as out, open(log_stderr, "w") as err:
            result = subprocess.run(
                [exe, str(input_to_run)],
                cwd=cwd,
                stdout=out,
                stderr=err,
                text=True,
                timeout=120,
                stdin=subprocess.DEVNULL,
            )
        if result.returncode != 0:
            err_text = log_stderr.read_text().strip() or log_stdout.read_text().strip() or f"Exit code {result.returncode}"
            lines = [ln.strip() for ln in err_text.splitlines() if ln.strip() and "PHREEQC" not in ln and "___" not in ln and len(ln.strip()) > 2]
            err_short = None
            for ln in lines:
                if "ERROR" in ln or "error:" in ln.lower() or "cannot open" in ln.lower() or "not found" in ln.lower():
                    err_short = ln[:300]
                    break
            if not err_short and lines:
                err_short = lines[-1][:300]
            if not err_short:
                err_short = err_text[:250] if len(err_text) > 250 else err_text
            if len(err_short) > 280:
                err_short = err_short[:277] + "..."
            print(f"[phreeqc] Failed: {err_text[:500]}", flush=True)
            return f"phreeqc failed: {err_short}"
        print(f"[phreeqc] Done. Output in {cwd}", flush=True)
        return f"Ran in {cwd}. Click Refresh to see charts."
    except FileNotFoundError:
        return "phreeqc not found. Build the project or add phreeqc to PATH."
    except subprocess.TimeoutExpired:
        return "Run timed out (2 min)."
    except Exception as e:
        print(f"[phreeqc] Error: {e}", flush=True)
        return str(e)


def _classify_graphic_type(chart: dict) -> tuple[Optional[str], Optional[str]]:
    """
    Best-effort classification of a USER_GRAPH JSON into a generic graphic type.
    Returns (type_id, label) or (None, None) if unknown.
    """
    title = (chart.get("chart_title") or "").strip()
    axis_titles = chart.get("axis_titles") or []
    x_title = (axis_titles[0] if len(axis_titles) > 0 else "") or ""
    y_title = (axis_titles[1] if len(axis_titles) > 1 else "") or ""
    t_low = title.lower()
    x_low = x_title.lower()
    y_low = y_title.lower()

    # These labels mirror the vocabulary used in the frontend.
    if "k-feldspar reaction path" in t_low:
        return "stability_field", "Phase / stability-field diagram"
    if "reaction path" in t_low:
        return "reaction_path", "Reaction path diagram"
    if "fluorite equilibrium" in t_low:
        return "solubility_curve", "Solubility curve"
    if "pyrite oxidation" in t_low:
        return "multi_dissolution", "Multi-curve stoichiometry / dissolution plot"
    if "log y" in t_low and "axis_scale log" in t_low:
        return "solubility_curve", "Solubility curve"
    if "angle, in degrees" in x_low and "sine(angle" in y_low:
        return "simple_xy", "Simple x–y function plot"
    if "eh" in y_low and "ph" in x_low:
        return "ph_eh", "pH–Eh diagram"
    return None, None


def _chart_entry(path: Path, rel_path: str, data_dir: Path, repo_root: Path) -> dict:
    """Build one chart list entry with path, name, source (example), title, and generic graphic type."""
    name = path.name
    try:
        # Source = parent dir name (e.g. ex5, all_manual_graphics) so list is clearer
        parent = path.parent.name
    except Exception:
        parent = ""
    title: Optional[str] = None
    graphic_type_id: Optional[str] = None
    graphic_type_label: Optional[str] = None
    try:
        with open(path) as f:
            data = json.load(f)
            t = data.get("chart_title")
            if isinstance(t, str) and t.strip():
                title = t.strip()
            type_id, type_label = _classify_graphic_type(data)
            graphic_type_id, graphic_type_label = type_id, type_label
    except Exception:
        title = None
    entry = {
        "path": rel_path,
        "name": name,
        "source": parent or None,
        "title": title,
    }
    if graphic_type_id and graphic_type_label:
        entry["graphic_type_id"] = graphic_type_id
        entry["graphic_type_label"] = graphic_type_label
    return entry


def _repo_example_names() -> set:
    """Set of repo example dir names (ex1, ex2b, ex22, ...) so we only show their charts."""
    if not REPO_EXAMPLES_DIR.is_dir():
        return set()
    return {p.stem for p in REPO_EXAMPLES_DIR.iterdir() if _is_repo_example_input(p)}


def _chart_sort_key(entry: dict) -> tuple:
    """Sort charts by example (ex1, ex2, ... ex12) then by graph number."""
    source = (entry.get("source") or "").lower()
    name = entry.get("name") or ""
    ex_key = _example_sort_key(source) if source.startswith("ex") else (999, source)
    num_match = re.search(r"phreeqc_user_graph_(\d+)\.json", name, re.IGNORECASE)
    graph_num = int(num_match.group(1)) if num_match else 0
    return (ex_key[0], ex_key[1], graph_num)


@app.route("/api/charts")
def list_charts():
    """List USER_GRAPH JSON from data/output, only from runs that match repo example names (no legacy uploads)."""
    valid_sources = _repo_example_names()
    files = []
    for d in [OUTPUT_DIR] + list(OUTPUT_DIR.iterdir()):
        if not d.is_dir():
            continue
        if valid_sources and d.name not in valid_sources:
            continue
        for p in d.glob("phreeqc_user_graph_*.json"):
            files.append(_chart_entry(p, p.relative_to(DATA_DIR).as_posix(), DATA_DIR, REPO_ROOT))
    for p in DATA_DIR.rglob("phreeqc_user_graph_*.json"):
        if valid_sources and p.parent.name not in valid_sources:
            continue
        rel = p.relative_to(DATA_DIR).as_posix()
        if not any(f["path"] == rel for f in files):
            files.append(_chart_entry(p, rel, DATA_DIR, REPO_ROOT))
    files.sort(key=_chart_sort_key)
    return jsonify({"charts": files})


@app.route("/api/charts/<path:subpath>")
def get_chart(subpath):
    """Serve chart JSON from data/ or from manual_examples/ (path prefix manual_examples/)."""
    if subpath.startswith("manual_examples/"):
        path = (REPO_ROOT / subpath).resolve()
        try:
            path.relative_to(REPO_ROOT.resolve())
        except ValueError:
            return jsonify({"error": "Not found"}), 404
    else:
        path = (DATA_DIR / subpath).resolve()
        try:
            path.relative_to(DATA_DIR.resolve())
        except ValueError:
            return jsonify({"error": "Not found"}), 404
    if not path.is_file():
        return jsonify({"error": "Not found"}), 404
    with open(path) as f:
        data = json.load(f)
    return jsonify(data)


@app.route("/data/<path:subpath>")
def data_file(subpath):
    """Serve a file from data/ or manual_examples/ (prefix manual_examples/)."""
    if subpath.startswith("manual_examples/"):
        rest = subpath[len("manual_examples/"):].lstrip("/")
        return send_from_directory(
            MANUAL_EXAMPLES_DIR,
            rest,
            mimetype="application/json",
        )
    return send_from_directory(DATA_DIR, subpath, mimetype="application/json")


# Repo examples use no extension (ex1, ex5, ex20a). Short descriptions for tooltips.
EXAMPLE_DESCRIPTIONS = {
    "ex1": "Speciation — seawater with uranium",
    "ex2": "Gypsum/anhydrite solubility vs temperature",
    "ex2b": "Gypsum/anhydrite 30–170 °C, 1–1000 atm",
    "ex3": "Mixing — calcite equilibrium",
    "ex4": "Evaporation of rainwater; homogeneous redox",
    "ex5": "Pyrite oxidation (USER_GRAPH)",
    "ex6": "Reaction-path (6A–6C)",
    "ex7": "Gas-phase — organic decomposition",
    "ex8": "Surface complexation — Zn on Fe oxides",
    "ex9": "Kinetic Fe²⁺ oxidation",
    "ex10": "Aragonite–strontianite solid solution",
    "ex11": "1D transport, cation exchange",
    "ex12": "Advective–diffusive transport",
    "ex12a": "Advective–diffusive (variant a)",
    "ex12b": "Advective–diffusive (variant b)",
    "ex13a": "Dual-porosity — implicit mixing",
    "ex13ac": "Dual-porosity — combined",
    "ex13b": "Dual-porosity — explicit mixing",
    "ex13c": "Dual-porosity — finite-difference",
    "ex14": "Transport with phases, exchange, surface",
    "ex15": "1D transport: biodegradation, sorption",
    "ex15a": "1D transport (variant a)",
    "ex15b": "1D transport (variant b)",
    "ex16": "Inverse modeling — Sierra springs",
    "ex17": "Inverse modeling — Black Sea",
    "ex17b": "Inverse modeling with isotopes",
    "ex18": "Inverse modeling — Madison Aquifer",
    "ex19": "Cd²⁺ sorption isotherms",
    "ex19b": "Cd sorption on X, Hfo, OC",
    "ex20a": "Carbonate solid-solution equilibria",
    "ex20b": "Isotope evolution ¹³C/¹²C",
    "ex21": "Multicomponent diffusion — Opalinus Clay",
    "ex22": "CO₂ solubility, high P (Peng–Robinson)",
}


def _example_label(name: str) -> str:
    """Return button label: Ex. 1, Ex. 5, Ex. 20a, etc."""
    base = name.lower()
    if base.startswith("ex"):
        return "Ex. " + base[2:]
    return base


def _example_sort_key(name: str):
    """Sort key so ex1, ex2, ex2b, ... ex9, ex10, ... ex22."""
    base = name.lower()
    if base.startswith("ex"):
        rest = base[2:]
        num_part = ""
        for c in rest:
            if c.isdigit():
                num_part += c
            else:
                letter_part = rest[len(num_part):]
                return (int(num_part) if num_part else 0, letter_part)
        return (int(num_part) if num_part else 0, "")
    return (0, base)


def _is_repo_example_input(p: Path) -> bool:
    """True if path is an example input file in repo examples/ (ex1, ex5, ex20a, no extension)."""
    return p.is_file() and not p.suffix and re.match(r"^ex\d+[a-z]*$", p.name, re.IGNORECASE)


@app.route("/api/examples")
def list_examples():
    """List input files from repo examples/ (extensionless: ex1, ex5, ex20a, ...)."""
    examples = []
    if REPO_EXAMPLES_DIR.is_dir():
        files = [p for p in REPO_EXAMPLES_DIR.iterdir() if _is_repo_example_input(p)]
        files.sort(key=lambda p: _example_sort_key(p.name))
        for p in files:
            has_graph = False
            try:
                text = (p.read_text(encoding="utf-8", errors="ignore") or "").upper()
                has_graph = "USER_GRAPH" in text
            except Exception:
                has_graph = False
            examples.append({
                "name": p.name,
                "label": _example_label(p.name),
                "description": EXAMPLE_DESCRIPTIONS.get(p.name.lower(), ""),
                "has_graph": has_graph,
            })
    return jsonify({"examples": examples})


@app.route("/api/run-example", methods=["POST"])
def run_example():
    """Run phreeqc on a file from og/examples/; output to rrt_webapp data/output/<stem>/ so charts plot."""
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or data.get("path") or request.form.get("name") or "").strip()
    if not name or name != os.path.basename(name):
        return jsonify({"error": "Invalid example name"}), 400
    input_path = REPO_EXAMPLES_DIR / name
    if not input_path.is_file():
        return jsonify({"error": f"Example not found: {name}"}), 404
    msg = run_phreeqc(input_path, output_dir=OUTPUT_DIR)
    # If phreeqc failed, return error response (no "No charts" suffix)
    if msg.startswith("phreeqc failed") or msg.startswith("phreeqc not found") or "timed out" in msg.lower():
        return jsonify({"error": msg}), 422
    run_output_dir = OUTPUT_DIR / input_path.stem
    chart_files = sorted(run_output_dir.glob("phreeqc_user_graph_*.json")) if run_output_dir.is_dir() else []
    chart_count = len(chart_files)
    first_chart_path = None
    if chart_files:
        first_chart_path = chart_files[0].relative_to(DATA_DIR).as_posix()
        msg = f"{msg} {chart_count} chart(s) — chart list updates automatically."
    else:
        msg = f"{msg} No charts (this example has no USER_GRAPH)."
    out = {"message": msg, "charts_created": chart_count}
    if first_chart_path:
        out["first_chart_path"] = first_chart_path
    return jsonify(out)


@app.route("/uploads")
def list_uploads():
    """List uploaded input files."""
    names = [p.name for p in UPLOAD_DIR.iterdir() if p.is_file()]
    return jsonify({"uploads": sorted(names)})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
