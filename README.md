# PHREEQC ![workflow](https://github.com/usgs-coupled/phreeqc3/actions/workflows/cmake.yml/badge.svg)

**This repo is organized into two main folders:** **`og/`** — original app from the authors (sources, examples, database, doc; at root, `examples` is a symlink to `og/examples`). **`rrt_webapp/`** — Flask webapp for running examples and viewing USER_GRAPH charts. Build from repo root: `cmake -S og -B build && cmake --build build`. See `og/README.md` and `rrt_webapp/README.md`.

## Description

PHREEQC Version 3 is a computer program written in the C++ programming language 
that is designed to perform a wide variety of aqueous geochemical calculations. 
PHREEQC implements several types of aqueous models including two ion-association aqueous models. 

## Disclaimer

This software is preliminary or provisional and is subject to revision. It is
being provided to meet the need for timely best science. The software has not
received final approval by the U.S. Geological Survey (USGS). No warranty,
expressed or implied, is made by the USGS or the U.S. Government as to the
functionality of the software and related material nor shall the fact of release
constitute any such warranty. The software is provided on the condition that
neither the USGS nor the U.S. Government shall be held liable for any damages
resulting from the authorized or unauthorized use of the software.
