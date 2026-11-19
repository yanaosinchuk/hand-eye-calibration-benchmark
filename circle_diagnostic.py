"""Check robot/image pairing on the circular target using relative rotation angles."""
import argparse
from itertools import combinations
from pathlib import Path
import re
import zipfile

import cv2
import numpy as np

from laboratory import ROOT


def rotation_angle(first, second):
    return np.rad2deg(np.linalg.norm(cv2.Rodrigues(first.T @ second)[0]))


def compare(archive):
    corners, ids = [], []
    size = (1371, 1003)
    with zipfile.ZipFile(archive) as source:
        data = np.loadtxt(source.open(ROOT + "denso_pos_data.txt"))
        for name in sorted(source.namelist()):
            match = re.fullmatch(ROOT + r"run2_halcon/hal_p(\d+)\.png", name)
            if not match:
                continue
            frame = cv2.imdecode(np.frombuffer(source.read(name), np.uint8), cv2.IMREAD_GRAYSCALE)
            ok, points = cv2.findCirclesGrid(cv2.resize(frame, size), (11, 11),
                flags=cv2.CALIB_CB_SYMMETRIC_GRID | cv2.CALIB_CB_CLUSTERING)
            if ok:
                ids.append(int(match[1]))
                corners.append(points)
            else:
                print(f"Grid not detected in {name}")
    if len(ids) < 3:
        raise ValueError("At least three detected grids are needed.")
    grid = np.float32([(x, y, 0) for y in range(11) for x in range(11)])
    _, _, _, angles, _ = cv2.calibrateCamera([grid]*len(ids), corners, size, None, None)
    cameras = [cv2.Rodrigues(a)[0] for a in angles]
    robots = {}
    for pid, _, _, _, rx, ry, rz in data:
        x, y, z = [cv2.Rodrigues(axis * a)[0] for axis, a in zip(np.eye(3), np.deg2rad([rx, ry, rz]))]
        robots[int(pid)] = z @ y @ x
    for label, keys in [('pose ID', ids), ('row order', list(robots)[:len(ids)])]:
        error = [abs(rotation_angle(robots[keys[i]], robots[keys[j]]) - rotation_angle(cameras[i], cameras[j]))
                 for i, j in combinations(range(len(ids)), 2)]
        print(f"{label}: median {np.median(error):.3f}°, maximum {max(error):.3f}°")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    compare(parser.parse_args().archive)
