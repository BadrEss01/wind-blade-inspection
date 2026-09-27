"""Compact U-Net segmentation, supervised training and checkpoint inference.

No pretrained weights are bundled. Synthetic smoke tests verify execution only.
"""

import argparse
import csv
import hashlib
import json
from pathlib import Path

import cv2
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import Dataset, DataLoader


class Block(nn.Sequential):
    def __init__(self, incoming, outgoing):
        super().__init__(
            nn.Conv2d(incoming, outgoing, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(outgoing, outgoing, 3, padding=1),
            nn.ReLU(),
        )


class SmallUNet(nn.Module):
    """Two-level encoder/decoder with skip connections; returns pixel logits."""

    def __init__(self, width=16):
        super().__init__()
        self.enc1 = Block(3, width)
        self.enc2 = Block(width, width * 2)
        self.bridge = Block(width * 2, width * 4)
        self.dec2 = Block(width * 6, width * 2)
        self.dec1 = Block(width * 3, width)
        self.head = nn.Conv2d(width, 1, 1)

    def forward(self, x):
        a = self.enc1(x)
        b = self.enc2(F.max_pool2d(a, 2))
        c = self.bridge(F.max_pool2d(b, 2))
        d = self.dec2(
            torch.cat(
                [
                    F.interpolate(
                        c, size=b.shape[-2:], mode="bilinear", align_corners=False
                    ),
                    b,
                ],
                1,
            )
        )
        e = self.dec1(
            torch.cat(
                [
                    F.interpolate(
                        d, size=a.shape[-2:], mode="bilinear", align_corners=False
                    ),
                    a,
                ],
                1,
            )
        )
        return self.head(e)


def read_manifest(path):
    path = Path(path)
    with path.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    if not rows or not {"image", "mask", "split", "group"}.issubset(rows[0]):
        raise ValueError("Manifest requires image,mask,split,group columns")
    groups, hashes = {}, {}
    for row in rows:
        if row["split"] not in ("train", "val", "test") or not row["group"]:
            raise ValueError(
                "Each row needs train/val/test split and a blade/session group"
            )
        prior = groups.setdefault(row["group"], row["split"])
        if prior != row["split"]:
            raise ValueError("Group leakage across splits")
        for key in ("image", "mask"):
            row[key] = str((path.parent / row[key]).resolve())
            if not Path(row[key]).is_file():
                raise ValueError("Missing " + row[key])
        digest = hashlib.sha256(Path(row["image"]).read_bytes()).hexdigest()
        if digest in hashes and hashes[digest] != row["split"]:
            raise ValueError("Duplicate image leakage across splits")
        hashes[digest] = row["split"]
    return rows


def image_tensor(image, size):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    rgb = cv2.resize(rgb, (size, size), interpolation=cv2.INTER_AREA)
    return torch.from_numpy(rgb.transpose(2, 0, 1).copy()).float() / 255.0


class MaskDataset(Dataset):
    def __init__(self, rows, split, size, augment=False):
        self.rows = [r for r in rows if r["split"] == split]
        self.size, self.augment = size, augment
        if not self.rows:
            raise ValueError("No samples for split " + split)

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, index):
        row = self.rows[index]
        image = cv2.imread(row["image"])
        mask = cv2.imread(row["mask"], cv2.IMREAD_GRAYSCALE)
        if image is None or mask is None or image.shape[:2] != mask.shape:
            raise ValueError("Unreadable or mismatched image/mask: " + row["image"])
        if not np.isin(mask, [0, 255]).all():
            raise ValueError("Masks must use 0 background and 255 foreground")
        x = image_tensor(image, self.size)
        y = (
            torch.from_numpy(
                cv2.resize(
                    mask, (self.size, self.size), interpolation=cv2.INTER_NEAREST
                ).copy()
            ).float()[None]
            / 255.0
        )
        if self.augment and torch.rand(()).item() < 0.5:
            x, y = x.flip(-1), y.flip(-1)
        return x, y


def loss_fn(logits, target):
    probability = logits.sigmoid()
    dims = (1, 2, 3)
    dice = (2 * (probability * target).sum(dims) + 1) / (
        probability.sum(dims) + target.sum(dims) + 1
    )
    return F.binary_cross_entropy_with_logits(logits, target) + (1 - dice).mean()


@torch.no_grad()
def evaluate(model, loader):
    model.eval()
    tp = fp = fn = 0
    loss, count = 0.0, 0
    for x, y in loader:
        logits = model(x)
        loss += loss_fn(logits, y).item() * len(x)
        count += len(x)
        p, t = logits.sigmoid() >= 0.5, y.bool()
        tp += (p & t).sum().item()
        fp += (p & ~t).sum().item()
        fn += (~p & t).sum().item()
    return {
        "loss": loss / count,
        "iou": tp / max(tp + fp + fn, 1),
        "dice": 2 * tp / max(2 * tp + fp + fn, 1),
        "precision": tp / max(tp + fp, 1),
        "recall": tp / max(tp + fn, 1),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "images": count,
        "threshold": 0.5,
    }


