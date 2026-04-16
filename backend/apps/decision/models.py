from django.db import models


class DecisionPlan(models.Model):
    """
    水肥处方策略记录。

    当前阶段：
    - 使用 mock 规则生成策略
    - 不接真实控制系统，不下发真实控制命令

    未来阶段：
    - 接入智能决策模型
    - 接入水肥控制器与自动灌溉执行单元
    - 接入 MQTT 实际控制下发与回执
    """

    plan_code = models.CharField(max_length=40, unique=True, verbose_name="策略编号")
    block_code = models.CharField(max_length=32, verbose_name="地块编号")
    block_name = models.CharField(max_length=100, verbose_name="地块名称")
    growth_summary = models.CharField(max_length=255, verbose_name="长势摘要")
    risk_summary = models.CharField(max_length=255, verbose_name="风险摘要")
    irrigation_amount = models.FloatField(default=0, verbose_name="建议灌溉量(m3)")
    fertilizer_amount = models.FloatField(default=0, verbose_name="建议施肥量(kg/亩)")
    execution_window = models.CharField(max_length=64, verbose_name="执行时段建议")
    prescription_grade = models.CharField(max_length=16, verbose_name="处方等级")
    status = models.CharField(max_length=20, default="待下发", verbose_name="状态")
    source_mode = models.CharField(max_length=20, default="mock", verbose_name="生成模式")
    payload = models.JSONField(default=dict, blank=True, verbose_name="扩展负载")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "决策策略"
        verbose_name_plural = "决策策略"

    def __str__(self):
        return self.plan_code
