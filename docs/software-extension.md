# Surface Inspection — Later Software Extension

This extension was added in September 2026 after the original climbing-robot research. It explores still-image surface screening with OpenCV and a trainable PyTorch U-Net. Development used AI coding assistance.

The original research focused on building a platform that could adhere to and move along a wind turbine blade. The software has not been integrated with that prototype or validated on real turbine defects.

## Try it

Requires Python 3.10 or newer. From the repository root:

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell instead:
# .venv\Scripts\Activate.ps1
python -m pip install -e .
python scripts/make_demo.py
blade-inspect examples/synthetic_surface.png --output-dir outputs/demo
python -m unittest discover -s tests -v
```

Inspect your own photograph:

```bash
blade-inspect path/to/image.jpg --output-dir outputs/my-image --threshold 22 --min-area 20 --blur-kernel 31
```

Each run writes `overlay.png`, `mask.png` and `report.json`. Boxes use `[x, y, width, height]` in pixels. Parameters and image dimensions are saved with the results. Use a separate output directory for each image; existing output files in that directory are replaced.

## Example result

![OpenCV baseline on a synthetic line and spot](../examples/result/overlay.png)

The demo input is generated, not a blade photograph. The dark line and spot demonstrate software behavior only. Recreate the sample and outputs with `python scripts/make_demo.py`.

## Trainable ML segmentation (2026 extension)

A compact PyTorch U-Net complements the classical OpenCV baseline. It includes
paired image/mask loading, group-aware split checks, augmentation, BCE + Dice loss,
validation-based checkpoint selection, held-out evaluation and inference exports.
No pretrained or real-blade-trained weights are bundled. Read the [model card](MODEL_CARD.md).

Run the complete synthetic smoke experiment from the repository root:

```bash
python -m pip install 'torch>=2.6,<3' --index-url https://download.pytorch.org/whl/cpu
python -m pip install -e '.[ml]'
python scripts/make_training_demo.py
blade-ml train data/synthetic/manifest.csv --output outputs/ml --epochs 20 --size 64 --data-kind synthetic
blade-ml evaluate outputs/ml/best.pt data/synthetic/manifest.csv
blade-ml predict outputs/ml/best.pt data/synthetic/image_21.png --output outputs/ml-preview
```

For your own labeled data, use CSV columns `image,mask,split,group`; paths are relative
to the manifest. Keep each blade/capture session within one split. Training requires
train and val rows; final evaluation requires test rows. Masks use 0/255 pixels.
Use `--data-kind real` only for actual photographed data. Synthetic metrics measure pipeline behavior rather than field accuracy.

The ML commands export checkpoints/history, pixel-level metrics, probability arrays,
masks and overlays. The simple baseline remains available for comparison.


## Current limitations and next steps

The executable pipeline highlights local grayscale contrast, removes small regions and exports reviewable outputs. It does not distinguish cracks from dirt, shadows or reflections, determine structural severity, control a robot or provide a safety decision. Thin cracks may disappear during morphological filtering. No field accuracy, payload capability or autonomous blade-climbing performance is claimed.

Next technical milestones: collect legally usable labelled blade images, evaluate false positives and missed defects, compare against a learned detector, then validate a camera interface independently of robot motion. See [validation plan](inspection.md#validation-plan).

[Badr's profile](https://github.com/BadrEss01) · [Source and reuse notes](../NOTICE.md)

[Back to climbing-robot research](../README.md)
