import hashlib
from datetime import datetime

from django.conf import settings


class AIInferenceService:
    def info(self):
        return {
            "enabled": False,
            "config": settings.AI_SERVICE_CONFIG,
            "message": "TODO: 接入病虫害识别模型、长势分析模型和推理任务编排。",
        }

    def run_diagnosis(self, file_name, file_path, file_size):
        """
        当前 mock 推理流程：
        - 根据文件名和文件大小生成稳定的演示结果
        - 返回结构与未来真实模型推理保持一致，便于后续平滑替换

        未来真实模型接入点：
        - 在这里加载 PyTorch / ONNX / TensorFlow 模型
        - 对输入图片做预处理、推理、后处理
        - 输出真实类别、置信度、风险等级和标注框
        """

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
            "task_code": f"DIA{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "status": "success",
            "inference_mode": "mock",
            "message": "当前为 mock 推理结果，待后续接入真实模型。",
            "model_hint": "TODO: 在 AIInferenceService.run_diagnosis 中替换为真实模型推理。",
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
            },
            "source_file": file_path,
        }

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
