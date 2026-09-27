import importlib.util
from pathlib import Path
import tempfile
import unittest


@unittest.skipUnless(importlib.util.find_spec("torch"), "install the ml extra")
class MLTests(unittest.TestCase):
    def test_training_checkpoint_inference_and_leakage(self):
        import torch
        from blade_inspection.ml import SmallUNet, train, predict, read_manifest

        spec = importlib.util.spec_from_file_location(
            "demo", Path(__file__).parents[1] / "scripts/make_training_demo.py"
        )
        demo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(demo)
        torch.set_num_threads(2)
        self.assertEqual(
            tuple(SmallUNet()(torch.zeros(1, 3, 31, 35)).shape), (1, 1, 31, 35)
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = demo.generate(root / "data")
            history = train(manifest, root / "run", epochs=1, size=32)
            self.assertTrue(0 <= history[0]["validation"]["iou"] <= 1)
            report = predict(
                root / "run/best.pt", root / "data/image_20.png", root / "prediction"
            )
            self.assertEqual(report["training_status"], "trained_synthetic")
            self.assertTrue((root / "prediction/probability.npy").is_file())
            text = manifest.read_text().replace("synthetic_20", "synthetic_0")
            manifest.write_text(text)
            with self.assertRaisesRegex(ValueError, "leakage"):
                read_manifest(manifest)
