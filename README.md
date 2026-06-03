# 基于 AI + 无人机的火龙果长势监测与精准水肥一体化系统研发

## 项目定位

本项目当前交付的是“可演示第一版”单体 Web 应用，面向火龙果种植园的监测、诊断、决策、设备管理场景，重点完成：

- PC 端智慧农业监控驾驶舱
- 长势监测页面
- 病虫害图片检测流程页面
- 处方图 / 水肥一体化策略页面
- 设备管理页面
- 基础登录校验占位
- RESTful API 与扩展服务骨架

当前阶段明确边界：

- 病虫害检测已接入本地 YOLOv8 权重加载逻辑，未放置权重时使用 mock 兜底
- 不接真实无人机航测链路
- 不接真实传感器
- 不接真实灌溉控制器
- 不接真实 MQTT Broker
- 不接真实 Redis / InfluxDB 服务

以上能力均已保留清晰扩展点。

## 技术栈

- 后端：Django + Django REST Framework
- 前端：HTML + CSS + 原生 JavaScript
- 图表：ECharts
- 地图：Mapbox GL
- 数据存储：当前默认 SQLite，已预留 MySQL 配置
- 扩展服务预留：Redis、InfluxDB、MQTT、AI 推理服务

## 当前已完成功能

### 1. 登录与整体框架

- 登录页 `/login`
- 基础登录校验占位
- 顶部用户信息区
- 左侧菜单高亮
- breadcrumb 导航
- 404 页面

### 2. 系统首页 / 驾驶舱

- 系统标题区
- 今日概览卡片
- 火龙果长势趋势图
- 病虫害检测统计图
- 水肥策略执行概览
- 地块热力地图
- 浏览器摄像头实时画面
- 最近告警列表
- 快捷入口

### 3. 长势监测页面

- 地块筛选
- 时间范围筛选
- 长势总览卡
- 长势等级分布图
- 长势趋势图
- NDVI / 健康指数占位图
- 热力地图
- 巡检记录列表
- 无人机巡检信息卡

### 4. 病虫害检测页面

- 点击上传
- 拖拽上传
- 图片预览
- 检测进度反馈
- YOLOv8 / mock 兜底推理结果展示
- 风险等级标签
- 标注框 overlay
- 历史检测记录
- 常见病虫害说明

### 5. 处方图 / 水肥策略页面

- 地块选择
- 长势 / 风险摘要
- 建议灌溉量
- 建议施肥量
- 执行时段建议
- 处方等级分布图
- 处方地图
- 历史策略记录
- 生成新策略
- 下发策略占位

### 6. 设备管理页面

- 设备总览统计
- 在线 / 离线数量
- 设备列表表格
- 设备类型标签
- 设备状态卡片
- 最近心跳时间
- 电量 / 信号强度占位
- 连接测试占位
- 查看日志占位
- 下发命令占位

### 7. 文档与说明

- Web 版 API 简要文档 `/api-docs`
- 根目录 `docs/API.md`
- 根目录 `docs/MOCK_DATA.md`
- 根目录 `docs/EXTENSIONS.md`

## 项目结构

```text
competition/
├── backend/
│   ├── manage.py
│   ├── config/
│   │   ├── settings.py
│   │   └── urls.py
│   ├── apps/
│   │   ├── common/
│   │   ├── user/
│   │   ├── monitoring/
│   │   ├── diagnosis/
│   │   ├── decision/
│   │   └── device/
│   └── services/
│       ├── ai/
│       ├── mqtt/
│       ├── cache/
│       └── tsdb/
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   └── templates/
│       ├── base.html
│       ├── login.html
│       ├── dashboard.html
│       ├── monitoring.html
│       ├── diagnosis.html
│       ├── decision.html
│       ├── devices.html
│       ├── api_docs.html
│       └── 404.html
├── docs/
│   ├── API.md
│   ├── MOCK_DATA.md
│   └── EXTENSIONS.md
├── media/
├── models/
│   └── README.md
├── .env.example
└── requirements.txt
```

