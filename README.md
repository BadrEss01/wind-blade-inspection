# Wind-blade inspection: climbing robot and visual screening

[![Inspection tests](https://github.com/BadrEss01/wind-blade-inspection/actions/workflows/tests.yml/badge.svg)](https://github.com/BadrEss01/wind-blade-inspection/actions/workflows/tests.yml)

A robotics design case study paired with a runnable Python/OpenCV surface-inspection extension. The original cooperative project investigated deploying a wall-climbing robot onto a wind-turbine blade. This repository brings its mechanical design context together with an image-processing tool for locating candidate surface anomalies.

**Two stages, one project:** the historical work covers the robot concept and prototype; the September 2026 extension processes still images. The detector has not been integrated with the robot or validated on real turbine defects.

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

![OpenCV baseline on a synthetic line and spot](examples/result/overlay.png)

The demo input is generated, not a blade photograph. The dark line and spot demonstrate software behavior only. Recreate the sample and outputs with `python scripts/make_demo.py`.

## Trainable ML segmentation (2026 extension)

A compact PyTorch U-Net complements the classical OpenCV baseline. It includes
paired image/mask loading, group-aware split checks, augmentation, BCE + Dice loss,
validation-based checkpoint selection, held-out evaluation and inference exports.
No pretrained or real-blade-trained weights are bundled. Read the [model card](docs/MODEL_CARD.md).

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
Use `--data-kind real` only for actual photographed data. Synthetic metrics verify
the pipeline and must not be described as field accuracy.

The ML commands export checkpoints/history, pixel-level metrics, probability arrays,
masks and overlays. The simple baseline remains available for comparison.

## Robot design details

The report describes two belt-driven climbing modules with passive suction cups. A guide rail presses cups onto the surface, manages their transition and detachment, and uses a tail to help balance reaction forces. A swivel couples the modules to the payload chassis to support turning.

The assembly section specifies two 12 V, 146 RPM brushed DC motors with encoders, a dual H-bridge driver and an HX711-based force-sensor module. It describes PID mobility control using an ArduPilot board. Original CAD source, wiring, firmware and experiment logs have not been recovered, so this is design documentation rather than a build-ready hardware release.

Read the [hardware design and evidence](docs/robot-design.md), [inspection method and validation](docs/inspection.md), and [authorship and sources](docs/provenance.md).

## Contribution and authorship

Badr Essefiany reports work on the ground-robot design in Fusion 360, 3D-printed parts, assembly and programming. The report is coauthored with **Calin Constantin Clichici, Dongwook Lee and Wail Bougida**, supervised by **Acquahmeyer Drone Tech and Prof. Francesco Maurelli**, at Jacobs University Bremen. Its UAV experiments are team context and are not attributed solely to Badr.

The image-inspection software is a new AI-assisted extension maintained by Badr, evolved from the earlier baseline in [Computer_Vision](https://github.com/BadrEss01/Computer_Vision/tree/main/projects/wall-blade-surface-defects). It is not presented as original thesis code.

## Repository layout

| Location | Contents |
| --- | --- |
| `src/blade_inspection/` | Detection library and command-line interface |
| `tests/` | Detector and end-to-end file-output tests |
| `examples/` | Synthetic input, reference mask and generated outputs |
| `scripts/make_demo.py` | Deterministic sample generator |
| `docs/` | Robot design, source evidence and validation limits |
| `.github/workflows/` | Automated tests on Python 3.10 and 3.12 |

## What it can establish

The executable pipeline highlights local grayscale contrast, removes small regions and exports reviewable outputs. It does not distinguish cracks from dirt, shadows or reflections, determine structural severity, control a robot or provide a safety decision. Thin cracks may disappear during morphological filtering. No field accuracy, payload capability or autonomous blade-climbing performance is claimed.

Next technical milestones: collect legally usable labelled blade images, evaluate false positives and missed defects, compare against a learned detector, then validate a camera interface independently of robot motion. See [validation plan](docs/inspection.md#validation-plan).

[Badr's profile](https://github.com/BadrEss01) · [Source and reuse notes](NOTICE.md)
