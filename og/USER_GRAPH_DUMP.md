# USER_GRAPH dump on Mac/Linux (no ZedGraph)

On Windows, PHREEQC uses ZedGraph (/.NET) to draw USER_GRAPH charts. On Mac and Linux there is no GUI; this build uses **USER_GRAPH_DUMP** to write the same graph data to **JSON files** so an external viewer can plot them.

## Build

- **Windows (MSVC):** Chart sources are `ChartHandler.cpp`, `ChartObject.cpp`, `CurveObject.cpp`. ClrRelease/ClrDebug define `MULTICHART` and use ZedGraph.
- **Mac/Linux (CMake):** Chart sources are `ChartHandlerDump.cpp`, `ChartObjectDump.cpp`, `CurveObject.cpp`. CMake defines `USER_GRAPH_DUMP`; no .NET or ZedGraph.

Configure and build with CMake as usual. On non-Windows hosts, `USER_GRAPH_DUMP` is defined and the dump path is compiled.

## Output files

For each USER_GRAPH that runs, a file is written at **run end** (when charts are “detached”):

- **Filename:** `phreeqc_user_graph_<n_user>.json` (e.g. `phreeqc_user_graph_1.json`)
- **Location:** current working directory when PHREEQC exits

## JSON format

Each file describes one chart:

| Field | Description |
|-------|-------------|
| `chart_title` | Title from `-chart_title` |
| `axis_titles` | Array of axis title strings from `-axis_titles` |
| `axis_scale_x` | `[min, max, ...]` or `"auto"`, optional `"log"` |
| `axis_scale_y` | Same for primary Y |
| `axis_scale_y2` | Same for secondary Y (sy) |
| `plot_tsv_file` | Array of overlay file paths from `-plot_tsv_file` |
| `series` | Array of series; each has `id`, `color`, `symbol`, `y_axis`, `x`, `y` (arrays of numbers) |

Series come from:

- `graph_x` / `graph_y` / `graph_sy` in the USER_GRAPH Basic script
- `PLOT_XY` in the script
- `-plot_tsv_file` overlay data (in `CurvesCSV`)

## Viewing

Use any JSON-capable plotter (Python/matplotlib, R, Excel, or a small script) to read these files and draw the chart. Axis scales and titles are preserved so you can match the intended axis ranges and log/linear scaling.

## Code layout

- **ChartObject.h**  
  Used for both MULTICHART and USER_GRAPH_DUMP. ZedGraph-specific API (e.g. `Return_SymbolType`) is under `#if defined(MULTICHART)`; `DumpChartToFile()` is under `#ifdef USER_GRAPH_DUMP`.

- **ChartObjectDump.cpp**  
  ChartObject implementation when `USER_GRAPH_DUMP` is set: same parsing and curve logic as the Windows path, but no Form1/ZedGraph; `start_chart()` only sets flags; `DumpChartToFile()` writes the JSON.

- **ChartHandlerDump.cpp**  
  ChartHandler implementation for USER_GRAPH_DUMP: no .NET threading; at `End_timer()` it calls `DumpChartToFile()` on each chart, then frees resources.

- **CurveObject.cpp**  
  Built for both MULTICHART and USER_GRAPH_DUMP.

- **read.cpp, print.cpp, PBasic.cpp, Phreeqc.h/cpp, ReadClass.cxx, readtr.cpp, structures.cpp**  
  USER_GRAPH handling (read, punch, Basic tokens, chart_handler) is enabled for both `MULTICHART` and `USER_GRAPH_DUMP` via `#if defined(MULTICHART) || defined(USER_GRAPH_DUMP)` (or the equivalent with `PHREEQ98` where applicable).
