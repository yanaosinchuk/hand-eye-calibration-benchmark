"""Build thesis tables and figures from recorded experiment outputs.

Run from any directory: python scripts/build_paper_results.py
This command formats existing measurements; it does not rerun calibration.
"""
import csv
import json
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "paper" / "generated"
FIGURES = ROOT / "paper" / "figures"
METHODS = ("Tsai", "Park", "Horaud", "Andreff", "Daniilidis")
PROFILES = ("diverse", "narrow", "nearly_single_axis")
NOISES = ("exact", "low", "high")


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def number(value):
    if value is None or value == "":
        return "---"
    value = float(value)
    if not np.isfinite(value):
        raise ValueError("Nonfinite value in published summary")
    result = f"{value:.4g}"
    if "e" in result:
        mantissa, exponent = result.split("e")
        return rf"${mantissa}\times10^{{{int(exponent)}}}$"
    return f"${result}$"


def write_table(name, caption, label, headers, rows, alignment, long=False):
    width = " & ".join(headers) + r" \\"
    if long:
        lines = [r"\begingroup\small\setlength{\tabcolsep}{4pt}",
                 rf"\begin{{longtable}}{{{alignment}}}",
                 rf"\caption{{{caption}}}\label{{{label}}}\\",
                 r"\toprule", width, r"\midrule", r"\endfirsthead",
                 rf"\multicolumn{{{len(headers)}}}{{l}}{{\small\tablename~\thetable\ (continued)}}\\",
                 r"\toprule", width, r"\midrule", r"\endhead",
                 r"\midrule", rf"\multicolumn{{{len(headers)}}}{{r}}{{\small Continued on next page}}\\",
                 r"\endfoot", r"\bottomrule", r"\endlastfoot"]
        lines += [" & ".join(row) + r" \\" for row in rows]
        lines += [r"\end{longtable}", r"\endgroup"]
    else:
        lines = [r"\begin{table}[!htbp]\centering\small",
                 rf"\caption{{{caption}}}\label{{{label}}}",
                 rf"\begin{{tabular}}{{{alignment}}}", r"\toprule", width, r"\midrule"]
        lines += [" & ".join(row) + r" \\" for row in rows]
        lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    (GENERATED / name).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    GENERATED.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    controlled = {mode: read_csv(ROOT / "results" / mode / "summary.csv")
                  for mode in ("poses", "pixels")}
    replay = read_csv(ROOT / "results/thesis/summary.csv")
    if any(len(rows) != 135 for rows in controlled.values()) or len(replay) != 60:
        raise ValueError("Expected 135 conditions per generic model and 60 replay conditions")
    for mode, rows in controlled.items():
        expected = {(str(n), profile, level, method)
                    for n in (8, 16, 32) for profile in PROFILES
                    for level in NOISES for method in METHODS}
        actual = [(r['poses'], r['profile'], r['noise'], r['method']) for r in rows]
        if len(set(actual)) != len(actual) or set(actual) != expected:
            raise ValueError(f"Missing or duplicate controlled conditions: {mode}")
        if any(r['opencv'] != '4.12.0' or r['seed'] != '42' or r['trials'] != '100'
               or r['model'] != mode for r in rows):
            raise ValueError("Recorded experiment metadata differs from the manuscript")

    # Aggregate the recorded held-out predictions so this table can be rebuilt.
    real = []
    for series, filename in (("June", "june_held_out.csv"), ("July", "held_out.csv")):
        observations = read_csv(ROOT / "results/thesis" / filename)
        expected_count = 15 if series == "June" else 18
        if Counter(r['method'] for r in observations) != Counter({m: expected_count for m in METHODS}):
            raise ValueError("Unexpected held-out prediction counts")
        for method in METHODS:
            values = np.array([[float(r[k]) for k in ('rotation_deg', 'translation_mm', 'pixel_rmse')]
                               for r in observations if r['method'] == method])
            median, p95 = np.percentile(values, [50, 95], axis=0)
            real.append(dict(series=series, method=method, median_deg=median[0], median_mm=median[1],
                             median_px=median[2], p95_deg=p95[0], p95_mm=p95[1], p95_px=p95[2]))
    with (ROOT / 'results/thesis/real_summary.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(real[0]))
        writer.writeheader()
        writer.writerows(real)

    write_table('replay_low.tex', 'Trajectory replay: 20 poses, low noise, 100 trials per method.',
                'tab:replay-low', ['Method', r'Med. $e_R$ ($^\circ$)', r'Med. $e_t$ (mm)',
                                   r'$p_{95}(e_t)$ (mm)', 'Failed'],
                [[r['method'], number(r['median_deg']), number(r['median_mm']), number(r['p95_mm']),
                  r['failures']] for r in replay if r['poses'] == '20' and r['noise'] == 'low'], 'lrrrr')
    write_table('real_results.tex', 'Leave-one-pose-out image prediction. Each method has 15 June and 18 July predictions.',
                'tab:real', ['Series', 'Method', r'Med. $e_R$ ($^\circ$)', r'Med. $e_t$ (mm)',
                            r'Med. RMSE (px)', r'$p_{95}$ RMSE (px)'],
                [[r['series'], r['method'], number(r['median_deg']), number(r['median_mm']),
                  number(r['median_px']), number(r['p95_px'])] for r in real], 'llrrrr')
    write_table('failure_totals.tex', 'Rejected outputs across the controlled synthetic conditions. Each method is attempted 2,700 times per model.',
                'tab:failures', ['Method', 'Pose model failed', 'Pixel model failed'],
                [[m] + [str(sum(int(r['failures']) for r in controlled[mode] if r['method'] == m))
                         for mode in ('poses', 'pixels')] for m in METHODS], 'lrr')
    write_table('axis_tails.tex', 'Nearly single-axis profile, 32 poses and high noise. Translation errors remain in mm; all five methods return valid outputs in the pose model, while Park has one rejected output in the pixel model.',
                'tab:axis-tails', ['Method', r'Med. $e_t$, poses', r'$p_{95}$, poses',
                                  r'Med. $e_t$, pixels', r'$p_{95}$, pixels'],
                [[m] + [number(next(r for r in controlled[mode] if r['poses'] == '32'
                                  and r['profile'] == 'nearly_single_axis' and r['noise'] == 'high'
                                  and r['method'] == m)[k])
                         for mode in ('poses', 'pixels') for k in ('median_mm', 'p95_mm')]
                 for m in METHODS], 'lrrrr')

    complete = []
    for mode in ('poses', 'pixels'):
        for profile in PROFILES:
            filename = f'{mode}_{profile}.tex'
            rows = sorted((r for r in controlled[mode] if r['profile'] == profile),
                          key=lambda r: (int(r['poses']), NOISES.index(r['noise']), METHODS.index(r['method'])))
            write_table(filename, f'Controlled {mode} model, {profile.replace("_", " ")} profile; 100 trials per row.',
                        f'tab:{mode}-{profile.replace("_", "-")}',
                        ['$N$', 'Noise', 'Method', 'Failed', r'Med. $e_R$', r'$p_{95}(e_R)$',
                         r'Med. $e_t$', r'$p_{95}(e_t)$'],
                        [[r['poses'], r['noise'], r['method'], r['failures']] +
                         [number(r[k]) for k in ('median_deg', 'p95_deg', 'median_mm', 'p95_mm')] for r in rows],
                        'rllrrrrr', long=True)
            complete.append(rf'\input{{generated/{filename}}}')
    (GENERATED/'controlled_all.tex').write_text('\n'.join(complete)+'\n', encoding='utf-8')
    write_table('replay_all.tex', 'Complete trajectory-replay summaries; 100 trials per row. Angular errors are in degrees and translation errors in mm.',
                'tab:replay-all', ['$N$', 'Noise', 'Method', 'Failed', r'Med. $e_R$', r'$p_{95}(e_R)$',
                                   r'Med. $e_t$', r'$p_{95}(e_t)$'],
                [[r['poses'],r['noise'],r['method'],r['failures']] +
                 [number(r[k]) for k in ('median_deg','p95_deg','median_mm','p95_mm')] for r in replay],
                'rllrrrrr', long=True)
    fixes = read_csv(ROOT/'results/thesis/june_corrections.csv')
    write_table('june_corrections.tex', 'Inferred corrections applied to the June ODS table. Translations use mm and rotation components use degrees.',
                'tab:corrections', ['Pose', 'Component', 'Input', 'Used value'],
                [[r['pose'], r['column'], r['original'], r['corrected']] for r in fixes], 'rlrr')

    geometry = json.loads((ROOT/'results/thesis/geometry_metadata.json').read_text())
    matrices = []
    for symbol, key in ((r'Y_\star', 'synthetic_camera'), (r'M_\star', 'synthetic_mount')):
        rows = [' & '.join(f'{float(v):.6f}' for v in row) for row in geometry[key]]
        matrices.append(r'\[' + symbol + r'=\begin{pmatrix}' +
                        r' \\ '.join(rows) + r'\end{pmatrix}.\]')
    (GENERATED/'nominal_geometry.tex').write_text('\n'.join(matrices)+'\n', encoding='utf-8')

    plt.rcParams.update({'font.size': 9, 'axes.spines.top': False, 'axes.spines.right': False})
    fig, axes = plt.subplots(2, 3, figsize=(10.2, 6), sharex=True, layout='constrained')
    for i, mode in enumerate(('poses', 'pixels')):
        for j, profile in enumerate(PROFILES):
            ax = axes[i, j]
            for method in METHODS:
                rows = sorted((r for r in controlled[mode] if r['noise'] == 'high'
                               and r['profile'] == profile and r['method'] == method),
                              key=lambda r: int(r['poses']))
                ax.plot([int(r['poses']) for r in rows], [float(r['median_mm']) for r in rows],
                        marker='o', markersize=3, label=method)
            ax.set_yscale('log')
            ax.set_xticks([8, 16, 32])
            ax.grid(True, alpha=.2)
            if i == 0: ax.set_title(profile.replace('_', ' '))
            if j == 0: ax.set_ylabel(f'{mode}: median error (mm)')
            if i == 1: ax.set_xlabel('Acquisition poses')
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='outside lower center', ncol=5, frameon=False)
    fig.savefig(FIGURES/'controlled_sensitivity.pdf')
    fig.savefig(FIGURES/'controlled_sensitivity.png', dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(10.4, 3.25), layout='constrained')
    for method in METHODS:
        rows = sorted((r for r in replay if r['noise'] == 'low' and r['method'] == method),
                      key=lambda r: int(r['poses']))
        for ax, key in zip(axes[:2], ('median_deg','median_mm')):
            ax.plot([int(r['poses']) for r in rows], [float(r[key]) for r in rows], marker='o', markersize=3, label=method)
        series = [next(r for r in real if r['series'] == s and r['method'] == method) for s in ('June','July')]
        axes[2].plot(['June','July'], [r['median_px'] for r in series], marker='o', markersize=3, label=method)
    for ax, title, unit in zip(axes, ('Replay: low noise','Replay: low noise','Held-out images'),
                               ('Median angle error (deg)','Median position error (mm)','Median pixel RMSE (px)')):
        ax.set_title(title); ax.set_ylabel(unit); ax.grid(True, alpha=.2)
    for ax in axes[:2]: ax.set_xticks([8,12,16,20]); ax.set_xlabel('Acquisition poses')
    handles,labels = axes[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='outside lower center',ncol=5,frameon=False)
    fig.savefig(FIGURES/'comparison.pdf')
    fig.savefig(FIGURES/'comparison.png',dpi=180)
    plt.close(fig)
    print('Generated thesis tables for 270 controlled, 60 replay and 10 held-out summary rows.')


if __name__ == '__main__':
    main()
