from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True


class OrchardBlock(TimestampedModel):
    block_code = models.CharField(max_length=32, unique=True, verbose_name="地块编号")
    name = models.CharField(max_length=64, verbose_name="地块名称")
    area_mu = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name="面积(亩)",
    )
    growth_stage = models.CharField(max_length=32, blank=True, verbose_name="生长阶段")
    metadata = models.JSONField(default=dict, blank=True, verbose_name="扩展信息")

    class Meta:
        verbose_name = "园区地块"
        verbose_name_plural = "园区地块"

    def __str__(self):
        return f"{self.block_code} - {self.name}"


class DeviceRecord(TimestampedModel):
    device_code = models.CharField(max_length=32, unique=True, verbose_name="设备编码")
    name = models.CharField(max_length=64, verbose_name="设备名称")
    device_type = models.CharField(max_length=32, verbose_name="设备类型")
    status = models.CharField(max_length=24, default="offline", verbose_name="设备状态")
    online = models.BooleanField(default=False, verbose_name="是否在线")
    last_seen = models.DateTimeField(null=True, blank=True, verbose_name="最后心跳时间")
    metadata = models.JSONField(default=dict, blank=True, verbose_name="扩展信息")

    class Meta:
        verbose_name = "设备台账"
        verbose_name_plural = "设备台账"

    def __str__(self):
        return f"{self.device_code} - {self.name}"


class PrescriptionPlan(TimestampedModel):
    plan_code = models.CharField(max_length=32, unique=True, verbose_name="策略编号")
    block_code = models.CharField(max_length=32, verbose_name="地块编号")
    status = models.CharField(max_length=24, default="draft", verbose_name="状态")
    target_date = models.DateField(null=True, blank=True, verbose_name="执行日期")
    payload = models.JSONField(default=dict, blank=True, verbose_name="策略内容")

    class Meta:
        verbose_name = "水肥处方"
        verbose_name_plural = "水肥处方"

    def __str__(self):
        return self.plan_code


class DiseaseDetectionRecord(TimestampedModel):
    task_code = models.CharField(max_length=32, unique=True, verbose_name="任务编号")
    image_name = models.CharField(max_length=128, verbose_name="原始文件名")
    stored_path = models.CharField(max_length=255, blank=True, verbose_name="存储路径")
    plot_code = models.CharField(max_length=32, blank=True, verbose_name="地块编号")
    disease_name = models.CharField(max_length=64, blank=True, verbose_name="识别结果")
    confidence = models.FloatField(default=0, verbose_name="置信度")
    severity = models.CharField(max_length=24, blank=True, verbose_name="风险等级")
    status = models.CharField(max_length=24, default="completed", verbose_name="任务状态")
    result_payload = models.JSONField(default=dict, blank=True, verbose_name="结果详情")

    class Meta:
        verbose_name = "病虫害检测记录"
        verbose_name_plural = "病虫害检测记录"
        ordering = ["-created_at"]

    def __str__(self):
        return self.task_code
