DEVICE_LIST = [
    {
        "device_code": "CAM-01",
        "name": "中控摄像头 01",
        "type": "摄像头",
        "status": "在线",
        "online": True,
        "heartbeat_at": "2026-04-10 11:03",
        "battery": "--",
        "signal": "有线",
        "location": "中控区",
        "ip_address": "192.168.10.21",
        "mqtt_topic": "dragonfruit/farm/camera/CAM-01/state",
        "risk": "低",
    },
    {
        "device_code": "UAV-01",
        "name": "巡检无人机 01",
        "type": "无人机",
        "status": "在线",
        "online": True,
        "heartbeat_at": "2026-04-10 11:01",
        "battery": "76%",
        "signal": "92%",
        "location": "东一区机库",
        "ip_address": "192.168.10.31",
        "mqtt_topic": "dragonfruit/farm/uav/UAV-01/state",
        "risk": "低",
    },
    {
        "device_code": "UAV-02",
        "name": "巡检无人机 02",
        "type": "无人机",
        "status": "维护中",
        "online": False,
        "heartbeat_at": "2026-04-10 08:55",
        "battery": "18%",
        "signal": "0%",
        "location": "设备维护区",
        "ip_address": "192.168.10.32",
        "mqtt_topic": "dragonfruit/farm/uav/UAV-02/state",
        "risk": "中",
    },
    {
        "device_code": "CTRL-01",
        "name": "水肥一体化控制器",
        "type": "灌溉控制器",
        "status": "在线",
        "online": True,
        "heartbeat_at": "2026-04-10 11:02",
        "battery": "--",
        "signal": "有线",
        "location": "控制柜 A",
        "ip_address": "192.168.10.41",
        "mqtt_topic": "dragonfruit/farm/controller/CTRL-01/state",
        "risk": "低",
    },
    {
        "device_code": "SEN-01",
        "name": "东区环境传感器",
        "type": "环境传感器",
        "status": "在线",
        "online": True,
        "heartbeat_at": "2026-04-10 10:59",
        "battery": "64%",
        "signal": "86%",
        "location": "A01",
        "ip_address": "192.168.10.51",
        "mqtt_topic": "dragonfruit/farm/sensor/SEN-01/state",
        "risk": "低",
    },
    {
        "device_code": "SEN-02",
        "name": "中区土壤墒情节点",
        "type": "环境传感器",
        "status": "离线",
        "online": False,
        "heartbeat_at": "2026-04-09 18:12",
        "battery": "21%",
        "signal": "0%",
        "location": "B02",
        "ip_address": "192.168.10.52",
        "mqtt_topic": "dragonfruit/farm/sensor/SEN-02/state",
        "risk": "高",
    },
    {
        "device_code": "GW-01",
        "name": "边缘采集网关",
        "type": "网关",
        "status": "在线",
        "online": True,
        "heartbeat_at": "2026-04-10 11:04",
        "battery": "--",
        "signal": "有线",
        "location": "机房",
        "ip_address": "192.168.10.11",
        "mqtt_topic": "dragonfruit/farm/gateway/GW-01/state",
        "risk": "低",
    },
]


def get_devices():
    return DEVICE_LIST


def get_device(device_code):
    return next((item for item in DEVICE_LIST if item["device_code"] == device_code), None)


def get_status_payload():
    total = len(DEVICE_LIST)
    online = len([item for item in DEVICE_LIST if item["online"]])
    offline = len([item for item in DEVICE_LIST if not item["online"]])
    alert = len([item for item in DEVICE_LIST if item["risk"] in {"中", "高"}])

    type_cards = [
        {
            "type": "摄像头",
            "count": len([item for item in DEVICE_LIST if item["type"] == "摄像头"]),
            "status": "视频采集预留",
            "hint": "后续可接入 RTSP / HLS 视频流网关",
        },
        {
            "type": "无人机",
            "count": len([item for item in DEVICE_LIST if item["type"] == "无人机"]),
            "status": "巡检链路预留",
            "hint": "后续接入航测任务、飞控状态与影像回传",
        },
        {
            "type": "灌溉控制器",
            "count": len([item for item in DEVICE_LIST if item["type"] == "灌溉控制器"]),
            "status": "联控预留",
            "hint": "后续接入水肥控制器和执行单元",
        },
        {
            "type": "环境传感器",
            "count": len([item for item in DEVICE_LIST if item["type"] == "环境传感器"]),
            "status": "采集预留",
            "hint": "后续接入土壤、温湿度、EC 等实时采样",
        },
        {
            "type": "网关",
            "count": len([item for item in DEVICE_LIST if item["type"] == "网关"]),
            "status": "边缘节点",
            "hint": "后续接入协议转换、边缘缓冲与设备桥接",
        },
    ]

    return {
        "summary_cards": [
            {"label": "设备总数", "value": total, "unit": "台", "accent": "cyan"},
            {"label": "在线设备", "value": online, "unit": "台", "accent": "blue"},
            {"label": "离线设备", "value": offline, "unit": "台", "accent": "violet"},
            {"label": "异常关注", "value": alert, "unit": "台", "accent": "red"},
        ],
        "status_overview": {
            "online_count": online,
            "offline_count": offline,
            "status_cards": type_cards,
        },
        "boundary_notice": "当前页面全部为 mock 状态展示，未接入真实硬件、未建立真实在线控制链路。",
    }


def get_logs(device_code):
    device = get_device(device_code)
    if not device:
        return []
    return [
        {
            "time": "2026-04-10 11:03:15",
            "level": "INFO",
            "message": f"{device['device_code']} 状态同步完成，当前为 mock 设备日志。",
        },
        {
            "time": "2026-04-10 10:42:08",
            "level": "INFO",
            "message": f"{device['device_code']} 最近心跳已记录，未来可接入 Redis 缓存。",
        },
        {
            "time": "2026-04-10 09:15:31",
            "level": "WARN",
            "message": f"{device['device_code']} 日志为占位数据，未接真实 MQTT / WebSocket 推送。",
        },
    ]
