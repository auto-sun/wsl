document.addEventListener("DOMContentLoaded", async () => {
    const ui = window.SmartAgriUI;

    function renderTrendChart(trend) {
        const chart = ui.safeChart("growthMetricsChart");
        if (!chart) {
            return;
        }
        chart.setOption({
            tooltip: { trigger: "axis" },
            legend: { textStyle: { color: "#edf7f3" } },
            grid: { left: 42, right: 22, top: 48, bottom: 30 },
            xAxis: {
                type: "category",
                data: trend.dates,
                axisLabel: { color: "rgba(237,247,243,.72)" },
                axisLine: { lineStyle: { color: "rgba(255,255,255,.16)" } },
            },
            yAxis: [
                {
                    type: "value",
                    name: "指数/占比",
                    axisLabel: { color: "rgba(237,247,243,.72)" },
                    splitLine: { lineStyle: { color: "rgba(255,255,255,.08)" } },
                },
                {
                    type: "value",
                    name: "墒情%",
                    axisLabel: { color: "rgba(237,247,243,.72)" },
                    splitLine: { show: false },
                },
            ],
            series: [
                { name: "NDVI", type: "line", smooth: true, data: trend.ndvi, lineStyle: { color: "#2de2b6" }, areaStyle: { color: "rgba(45,226,182,.12)" } },
                { name: "土壤墒情", type: "bar", yAxisIndex: 1, data: trend.moisture, itemStyle: { color: "#1da7d9", borderRadius: [10, 10, 0, 0] } },
                { name: "开花同步率", type: "line", smooth: true, data: trend.flowering, lineStyle: { color: "#ffcf5c" } },
            ],
        });
    }

    function renderBlocks(blocks) {
        ui.renderStackList("blockInsightList", blocks, (block) => `
            <div class="list-card">
                <div class="list-card-top">
                    <h4>${ui.escapeHtml(block.code)} · ${ui.escapeHtml(block.name)}</h4>
                    <span class="status-badge ${ui.statusClass(block.risk)}">${ui.escapeHtml(block.risk)}风险</span>
                </div>
                <p>长势指数：${ui.escapeHtml(block.vigor)}，墒情：${ui.escapeHtml(block.moisture)}%</p>
            </div>
        `);
    }

    function renderInsight(insight) {
        const container = document.getElementById("growthInsight");
        if (!container) {
            return;
        }
        container.innerHTML = `
            <h4>${ui.escapeHtml(insight.title)}</h4>
            <p>${ui.escapeHtml(insight.summary)}</p>
        `;
    }

    try {
        const [growth, heatmap] = await Promise.all([
            apiClient.get("/api/monitoring/growth/"),
            apiClient.get("/api/monitoring/heatmap/"),
        ]);

        ui.renderSummaryCards("growthKpis", growth.kpis);
        renderTrendChart(growth.trend);
        renderBlocks(growth.blocks);
        renderInsight(growth.insight);
        ui.createOrchardMap("growthMap", heatmap.geojson, heatmap.map);
    } catch (error) {
        alert(error.message);
    }
});
