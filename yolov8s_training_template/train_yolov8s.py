from __future__ import annotations

import argparse
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_YAML = ROOT_DIR / "dataset.yaml"
DEFAULT_RUNS_DIR = ROOT_DIR / "runs"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a YOLOv8s detection model.")
    parser.add_argument("--data", default=str(DEFAULT_DATA_YAML), help="Path to dataset yaml.")
    parser.add_argument("--model", default="yolov8s.pt", help="Model checkpoint or config.")
    parser.add_argument("--epochs", type=int, default=100, help="Training epochs.")
    parser.add_argument("--imgsz", type=int, default=640, help="Input image size.")
    parser.add_argument("--batch", type=int, default=16, help="Batch size.")
    parser.add_argument("--device", default="0", help="CUDA device id, 'cpu', or comma-separated ids.")
    parser.add_argument("--workers", type=int, default=8, help="Data loader workers.")
    parser.add_argument("--project", default=str(DEFAULT_RUNS_DIR), help="Output project directory.")
    parser.add_argument("--name", default="yolov8s_train", help="Run name.")
    parser.add_argument("--patience", type=int, default=50, help="Early stopping patience.")
    parser.add_argument("--cache", action="store_true", help="Cache images for faster training.")
    parser.add_argument("--resume", action="store_true", help="Resume previous training.")
    return parser.parse_args()


def has_dataset_config(data_yaml: Path) -> bool:
    if not data_yaml.exists():
        return False

    for line in data_yaml.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return True
    return False


def main() -> None:
    args = parse_args()
    data_yaml = Path(args.data).expanduser().resolve()

    if not has_dataset_config(data_yaml):
        raise SystemExit(
            f"Dataset config is empty: {data_yaml}\n"
            "Fill dataset.yaml before starting training."
        )

    try:
        from ultralytics import YOLO
    except ImportError as exc:
        raise SystemExit(
            "Missing dependency: ultralytics\n"
            "Install it with: pip install -r yolov8s_training_template/requirements.txt"
        ) from exc

    model = YOLO(args.model)
    model.train(
        data=str(data_yaml),
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        workers=args.workers,
        project=args.project,
        name=args.name,
        patience=args.patience,
        cache=args.cache,
        resume=args.resume,
    )


if __name__ == "__main__":
    main()
