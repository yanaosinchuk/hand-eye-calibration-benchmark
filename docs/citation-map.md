# Manuscript source and result provenance

The manuscript retains the original introduction, title-page presentation, Latin Modern typography, default article page layout, paragraph spacing and thesis structure. Every main chapter and appendix starts on a fresh page. The five OpenCV hand-eye methods form the shortened theoretical framework. General matrix algebra, basic coordinate tutorials, worked foundation examples and their former 104-equation inventory have been removed. Numeric citations are generated with natbib and BibTeX (`unsrtnat`). A subsection's shared source is normally cited once in its closing paragraph; distinct sources remain beside the relevant discussion.

## Introduction

The motivation, research question, scope and reading guide are retained as a separate introduction. `marr2010` supports the original attributed opening quotation; `wenhardtde`, `tsai` and `halconde` support the calibration setting. `eauncertainty` distinguishes physical repeatability and reference-based accuracy from the numerical sensitivity and held-out consistency that were actually evaluated. The personal preface is restored verbatim from the initial manuscript.

## Method and implementation claims

| Key | Used for |
| --- | --- |
| `tsai` | Tsai-Lenz quaternion-vector rotation system and separate translation fit |
| `park` | Park-Martin rotation-logarithm alignment |
| `horaud` | Horaud-Dornaika quaternion eigenproblem; the implemented separable method is distinguished from other procedures in the original article |
| `andreff` | Joint linear rotation/translation system with row-wise vectorisation |
| `daniilidis` | Dual-quaternion constraints and coupled calibration |
| `opencv` | Camera calibration, projection, PnP, hand-eye input/output conventions and feature-refinement interfaces |
| `opencvsource` | Actual OpenCV 4.12.0 solver behaviour, including Tsai thresholds/identity fallback, Park inverse square root, Andreff normalisation and Daniilidis SVD/quadratic construction |
| `halconde` | Fixed-camera/fixed-mount geometric chain and acquisition conventions |
| `eauncertainty` | Distinction between reference-based error, observation consistency and repeated acquisition; correlated observations |

The inspected OpenCV source is `modules/calib3d/src/calibration_handeye.cpp` at tag `4.12.0`, blob `cd4999a61831d7cf20831ed7ffd138194be49a73`. The former bibliography pointed to a 5.x source snapshot. The current citation matches the installed experiment version; the mathematical routines were compared with that earlier snapshot and the observed differences were source syntax rather than solver mathematics.

The principal method equations are adapted to the manuscript's conventions. The common rotation/translation relation and all five method formulations are attributed to original papers and/or the inspected implementation. No new independent solver implementation is claimed.

## Experiment and dataset claims

| Key | Evidence |
| --- | --- |
| `experimentcode` | Numerical source revision `4091828055efe2b13eefb3d59bc8756474ed5b2c`, published condition CSVs, reproduced output records, current paper tables and generation script |
| `laboratoryarchive` | Supplied `Data4Osinchuk.zip`: dated acquisition journals, ODS/July robot tables, photographs, and the MATLAB `Rz Ry Rx` conversion example |
| `lectureplan` | User-supplied screenshots at 12:33, 14:01, 14:23, 14:33, 16:20 and 16:29; supplied on 19 November 2026, with recording date not established |

Simulation camera/target values, random distributions, noise levels, validity rules and error metrics are experiment definitions, not manufacturer specifications. Numeric result claims come from the recorded CSVs. The pose and replay angle formula is the `atan2` expression in `pose_error`, matching the code rather than the old manuscript's equivalent `acos` presentation.

The screenshot camera rotation/translation is distinguished from the actual generic benchmark: the centres agree and orientations differ by six degrees. The replay uses a full-data nominal fit only to define its synthetic world; held-out scoring refits everything within each training fold. The chapter states that literal reproduction of all handwritten numerical camera parameters has not been performed.

June's eight decimal corrections are explicitly inferred. P47/P48 duplication was verified by image bytes. The circular-target unit grid supports only an angle-based check. The naive row-order comparison has a detection-filtering issue, and the alternate 12.997-degree result is labelled as a separate audit rather than silently replacing the current script's 13.989-degree output.

## Recorded outputs and manuscript locations

| Recorded evidence | Manuscript use |
| --- | --- |
| `results/poses/summary.csv`, `results/pixels/summary.csv` | Controlled results, failure totals, sensitivity figure and all 270 condition rows in the appendix |
| `results/thesis/summary.csv` | Replay low-noise table, pose-count figure and all 60 replay condition rows |
| `results/thesis/held_out.csv`, `june_held_out.csv` | 165 held-out predictions, recomputed ten-row real summary, laboratory result table and figure |
| `results/thesis/june_corrections.csv` | Complete eight-entry correction table |
| `results/thesis/geometry_metadata.json` | Full July nominal intrinsics, distortion, camera/mount transforms and fit pose IDs |
| `docs/reproducibility-check.md` | Rerun scope, source revision, exact numerical comparison and geometric checks |

The title, declaration, personal preface, research objective and conclusions are author statements. Sources do not establish laboratory accuracy that was not measured. Wikipedia, the former unused foundation citations and drafting instructions do not appear in the shortened manuscript.
