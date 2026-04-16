MONITORING_DATES = [
    "2026-04-04",
    "2026-04-05",
    "2026-04-06",
    "2026-04-07",
    "2026-04-08",
    "2026-04-09",
    "2026-04-10",
]


def _summary_card(label, value, unit, trend, accent):
    return {
        "label": label,
        "value": value,
        "unit": unit,
        "trend": trend,
        "accent": accent,
    }


def _block_profile(
    code,
    name,
    grade,
    summary_cards,
    grade_distribution,
    growth_trend,
    ndvi_chart,
    drone_info,
):
    return {
        "code": code,
        "name": name,
        "grade": grade,
        "summary_cards": summary_cards,
        "grade_distribution": grade_distribution,
        "growth_trend": growth_trend,
        "ndvi_chart": ndvi_chart,
        "drone_info": drone_info,
    }


def get_growth_summary_payload():
    """
    TODO:
    - 后续在这里接入无人机航测原始结果
    - 后续接入遥感识别与多光谱分析结果
    - 后续将趋势数据切换为时序数据库查询结果
    """

    block_profiles = [
        _block_profile(
            "A01",
            "东一区示范棚",
            "优",
            [
                _summary_card("平均长势指数", 84, "分", "+3.8", "cyan"),
                _summary_card("健康指数", 88, "分", "+2.6", "blue"),
                _summary_card("平均 NDVI", 0.82, "", "+0.04", "violet"),
                _summary_card("预警地块数", 0, "块", "0", "red"),
            ],
            {"labels": ["优", "良", "中", "弱"], "values": [5, 2, 0, 0]},
            {
                "dates": MONITORING_DATES,
                "growth_index": [76, 78, 79, 81, 82, 83, 84],
                "health_index": [80, 81, 83, 84, 86, 87, 88],
                "moisture": [69, 68, 67, 66, 65, 64, 63],
            },
            {
                "dates": MONITORING_DATES,
                "ndvi": [0.73, 0.75, 0.76, 0.78, 0.79, 0.81, 0.82],
                "health_index": [80, 81, 83, 84, 86, 87, 88],
                "canopy_cover": [61, 63, 64, 66, 67, 69, 71],
            },
            {
                "uav_code": "UAV-01",
                "mission_name": "东区精细长势巡检",
                "pilot": "李工",
                "route": "A01 全棚往返航线",
                "flight_time": "18 分钟",
                "covered_area": "22 亩",
                "payload": "可见光镜头，预留多光谱挂载口",
                "status": "巡检完成",
                "next_task": "后续接入遥感识别与多光谱长势反演分析",
            },
        ),
        _block_profile(
            "A02",
            "东二区无人机主航线区",
            "良",
            [
                _summary_card("平均长势指数", 78, "分", "+2.1", "cyan"),
                _summary_card("健康指数", 80, "分", "+1.9", "blue"),
                _summary_card("平均 NDVI", 0.76, "", "+0.03", "violet"),
                _summary_card("预警地块数", 1, "块", "-1", "red"),
            ],
            {"labels": ["优", "良", "中", "弱"], "values": [2, 4, 1, 0]},
            {
                "dates": MONITORING_DATES,
                "growth_index": [70, 72, 73, 74, 76, 77, 78],
                "health_index": [73, 74, 76, 77, 78, 79, 80],
                "moisture": [66, 65, 64, 62, 61, 60, 60],
            },
            {
                "dates": MONITORING_DATES,
                "ndvi": [0.68, 0.70, 0.71, 0.72, 0.74, 0.75, 0.76],
                "health_index": [73, 74, 76, 77, 78, 79, 80],
                "canopy_cover": [56, 57, 59, 61, 62, 64, 65],
            },
            {
                "uav_code": "UAV-02",
                "mission_name": "主航线标准巡检",
                "pilot": "周工",
                "route": "A02 南北主航线",
                "flight_time": "21 分钟",
                "covered_area": "26 亩",
                "payload": "可见光镜头，预留遥感识别接口",
                "status": "巡检完成",
                "next_task": "待接入多源影像后输出长势分层处方建议",
            },
        ),
        _block_profile(
            "B01",
            "中区精准滴灌试验区",
            "良",
            [
                _summary_card("平均长势指数", 75, "分", "+1.8", "cyan"),
                _summary_card("健康指数", 77, "分", "+1.4", "blue"),
                _summary_card("平均 NDVI", 0.72, "", "+0.02", "violet"),
                _summary_card("预警地块数", 1, "块", "0", "red"),
            ],
            {"labels": ["优", "良", "中", "弱"], "values": [2, 3, 2, 0]},
            {
                "dates": MONITORING_DATES,
                "growth_index": [68, 69, 71, 72, 73, 74, 75],
                "health_index": [71, 72, 73, 74, 75, 76, 77],
                "moisture": [62, 61, 59, 58, 57, 56, 55],
            },
            {
                "dates": MONITORING_DATES,
                "ndvi": [0.64, 0.66, 0.67, 0.68, 0.70, 0.71, 0.72],
                "health_index": [71, 72, 73, 74, 75, 76, 77],
                "canopy_cover": [51, 52, 54, 55, 57, 58, 60],
            },
            {
                "uav_code": "UAV-03",
                "mission_name": "滴灌试验区增补巡检",
                "pilot": "王工",
                "route": "B01 滴灌管线沿线航线",
                "flight_time": "16 分钟",
                "covered_area": "18 亩",
                "payload": "可见光镜头，预留水分反演分析接口",
                "status": "巡检完成",
                "next_task": "后续接入土壤墒情节点，实现空地协同分析",
            },
        ),
        _block_profile(
            "B02",
            "中区干旱胁迫观测区",
            "中",
            [
                _summary_card("平均长势指数", 66, "分", "-2.6", "cyan"),
                _summary_card("健康指数", 68, "分", "-2.1", "blue"),
                _summary_card("平均 NDVI", 0.61, "", "-0.03", "violet"),
                _summary_card("预警地块数", 2, "块", "+1", "red"),
            ],
            {"labels": ["优", "良", "中", "弱"], "values": [0, 2, 3, 2]},
            {
                "dates": MONITORING_DATES,
                "growth_index": [71, 70, 69, 68, 67, 66, 66],
                "health_index": [73, 72, 71, 70, 69, 68, 68],
                "moisture": [56, 54, 52, 50, 49, 48, 47],
            },
            {
                "dates": MONITORING_DATES,
                "ndvi": [0.68, 0.66, 0.65, 0.63, 0.62, 0.61, 0.61],
                "health_index": [73, 72, 71, 70, 69, 68, 68],
                "canopy_cover": [49, 48, 47, 45, 44, 43, 42],
            },
            {
                "uav_code": "UAV-02",
                "mission_name": "干旱胁迫复飞核查",
                "pilot": "周工",
                "route": "B02 低空网格巡检",
                "flight_time": "24 分钟",
                "covered_area": "20 亩",
                "payload": "可见光镜头，预留多光谱与热红外接口",
                "status": "重点关注",
                "next_task": "后续接入热红外与多光谱后输出干旱胁迫强度分级",
            },
        ),
        _block_profile(
            "C01",
            "西区病斑复核区",
            "中",
            [
                _summary_card("平均长势指数", 69, "分", "-1.4", "cyan"),
                _summary_card("健康指数", 71, "分", "-0.9", "blue"),
                _summary_card("平均 NDVI", 0.65, "", "-0.01", "violet"),
                _summary_card("预警地块数", 2, "块", "+1", "red"),
            ],
            {"labels": ["优", "良", "中", "弱"], "values": [1, 2, 3, 1]},
            {
                "dates": MONITORING_DATES,
                "growth_index": [70, 70, 71, 70, 69, 69, 69],
                "health_index": [73, 73, 73, 72, 71, 71, 71],
                "moisture": [60, 59, 58, 57, 57, 56, 55],
            },
            {
                "dates": MONITORING_DATES,
                "ndvi": [0.67, 0.67, 0.68, 0.67, 0.66, 0.65, 0.65],
                "health_index": [73, 73, 73, 72, 71, 71, 71],
                "canopy_cover": [53, 53, 54, 53, 52, 51, 51],
            },
            {
                "uav_code": "UAV-04",
                "mission_name": "病斑复核近景巡检",
                "pilot": "陈工",
                "route": "C01 病斑点位复飞",
                "flight_time": "14 分钟",
                "covered_area": "12 亩",
                "payload": "可见光镜头，预留病斑识别与目标检测挂载",
                "status": "复核完成",
                "next_task": "后续接入病斑目标检测与多尺度遥感识别",
            },
        ),
        _block_profile(
            "C02",
            "西二区果实膨大区",
            "良",
            [
                _summary_card("平均长势指数", 79, "分", "+2.7", "cyan"),
                _summary_card("健康指数", 82, "分", "+2.2", "blue"),
                _summary_card("平均 NDVI", 0.77, "", "+0.03", "violet"),
                _summary_card("预警地块数", 0, "块", "-1", "red"),
            ],
            {"labels": ["优", "良", "中", "弱"], "values": [3, 3, 1, 0]},
            {
                "dates": MONITORING_DATES,
                "growth_index": [72, 74, 75, 76, 77, 78, 79],
                "health_index": [75, 76, 77, 78, 79, 81, 82],
                "moisture": [64, 64, 63, 62, 61, 60, 59],
            },
            {
                "dates": MONITORING_DATES,
                "ndvi": [0.69, 0.71, 0.72, 0.73, 0.75, 0.76, 0.77],
                "health_index": [75, 76, 77, 78, 79, 81, 82],
                "canopy_cover": [54, 56, 57, 59, 60, 62, 64],
            },
            {
                "uav_code": "UAV-01",
                "mission_name": "果实膨大区补飞监测",
                "pilot": "李工",
                "route": "C02 西侧环绕航线",
                "flight_time": "17 分钟",
                "covered_area": "19 亩",
                "payload": "可见光镜头，预留果实识别与成熟度分析接口",
                "status": "巡检完成",
                "next_task": "后续接入果实识别、成熟度估计与多光谱分析",
            },
        ),
    ]

    return {
        "filters": {
            "blocks": [{"code": item["code"], "name": item["name"]} for item in block_profiles],
            "default_block": "ALL",
            "default_start": MONITORING_DATES[0],
            "default_end": MONITORING_DATES[-1],
        },
        "summary_cards": [
            _summary_card("监测地块", 6, "块", "+1", "cyan"),
            _summary_card("平均长势指数", 75.2, "分", "+1.7", "blue"),
            _summary_card("高风险地块", 2, "块", "-1", "red"),
            _summary_card("巡检覆盖面积", 117, "亩", "+12", "violet"),
        ],
        "grade_distribution": {
            "labels": ["优", "良", "中", "弱"],
            "values": [13, 16, 11, 4],
        },
        "growth_trend": {
            "dates": MONITORING_DATES,
            "growth_index": [71, 72, 73, 74, 75, 75, 76],
            "health_index": [74, 75, 76, 77, 78, 78, 79],
            "moisture": [63, 62, 61, 59, 58, 57, 56],
        },
        "ndvi_chart": {
            "dates": MONITORING_DATES,
            "ndvi": [0.68, 0.69, 0.70, 0.71, 0.72, 0.73, 0.74],
            "health_index": [74, 75, 76, 77, 78, 78, 79],
            "canopy_cover": [54, 55, 56, 58, 59, 60, 61],
        },
        "inspection_records": [
            {
                "recorded_at": "2026-04-10 10:25",
                "block_code": "B02",
                "block_name": "中区干旱胁迫观测区",
                "route": "低空网格巡检",
                "summary": "发现墒情持续下降，长势指数低于园区均值。",
                "result": "建议优先补水",
            },
            {
                "recorded_at": "2026-04-10 09:50",
                "block_code": "C01",
                "block_name": "西区病斑复核区",
                "route": "病斑点位复飞",
                "summary": "重点区域完成近景图像补采，待诊断模块复核。",
                "result": "转入病虫害检测",
            },
            {
                "recorded_at": "2026-04-10 08:30",
                "block_code": "A01",
                "block_name": "东一区示范棚",
                "route": "精细长势巡检",
                "summary": "长势保持稳定，冠层覆盖连续提升。",
                "result": "维持当前策略",
            },
            {
                "recorded_at": "2026-04-09 16:18",
                "block_code": "C02",
                "block_name": "西二区果实膨大区",
                "route": "环绕补飞监测",
                "summary": "果实膨大期长势良好，健康指数上升。",
                "result": "建议轻量补水",
            },
            {
                "recorded_at": "2026-04-08 15:05",
                "block_code": "A02",
                "block_name": "东二区无人机主航线区",
                "route": "标准巡检",
                "summary": "航线区整体稳定，局部墒情偏低但可控。",
                "result": "继续观察",
            },
            {
                "recorded_at": "2026-04-07 14:35",
                "block_code": "B01",
                "block_name": "中区精准滴灌试验区",
                "route": "滴灌沿线巡检",
                "summary": "滴灌试验效果稳定，健康指数缓慢提升。",
                "result": "继续验证试验策略",
            },
        ],
        "drone_info": {
            "uav_code": "UAV-02",
            "mission_name": "全园长势复核巡检",
            "pilot": "周工",
            "route": "A区 -> B区 -> C区",
            "flight_time": "32 分钟",
            "covered_area": "117 亩",
            "payload": "可见光镜头，预留多光谱与热红外扩展能力",
            "status": "执行中",
            "next_task": "后续接入无人机航测、遥感识别、多光谱分析结果流",
        },
        "future_extensions": [
            "TODO: 接入无人机航测原始影像和正射拼接结果。",
            "TODO: 接入遥感识别、多光谱分析与热红外反演结果。",
            "TODO: 接入时序数据库后按时间范围查询真实长势曲线。",
        ],
        "block_profiles": block_profiles,
    }


