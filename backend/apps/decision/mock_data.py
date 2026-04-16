from datetime import datetime

from .models import DecisionPlan


SEED_PLANS = [
    {
        "plan_code": "PLAN-20260410-A01",
        "block_code": "A01",
        "block_name": "东一区示范棚",
        "growth_summary": "长势稳定，冠层扩展均匀",
        "risk_summary": "病害风险低，墒情适中",
        "irrigation_amount": 9.5,
        "fertilizer_amount": 1.2,
        "execution_window": "06:30-08:00",
        "prescription_grade": "A",
        "status": "待下发",
        "payload": {
            "fertilizer_formula": "N:P:K = 16:8:18",
            "control_hint": "维持当前策略，轻量补水",
            "growth_score": 84,
            "risk_level": "低",
        },
    },
    {
        "plan_code": "PLAN-20260410-A02",
        "block_code": "A02",
        "block_name": "东二区无人机主航线区",
        "growth_summary": "长势良好，局部墒情偏低",
        "risk_summary": "低风险，需观察灌溉均匀性",
        "irrigation_amount": 11.0,
        "fertilizer_amount": 1.4,
        "execution_window": "08:00-09:30",
        "prescription_grade": "B",
        "status": "待下发",
        "payload": {
            "fertilizer_formula": "N:P:K = 15:8:20",
            "control_hint": "建议早间补水，维持氮钾平衡",
            "growth_score": 78,
            "risk_level": "低",
        },
    },
    {
        "plan_code": "PLAN-20260410-B01",
        "block_code": "B01",
        "block_name": "中区精准滴灌试验区",
        "growth_summary": "试验区长势平稳，滴灌效果可控",
        "risk_summary": "中低风险，关注滴头均匀性",
        "irrigation_amount": 13.5,
        "fertilizer_amount": 1.6,
        "execution_window": "09:30-11:00",
        "prescription_grade": "B",
        "status": "待下发",
        "payload": {
            "fertilizer_formula": "N:P:K = 14:10:20",
            "control_hint": "继续验证试验策略，平稳加肥",
            "growth_score": 75,
            "risk_level": "中",
        },
    },
    {
        "plan_code": "PLAN-20260410-B02",
        "block_code": "B02",
        "block_name": "中区干旱胁迫观测区",
        "growth_summary": "长势偏弱，干旱胁迫明显",
        "risk_summary": "高风险，优先补水降压",
        "irrigation_amount": 18.0,
        "fertilizer_amount": 1.1,
        "execution_window": "06:00-07:30 / 16:30-18:00",
        "prescription_grade": "C",
        "status": "待下发",
        "payload": {
            "fertilizer_formula": "N:P:K = 12:8:18",
            "control_hint": "分时段补水，降低施肥浓度",
            "growth_score": 66,
            "risk_level": "高",
        },
    },
    {
        "plan_code": "PLAN-20260410-C01",
        "block_code": "C01",
        "block_name": "西区病斑复核区",
        "growth_summary": "长势一般，病斑区域需控制投入",
        "risk_summary": "中风险，需兼顾病害防控",
        "irrigation_amount": 10.5,
        "fertilizer_amount": 1.0,
        "execution_window": "13:30-15:00",
        "prescription_grade": "C",
        "status": "待下发",
        "payload": {
            "fertilizer_formula": "N:P:K = 11:10:18",
            "control_hint": "控氮稳钾，避免高湿环境加剧病害",
            "growth_score": 69,
            "risk_level": "中",
        },
    },
    {
        "plan_code": "PLAN-20260410-C02",
        "block_code": "C02",
        "block_name": "西二区果实膨大区",
        "growth_summary": "果实膨大期长势较好",
        "risk_summary": "低风险，维持稳定补给",
        "irrigation_amount": 12.0,
        "fertilizer_amount": 1.5,
        "execution_window": "15:30-17:00",
        "prescription_grade": "A",
        "status": "待下发",
        "payload": {
            "fertilizer_formula": "N:P:K = 14:8:22",
            "control_hint": "维持水肥同步，促进果实膨大",
            "growth_score": 79,
            "risk_level": "低",
        },
    },
]


def bootstrap_mock_plans():
    if DecisionPlan.objects.exists():
        return
    for item in SEED_PLANS:
        DecisionPlan.objects.create(
            plan_code=item["plan_code"],
            block_code=item["block_code"],
            block_name=item["block_name"],
            growth_summary=item["growth_summary"],
            risk_summary=item["risk_summary"],
            irrigation_amount=item["irrigation_amount"],
            fertilizer_amount=item["fertilizer_amount"],
            execution_window=item["execution_window"],
            prescription_grade=item["prescription_grade"],
            status=item["status"],
            source_mode="mock",
            payload=item["payload"],
        )