def train(
    manifest, output, epochs=10, size=128, batch_size=4, seed=42, data_kind="synthetic"
):
    if epochs < 1 or size < 16 or batch_size < 1:
        raise ValueError("epochs/batch_size must be positive and size >=16")
    if data_kind not in ("synthetic", "real"):
        raise ValueError("data_kind must be synthetic or real")
    torch.manual_seed(seed)
    torch.set_num_threads(2)
    rows = read_manifest(manifest)
    training = DataLoader(
        MaskDataset(rows, "train", size, True), batch_size=batch_size, shuffle=True
    )
    validation = DataLoader(MaskDataset(rows, "val", size), batch_size=batch_size)
    model = SmallUNet()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    history, best = [], float("inf")
    for epoch in range(1, epochs + 1):
        model.train()
        for x, y in training:
            optimizer.zero_grad()
            loss_fn(model(x), y).backward()
            optimizer.step()
        metrics = evaluate(model, validation)
        history.append({"epoch": epoch, "validation": metrics})
        if metrics["loss"] < best:
            best = metrics["loss"]
            torch.save(
                {
                    "state_dict": model.state_dict(),
                    "architecture": "small_unet_v1",
                    "input_size": size,
                    "epoch": epoch,
                    "data_kind": data_kind,
                    "seed": seed,
                    "validation": metrics,
                    "manifest_sha256": hashlib.sha256(
                        Path(manifest).read_bytes()
                    ).hexdigest(),
                    "training_status": "trained_" + data_kind,
                },
                output / "best.pt",
            )
    (output / "history.json").write_text(json.dumps(history, indent=2) + "\n")
    return history


def load_model(checkpoint):
    # Load only your own/trusted checkpoints, even with weights_only enabled.
    data = torch.load(checkpoint, map_location="cpu", weights_only=True)
    if data.get("architecture") != "small_unet_v1" or data.get(
        "training_status"
    ) not in ("trained_real", "trained_synthetic"):
        raise ValueError("Expected a trained small_unet_v1 checkpoint")
    model = SmallUNet()
    model.load_state_dict(data["state_dict"])
    model.eval()
    return model, data


@torch.no_grad()
def predict(checkpoint, source, output):
    model, metadata = load_model(checkpoint)
    image = cv2.imread(str(source))
    if image is None:
        raise ValueError("Cannot read image " + str(source))
    probability = (
        model(image_tensor(image, metadata["input_size"])[None]).sigmoid()[0, 0].numpy()
    )
    probability = cv2.resize(probability, (image.shape[1], image.shape[0]))
    mask = (probability >= 0.5).astype(np.uint8) * 255
    overlay = image.copy()
    overlay[mask > 0] = (0.5 * image[mask > 0] + 0.5 * np.array([0, 0, 255])).astype(
        np.uint8
    )
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    for name, pixels in [("mask.png", mask), ("overlay.png", overlay)]:
        if not cv2.imwrite(str(output / name), pixels):
            raise OSError("Cannot write " + name)
    np.save(output / "probability.npy", probability)
    report = {
        k: metadata[k]
        for k in ("architecture", "training_status", "data_kind", "epoch")
    }
    report.update(
        {
            "threshold": 0.5,
            "mask_pixels": int(np.count_nonzero(mask)),
            "interpretation": "Model predictions; no field validation or structural diagnosis.",
        }
    )
    (output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    t = commands.add_parser("train")
    t.add_argument("manifest")
    t.add_argument("--output", default="outputs/ml")
    t.add_argument("--epochs", type=int, default=10)
    t.add_argument("--size", type=int, default=128)
    t.add_argument("--data-kind", choices=["real", "synthetic"], required=True)
    p = commands.add_parser("predict")
    p.add_argument("checkpoint")
    p.add_argument("image")
    p.add_argument("--output", default="outputs/prediction")
    e = commands.add_parser("evaluate")
    e.add_argument("checkpoint")
    e.add_argument("manifest")
    args = parser.parse_args()
    if args.command == "train":
        print(
            json.dumps(
                train(
                    args.manifest,
                    args.output,
                    args.epochs,
                    args.size,
                    data_kind=args.data_kind,
                ),
                indent=2,
            )
        )
    elif args.command == "predict":
        print(json.dumps(predict(args.checkpoint, args.image, args.output), indent=2))
    else:
        model, data = load_model(args.checkpoint)
        loader = DataLoader(
            MaskDataset(read_manifest(args.manifest), "test", data["input_size"]),
            batch_size=4,
        )
        print(
            json.dumps(
                {
                    "training_status": data["training_status"],
                    "test": evaluate(model, loader),
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