def get_heatmap_payload():
    """
    TODO:
    - 后续接入真实地块边界、多边形图层与飞行轨迹
    - 后续接入多时相热力栅格、病斑分布与处方图联动图层
    """

    return {
        "map": {
            "center": [107.3662, 22.4011],
            "zoom": 13.5,
        },
        "geojson": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "block_code": "A01",
                        "block_name": "东一区示范棚",
                        "intensity": 0.84,
                        "growth_grade": "优",
                        "ndvi": 0.82,
                    },
                    "geometry": {"type": "Point", "coordinates": [107.3609, 22.4059]},
                },
                {
                    "type": "Feature",
                    "properties": {
                        "block_code": "A02",
                        "block_name": "东二区无人机主航线区",
                        "intensity": 0.77,
                        "growth_grade": "良",
                        "ndvi": 0.76,
                    },
                    "geometry": {"type": "Point", "coordinates": [107.3642, 22.4047]},
                },
                {
                    "type": "Feature",
                    "properties": {
                        "block_code": "B01",
                        "block_name": "中区精准滴灌试验区",
                        "intensity": 0.74,
                        "growth_grade": "良",
                        "ndvi": 0.72,
                    },
                    "geometry": {"type": "Point", "coordinates": [107.3693, 22.4028]},
                },
                {
                    "type": "Feature",
                    "properties": {
                        "block_code": "B02",
                        "block_name": "中区干旱胁迫观测区",
                        "intensity": 0.62,
                        "growth_grade": "中",
                        "ndvi": 0.61,
                    },
                    "geometry": {"type": "Point", "coordinates": [107.3678, 22.3998]},
                },
                {
                    "type": "Feature",
                    "properties": {
                        "block_code": "C01",
                        "block_name": "西区病斑复核区",
                        "intensity": 0.66,
                        "growth_grade": "中",
                        "ndvi": 0.65,
                    },
                    "geometry": {"type": "Point", "coordinates": [107.3624, 22.3992]},
                },
                {
                    "type": "Feature",
                    "properties": {
                        "block_code": "C02",
                        "block_name": "西二区果实膨大区",
                        "intensity": 0.78,
                        "growth_grade": "良",
                        "ndvi": 0.77,
                    },
                    "geometry": {"type": "Point", "coordinates": [107.3598, 22.4022]},
                },
                {
                    "type": "Feature",
                    "properties": {
                        "block_code": "B02",
                        "block_name": "中区干旱胁迫观测区",
                        "intensity": 0.58,
                        "growth_grade": "弱",
                        "ndvi": 0.59,
                    },
                    "geometry": {"type": "Point", "coordinates": [107.3659, 22.3987]},
                },
                {
                    "type": "Feature",
                    "properties": {
                        "block_code": "C01",
                        "block_name": "西区病斑复核区",
                        "intensity": 0.63,
                        "growth_grade": "中",
                        "ndvi": 0.64,
                    },
                    "geometry": {"type": "Point", "coordinates": [107.3611, 22.4005]},
                },
            ],
        },
    }
