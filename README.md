# Hand–Eye Calibration Benchmark

Bachelor’s thesis project in Applied Mathematics at Hochschule Darmstadt.
An experimental comparison of OpenCV hand-eye calibration methods using synthetic data and laboratory robot measurements.

**Status: work in progress.** The repository contains the theoretical thesis draft and a runnable synthetic eye-to-hand benchmark. Laboratory validation covers the June and July checkerboard series.

## Research question

A camera and a robot describe positions in different coordinate systems. Hand-eye calibration estimates the fixed transformation connecting those descriptions [1].
The central equation is

$$
A_i X = X B_i,
$$

where $A_i$ and $B_i$ are corresponding relative motions and $X$ is the unknown rigid transformation [1].

The project will investigate how five calibration methods differ in accuracy, validation consistency and repeatability, and how those differences depend on the number and diversity of acquisition poses.

## Methods to compare

The benchmark uses the five methods provided by OpenCV’s `calibrateHandEye` interface [2]:

- Tsai–Lenz
- Park–Martin
- Horaud–Dornaika
- Andreff–Horaud–Espiau
- Daniilidis

All methods receive the same observations and preprocessing. Rotation and translation errors are reported separately.

## Repository contents

| Path | Contents |
| --- | --- |
| `README.md` | Project scope, current status and next steps |
| `.gitignore` | Exclusions for Python caches, LaTeX build products and temporary outputs |
| `benchmark.py` | Synthetic eye-to-hand simulation and Monte Carlo evaluation |
| `requirements.txt` | Pinned dependencies for reproducing the simulation |
| `paper/main.tex` | Complete LaTeX thesis draft, including mathematical derivations and the proposed experimental protocol |
| `paper/references.bib` | Bibliography for the thesis |
| `docs/citation-map.md` | Source locations and provenance of the displayed formulas and worked examples |
| `paper/Logo-Hochschule-Darmstadt.png` | University logo used by the title page |

## Run the synthetic benchmark

Use Python 3.12. All five methods receive the same observations in every trial.

```bash
python -m pip install -r requirements.txt
python benchmark.py --model poses --trials 100 --seed 42 --output outputs/poses
python benchmark.py --model pixels --trials 100 --seed 42 --output outputs/pixels
```

The camera is fixed relative to the robot base. A 7 × 5 grid of inner corners with 20 mm spacing is fixed relative to the gripper. With the convention that a transform maps from its subscript frame into its superscript frame, write `G = base_T_gripper`, `X = gripper_T_target`, `Y = base_T_camera`, and `C = camera_T_target`. The simulator constructs poses satisfying `G @ X = Y @ C`. OpenCV receives `inverse(G)` and `C`; the returned estimate is `Y` for this eye-to-hand arrangement [2].

| Factor | Values |
| --- | --- |
| Acquisition poses | 8, 16, 32 |
| Orientation profile | Isotropic rotation-vector standard deviation of 22° (diverse) or 4° (narrow), or per-axis standard deviations of 0.5°, 0.5°, and 22° (nearly single-axis) |
| Pose noise (standard deviations per component) | Exact, low (0.1° and 0.5 mm), high (0.5° and 2 mm) |
| Pixel noise (standard deviation per coordinate) | Exact, low (0.25 px), high (1 px) |

The `poses` model independently perturbs robot and camera-side target poses. The `pixels` model perturbs robot poses and projects the target through a fixed pinhole camera, adds pixel noise, and recovers camera-side poses with `solvePnP`. Distortion, uncertainty in intrinsics, and physical robot reachability are outside this simulation. Each trial uses the same seeded random draws across conditions, and shorter pose sets are prefixes of longer ones.

`trials.csv` contains the angular error and Euclidean translation error against the known camera pose, plus solver status. `summary.csv` reports medians and 95th percentiles for valid estimates and counts failed estimates. A fallback identity transform counts as a failure because the simulated true transform is nonidentity. A valid transform can still have a large error, so compare both error distributions and failure counts. Nominal pixel-mode trials still perform numerical PnP, even with exactly zero pixel noise.

