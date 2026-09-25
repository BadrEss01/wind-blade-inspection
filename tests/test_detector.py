import importlib.util
from pathlib import Path
import unittest
import cv2
import numpy as np

from blade_inspection import detector as module

class SurfaceDefectTests(unittest.TestCase):
    def test_detects_contrast_region(self):
        image = np.full((120, 160, 3), 150, dtype=np.uint8)
        image[50:70, 70:90] = 20
        mask, boxes = module.detect_defects(image, threshold=15, min_area=10)
        self.assertGreater(mask.sum(), 0)
        self.assertTrue(any(w > 0 and h > 0 for _, _, w, h in boxes))

    def test_rejects_empty_input(self):
        with self.assertRaises(ValueError):
            module.detect_defects(np.array([]))

    def test_uniform_surface_has_no_candidates(self):
        mask, boxes = module.detect_defects(np.full((80, 80), 150, dtype=np.uint8))
        self.assertEqual(np.count_nonzero(mask), 0)
        self.assertEqual(boxes, [])

    def test_rejects_unsupported_image_formats(self):
        for image in [np.ones((40, 40), dtype=float),
                      np.zeros((40, 40, 4), dtype=np.uint8),
                      np.zeros(40, dtype=np.uint8)]:
            with self.subTest(shape=image.shape, dtype=image.dtype):
                with self.assertRaises(ValueError):
                    module.detect_defects(image)

    def test_rejects_nonfinite_threshold(self):
        with self.assertRaises(ValueError):
            module.detect_defects(np.zeros((40, 40), dtype=np.uint8), threshold=float('nan'))

if __name__ == "__main__":
    unittest.main()

