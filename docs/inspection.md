# Visual inspection method

The pipeline is a classical contrast-anomaly baseline:

1. Accept a nonempty uint8 grayscale or BGR image.
2. Convert BGR to grayscale.
3. Estimate background intensity with a Gaussian blur.
4. Threshold the absolute intensity difference.
5. Apply a 3x3 morphological opening.
6. Remove connected components smaller than the selected area.
7. Export boxes, binary mask, annotated input and JSON metadata.

The Gaussian kernel must be an odd integer at least 3. The contrast threshold is finite and in (0,255]; the area is a positive integer in pixels. These parameters depend on resolution and lighting, with no physical units implied. The CLI loads images using OpenCV's BGR convention.

## Output schema

`report.json` records the input filename, image size, parameters, candidate count, nonzero mask-pixel count, `[x,y,width,height]` boxes and a plain-language interpretation. No class probability or defect severity is calculated.

## Tests and demo

Unit tests cover a local dark region, uniform surfaces, empty and unsupported images, invalid threshold, and file-output consistency. A subprocess test checks that a missing input exits unsuccessfully. GitHub Actions also runs the installed command against the committed sample.

The demo generator draws a line and a circular contrast region on a flat synthetic background. `synthetic_truth.png` describes those drawn regions; it is not a human-labelled field dataset. Morphology and local contrast alter their detected boundaries. The example is a reproducibility fixture, not an accuracy benchmark.

## Failure modes

Shadows, dirt, seams and reflections can create false positives. Low-contrast or very thin defects may be missed; opening erodes narrow features. Large uniform defects may be detected only at their boundaries. Color-only changes may disappear in grayscale. Perspective changes and curved blade surfaces are unmodelled.

## Validation plan

Obtain permissioned blade photographs and pixel masks or boxes. Record specimen and capture-session identifiers. Split by blade/session to avoid near-duplicate leakage. Tune parameters only on training/validation data and retain a held-out test set. Report precision, recall, localization quality and failure examples at fixed thresholds, including negative images and varied lighting. Compare with a learned detector on the same split. Hardware integration comes after image-level evaluation.
