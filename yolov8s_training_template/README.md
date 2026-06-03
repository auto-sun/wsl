# YOLOv8s Training Template

这个目录是 YOLOv8s 目标检测训练模板，数据集和参数后续再补。

## 目录内容

- `train_yolov8s.py`: Python 训练入口。
- `dataset.yaml`: 数据集配置占位文件，目前只保留注释模板。
- `requirements.txt`: 训练相关依赖提示。

## 使用步骤

1. 准备数据集，建议结构：

```text
dataset/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
└── labels/
    ├── train/
    ├── val/
    └── test/
```

2. 填写 `dataset.yaml`。

3. 安装训练依赖：

```bash
conda activate dragon-fruit
pip install -r yolov8s_training_template/requirements.txt
```

4. 启动训练：

```bash
python yolov8s_training_template/train_yolov8s.py
```

也可以临时覆盖参数：

```bash
python yolov8s_training_template/train_yolov8s.py \
  --epochs 100 \
  --imgsz 640 \
  --batch 16 \
  --device 0
```

## 说明

- 默认模型为 `yolov8s.pt`。
- 默认输出目录为 `yolov8s_training_template/runs/`。
- 当前 `dataset.yaml` 未填写时，脚本会直接退出并提示先补数据集配置。
