"""Explainable baseline for visual surface-anomaly screening.

This is a new follow-up extension, not code from the original thesis.
"""
from __future__ import annotations


import cv2
import numpy as np


def detect_defects(
    image: np.ndarray,
    *,
    blur_kernel: int = 31,
    threshold: float = 22.0,
    min_area: int = 20,
) -> tuple[np.ndarray, list[tuple[int, int, int, int]]]:
    """Return a binary candidate mask and bounding boxes.

    The method detects local grayscale contrast and should be treated as a
    screening baseline. It does not classify the cause of an anomaly.
    """
    if not isinstance(image, np.ndarray) or image.size == 0:
        raise ValueError("image must be a non-empty array")
    if image.dtype != np.uint8:
        raise ValueError("image must use uint8 pixels in the range 0-255")
    if image.ndim not in (2, 3) or (image.ndim == 3 and image.shape[2] != 3):
        raise ValueError("image must be grayscale or three-channel BGR")
    if isinstance(blur_kernel, bool) or not isinstance(blur_kernel, int) or blur_kernel < 3 or blur_kernel % 2 == 0:
        raise ValueError("blur_kernel must be odd and at least 3")
    if not np.isfinite(threshold) or threshold <= 0 or threshold > 255:
        raise ValueError("threshold must be finite and in (0, 255]")
    if isinstance(min_area, bool) or not isinstance(min_area, int) or min_area < 1:
        raise ValueError("threshold and min_area must be positive")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
    gray = np.asarray(gray, dtype=np.uint8)
    background = cv2.GaussianBlur(gray, (blur_kernel, blur_kernel), 0)
    contrast = cv2.absdiff(gray, background)
    mask = (contrast >= threshold).astype(np.uint8) * 255
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    count, labels, stats, _ = cv2.connectedComponentsWithStats(mask)
    clean = np.zeros_like(mask)
    boxes = []
    for label in range(1, count):
        x, y, w, h, area = stats[label]
        if area >= min_area:
            clean[labels == label] = 255
            boxes.append((int(x), int(y), int(w), int(h)))
    return clean, boxes


def annotate(image: np.ndarray, boxes: list[tuple[int, int, int, int]]) -> np.ndarray:
    output = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR) if image.ndim == 2 else image.copy()
    for x, y, w, h in boxes:
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 0, 255), 2)
    return output

