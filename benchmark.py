"""Monte Carlo comparison of OpenCV's eye-to-hand solvers."""
import argparse
import csv
from itertools import product
from pathlib import Path

import cv2
import numpy as np


METHODS = {
    "Tsai": cv2.CALIB_HAND_EYE_TSAI,
    "Park": cv2.CALIB_HAND_EYE_PARK,
    "Horaud": cv2.CALIB_HAND_EYE_HORAUD,
    "Andreff": cv2.CALIB_HAND_EYE_ANDREFF,
    "Daniilidis": cv2.CALIB_HAND_EYE_DANIILIDIS,
}
POSE_COUNTS = (8, 16, 32)
# Per-axis standard deviations of the rotation vectors, in degrees.
POSE_SPREADS = {
    "diverse": (22, 22, 22),
    "narrow": (4, 4, 4),
    "nearly_single_axis": (0.5, 0.5, 22),
}
POSE_NOISE = {"exact": (0, 0), "low": (0.1, 0.5), "high": (0.5, 2)}
PIXEL_NOISE = {"exact": 0, "low": 0.25, "high": 1}
K = np.array([[4379.56, 0, 2048], [0, 4379.56, 1500], [0, 0, 1]])
BOARD = np.array([(20 * x, 20 * y, 0) for y in range(-2, 3) for x in range(-3, 4)],
                 dtype=np.float64)


def transform(rotvec, translation):
    pose = np.eye(4)
    pose[:3, :3] = cv2.Rodrigues(np.asarray(rotvec, dtype=float))[0]
    pose[:3, 3] = translation
    return pose


def inverse(pose):
    result = np.eye(4)
    result[:3, :3] = pose[:3, :3].T
    result[:3, 3] = -result[:3, :3] @ pose[:3, 3]
    return result


# All translations are in millimetres. The camera looks down with a small tilt.
BASE_CAMERA = transform(np.deg2rad(174) * np.array([1, -1, 0]) / np.sqrt(2),
                        [300, 200, 1000])
GRIPPER_TARGET = transform(np.deg2rad([9, -13, 18]), [15, -10, 85])


def noisy_pose(pose, draw, sigma_deg, sigma_mm):
    # Left perturbation of orientation with independently perturbed position
    # of the frame origin, both expressed in the destination frame.
    noisy = pose.copy()
    noisy[:3, :3] = cv2.Rodrigues(draw[:3] * np.deg2rad(sigma_deg))[0] @ pose[:3, :3]
    noisy[:3, 3] += draw[3:] * sigma_mm
    return noisy


def observed_target(pose, draw, sigma_px):
    rotvec = cv2.Rodrigues(pose[:3, :3])[0]
    pixels, _ = cv2.projectPoints(BOARD, rotvec, pose[:3, 3], K, None)
    pixels = pixels.reshape(-1, 2)
    camera_points = BOARD @ pose[:3, :3].T + pose[:3, 3]
    if (np.any(camera_points[:, 2] <= 0) or np.any(pixels < 0)
            or np.any(pixels >= [4096, 3000])):
        raise ValueError("Target outside the simulated camera's field of view.")
    ok, rotation, translation = cv2.solvePnP(
        BOARD, pixels + sigma_px * draw, K, None, flags=cv2.SOLVEPNP_ITERATIVE
    )
    if not ok:
        raise ValueError("solvePnP failed.")
    return transform(rotation, translation.ravel())


