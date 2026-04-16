# API 简要文档

## 统一约定

- 基础返回结构：`{"code": 0, "message": "ok", "data": {...}}`
- 当前阶段 API 默认开放，便于前端联调与演示
- HTML 页面采用基础登录占位，演示账号为 `admin / 123456`
- 所有接口均为 mock 数据或占位逻辑，已为未来真实接入保留结构

## 页面路由

| 路径 | 说明 |
| --- | --- |
| `/login` | 登录页 |
| `/dashboard` | 系统首页 / 驾驶舱 |
| `/monitoring` | 长势监测页 |
| `/diagnosis` | 病虫害检测页 |
| `/decision` | 处方图 / 水肥策略页 |
| `/devices` | 设备管理页 |
| `/api-docs` | Web 版 API 简要文档 |

## 公共接口

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/` | API 根入口 |
| GET | `/api/health` | 基础健康检查与扩展服务占位信息 |
| GET | `/api/dashboard/overview` | 驾驶舱首页 mock 数据 |

## 长势监测

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/monitoring/growth-summary` | 长势总览、趋势、NDVI、巡检记录 |
| GET | `/api/monitoring/heatmap-data` | 地块热力地图与地理数据 |

## 病虫害检测

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/api/diagnosis/upload` | 上传病虫害图片，保存图片并返回 mock 推理结果 |
| GET | `/api/diagnosis/history` | 查询最近历史检测记录 |

### 诊断返回要点

- `image_name`
- `diagnosis_name`
- `confidence`
- `risk_level`
- `suggestions`
- `overlay_boxes`
- `inference_mode`

## 处方策略

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/decision/plans` | 获取地块策略列表、地图、历史记录 |
| POST | `/api/decision/generate` | 生成新 mock 策略 |
| POST | `/api/decision/dispatch` | 下发策略占位，不执行真实控制 |

## 设备管理

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/devices/status` | 设备总览、状态统计、扩展说明 |
| GET | `/api/devices/list` | 设备列表 |
| GET | `/api/devices/logs?device_code=CAM-01` | 设备日志 mock 数据 |
| POST | `/api/devices/test` | 设备连接测试占位 |
| POST | `/api/devices/command` | 设备命令下发占位 |

## 说明

- `services/ai/inference.py` 是 AI 推理统一入口，当前返回 mock 数据
- `services/mqtt/client.py` 与 `services/mqtt/topics.py` 预留 MQTT 下发与 topic 约定
- `services/cache/device_status.py` 预留 Redis 实时状态缓存逻辑
- `services/tsdb/influx_client.py` 预留 InfluxDB 时序数据接入
