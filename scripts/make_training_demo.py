"""Generate independent synthetic shapes, not photographs of turbine defects."""

import csv
from pathlib import Path
import cv2
import numpy as np


def generate(root):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(42)
    rows = []
    for i in range(24):
        image = np.clip(rng.normal(180, 5, (64, 64, 3)), 0, 255).astype(np.uint8)
        mask = np.zeros((64, 64), np.uint8)
        if i % 4 != 0:
            a = tuple(int(v) for v in rng.integers(8, 28, 2))
            b = tuple(int(v) for v in rng.integers(35, 56, 2))
            cv2.line(image, a, b, (35, 35, 35), 3)
            cv2.line(mask, a, b, 255, 3)
        cv2.imwrite(str(root / f"image_{i}.png"), image)
        cv2.imwrite(str(root / f"mask_{i}.png"), mask)
        rows.append(
            [
                f"image_{i}.png",
                f"mask_{i}.png",
                "train" if i < 16 else ("val" if i < 20 else "test"),
                f"synthetic_{i}",
            ]
        )
    with (root / "manifest.csv").open("w", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["image", "mask", "split", "group"])
        writer.writerows(rows)
    return root / "manifest.csv"


if __name__ == "__main__":
    print(generate("data/synthetic"))
