# Reproduction of the recorded numerical experiments

Numerical source revision: `4091828055efe2b13eefb3d59bc8756474ed5b2c`.
Environment: Python 3.12.14, NumPy 2.2.6 and OpenCV 4.12.0 (`opencv-python-headless==4.12.0.88`). Seed 42, 100 trials per synthetic condition. Original input: the supplied `Data4Osinchuk.zip`.

The numerical source files were not modified by the manuscript rewrite.

| Run | Method attempts or predictions | Compared summary rows | Outcome |
| --- | ---: | ---: | --- |
| Generic pose model | 13,500 | 135 | Numeric values reproduced exactly |
| Generic pixel/PnP model | 13,500 | 135 | Numeric values reproduced exactly |
| Recorded-trajectory replay | 6,000 | 60 | Numeric values reproduced exactly |
| Leave-one-pose-out image prediction | 165 | 10 | Medians and 95th percentiles reproduced exactly |

Rejected outputs are part of these results: 414 generic pose-model attempts (395 Tsai, 19 Park), 427 generic pixel-model attempts (398 Tsai, 29 Park) and zero trajectory-replay attempts. The image-prediction run completed all 165 outputs. Large finite errors are retained and are not included in the rejection count.

## Additional geometric checks

- Exact diverse 32-pose sample: all five methods recovered the generic camera; largest angle error approximately `3.46e-12` degrees and largest translation error `2.43e-11` mm.
- Maximum exact `G @ M - Y @ C` entrywise residual on that sample: `2.28e-13` mm for the translation block (rotation entries are dimensionless).
- Forward point construction `inverse(Y) @ G @ M @ point` and the generic benchmark's reverse construction agreed within `2.85e-13` mm on an exact 16-pose sample.
- The generic synthetic camera centre matches the screenshot example at `[300, 200, 1000]` mm; its orientation differs by 6 degrees.

## Circular diagnostic audit

Nine grids detected out of eleven; P43 and P54 were not detected. Pose-ID pairing: median 0.077 degrees, maximum 0.383 degrees. Current script's post-detection naive row order: median 13.989 degrees, maximum 60.897 degrees. Forming raw row-order pairs before discarding failed detections: median 12.997 degrees, maximum 46.441 degrees. This separate audit preserves the filtering operation; neither baseline establishes what an undocumented historical calibration program actually did.

## Scope of the checks

The repeated numerical results and frame-chain checks support the recorded configurations. They do not supply an independently surveyed camera pose, a full circular-target calibration, a verified physical pixel pitch, robot joint reachability, detector-failure simulation, automated numerical regression tests or CI. Injecting a solver exception into the current `validate` loop confirms that it aborts the laboratory run; per-fold failure handling is unfinished.

`python scripts/build_paper_results.py` rebuilds printable tables and figures from committed outputs. It also recomputes `results/thesis/real_summary.csv` from the 165 committed held-out rows. Full synthetic trial files remain reproducible with the numerical commands in README; laboratory feature extraction requires the original archive.
