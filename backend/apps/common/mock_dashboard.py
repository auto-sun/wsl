def get_dashboard_payload():
    return {
        "system_title": "基于AI+无人机的火龙果长势监测与精准水肥一体化系统",
        "system_subtitle": "融合无人机巡检、病虫害识别、长势评估与水肥策略控制的智慧农业监控驾驶舱",
        "drone_status": {
            "mission_name": "无人机晨间全园巡航",
            "route": "A区 -> B区 -> C区",
            "progress": 68,
            "message": "当前执行热区复飞与长势复核任务",
        },
        "overview_cards": [
            {"label": "地块数量", "value": 18, "unit": "块", "trend": "+2", "accent": "cyan"},
            {"label": "在线设备数", "value": 26, "unit": "台", "trend": "+3", "accent": "blue"},
            {"label": "巡检次数", "value": 7, "unit": "次", "trend": "+1", "accent": "violet"},
            {"label": "异常告警数", "value": 4, "unit": "条", "trend": "-1", "accent": "red"},
        ],
        "growth_trend": {
            "dates": ["04-04", "04-05", "04-06", "04-07", "04-08", "04-09", "04-10"],
            "growth_index": [62, 64, 67, 70, 73, 75, 78],
            "flower_index": [48, 50, 53, 56, 58, 61, 65],
            "moisture": [71, 69, 66, 63, 61, 59, 57],
        },
        "diagnosis_stats": {
            "labels": ["健康", "疑似炭疽病", "疑似茎腐病", "虫害风险"],
            "values": [56, 18, 11, 15],
        },
        "strategy_overview": {
            "zones": ["A01", "A02", "B01", "B02", "C01", "C02"],
            "water_plan": [12, 10, 16, 18, 13, 9],
            "fertilizer_plan": [1.4, 1.3, 1.7, 1.9, 1.6, 1.2],
            "completion": [92, 88, 80, 76, 85, 94],
        },
        "map": {
            "center": [107.3662, 22.4011],
            "zoom": 13.4,
            "geojson": {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "properties": {
                            "block": "A01",
                            "intensity": 0.82,
                            "growth": "优",
                            "moisture": 64,
                        },
                        "geometry": {"type": "Point", "coordinates": [107.3609, 22.4059]},
                    },
                    {
                        "type": "Feature",
                        "properties": {
                            "block": "A02",
                            "intensity": 0.76,
                            "growth": "良",
                            "moisture": 60,
                        },
                        "geometry": {"type": "Point", "coordinates": [107.3642, 22.4047]},
                    },
                    {
                        "type": "Feature",
                        "properties": {
                            "block": "B01",
                            "intensity": 0.73,
                            "growth": "良",
                            "moisture": 58,
                        },
                        "geometry": {"type": "Point", "coordinates": [107.3693, 22.4028]},
                    },
                    {
                        "type": "Feature",
                        "properties": {
                            "block": "B02",
                            "intensity": 0.64,
                            "growth": "偏弱",
                            "moisture": 49,
                        },
                        "geometry": {"type": "Point", "coordinates": [107.3678, 22.3998]},
                    },
                    {
                        "type": "Feature",
                        "properties": {
                            "block": "C01",
                            "intensity": 0.69,
                            "growth": "一般",
                            "moisture": 55,
                        },
                        "geometry": {"type": "Point", "coordinates": [107.3624, 22.3992]},
                    },
                    {
                        "type": "Feature",
                        "properties": {
                            "block": "C02",
                            "intensity": 0.79,
                            "growth": "良",
                            "moisture": 62,
                        },
                        "geometry": {"type": "Point", "coordinates": [107.3598, 22.4022]},
                    },
                ],
            },
        },
        "alerts": [
            {
                "level": "高",
                "title": "B02 地块墒情持续下降",
                "time": "10:18",
                "detail": "建议优先执行滴灌补水，当前墒情低于阈值 12%。",
            },
            {
                "level": "中",
                "title": "C01 区疑似病斑待复核",
                "time": "09:42",
                "detail": "无人机近景照片发现红色病斑区域，建议进入诊断页复核。",
            },
            {
                "level": "中",
                "title": "2 号无人机电池循环接近阈值",
                "time": "08:55",
                "detail": "剩余安全循环 16 次，建议安排维护计划。",
            },
            {
                "level": "低",
                "title": "A02 灌溉策略执行延迟",
                "time": "08:20",
                "detail": "联控未启用，当前为策略预览状态。",
            },
        ],
        "quick_links": [
            {"label": "进入长势监测", "path": "/monitoring", "description": "查看地块长势趋势与热力图"},
            {"label": "病虫害检测", "path": "/diagnosis", "description": "上传样图并查看检测结果"},
            {"label": "水肥策略", "path": "/decision", "description": "查看处方图与执行概览"},
            {"label": "设备管理", "path": "/devices", "description": "巡检无人机、摄像头和执行器状态"},
        ],
    }