## Build the thesis

Use a TeX installation containing pdfLaTeX, Biber, biblatex, PGFPlots, listings, German and Ukrainian Babel language files, and T2A Cyrillic fonts (for example CM-Super). The Ukrainian bibliography preserves the original titles and author names.

```bash
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Alternatively:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
biber main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

For Overleaf, upload the files inside `paper/` into the project root and select pdfLaTeX. The source uses Biber and refers to the logo as `Logo-Hochschule-Darmstadt.png`.

The manuscript is a working draft. Examiner names, the final declaration of authorship, hardware specifications and experimental findings remain to be completed.

## Planned experiments

1. Generate synthetic robot and camera poses from a known rigid transformation and verify calibration on exact data.
2. Compare rotation and translation errors under controlled measurement noise using repeated trials and recorded random seeds.
3. Vary the pose count and the diversity of orientations and positions.
4. Acquire laboratory observations using a documented camera, robot and calibration-target setup.
5. Evaluate repeatability and consistency on held-out observations; report absolute laboratory accuracy when an independent reference is available.

Finite solver outputs will be checked for valid rigid transformations. Numerical failures will be recorded explicitly. Coordinate conventions, translation units and the installed OpenCV version will be documented with the experiments.

## Starting references

- Peter Corke, *Robotics, Vision and Control*: [author’s book overview](https://petercorke.com/books/robotics-vision-control-all-versions/).
- Roger Y. Tsai and Reimar K. Lenz, *A New Technique for Fully Autonomous and Efficient 3D Robotics Hand/Eye Calibration* (1989): [IEEE](https://ieeexplore.ieee.org/document/34770), DOI `10.1109/70.34770`.
- OpenCV, [`calibrateHandEye` documentation](https://docs.opencv.org/5.0/main_modules/calib.html#calibratehandeye).

The thesis bibliography also includes the original papers for the other compared methods, the inspected OpenCV source and David Marr’s *Vision*. German robotics and numerical-algebra texts and two Ukrainian textbooks support the mathematical foundations. See the [citation map](docs/citation-map.md) for the passages used and for the distinction between source relations and calculations constructed in this thesis.

The thesis uses plain numbered citations. A subsection that mainly draws on the same source cites it once in its closing paragraph; references for distinct material and direct quotations remain beside the relevant discussion. Worked examples cite their underlying mathematical relations. Draft-only instructions, provisional experiment plans and empty chapter headings are preserved as LaTeX comments and do not appear in the PDF.

[1] Stefan Wenhardt, *Ansichtenauswahl für die 3-D-Rekonstruktion statischer Szenen* (2013), Section 2.3: [German dissertation](https://www5.cs.fau.de/fileadmin/research/Publikationen/2013/Wenhardt13-AFD.pdf).

[2] OpenCV, [`calibrateHandEye` documentation](https://docs.opencv.org/5.0/main_modules/calib.html#calibratehandeye).

## Author

Yana Osinchuk — B.Sc. Applied Mathematics, Hochschule Darmstadt.


## Professor's DENSO data

Run the paired trajectory simulation and leave-one-pose-out image validation with the original archive.

```bash
python laboratory.py Data4Osinchuk.zip --output outputs/thesis --trials 100 --seed 42
```

See `EXPERIMENT.md` for the dataset audit, scoring rules and run results.

The published summaries and comparison figure are in [results](results/). Running the commands above regenerates the trial-level CSV files. The laboratory command uses the separately supplied archive. The synthetic benchmark runs without it.

Run `python circle_diagnostic.py Data4Osinchuk.zip` to compare pose-ID pairing and row-order pairing for the July circular target. On nine detected grids, the median relative rotation discrepancy was 0.077° with pose-ID pairing and 13.989° with row-order pairing. This diagnostic tests rotation consistency only. The physical circle spacing and full circular-target hand–eye transform were not validated.
