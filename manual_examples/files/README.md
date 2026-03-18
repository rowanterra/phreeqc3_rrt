# PHREEQC Version 3 — Example Input Files

Extracted from: Parkhurst, D.L. and Appelo, C.A.J., 2013, *Description of input and examples for PHREEQC version 3*, USGS Techniques and Methods 6–A43.

## Relationship to repo `examples/`

The **official** PHREEQC examples live in the repo at [examples/](https://github.com/rowanterra/phreeqc3_rrt/tree/master/examples). They use **no file extension** (e.g. `ex1`, `ex5`, `ex20a`) and **lowercase** variant names (`ex13a`, `ex20a`, `ex20b`).

This folder (`manual_examples/files/`) contains **manual-extracted** versions with a `.pqi` extension and some **capital** variant names (`ex13A.pqi`, `ex20A.pqi`) to match the manual. They are **not** identical to the repo:

| Repo `examples/` | `manual_examples/files/` |
|------------------|--------------------------|
| No extension (`ex1`, `ex5`) | `.pqi` extension (`ex1.pqi`, `ex5.pqi`) |
| Lowercase variants (`ex20a`, `ex13a`) | Capital variants (`ex20A.pqi`, `ex13A.pqi`) |
| Has **ex12a**, **ex12b**, **ex13ac**, **ex15a**, **ex15b** | **Missing** these five (only ex12, ex13A/B/C, ex15 here) |
| One input per example | Same + **all_manual_graphics.pqi** (combined USER_GRAPH demo) |

Content is very similar (e.g. ex5 vs ex5.pqi); use repo `examples/` when you want the canonical PHREEQC distribution inputs.

## Files

| File | Example | Description |
|------|---------|-------------|
| ex1.pqi | 1 | Speciation — seawater with uranium |
| ex2.pqi | 2 | Temperature dependence of gypsum/anhydrite solubility |
| ex2B.pqi | 2B | Gypsum/anhydrite transitions, 30–170 °C, 1–1000 atm |
| ex3.pqi | 3 | Mixing — calcite equilibrium |
| ex4.pqi | 4 | Evaporation of rainwater; homogeneous redox |
| ex5.pqi | 5 | Irreversible reactions — pyrite oxidation |
| ex6.pqi | 6 | Reaction-path calculations (6A–6C) |
| ex7.pqi | 7 | Gas-phase calculations — organic decomposition |
| ex8.pqi | 8 | Surface complexation — Zn on hydrous iron oxides |
| ex9.pqi | 9 | Kinetic oxidation of dissolved Fe²⁺ with O₂ |
| ex10.pqi | 10 | Aragonite–strontianite solid solution |
| ex11.pqi | 11 | 1D transport with cation exchange |
| ex12.pqi | 12 | Advective–diffusive transport of heat and solutes |
| ex13A.pqi | 13A | Dual-porosity transport — implicit mixing factors |
| ex13B.pqi | 13B | Dual-porosity transport — explicit mixing factors |
| ex13C.pqi | 13C | Dual-porosity transport — finite-difference diffusion |
| ex14.pqi | 14 | Transport with equilibrium phases, exchange, and surface |
| ex15.pqi | 15 | 1D transport: kinetic biodegradation, cell growth, sorption |
| ex16.pqi | 16 | Inverse modeling — Sierra springs |
| ex17.pqi | 17 | Inverse modeling — Black Sea evaporation |
| ex17B.pqi | 17B | Inverse modeling with isotopes |
| ex18.pqi | 18 | Inverse modeling — Madison Aquifer |
| ex19.pqi | 19 | Cd²⁺ sorption: linear, Freundlich, Langmuir isotherms |
| ex19B.pqi | 19B | Cd sorption on X, Hfo, and OC in loamy soil |
| ex20A.pqi | 20A | Carbonate solid-solution equilibria |
| ex20B.pqi | 20B | Isotope evolution — ¹³C/¹²C fractionation |
| ex21.pqi | 21 | Multicomponent diffusion through Opalinus Clay |
| ex22.pqi | 22 | CO₂ solubilities at high pressures (Peng–Robinson EOS) |
| all_manual_graphics.pqi | — | **All USER_GRAPH types** (manual Examples 1–2, Fig. 3, Pyrite-style, log Y); produces 5 charts |

## Usage

```bash
phreeqc ex1.pqi ex1.out phreeqc.dat
```

Or with a specific database:
```bash
phreeqc ex22.pqi ex22.out pitzer.dat
```

**USER_GRAPH charts:** The webapp discovers chart JSON under `manual_examples/` as well as under `webapp/data/`. To generate the all-graphics example and have its charts show in the webapp, from repo root run:

```bash
./webapp/run_all_manual_graphics.sh
```

Charts are written to `manual_examples/output/all_manual_graphics/`. Start the webapp and click **Refresh** to list and view them.

## Notes

- These files were extracted from the PDF via text extraction and may contain minor formatting artifacts (e.g., extra leading whitespace in ex21). PHREEQC is whitespace-tolerant, so files should run correctly.
- Example 9 is a *partial* input file per the manual — it requires additional RATES block definitions.
- SOLUTION_SPREAD tables (ex16, etc.) use tab-delimited columns.
- The official example files are also distributed with PHREEQC itself at https://www.usgs.gov/software/phreeqc-version-3
