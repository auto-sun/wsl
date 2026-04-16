from .mock_data import get_growth_summary_payload, get_heatmap_payload


class MonitoringService:
    """
    长势监测服务。

    当前阶段：
    - 统一输出长势总览与热力地图 mock 数据
    - 避免将 mock 数据选择逻辑直接放在 view 中

    未来阶段：
    - 可在这里接入无人机航测、遥感识别、多光谱分析与时序库查询
    """

    def get_growth_summary_payload(self):
        return get_growth_summary_payload()

    def get_heatmap_payload(self):
        return get_heatmap_payload()
