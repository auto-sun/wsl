# API 文档

## 统一响应结构

```json
{
  "code": 0,
  "message": "ok",
  "data": {}
}
```

## 认证

### POST `/api/auth/login/`

请求体：

```json
{
  "username": "admin",
  "password": "123456"
}
```

说明：

- 创建会话并返回跳转地址。
- 当前阶段为演示登录，账号密码来自配置项。

### POST `/api/auth/logout/`

说明：

- 清理当前会话并退出系统。

## 驾驶舱

### GET `/api/dashboard/overview/`

返回：

- 核心指标卡片
- 长势趋势曲线数据
- 水肥策略图表数据
- 无人机任务
- 预警清单

## 长势监测

### GET `/api/monitoring/growth/`

返回：

- 长势 KPI
- NDVI / 墒情 / 开花同步率趋势
- 地块监测清单
- AI 解读摘要

### GET `/api/monitoring/heatmap/`

返回：

- 地图中心点与缩放等级
- 地块热力 GeoJSON

## 病虫害检测

### GET `/api/disease-detections/`

返回：

- 最近检测历史
- 若数据库暂无记录，则回退到 mock 历史数据

### POST `/api/disease-detections/`

表单字段：

- `image`：图片文件，必填
- `plot_code`：地块编号，可选
- `remarks`：备注，可选

返回：

- `task_code`
- `disease_name`
- `confidence`
- `severity`
- `detected_area`
- `suggestions`
- `boxes`
- `storage_path`
- `inference`

说明：

- 当前阶段保存上传文件并返回 mock 推理结果。
- `ModelInferenceService` 已保留真实模型调用入口。

## 处方图与策略

### GET `/api/prescriptions/current/`

返回：

- 处方总览卡片
- 雷达图配置数据
- 时段排程数据
- 分区处方表
- MQTT 下发预览
- TODO 清单

## 设备管理

### GET `/api/devices/`

返回：

- 设备汇总指标
- 设备状态分布
- 设备清单
- 基础设施预留状态
- 平台与外围系统连接说明

### GET `/api/infrastructure/status/`

返回：

- MySQL 配置预留说明
- MQTT / 传感器 / InfluxDB / Redis / 模型服务占位状态

## TODO 接口约定

- MQTT 真正联控时，继续沿用 `publish_irrigation_plan(plan_payload)` 的服务入口。
- 病虫害真实模型接入时，继续沿用 `infer_disease(file_path)` 的服务入口。
- 传感器接入时，在 `SensorGatewayService.latest_snapshot()` 中返回真实采样数据。
