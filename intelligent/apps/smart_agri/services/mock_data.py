import hashlib
from datetime import date, datetime, timedelta

from django.conf import settings


ORCHARD_CENTER = [107.3662, 22.4011]


def get_demo_user():
    return {
        "username": settings.SMART_AGRI_PROJECT["DEMO_USER"],
        "password": settings.SMART_AGRI_PROJECT["DEMO_PASSWORD"],
        "display_name": settings.SMART_AGRI_PROJECT["DEMO_NAME"],
        "role": "智慧农场总控",
    }


def get_navigation_summary():
    return {
        "project_name": settings.SMART_AGRI_PROJECT["NAME"],
        "orchard_name": "龙穗一号火龙果示范园",
        "current_season": "春季促花与幼果膨大期",
        "weather": "多云 24℃ / 湿度 68%",
    }


def get_dashboard_payload():
    days = ["04-04", "04-05", "04-06", "04-07", "04-08", "04-09", "04-10"]
    return {
        "summary_cards": [
            {"label": "在线设备", "value": 26, "unit": "台", "trend": "+3"},
            {"label": "今日巡检架次", "value": 4, "unit": "次", "trend": "+1"},
            {"label": "重点预警地块", "value": 3, "unit": "块", "trend": "-1"},
            {"label": "预计节水率", "value": 18.6, "unit": "%", "trend": "+2.1%"},
        ],
        "growth_trend": {
            "dates": days,
            "canopy": [61, 63, 66, 68, 69, 71, 72],
            "flowering": [45, 46, 48, 52, 55, 57, 60],
            "fruiting": [31, 34, 36, 38, 41, 43, 46],
        },
        "water_fertilizer": {
            "zones": ["A01", "A02", "B01", "B02", "C01", "C02"],
            "water": [11, 10, 13, 12, 14, 9],
            "fertilizer": [3.4, 3.2, 3.8, 3.6, 4.1, 2.8],
        },
        "drone_tasks": [
            {"time": "08:20", "name": "晨间长势巡检", "status": "已完成"},
            {"time": "10:40", "name": "异常热区复飞", "status": "执行中"},
            {"time": "14:30", "name": "病斑复核航线", "status": "待执行"},
        ],
        "alerts": [
            {"level": "高", "title": "B02 地块土壤含水偏低", "detail": "建议优先执行滴灌 12m3/h。"},
            {"level": "中", "title": "C01 地块疑似茎部病斑", "detail": "建议上传样张并触发模型复核。"},
            {"level": "低", "title": "无人机 02 号电池寿命接近阈值", "detail": "预计剩余循环 18 次。"},
        ],
        "camera": {
            "title": "中控实时画面",
            "message": "调用浏览器摄像头模拟中控视频流，后续可替换为 RTSP/HLS 网关。"
        },
        "map": {
            "center": ORCHARD_CENTER,
            "zoom": 13.6,
        },
    }


def _heat_feature(lng, lat, block_code, vigor, moisture, temperature):
    return {
        "type": "Feature",
        "properties": {
            "block_code": block_code,
            "intensity": vigor,
            "vigor": vigor,
            "moisture": moisture,
            "temperature": temperature,
        },
        "geometry": {
            "type": "Point",
            "coordinates": [lng, lat],
        },
    }


def get_growth_heatmap_geojson():
    features = [
        _heat_feature(107.3614, 22.4065, "A01", 0.86, 64, 27.2),
        _heat_feature(107.3648, 22.4052, "A02", 0.82, 61, 27.8),
        _heat_feature(107.3686, 22.4037, "A03", 0.79, 58, 28.1),
        _heat_feature(107.3705, 22.4016, "B01", 0.74, 53, 28.6),
        _heat_feature(107.3667, 22.3998, "B02", 0.69, 47, 29.2),
        _heat_feature(107.3629, 22.3989, "B03", 0.71, 51, 28.9),
        _heat_feature(107.3596, 22.4012, "C01", 0.76, 56, 28.3),
        _heat_feature(107.3584, 22.4043, "C02", 0.81, 60, 27.7),
    ]
    return {
        "type": "FeatureCollection",
        "features": features,
    }


