"""Generate a synthetic surface, known candidate mask and inspection outputs."""
from pathlib import Path
import cv2
import numpy as np
from blade_inspection.cli import inspect_file

root = Path(__file__).resolve().parents[1]
folder = root / "examples"
folder.mkdir(exist_ok=True)
image = np.full((240, 400, 3), 180, dtype=np.uint8)
truth = np.zeros(image.shape[:2], dtype=np.uint8)
cv2.line(image, (90, 60), (140, 180), (35, 35, 35), 5)
cv2.line(truth, (90, 60), (140, 180), 255, 5)
cv2.circle(image, (280, 120), 8, (45, 45, 45), -1)
cv2.circle(truth, (280, 120), 8, 255, -1)
for name, data in [("synthetic_surface.png", image), ("synthetic_truth.png", truth)]:
    if not cv2.imwrite(str(folder / name), data):
        raise OSError(name)
inspect_file(folder / "synthetic_surface.png", folder / "result")
print("Synthetic demo generated. This is not a real blade image or field benchmark.")