def observations(seed, trial, count, spread, level, model):
    rng = np.random.default_rng(np.random.SeedSequence([seed, trial]))
    size = max(POSE_COUNTS)
    rotations = rng.normal(size=(size, 3)) * np.deg2rad(spread)
    translations = rng.uniform([-95, -75, 620], [95, 75, 800], size=(size, 3))
    robot_draws = rng.normal(size=(size, 6))
    camera_draws = rng.normal(size=(size, 6))
    pixel_draws = rng.normal(size=(size, len(BOARD), 2))
    sigma_deg, sigma_mm = POSE_NOISE[level]
    base_to_gripper, target_to_camera = [], []
    for i in range(count):
        camera_target = transform(rotations[i], translations[i])
        base_gripper = BASE_CAMERA @ camera_target @ inverse(GRIPPER_TARGET)
        robot = noisy_pose(base_gripper, robot_draws[i], sigma_deg, sigma_mm)
        target = (noisy_pose(camera_target, camera_draws[i], sigma_deg, sigma_mm)
                  if model == "poses" else
                  observed_target(camera_target, pixel_draws[i], PIXEL_NOISE[level]))
        # OpenCV's eye-to-hand convention requires base -> gripper and
        # target -> camera, and returns camera -> base.
        base_to_gripper.append(inverse(robot))
        target_to_camera.append(target)
    return np.array(base_to_gripper), np.array(target_to_camera)


def solve_handeye(base_to_gripper, target_to_camera, method):
    rotation, translation = cv2.calibrateHandEye(
        list(base_to_gripper[:, :3, :3]), list(base_to_gripper[:, :3, 3, None]),
        list(target_to_camera[:, :3, :3]), list(target_to_camera[:, :3, 3, None]),
        method=method,
    )
    if (not np.isfinite(rotation).all() or not np.isfinite(translation).all()
            or not np.allclose(rotation.T @ rotation, np.eye(3), atol=1e-6)
            or not np.isclose(np.linalg.det(rotation), 1, atol=1e-6)):
        raise ValueError("Solver returned an invalid rigid transform.")
    # OpenCV can log a solver failure and return the initialized identity.
    # This synthetic rig has a nonidentity ground truth in every trial.
    if np.array_equal(rotation, np.eye(3)) and np.count_nonzero(translation) == 0:
        raise ValueError("Solver returned the identity fallback.")
    pose = np.eye(4)
    pose[:3, :3] = rotation
    pose[:3, 3] = translation.ravel()
    return pose


def pose_error(reference, estimate_pose):
    delta = reference[:3, :3].T @ estimate_pose[:3, :3]
    skew = np.array([delta[2, 1] - delta[1, 2], delta[0, 2] - delta[2, 0],
                     delta[1, 0] - delta[0, 1]])
    angle = np.rad2deg(np.arctan2(np.linalg.norm(skew), np.trace(delta) - 1))
    distance = np.linalg.norm(estimate_pose[:3, 3] - reference[:3, 3])
    return float(angle), float(distance)


def estimate(base_to_gripper, target_to_camera, method):
    return pose_error(BASE_CAMERA, solve_handeye(base_to_gripper, target_to_camera, method))


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def run(seed, trials, model, output):
    summary, raw = [], []
    for count, profile, level in product(POSE_COUNTS, POSE_SPREADS, POSE_NOISE):
        condition = dict(opencv=cv2.__version__, seed=seed, model=model,
                         poses=count, profile=profile, noise=level)
        errors = {method: [] for method in METHODS}
        for trial in range(trials):
            poses = observations(seed, trial, count, POSE_SPREADS[profile], level, model)
            for method, code in METHODS.items():
                try:
                    rotation, translation = estimate(*poses, code)
                    errors[method].append((rotation, translation))
                    status = "ok"
                except (cv2.error, ValueError) as exc:
                    status = str(exc).strip()
                    rotation = translation = None
                raw.append(dict(condition, trial=trial, method=method, status=status,
                                rotation_deg=rotation, translation_mm=translation))
        for method, values in errors.items():
            med, p95 = (np.percentile(values, [50, 95], axis=0) if values else
                        ((None, None), (None, None)))
            summary.append(dict(condition, method=method, trials=trials,
                                failures=trials - len(values), median_deg=med[0],
                                p95_deg=p95[0], median_mm=med[1], p95_mm=p95[1]))
    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / "trials.csv", raw)
    write_csv(output / "summary.csv", summary)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--model", choices=["poses", "pixels"], default="poses")
    parser.add_argument("--output", type=Path, default=Path("outputs/benchmark"))
    args = parser.parse_args()
    if args.trials < 1 or args.seed < 0:
        parser.error("--trials must be positive and --seed nonnegative")
    run(args.seed, args.trials, args.model, args.output)