def get_growth_payload():
    days = ["04-04", "04-05", "04-06", "04-07", "04-08", "04-09", "04-10"]
    return {
        "kpis": [
            {"label": "冠层覆盖率", "value": 72.4, "unit": "%", "delta": "+2.3"},
            {"label": "开花同步率", "value": 60.1, "unit": "%", "delta": "+4.5"},
            {"label": "估算株高", "value": 128, "unit": "cm", "delta": "+6"},
            {"label": "异常热区", "value": 2, "unit": "处", "delta": "-1"},
        ],
        "trend": {
            "dates": days,
            "ndvi": [0.58, 0.61, 0.63, 0.66, 0.68, 0.70, 0.72],
            "moisture": [67, 66, 64, 62, 59, 57, 56],
            "flowering": [42, 45, 48, 53, 55, 58, 60],
        },
        "blocks": [
            {"code": "A01", "name": "东区示范棚", "vigor": 0.86, "moisture": 64, "risk": "低"},
            {"code": "A02", "name": "无人机主航线区", "vigor": 0.82, "moisture": 61, "risk": "低"},
            {"code": "B01", "name": "精准滴灌试验区", "vigor": 0.74, "moisture": 53, "risk": "中"},
            {"code": "B02", "name": "干旱胁迫观测区", "vigor": 0.69, "moisture": 47, "risk": "高"},
            {"code": "C01", "name": "病斑复核区", "vigor": 0.76, "moisture": 56, "risk": "中"},
        ],
        "insight": {
            "title": "AI 长势解读",
            "summary": "B02 地块连续 3 日含水率下行，长势指数低于园区均值 8.4%，建议优先执行低流量长时滴灌并在 24 小时后复测。",
        },
    }


def get_prescription_payload():
    timeline_hours = ["06:00", "08:00", "10:00", "12:00", "14:00", "16:00", "18:00"]
    return {
        "summary_cards": [
            {"label": "待执行处方", "value": 3, "unit": "份"},
            {"label": "今日建议灌溉量", "value": 62, "unit": "m3"},
            {"label": "目标施肥浓度", "value": 1.8, "unit": "EC"},
            {"label": "节肥预估", "value": 12.4, "unit": "%"},
        ],
        "radar": {
            "indicators": [
                {"name": "水分补给", "max": 100},
                {"name": "氮肥供给", "max": 100},
                {"name": "钾肥提升", "max": 100},
                {"name": "病害抑制", "max": 100},
                {"name": "果实膨大", "max": 100},
            ],
            "values": [82, 58, 74, 61, 80],
        },
        "schedule": {
            "hours": timeline_hours,
            "water_flow": [8, 9, 10, 11, 10, 8, 6],
            "fertilizer_ratio": [1.2, 1.4, 1.6, 1.8, 1.8, 1.5, 1.1],
        },
        "zones": [
            {
                "block_code": "B02",
                "strategy": "分两段滴灌，优先补水",
                "water": "18 m3",
                "fertilizer": "N:P:K = 15:8:22",
                "window": "09:00-12:00",
            },
            {
                "block_code": "C01",
                "strategy": "控氮稳钾，降低病害风险",
                "water": "12 m3",
                "fertilizer": "N:P:K = 12:10:20",
                "window": "14:00-16:00",
            },
            {
                "block_code": "A02",
                "strategy": "维持生长，轻量补水",
                "water": "9 m3",
                "fertilizer": "N:P:K = 16:8:18",
                "window": "16:00-18:00",
            },
        ],
        "todo_modules": [
            "TODO: 与 MQTT 控制网关对接后，执行按钮可下发阀门与施肥机指令。",
            "TODO: 与 InfluxDB 连接后，自动读取地块时序阈值并闭环修正处方。",
            "TODO: 接入真实模型后，病虫害风险可自动影响肥液配方。",
        ],
    }


