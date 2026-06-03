import hashlib
import importlib.util
from datetime import datetime
from pathlib import Path

from django.conf import settings


class AIInferenceService:
    _model_cache = {}

    def info(self):
        model_path = Path(settings.AI_SERVICE_CONFIG["MODEL_PATH"])
        has_ultralytics = importlib.util.find_spec("ultralytics") is not None
        enabled = model_path.exists() and has_ultralytics
        return {
            "enabled": enabled,
            "config": settings.AI_SERVICE_CONFIG,
            "model_exists": model_path.exists(),
            "ultralytics_available": has_ultralytics,
            "message": (
                "YOLOv8 病虫害检测模型已就绪。"
                if enabled
                else "未检测到可用 YOLOv8 权重或 ultralytics，诊断接口将使用 mock 兜底。"
            ),
        }

    def run_diagnosis(self, file_name, file_path, file_size):
        """
        病虫害诊断统一入口。

        - 如果本地 YOLOv8 权重存在，则直接调用 ultralytics 推理。
        - 如果权重缺失、依赖未安装或推理异常，默认回退到 mock 结果，保证演示流程不断。
        """

        model_path = Path(settings.AI_SERVICE_CONFIG["MODEL_PATH"])
        if not model_path.exists():
            return self._run_mock_diagnosis(
                file_name=file_name,
                file_path=file_path,
                file_size=file_size,
                fallback_reason=f"模型文件不存在：{model_path}",
            )

        try:
            return self._run_yolo_diagnosis(
                file_name=file_name,
                file_path=file_path,
                model_path=model_path,
            )
        except Exception as exc:
            if settings.AI_SERVICE_CONFIG["FALLBACK_TO_MOCK"]:
                return self._run_mock_diagnosis(
                    file_name=file_name,
                    file_path=file_path,
                    file_size=file_size,
                    fallback_reason=f"YOLOv8 推理失败，已回退 mock：{exc}",
                )
            raise

    def _run_yolo_diagnosis(self, file_name, file_path, model_path):
        try:
            from ultralytics import YOLO
        except ImportError as exc:
            raise RuntimeError("缺少 ultralytics 依赖，请先安装 requirements.txt") from exc

        model = self._get_yolo_model(YOLO, model_path)
        predictions = model.predict(
            source=file_path,
            imgsz=settings.AI_SERVICE_CONFIG["IMAGE_SIZE"],
            conf=settings.AI_SERVICE_CONFIG["CONFIDENCE_THRESHOLD"],
            iou=settings.AI_SERVICE_CONFIG["IOU_THRESHOLD"],
            device=settings.AI_SERVICE_CONFIG["DEVICE"],
            verbose=False,
        )
        if not predictions:
            raise RuntimeError("模型未返回推理结果")

        result = predictions[0]
        image_height, image_width = self._get_result_image_size(result)
        boxes = self._serialize_yolo_boxes(result, image_width=image_width, image_height=image_height)
        top_box = boxes[0] if boxes else None

        if top_box:
            disease_name = top_box["label"]
            confidence = top_box["score"]
            risk_level = self._risk_level_from_confidence(confidence)
            suggestion = self._build_suggestion(disease_name, risk_level, confidence)
        else:
            disease_name = "未见明显病虫害"
            confidence = 0
            risk_level = "低"
            suggestion = "模型未检出明显病虫害目标，建议保持常规巡检并继续积累样本。"

        return {
            "task_code": self._build_task_code(),
            "status": "success",
            "inference_mode": "yolov8",
            "message": "已调用本地 YOLOv8 病虫害检测模型完成识别。",
            "model_hint": f"model_path={model_path}",
            "result": {
                "disease_name": disease_name,
                "confidence": confidence,
                "risk_level": risk_level,
                "suggestion": suggestion,
                "boxes": boxes,
                "image_size": {
                    "width": image_width,
                    "height": image_height,
                },
                "detected_count": len(boxes),
            },
            "source_file": file_path,
        }

    def _run_mock_diagnosis(self, file_name, file_path, file_size, fallback_reason=""):
        seed = hashlib.md5(f"{file_name}:{file_size}".encode("utf-8")).hexdigest()
        templates = [
            {
                "disease_name": "茎腐病",
                "risk_level": "高",
                "suggestion": "建议立即隔离疑似病株，优先开展人工复核，并结合园区植保方案进行定点防治。",
                "boxes": [
                    {"x": 92, "y": 74, "width": 146, "height": 112, "label": "疑似茎腐病", "score": 0.93},
                    {"x": 282, "y": 168, "width": 118, "height": 88, "label": "高风险区域", "score": 0.88},
                ],
            },
            {
                "disease_name": "炭疽病",
                "risk_level": "中高",
                "suggestion": "建议及时清理病斑枝条，并结合实际情况进行药剂防治。",
                "boxes": [
                    {"x": 120, "y": 80, "width": 160, "height": 120, "label": "疑似病斑", "score": 0.91},
                    {"x": 308, "y": 188, "width": 126, "height": 92, "label": "扩散关注区", "score": 0.86},
                ],
            },
            {
                "disease_name": "红蜘蛛虫害",
                "risk_level": "中",
                "suggestion": "建议加强叶背复核与虫口密度监测，必要时对重点区域实施精准防治。",
                "boxes": [
                    {"x": 108, "y": 98, "width": 154, "height": 110, "label": "虫害疑似区", "score": 0.89},
                    {"x": 294, "y": 144, "width": 112, "height": 84, "label": "叶背重点区", "score": 0.84},
                ],
            },
            {
                "disease_name": "未见明显病虫害",
                "risk_level": "低",
                "suggestion": "当前未发现明显异常，可维持现有巡检频次并继续积累样本用于后续模型训练。",
                "boxes": [
                    {"x": 136, "y": 94, "width": 148, "height": 116, "label": "重点观察区", "score": 0.79},
                ],
            },
        ]

        template = templates[int(seed[:2], 16) % len(templates)]
        confidence = round(0.74 + (int(seed[2:4], 16) / 255) * 0.23, 3)

        return {
            "task_code": self._build_task_code(),
            "status": "success",
            "inference_mode": "mock",
            "message": fallback_reason or "当前为 mock 推理结果，待放置 YOLOv8 权重后自动切换真实模型。",
            "model_hint": "将训练好的 .pt 放到 models/dragonfruit_disease_yolov8s.pt 后启用 YOLOv8 推理。",
            "result": {
                "disease_name": template["disease_name"],
                "confidence": confidence,
                "risk_level": template["risk_level"],
                "suggestion": template["suggestion"],
                "boxes": [
                    {
                        **box,
                        "score": round(min(confidence, box["score"]), 2),
                    }
                    for box in template["boxes"]
                ],
                "image_size": {
                    "width": 640,
                    "height": 360,
                },
                "detected_count": len(template["boxes"]),
            },
            "source_file": file_path,
        }

    def _get_yolo_model(self, yolo_class, model_path):
        cache_key = str(model_path)
        if cache_key not in self._model_cache:
            self._model_cache[cache_key] = yolo_class(cache_key)
        return self._model_cache[cache_key]

    def _get_result_image_size(self, result):
        shape = getattr(result, "orig_shape", None)
        if shape and len(shape) >= 2:
            return int(shape[0]), int(shape[1])
        return 360, 640

    def _serialize_yolo_boxes(self, result, image_width, image_height):
        raw_boxes = getattr(result, "boxes", None)
        if raw_boxes is None or len(raw_boxes) == 0:
            return []

        xyxy_values = raw_boxes.xyxy.detach().cpu().tolist()
        conf_values = raw_boxes.conf.detach().cpu().tolist()
        cls_values = raw_boxes.cls.detach().cpu().tolist()
        names = getattr(result, "names", {}) or {}

        boxes = []
        for xyxy, confidence, class_id in zip(xyxy_values, conf_values, cls_values):
            x1, y1, x2, y2 = xyxy
            x1 = max(0.0, min(float(x1), float(image_width)))
            y1 = max(0.0, min(float(y1), float(image_height)))
            x2 = max(0.0, min(float(x2), float(image_width)))
            y2 = max(0.0, min(float(y2), float(image_height)))
            width = max(0.0, x2 - x1)
            height = max(0.0, y2 - y1)
            if width <= 0 or height <= 0:
                continue

            boxes.append(
                {
                    "x": round(x1, 2),
                    "y": round(y1, 2),
                    "width": round(width, 2),
                    "height": round(height, 2),
                    "label": self._resolve_class_name(names, int(class_id)),
                    "score": round(float(confidence), 4),
                    "class_id": int(class_id),
                }
            )

        return sorted(boxes, key=lambda item: item["score"], reverse=True)

    def _resolve_class_name(self, names, class_id):
        if isinstance(names, dict):
            return str(names.get(class_id, class_id))
        if isinstance(names, (list, tuple)) and 0 <= class_id < len(names):
            return str(names[class_id])
        return str(class_id)

    def _risk_level_from_confidence(self, confidence):
        if confidence >= 0.85:
            return "高"
        if confidence >= 0.7:
            return "中高"
        if confidence >= 0.45:
            return "中"
        return "低"

    def _build_suggestion(self, disease_name, risk_level, confidence):
        suggestion_map = {
            "茎腐病": "建议隔离疑似病株，减少高湿环境，并尽快安排人工复核和定点防治。",
            "炭疽病": "建议清理病斑枝条或果面样本，加强通风，并结合植保方案进行药剂防控。",
            "红蜘蛛": "建议重点复核叶背和嫩梢区域，监测虫口密度，必要时进行精准防治。",
        }
        for keyword, suggestion in suggestion_map.items():
            if keyword in disease_name:
                return suggestion
        return (
            f"模型识别为 {disease_name}，风险等级 {risk_level}，"
            f"置信度 {confidence:.1%}。建议结合现场样本进行人工复核后处理。"
        )

    def _build_task_code(self):
        return f"DIA{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

    def generate_decision_strategy(self, block_code, seed_payload):
        """
        当前 mock 决策流程：
        - 直接基于种子 payload 返回模拟策略

        未来真实模型接入点：
        - 在这里接入智能决策模型
        - 输入长势、病害、土壤、气象、设备反馈等多源特征
        - 输出处方等级、灌溉量、施肥量和执行时段建议
        """

        return {
            **seed_payload,
            "payload": {
                **seed_payload["payload"],
                "decision_model_hint": "当前为 mock 决策结果，后续在此接入智能决策模型。",
                "target_block": block_code,
            },
        }
