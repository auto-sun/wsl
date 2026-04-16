# 未来扩展说明

## 真实模型接入

- 病虫害识别模型接入点：`backend/services/ai/inference.py -> run_diagnosis`
- 智能决策模型接入点：`backend/services/ai/inference.py -> generate_decision_strategy`
- 可扩展为 PyTorch、ONNX Runtime、TensorFlow Serving 或独立推理服务

## 真实设备接入

- MQTT 客户端占位：`backend/services/mqtt/client.py`
- MQTT topic 约定：`backend/services/mqtt/topics.py`
- 设备状态缓存占位：`backend/services/cache/device_status.py`
- 后续可接入灌溉控制器、施肥机、环境传感器、无人机网关

## 实时链路

- 当前前端以一次性请求 + 页面内状态管理为主
- 后续可扩展 WebSocket、SSE 或轮询
- Redis 可作为设备状态与告警摘要的中间缓存层

## 时序数据

- InfluxDB 占位服务：`backend/services/tsdb/influx_client.py`
- 后续可承载环境传感器、灌溉日志、飞行巡检、长势指数等时序数据

## 鉴权与权限

- 当前仅保留基础登录校验占位
- 后续可切换 Django Auth、JWT、RBAC、统一身份认证
