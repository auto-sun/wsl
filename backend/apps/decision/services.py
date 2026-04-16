from django.utils import timezone

from services.ai.inference import AIInferenceService
from services.mqtt.client import MQTTService

from .mock_data import (
    bootstrap_mock_plans,
    build_generated_plan,
    get_block_options,
    get_map_payload,
)
from .models import DecisionPlan


class DecisionPlanService:
    """
    水肥处方策略服务。

    当前阶段：
    - 负责 mock 策略装载、策略生成、下发占位和前端展示数据组装
    - 统一承接 AI mock 决策与 MQTT mock 下发流程

    未来阶段：
    - 可在这里接入真实智能决策模型
    - 可对接真实水肥控制器、自动灌溉执行单元和 MQTT Broker
    """

    def __init__(self, inference_service=None, mqtt_service=None):
        self.inference_service = inference_service or AIInferenceService()
        self.mqtt_service = mqtt_service or MQTTService()

    def build_plans_payload(self, selected_block=None):
        bootstrap_mock_plans()
        latest_plans = self._get_latest_plan_per_block()
        history = [self._serialize_plan(plan) for plan in DecisionPlan.objects.all()[:12]]
        active_plan = self._resolve_active_plan(latest_plans, selected_block)

        grade_counts = {"A": 0, "B": 0, "C": 0}
        for plan in latest_plans:
            grade_counts[plan.prescription_grade] = grade_counts.get(plan.prescription_grade, 0) + 1

        return {
            "blocks": get_block_options(),
            "selected_block": active_plan.block_code,
            "plans": [self._serialize_plan(plan) for plan in latest_plans],
            "active_plan": self._serialize_plan(active_plan),
            "grade_distribution": {
                "labels": ["A级", "B级", "C级"],
                "values": [grade_counts["A"], grade_counts["B"], grade_counts["C"]],
            },
            "map": get_map_payload(),
            "history": history,
            "future_extensions": [
                "TODO: 在 AIInferenceService.generate_decision_strategy 中接入智能决策模型。",
                "TODO: 在 MQTTService.dispatch_strategy 中接入水肥控制器与自动灌溉执行单元。",
                "TODO: 接入真实 MQTT 命令下发、执行回执和闭环修正。",
            ],
            "dispatch_placeholder": {
                "controller": "水肥控制器",
                "executor": "自动灌溉执行单元",
                "message": "当前仅执行下发预留，不会触发真实控制。",
            },
        }

    def generate_plan(self, block_code):
        # 当前 mock 流程：
        # - 由统一推理服务返回模拟策略结果
        # 未来真实接入点：
        # - 在统一推理服务中融合长势、病害、土壤、气象与设备反馈
        generated = self.inference_service.generate_decision_strategy(
            block_code,
            build_generated_plan(block_code),
        )

        DecisionPlan.objects.create(
            plan_code=generated["plan_code"],
            block_code=generated["block_code"],
            block_name=generated["block_name"],
            growth_summary=generated["growth_summary"],
            risk_summary=generated["risk_summary"],
            irrigation_amount=generated["irrigation_amount"],
            fertilizer_amount=generated["fertilizer_amount"],
            execution_window=generated["execution_window"],
            prescription_grade=generated["prescription_grade"],
            status="待下发",
            source_mode="mock",
            payload=generated["payload"],
        )
        return generated

    def dispatch_plan(self, plan_code):
        plan = DecisionPlan.objects.filter(plan_code=plan_code).first()
        if plan is None:
            return None

        dispatch_preview = self.mqtt_service.dispatch_strategy(
            {
                "plan_code": plan.plan_code,
                "block_code": plan.block_code,
                "irrigation_amount": plan.irrigation_amount,
                "fertilizer_amount": plan.fertilizer_amount,
                "execution_window": plan.execution_window,
            }
        )

        plan.status = "已下发预留"
        plan.payload = {
            **plan.payload,
            "dispatch_message": dispatch_preview["message"],
            "dispatch_topic": dispatch_preview["topic"],
        }
        plan.save(update_fields=["status", "payload", "updated_at"])
        return dispatch_preview

    def _get_latest_plan_per_block(self):
        latest_by_block = {}
        for plan in DecisionPlan.objects.all():
            if plan.block_code not in latest_by_block:
                latest_by_block[plan.block_code] = plan
        return list(latest_by_block.values())

    def _resolve_active_plan(self, latest_plans, selected_block):
        default_plan = next((plan for plan in latest_plans if plan.block_code == "B02"), latest_plans[0])
        if not selected_block:
            return default_plan
        return next((plan for plan in latest_plans if plan.block_code == selected_block), default_plan)

    def _serialize_plan(self, plan):
        return {
            "plan_code": plan.plan_code,
            "block_code": plan.block_code,
            "block_name": plan.block_name,
            "growth_summary": plan.growth_summary,
            "risk_summary": plan.risk_summary,
            "irrigation_amount": plan.irrigation_amount,
            "fertilizer_amount": plan.fertilizer_amount,
            "execution_window": plan.execution_window,
            "prescription_grade": plan.prescription_grade,
            "status": plan.status,
            "source_mode": plan.source_mode,
            "fertilizer_formula": plan.payload.get("fertilizer_formula", "--"),
            "control_hint": plan.payload.get("control_hint", "--"),
            "growth_score": plan.payload.get("growth_score", "--"),
            "risk_level": plan.payload.get("risk_level", "--"),
            "created_at": timezone.localtime(plan.created_at).strftime("%Y-%m-%d %H:%M"),
        }