def get_device_payload():
    return {
        "summary": [
            {"label": "设备总数", "value": 34, "unit": "台"},
            {"label": "在线率", "value": 76.5, "unit": "%"},
            {"label": "待维护", "value": 4, "unit": "台"},
            {"label": "异常链路", "value": 2, "unit": "条"},
        ],
        "status_distribution": [
            {"name": "在线", "value": 26},
            {"name": "离线", "value": 6},
            {"name": "告警", "value": 2},
        ],
        "devices": [
            {
                "device_code": "UAV-01",
                "name": "巡检无人机 01",
                "type": "无人机",
                "status": "在线",
                "signal": "92%",
                "battery": "74%",
                "last_seen": "2026-04-10 10:42",
            },
            {
                "device_code": "CAM-01",
                "name": "中控摄像头",
                "type": "视频监控",
                "status": "在线",
                "signal": "有线",
                "battery": "--",
                "last_seen": "2026-04-10 10:40",
            },
            {
                "device_code": "VALVE-B02",
                "name": "B02 区电磁阀",
                "type": "灌溉执行器",
                "status": "告警",
                "signal": "68%",
                "battery": "--",
                "last_seen": "2026-04-10 09:50",
            },
            {
                "device_code": "SENSOR-C01",
                "name": "C01 土壤墒情节点",
                "type": "传感器",
                "status": "离线",
                "signal": "0%",
                "battery": "21%",
                "last_seen": "2026-04-09 18:12",
            },
            {
                "device_code": "CTRL-01",
                "name": "水肥一体机控制器",
                "type": "控制器",
                "status": "在线",
                "signal": "有线",
                "battery": "--",
                "last_seen": "2026-04-10 10:41",
            },
        ],
        "network_links": [
            "中控平台 -> MQTT 网关：已预留",
            "中控平台 -> InfluxDB：已预留",
            "中控平台 -> Redis：已预留",
            "中控平台 -> 模型推理服务：已预留",
        ],
    }


def build_detection_result(file_name, file_size, plot_code=""):
    disease_templates = [
        {
            "name": "茎腐病疑似",
            "severity": "高",
            "suggestions": [
                "隔离可疑病株，减少交叉灌溉。",
                "优先喷施针对茎腐病的保护性药剂。",
                "24 小时内安排无人机复飞复核。",
            ],
        },
        {
            "name": "炭疽病风险",
            "severity": "中",
            "suggestions": [
                "控制棚内湿度，避免连续叶面潮湿。",
                "对病斑区域实施定点用药。",
                "结合长势数据调低氮肥输入。",
            ],
        },
        {
            "name": "红蜘蛛虫害风险",
            "severity": "中",
            "suggestions": [
                "增强叶背巡检频率。",
                "在高风险区实施生物防治或精准喷施。",
                "同步复核滴灌末端压力，减少植株胁迫。",
            ],
        },
        {
            "name": "未见明显病虫害",
            "severity": "低",
            "suggestions": [
                "建议继续保持当前巡检频次。",
                "将图像样本纳入后续模型训练集。",
                "关注后续 48 小时极端天气变化。",
            ],
        },
    ]
    digest = hashlib.md5(f"{file_name}:{file_size}".encode("utf-8")).hexdigest()
    template = disease_templates[int(digest[:2], 16) % len(disease_templates)]
    confidence = round(0.72 + (int(digest[2:4], 16) / 255) * 0.25, 3)
    detected_area = 8 + int(digest[4:6], 16) % 23
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "task_code": f"DET{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "plot_code": plot_code or "C01",
        "disease_name": template["name"],
        "confidence": confidence,
        "severity": template["severity"],
        "detected_area": f"{detected_area}%",
        "capture_time": now,
        "suggestions": template["suggestions"],
        "boxes": [
            {"x": 14, "y": 21, "w": 26, "h": 20, "label": template["name"]},
            {"x": 55, "y": 48, "w": 18, "h": 16, "label": "关注区域"},
        ],
        "remarks": "当前为 mock 推理结果，输出结构已按真实业务流保留。",
    }


def get_recent_detection_history():
    today = date.today()
    return [
        {
            "task_code": "DET20260410093001",
            "image_name": "stem-a01.jpg",
            "plot_code": "A01",
            "disease_name": "未见明显病虫害",
            "severity": "低",
            "confidence": 0.91,
            "created_at": f"{today.isoformat()} 09:30",
        },
        {
            "task_code": "DET20260410084210",
            "image_name": "b02-spot.png",
            "plot_code": "B02",
            "disease_name": "炭疽病风险",
            "severity": "中",
            "confidence": 0.87,
            "created_at": f"{today.isoformat()} 08:42",
        },
        {
            "task_code": "DET20260409172008",
            "image_name": "c01-drone.jpeg",
            "plot_code": "C01",
            "disease_name": "茎腐病疑似",
            "severity": "高",
            "confidence": 0.93,
            "created_at": f"{(today - timedelta(days=1)).isoformat()} 17:20",
        },
    ]
