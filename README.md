# Hand–Eye Calibration Benchmark

Bachelor’s thesis project in Applied Mathematics at Hochschule Darmstadt.
An experimental comparison of OpenCV hand-eye calibration methods using synthetic data and laboratory robot measurements.

**Status: work in progress.** This initial version contains the theoretical thesis draft. The Python benchmark, synthetic experiments and laboratory evaluation are planned; measured comparison results are not yet available.

## Research question

A camera and a robot describe positions in different coordinate systems. Hand-eye calibration estimates the fixed transformation connecting those descriptions [1].
The central equation is

$$
A_i X = X B_i,
$$

where $A_i$ and $B_i$ are corresponding relative motions and $X$ is the unknown rigid transformation [1].

The project will investigate how five calibration methods differ in accuracy, validation consistency and repeatability, and how those differences depend on the number and diversity of acquisition poses.

## Methods to compare

The planned benchmark will use the five methods provided by OpenCV’s `calibrateHandEye` interface [2]:

- Tsai–Lenz
- Park–Martin
- Horaud–Dornaika
- Andreff–Horaud–Espiau
- Daniilidis

All methods will receive the same observations and preprocessing. Rotation and translation errors will be reported separately.

## Repository contents

| Path | Contents |
| --- | --- |
| `README.md` | Project scope, current status and next steps |
| `.gitignore` | Exclusions for Python caches, LaTeX build products and temporary outputs |
| `paper/main.tex` | Complete LaTeX thesis draft, including mathematical derivations and the proposed experimental protocol |
| `paper/references.bib` | Bibliography for the thesis |
| `docs/citation-map.md` | Source locations and provenance of the displayed formulas and worked examples |
| `paper/Logo-Hochschule-Darmstadt.png` | University logo used by the title page |

Python modules, experiment scripts and datasets will be added as they are implemented.

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

