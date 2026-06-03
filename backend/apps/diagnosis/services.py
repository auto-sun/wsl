import os
import uuid

from django.core.files.storage import default_storage
from django.utils import timezone

from services.ai.inference import AIInferenceService

from .mock_history import get_default_history
from .models import DiagnosisTask


class DiagnosisService:
    """
    病虫害诊断服务。

    当前阶段：
    - 负责上传图片保存、YOLOv8/mock 推理调用、诊断记录创建、历史记录查询
    - 统一封装诊断流程，避免将模型调用逻辑直接堆在 API view 中

    未来阶段：
    - 可在这里切换为异步任务编排
    - 可接入任务队列、模型版本管理、批量检测
    """

    def __init__(self, inference_service=None):
        self.inference_service = inference_service or AIInferenceService()

    def create_diagnosis_task(self, upload_file, request):
        stored_path = self._store_upload_file(upload_file)

        # 文件保存成功后调用统一推理服务；推理服务会优先使用 YOLOv8 权重，
        # 权重缺失或推理异常时默认回退 mock，保证演示流程可用。
        inference_result = self.inference_service.run_diagnosis(
            file_name=upload_file.name,
            file_path=default_storage.path(stored_path),
            file_size=upload_file.size,
        )

        task = DiagnosisTask.objects.create(
            task_code=inference_result["task_code"],
            image_name=upload_file.name,
            stored_path=stored_path,
            diagnosis_name=inference_result["result"]["disease_name"],
            confidence=inference_result["result"]["confidence"],
            risk_level=inference_result["result"]["risk_level"],
            status=inference_result["status"],
            suggestions=[inference_result["result"]["suggestion"]],
            overlay_boxes=inference_result["result"]["boxes"],
            result_payload=inference_result,
            inference_mode=inference_result["inference_mode"],
        )

        return {
            "task_id": task.id,
            "image_url": f"/media/{stored_path}",
            "status": inference_result["status"],
            "result": inference_result["result"],
            "message": inference_result["message"],
            "inference_mode": inference_result["inference_mode"],
            "model_hint": inference_result.get("model_hint", ""),
        }

    def get_history_payload(self, limit=10):
        records = DiagnosisTask.objects.all()[:limit]
        if not records:
            return {
                "history": get_default_history(),
                "mode": "mock_seed",
            }

        return {
            "history": [self._serialize_history_record(item) for item in records],
            "mode": "database",
        }

    def _store_upload_file(self, upload_file):
        extension = os.path.splitext(upload_file.name)[1] or ".jpg"
        storage_key = f"diagnosis/{timezone.now().strftime('%Y%m%d')}/{uuid.uuid4().hex}{extension}"
        return default_storage.save(storage_key, upload_file)

    def _serialize_history_record(self, task):
        return {
            "task_code": task.task_code,
            "image_name": task.image_name,
            "diagnosis_name": task.diagnosis_name,
            "confidence": task.confidence,
            "risk_level": task.risk_level,
            "created_at": timezone.localtime(task.created_at).strftime("%Y-%m-%d %H:%M"),
        }
