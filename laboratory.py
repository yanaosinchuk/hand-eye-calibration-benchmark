"""Replay the DENSO trajectory and cross-validate the July 3 eye-to-hand series."""
import argparse
import io
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
import zipfile

import cv2
import numpy as np

from benchmark import METHODS, inverse, noisy_pose, pose_error, solve_handeye, transform, write_csv

GRID = (11, 8)
BOARD = np.float32([(12*x, 12*y, 0) for y in range(8) for x in range(11)])
ROOT = "24_07_03_HandAugeHalcon/"


def june_poses(archive):
    path = "24_06_21_HandAugeOpenCV/RobotPoses.ods"
    with zipfile.ZipFile(io.BytesIO(archive.read(path))) as ods:
        rows = ET.fromstring(ods.read("content.xml")).findall(".//{*}table-row")
    values = np.array([[float("".join(c.itertext())) for c in row[:7]] for row in rows[1:16]])
    corrections = []
    for i, j in zip(*np.where(np.abs(values[:, 1:]) > 10000)):
        j += 1
        original = values[i, j]
        values[i, j] /= 1000
        corrections.append(dict(pose=int(values[i, 0]), column=("id","x","y","z","rx","ry","rz")[j],
                                original=original, corrected=values[i,j]))
    return values, corrections


