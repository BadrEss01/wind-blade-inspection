"""Inspect one image and write an overlay, mask and machine-readable report."""
import argparse
import json
from pathlib import Path

import cv2
import numpy as np

from .detector import detect_defects, annotate


def inspect_file(source, output_dir, *, threshold=22.0, min_area=20, blur_kernel=31):
    source, output_dir = Path(source), Path(output_dir)
    image = cv2.imread(str(source))
    if image is None:
        raise ValueError(f"Cannot read image: {source}")
    mask, boxes = detect_defects(image, threshold=threshold,
                                 min_area=min_area, blur_kernel=blur_kernel)
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, data in [("overlay.png", annotate(image, boxes)), ("mask.png", mask)]:
        if not cv2.imwrite(str(output_dir / name), data):
            raise OSError(f"Cannot write {output_dir / name}")
    report = {
        "schema_version": 1,
        "input_file": source.name,
        "width": image.shape[1], "height": image.shape[0],
        "parameters": {"threshold": threshold, "min_area": min_area,
                       "blur_kernel": blur_kernel},
        "candidate_count": len(boxes),
        "mask_pixels": int(np.count_nonzero(mask)),
        "boxes_xywh": [list(box) for box in boxes],
        "interpretation": "Contrast anomalies; not classified or confirmed defects."
    }
    (output_dir / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/inspection"))
    parser.add_argument("--threshold", type=float, default=22.0)
    parser.add_argument("--min-area", type=int, default=20)
    parser.add_argument("--blur-kernel", type=int, default=31)
    args = parser.parse_args()
    try:
        result = inspect_file(args.image, args.output_dir, threshold=args.threshold,
                              min_area=args.min_area, blur_kernel=args.blur_kernel)
    except (ValueError, OSError, cv2.error) as error:
        parser.exit(2, f"Inspection failed: {error}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
