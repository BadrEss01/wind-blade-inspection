# Surface segmentation model

## Intended use and status

SmallUNet is a compact supervised segmentation baseline implemented in PyTorch.
No pretrained or real-blade-trained weights are bundled. A synthetic smoke run
trains on generated lines and clean backgrounds to verify training, checkpoint
reload and inference. This is not evidence of turbine defect recognition.

## Architecture and training

RGB input in [0,1], two encoder levels (16 and 32 channels), 64-channel bridge,
bilinear upsampling with skip connections, and one-channel logits. Training uses
Adam, binary cross entropy with logits plus soft Dice loss, and paired horizontal
flips on training data. Validation loss selects the checkpoint. The untouched test
split is evaluated separately. All execution defaults to CPU for reproducibility.

Images are resized to a square; masks use nearest-neighbor interpolation. Resizing
can erase thin cracks and distort geometry. For field use, investigate tiled native
resolution inference and image calibration before tuning the model architecture.

## Data contract

CSV columns: image,mask,split,group. Paths are relative to the manifest. Masks must
contain 0 background and 255 foreground. Split is train, val or test. Group should
identify a blade or capture session, so near-duplicate views do not cross splits.
The loader rejects groups and identical image files spanning multiple splits.
It cannot automatically detect renamed/recompressed near-duplicates.

The training data kind must be explicitly declared as real or synthetic. Keep
dataset source, license, annotation procedure and group definition with the data.
There is no automatic verification that a user-declared real dataset is genuine.

## Evaluation

Metrics are pixel-level micro IoU, Dice, precision and recall at threshold 0.5.
Undefined ratios return zero; counts are also reported for interpretation. No
real-world score is claimed. Synthetic scores must not be used as defect-detection
accuracy in a CV. Compare real-data results to the existing OpenCV baseline and
review false positives, missed small defects and performance on clean surfaces.

## Limits

No classification of crack/erosion/dirt; no physical severity estimate; no robot
interface. Lighting, curvature and surface texture can cause false detections.
Only load checkpoints from trusted sources. Training histories and checkpoints
are local outputs; no dataset or company material is published by these commands.