def read_series(archive, june=False):
    robots, corners, ids = [], [], []
    with zipfile.ZipFile(archive) as z:
        poses = june_poses(z)[0] if june else np.loadtxt(z.open(ROOT + "denso_pos_data.txt"))
        for pid, x, y, zpos, rx, ry, rz in poses:
            name = ROOT + f"run1_opencv/img_p{int(pid)}.png"
            if june:
                name = f"24_06_21_HandAugeOpenCV/img{int(pid)-39:02}.png"
            frame = cv2.imdecode(np.frombuffer(z.read(name), np.uint8), cv2.IMREAD_GRAYSCALE)
            h, w = frame.shape
            small = cv2.resize(frame, (w//3, h//3), interpolation=cv2.INTER_AREA)
            ok, points = cv2.findChessboardCorners(small, GRID)
            if not ok:
                raise ValueError(f"Missing checkerboard corners in {name}")
            points *= np.float32([w/small.shape[1], h/small.shape[0]])
            points = cv2.cornerSubPix(frame, points, (7, 7), (-1, -1),
                                      (cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 40, 0.001))
            corners.append(points)
            angles = np.deg2rad([rx, ry, rz])
            rotations = [cv2.Rodrigues(axis*a)[0] for axis, a in zip(np.eye(3), angles)]
            robot = np.eye(4)
            robot[:3, :3] = rotations[2] @ rotations[1] @ rotations[0]
            robot[:3, 3] = [x, y, zpos]
            robots.append(robot)
            ids.append(int(pid))
    return np.array(robots), np.array(corners), ids, (w, h)


def camera_fit(corners, size):
    rms, k, d, rs, ts = cv2.calibrateCamera(
        [BOARD]*len(corners), list(corners), size, None, None)
    return rms, k, d, np.array([transform(r, t.ravel()) for r, t in zip(rs, ts)])


def target_pose(points, k, d):
    ok, r, t = cv2.solvePnP(BOARD, points, k, d)
    if not ok:
        raise ValueError("Target PnP failed")
    return transform(r, t.ravel())


def project(pose, k, d):
    return cv2.projectPoints(BOARD, cv2.Rodrigues(pose[:3, :3])[0],
                             pose[:3, 3], k, d)[0]


def mount_pose(robots, targets, camera):
    mounts = np.array([inverse(g) @ camera @ c for g, c in zip(robots, targets)])
    u, _, vt = np.linalg.svd(mounts[:, :3, :3].mean(axis=0))
    result = np.eye(4)
    result[:3, :3] = u @ np.diag([1, 1, np.linalg.det(u @ vt)]) @ vt
    result[:3, 3] = mounts[:, :3, 3].mean(axis=0)
    return result


def validate(g, corners, ids, size):
    ig = np.array([inverse(p) for p in g])
    real = []
    for i, pid in enumerate(ids):
        train = np.arange(len(ids)) != i
        _, kt, dt, ct = camera_fit(corners[train], size)
        observed = target_pose(corners[i], kt, dt)
        for method, code in METHODS.items():
            camera = solve_handeye(ig[train], ct, code)
            mount = mount_pose(g[train], ct, camera)
            prediction = inverse(camera) @ g[i] @ mount
            deg, mm = pose_error(observed, prediction)
            residual = project(prediction, kt, dt) - corners[i]
            px = np.sqrt(np.mean(np.sum(residual**2, axis=-1)))
            real.append(dict(pose=pid, method=method, rotation_deg=deg, translation_mm=mm, pixel_rmse=px))
    return real


def run(archive, out, repetitions, seed):
    out.mkdir(parents=True, exist_ok=True)
    g, corners, ids, size = read_series(archive)
    ig = np.array([inverse(p) for p in g])
    keep = ~np.isin(ids, [47, 48])  # Conflicting pose labels for byte-identical images.
    rms, k, d, targets = camera_fit(corners[keep], size)
    y = solve_handeye(ig[keep], targets, METHODS["Park"])
    x = mount_pose(g[keep], targets, y)
    np.savez(out/"geometry.npz", ids=ids, base_gripper=g, corners=corners, K=k,
             distortion=d, reprojection_rms=rms, synthetic_camera=y, synthetic_mount=x)
    write_csv(out/"held_out.csv", validate(g[keep], corners[keep], np.array(ids)[keep], size))
    june_g, june_points, june_ids, june_size = read_series(archive, june=True)
    write_csv(out/"june_held_out.csv", validate(june_g, june_points, june_ids, june_size))
    with zipfile.ZipFile(archive) as source:
        write_csv(out/"june_corrections.csv", june_poses(source)[1])
    ideal = [inverse(y) @ pose @ x for pose in g]
    pixels = np.array([project(p, k, d) for p in ideal])
    records, groups = [], defaultdict(list)
    for trial in range(repetitions):
        rng = np.random.default_rng(np.random.SeedSequence([seed, trial]))
        order = rng.permutation(len(ids))
        robot_noise = rng.normal(size=(len(ids), 6))
        image_noise = rng.normal(size=corners.shape)
        for level, sd, sm, sp in [('exact',0,0,0), ('low',0.1,0.5,0.25), ('high',0.5,2,1)]:
            robot = np.array([inverse(noisy_pose(p, draw, sd, sm)) for p, draw in zip(g, robot_noise)])
            cam = np.array([target_pose(p+sp*noise, k, d) for p, noise in zip(pixels, image_noise)])
            for count in (8, 12, 16, 20):
                idx = order[:count]
                for method, code in METHODS.items():
                    try:
                        est = solve_handeye(robot[idx], cam[idx], code)
                        deg, mm = pose_error(y, est)
                        status = "ok"
                    except (ValueError, cv2.error) as exc:
                        deg = mm = None
                        status = str(exc)
                    records.append(dict(trial=trial,seed=seed,poses=count,noise=level,method=method,
                                        rotation_deg=deg,translation_mm=mm,status=status))
                    groups[count,level,method].append((deg,mm) if status=='ok' else None)
    write_csv(out/"simulation.csv", records)
    summary=[]
    for (count,level,method), rows in groups.items():
        valid = [p for p in rows if p is not None]
        med, tail = np.percentile(valid,[50,95],axis=0) if valid else ((None,None),)*2
        summary.append(dict(poses=count,noise=level,method=method,failures=len(rows)-len(valid),
                            median_deg=med[0],median_mm=med[1],p95_deg=tail[0],p95_mm=tail[1]))
    write_csv(out/"summary.csv",summary)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output",type=Path,default=Path("outputs/laboratory"))
    parser.add_argument("--trials",type=int,default=100)
    parser.add_argument("--seed",type=int,default=42)
    args=parser.parse_args()
    if args.trials < 1 or args.seed < 0:
        parser.error("Use positive trial count and nonnegative seed")
    run(args.archive,args.output,args.trials,args.seed)
