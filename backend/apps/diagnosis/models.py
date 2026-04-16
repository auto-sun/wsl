from django.db import models


class DiagnosisTask(models.Model):
    """
    病虫害诊断任务记录。

    当前阶段：
    - 仅保存上传图片与 mock 推理结果
    - 不接真实模型，不接消息队列

    后续阶段：
    - 可扩展任务状态机、异步推理、批量检测、真实标注框和模型版本管理
    """

    task_code = models.CharField(max_length=32, unique=True, verbose_name="任务编号")
    image_name = models.CharField(max_length=255, verbose_name="原始图片名称")
    stored_path = models.CharField(max_length=255, verbose_name="存储路径")
    diagnosis_name = models.CharField(max_length=100, blank=True, verbose_name="疑似病虫害名称")
    confidence = models.FloatField(default=0, verbose_name="置信度")
    risk_level = models.CharField(max_length=20, blank=True, verbose_name="风险等级")
    status = models.CharField(max_length=20, default="completed", verbose_name="任务状态")
    suggestions = models.JSONField(default=list, blank=True, verbose_name="建议措施")
    overlay_boxes = models.JSONField(default=list, blank=True, verbose_name="标注框")
    result_payload = models.JSONField(default=dict, blank=True, verbose_name="完整结果")
    inference_mode = models.CharField(max_length=20, default="mock", verbose_name="推理模式")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "病虫害诊断任务"
        verbose_name_plural = "病虫害诊断任务"

    def __str__(self):
        return self.task_code
