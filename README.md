# Hand-Eye Calibration Benchmark

Bachelor's thesis project in Applied Mathematics at Hochschule Darmstadt.
A comparison of the five OpenCV hand-eye implementations using controlled synthetic data, recorded DENSO robot motions and held-out laboratory images.

The manuscript preserves the original thesis structure and formatting: the introduction covers motivation, the research question, scope and a reading guide; the five OpenCV methods form a focused theoretical framework; simulation, laboratory processing, results and conclusions follow. Every main chapter and appendix starts on a new page. General coordinate-algebra tutorials have been removed, and full condition summaries are printed in the appendices.

- [Compiled thesis](paper/main.pdf)
- [LaTeX source](paper/main.tex)
- [Experiment record](EXPERIMENT.md)
- [Source and result provenance](docs/citation-map.md)

## Methods and implemented geometry

The evaluated implementations in OpenCV 4.12.0 are Tsai-Lenz, Park-Martin, Horaud-Dornaika, Andreff-Horaud-Espiau and Daniilidis. All methods receive the same observations within each trial.

The camera is stationary and the target is rigidly attached to the tool frame. A transform maps coordinates from its subscript frame into its superscript frame. Write `G = base_T_gripper`, `M = gripper_T_target`, `Y = base_T_camera` and `C = camera_T_target`. The observation chain is `G @ M = Y @ C`. OpenCV receives `inverse(G)` and `C`; its returned transform is interpreted as `Y` for this eye-to-hand arrangement. See the [OpenCV API](https://docs.opencv.org/4.12.0/d9/d0c/group__calib3d.html) and the [inspected 4.12.0 implementation](https://github.com/opencv/opencv/blob/4.12.0/modules/calib3d/src/calibration_handeye.cpp).

## Run the numerical experiments

Use Python 3.12 and the pinned numerical dependencies:

```bash
python -m pip install -r requirements.txt
python benchmark.py --model poses --trials 100 --seed 42 --output outputs/poses
python benchmark.py --model pixels --trials 100 --seed 42 --output outputs/pixels
python laboratory.py Data4Osinchuk.zip --trials 100 --seed 42 --output outputs/laboratory
python circle_diagnostic.py Data4Osinchuk.zip
```

`Data4Osinchuk.zip` is the separately supplied original acquisition archive. The two generic benchmarks run without it. Outputs go into ignored `outputs/` folders. Recorded summaries are in `results/`.

| Experiment | Conditions | Attempts or predictions |
| --- | ---: | ---: |
| Generic pose model | 27, each with 5 methods | 13,500 method attempts |
| Generic pixel/PnP model | 27, each with 5 methods | 13,500 method attempts |
| Recorded DENSO trajectory replay | 12, each with 5 methods | 6,000 method attempts |
| June and July held-out validation | 15 + 18 views, each with 5 methods | 165 predictions |

The generic benchmark uses 8, 16 and 32 poses; diverse, narrow and nearly single-axis rotation-vector profiles; and exact, low and high noise. Its target has 35 inner corners with 20 mm spacing and its image size is 4096 x 3000 pixels. `poses` perturbs complete robot and camera-side target poses. `pixels` perturbs the robot pose and projected image coordinates, then recovers the target pose with iterative PnP. Physical pixel pitch, image rasterisation, detector failures and robot reachability are not modelled.

The replay uses 20 recorded robot poses and 88 checkerboard corners at 12 mm spacing. A nominal camera/mount fit from 18 accepted July images defines the simulated truth. It is not an independently surveyed physical reference. The original July image dimensions are 4112 x 3008 pixels. The fitted nominal matrices and distortion coefficients are in [geometry_metadata.json](results/thesis/geometry_metadata.json).

Each trial reuses the same seeded observations across methods. Shorter subsets are nested. `summary.csv` reports error medians and 95th percentiles for valid transforms and counts rejected outputs separately. Large finite errors remain included. Narrow-motion Tsai failures and very large nearly single-axis Daniilidis translation tails are part of the results, so there is no universal winning method.

## Laboratory records and diagnostics

The June ODS parser applies eight explicitly logged inferred decimal-separator corrections. July checkerboard photographs P47 and P48 have identical bytes with different robot labels, so both are excluded from real-image fitting and scoring. The raw held-out prediction rows and corrections are now committed in `results/thesis/`.

All camera intrinsics, distortion, hand-eye and mount parameters are fitted on training observations only within each leave-one-pose-out fold. Image scores measure prediction consistency. The archive does not provide an independently measured camera pose.

The circular-target diagnostic detects nine of eleven grids. Pose-ID pairing gives a median relative rotation-angle discrepancy of 0.077 degrees and maximum 0.383 degrees. Its current naive row-order baseline gives 13.989 degrees and maximum 60.897 degrees, but does not preserve raw-row pairing when detections fail. A separate audit pairing before detection filtering gives median 12.997 degrees and maximum 46.441 degrees. These are rotation-only diagnostics; physical circle spacing and the full circular-target hand-eye transform remain unvalidated. The manuscript describes this limitation without treating a diagnostic baseline as a proven cause of the historical failure.

The real-validation loop currently stops on a solver exception; all 165 recorded predictions completed. Automated regression tests and CI for the numerical pipeline have not been added.

## Regenerate the thesis tables and figures

From the repository root:

```bash
python -m pip install -r requirements.txt -r requirements-paper.txt
python scripts/build_paper_results.py
```

This formats the recorded summaries, recomputes `results/thesis/real_summary.csv` from the committed per-view records, and rebuilds `paper/generated/` and `paper/figures/`. It does not rerun calibration or require the original image archive. The PDF includes 270 controlled condition rows, 60 replay rows, the laboratory summaries and the June correction log. Plotting uses Matplotlib 3.10.8, kept separate from the numerical experiment requirements.

## Build the LaTeX document

The paper uses pdfLaTeX with numbered BibTeX references. A TeX installation with the packages listed in `paper/main.tex`, Latin Modern fonts and German Babel support is sufficient. Biber and Ukrainian font packages are no longer required by this shortened manuscript.

```bash
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Or run `pdflatex main.tex`, `bibtex main`, then `pdflatex main.tex` twice. For Overleaf, upload the contents of `paper/` preserving `generated/` and `figures/`, and select pdfLaTeX. The committed tables and figures make the paper self-contained for a LaTeX build.

The numerical source revision used for the recorded experiments is `4091828055efe2b13eefb3d59bc8756474ed5b2c`. The source code was reviewed and rerun with NumPy 2.2.6 and OpenCV 4.12.0. The 270 controlled summaries, 60 replay summaries and ten laboratory summary rows were reproduced. The [verification record](docs/reproducibility-check.md) distinguishes these checks from unvalidated physical accuracy.

## Author

Yana Osinchuk - B.Sc. Applied Mathematics, Hochschule Darmstadt.