def get_block_options():
    return [{"code": item["block_code"], "name": item["block_name"]} for item in SEED_PLANS]


def get_map_payload():
    return {
        "center": [107.3662, 22.4011],
        "zoom": 13.45,
        "geojson": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "block_code": "A01",
                        "block_name": "东一区示范棚",
                        "grade": "A",
                        "irrigation": 9.5,
                        "fertilizer": 1.2,
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [107.3598, 22.4064],
                            [107.3620, 22.4064],
                            [107.3620, 22.4048],
                            [107.3598, 22.4048],
                            [107.3598, 22.4064],
                        ]],
                    },
                },
                {
                    "type": "Feature",
                    "properties": {
                        "block_code": "A02",
                        "block_name": "东二区无人机主航线区",
                        "grade": "B",
                        "irrigation": 11.0,
                        "fertilizer": 1.4,
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [107.3626, 22.4058],
                            [107.3650, 22.4058],
                            [107.3650, 22.4042],
                            [107.3626, 22.4042],
                            [107.3626, 22.4058],
                        ]],
                    },
                },
                {
                    "type": "Feature",
                    "properties": {
                        "block_code": "B01",
                        "block_name": "中区精准滴灌试验区",
                        "grade": "B",
                        "irrigation": 13.5,
                        "fertilizer": 1.6,
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [107.3666, 22.4038],
                            [107.3692, 22.4038],
                            [107.3692, 22.4022],
                            [107.3666, 22.4022],
                            [107.3666, 22.4038],
                        ]],
                    },
                },
                {
                    "type": "Feature",
                    "properties": {
                        "block_code": "B02",
                        "block_name": "中区干旱胁迫观测区",
                        "grade": "C",
                        "irrigation": 18.0,
                        "fertilizer": 1.1,
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [107.3643, 22.4010],
                            [107.3670, 22.4010],
                            [107.3670, 22.3994],
                            [107.3643, 22.3994],
                            [107.3643, 22.4010],
                        ]],
                    },
                },
                {
                    "type": "Feature",
                    "properties": {
                        "block_code": "C01",
                        "block_name": "西区病斑复核区",
                        "grade": "C",
                        "irrigation": 10.5,
                        "fertilizer": 1.0,
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [107.3605, 22.4006],
                            [107.3630, 22.4006],
                            [107.3630, 22.3990],
                            [107.3605, 22.3990],
                            [107.3605, 22.4006],
                        ]],
                    },
                },
                {
                    "type": "Feature",
                    "properties": {
                        "block_code": "C02",
                        "block_name": "西二区果实膨大区",
                        "grade": "A",
                        "irrigation": 12.0,
                        "fertilizer": 1.5,
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [107.3572, 22.4028],
                            [107.3596, 22.4028],
                            [107.3596, 22.4012],
                            [107.3572, 22.4012],
                            [107.3572, 22.4028],
                        ]],
                    },
                },
            ],
        },
    }


def build_generated_plan(block_code):
    source = next((item for item in SEED_PLANS if item["block_code"] == block_code), SEED_PLANS[0])
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    growth_score = source["payload"]["growth_score"]
    next_grade = source["prescription_grade"]
    if growth_score < 70:
        next_grade = "C"
    elif growth_score < 80:
        next_grade = "B"
    else:
        next_grade = "A"

    irrigation_amount = round(source["irrigation_amount"] + 1.5, 1)
    fertilizer_amount = round(max(source["fertilizer_amount"] - 0.1, 0.8), 1)

    return {
        "plan_code": f"PLAN-{timestamp}-{block_code}",
        "block_code": source["block_code"],
        "block_name": source["block_name"],
        "growth_summary": f"{source['growth_summary']}，已结合最新巡检结果重新计算",
        "risk_summary": source["risk_summary"],
        "irrigation_amount": irrigation_amount,
        "fertilizer_amount": fertilizer_amount,
        "execution_window": source["execution_window"],
        "prescription_grade": next_grade,
        "status": "待下发",
        "payload": {
            "fertilizer_formula": source["payload"]["fertilizer_formula"],
            "control_hint": f"mock 决策已生成，{source['payload']['control_hint']}",
            "growth_score": growth_score,
            "risk_level": source["payload"]["risk_level"],
            "decision_model_hint": "TODO: 未来在此接入智能决策模型输出。",
        },
    }
