import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import cv2
import numpy as np
from blade_inspection.cli import inspect_file


class CliTests(unittest.TestCase):
    def test_output_files_and_report_agree(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            image = np.full((100, 100, 3), 160, dtype=np.uint8)
            image[40:55, 40:55] = 10
            cv2.imwrite(str(root / "input.png"), image)
            result = inspect_file(root / "input.png", root / "out")
            saved = json.loads((root / "out/report.json").read_text())
            self.assertEqual(result, saved)
            mask = cv2.imread(str(root / "out/mask.png"), 0)
            self.assertEqual(int(np.count_nonzero(mask)), result["mask_pixels"])
            self.assertGreater(result["candidate_count"], 0)
            self.assertEqual(cv2.imread(str(root / "out/overlay.png")).shape, image.shape)

    def test_missing_file_has_nonzero_exit(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, "-m", "blade_inspection.cli",
                                     str(Path(directory) / "missing.png")], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("Cannot read image", result.stderr)


if __name__ == "__main__":
    unittest.main()
