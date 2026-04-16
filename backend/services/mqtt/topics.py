def get_device_topic_contract():
    return {
        "heartbeat": "dragonfruit/farm/<device_type>/<device_code>/heartbeat",
        "state": "dragonfruit/farm/<device_type>/<device_code>/state",
        "command": "dragonfruit/farm/<device_type>/<device_code>/command",
        "command_ack": "dragonfruit/farm/<device_type>/<device_code>/command_ack",
        "note": "当前仅为 topic 约定说明，未连接真实 MQTT Broker。",
    }