## 运行步骤

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 进入后端目录

```bash
cd backend
```

### 3. 执行数据库迁移

```bash
python manage.py migrate
```

### 4. 可选：放置病虫害识别模型

如果已经训练好 YOLOv8 权重，将 `.pt` 放到：

```text
models/dragonfruit_disease_yolov8s.pt
```

默认配置来自 `.env.example`：

```text
AI_MODEL_PATH=/home/autosun/code/competition/models/dragonfruit_disease_yolov8s.pt
AI_MODEL_DEVICE=cpu
AI_MODEL_CONFIDENCE_THRESHOLD=0.25
AI_MODEL_IOU_THRESHOLD=0.45
AI_MODEL_IMAGE_SIZE=640
AI_MODEL_FALLBACK_TO_MOCK=true
```

没有放置模型时，病虫害检测接口会自动回退 mock 结果。

### 5. 启动开发服务

```bash
python manage.py runserver
```

### 6. 打开浏览器

- 登录页：`http://127.0.0.1:8000/login`
- 系统首页：`http://127.0.0.1:8000/dashboard`
- API 根入口：`http://127.0.0.1:8000/api/`
- API 文档页：`http://127.0.0.1:8000/api-docs`

### 7. 演示账号

- 账号：`admin`
- 密码：`123456`

## 页面与路由清单

### 页面

- `/login`
- `/dashboard`
- `/monitoring`
- `/diagnosis`
- `/decision`
- `/devices`
- `/api-docs`

### 核心 API

- `GET /api/`
- `GET /api/health`
- `GET /api/dashboard/overview`
- `GET /api/monitoring/growth-summary`
- `GET /api/monitoring/heatmap-data`
- `POST /api/diagnosis/upload`
- `GET /api/diagnosis/history`
- `GET /api/decision/plans`
- `POST /api/decision/generate`
- `POST /api/decision/dispatch`
- `GET /api/devices/status`
- `GET /api/devices/list`
- `GET /api/devices/logs`
- `POST /api/devices/test`
- `POST /api/devices/command`

## Mock 数据说明

### 当前是真实执行的部分

- Django 页面路由与 API 路由
- 登录会话占位
- 图片上传保存
- 病虫害 YOLOv8 本地权重推理入口
- 检测记录 / 策略记录数据库写入
- 浏览器摄像头 `getUserMedia`

### 当前仍为 mock / 占位的部分

- 病虫害 AI 推理在未放置 `.pt` 或推理失败时使用 mock 兜底
- 长势监测业务数据
- 无人机巡检业务数据
- 处方策略生成
- 策略下发控制
- 设备在线状态与日志
- MQTT 下发
- Redis 实时缓存
- InfluxDB 时序数据

详见：

- `docs/MOCK_DATA.md`
- `docs/EXTENSIONS.md`

## 扩展点清单

### 真实模型接入

- `backend/services/ai/inference.py`
- 默认读取 `models/dragonfruit_disease_yolov8s.pt`
- 当前已支持通过 ultralytics 调用 YOLOv8 `.pt` 权重

### 真实设备接入

- `backend/services/mqtt/client.py`
- `backend/services/mqtt/topics.py`
- `backend/services/cache/device_status.py`

### 真实时序数据接入

- `backend/services/tsdb/influx_client.py`

### 实时推送

- 当前支持继续扩展为轮询
- 后续可接入 WebSocket / SSE

### 鉴权升级

- 当前为基础登录校验占位
- 后续可接入 Django Auth / JWT / RBAC

## 演示注意事项

- 图表与地图依赖浏览器访问 CDN 资源
- 首页摄像头模块依赖浏览器权限授权
- 如果浏览器禁用摄像头或设备不可用，页面会给出降级提示
- 当前所有“下发策略”“下发命令”“连接测试”均为占位动作，不会控制真实设备

## 自检建议

开发或演示前建议执行：

```bash
cd backend
python manage.py check
python manage.py test
```
