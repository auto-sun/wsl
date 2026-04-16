document.addEventListener("DOMContentLoaded", async () => {
    const ui = window.SmartAgriUI;

    function renderRadarChart(radar) {
        const chart = ui.safeChart("prescriptionRadarChart");
        if (!chart) {
            return;
        }
        chart.setOption({
            tooltip: {},
            radar: {
                indicator: radar.indicators,
                axisName: { color: "#edf7f3" },
                splitArea: { areaStyle: { color: ["rgba(255,255,255,.02)", "rgba(45,226,182,.04)"] } },
                splitLine: { lineStyle: { color: "rgba(255,255,255,.1)" } },
                axisLine: { lineStyle: { color: "rgba(255,255,255,.1)" } },
            },
            series: [
                {
                    type: "radar",
                    data: [
                        {
                            value: radar.values,
                            areaStyle: { color: "rgba(45,226,182,.18)" },
                            lineStyle: { color: "#2de2b6" },
                            itemStyle: { color: "#ffcf5c" },
                        },
                    ],
                },
            ],
        });
    }

    function renderScheduleChart(schedule) {
        const chart = ui.safeChart("prescriptionScheduleChart");
        if (!chart) {
            return;
        }
        chart.setOption({
            tooltip: { trigger: "axis" },
            legend: { textStyle: { color: "#edf7f3" } },
            grid: { left: 42, right: 22, top: 48, bottom: 30 },
            xAxis: {
                type: "category",
                data: schedule.hours,
                axisLabel: { color: "rgba(237,247,243,.72)" },
                axisLine: { lineStyle: { color: "rgba(255,255,255,.16)" } },
            },
            yAxis: [
                {
                    type: "value",
                    name: "m3/h",
                    axisLabel: { color: "rgba(237,247,243,.72)" },
                    splitLine: { lineStyle: { color: "rgba(255,255,255,.08)" } },
                },
                {
                    type: "value",
                    name: "EC",
                    axisLabel: { color: "rgba(237,247,243,.72)" },
                    splitLine: { show: false },
                },
            ],
            series: [
                {
                    name: "灌溉流量",
                    type: "bar",
                    data: schedule.water_flow,
                    itemStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: "#1da7d9" },
                            { offset: 1, color: "#10637f" },
                        ]),
                        borderRadius: [10, 10, 0, 0],
                    },
                },
                {
                    name: "施肥比例",
                    type: "line",
                    smooth: true,
                    yAxisIndex: 1,
                    data: schedule.fertilizer_ratio,
                    lineStyle: { color: "#ff6b6b" },
                    areaStyle: { color: "rgba(255,107,107,.08)" },
                },
            ],
        });
    }

    function renderDispatchPreview(preview) {
        const container = document.getElementById("dispatchPreview");
        if (!container) {
            return;
        }
        container.innerHTML = `
            <h4>MQTT 下发预览</h4>
            <p>主题：${ui.escapeHtml(preview.channel)}</p>
            <p>状态：${ui.escapeHtml(preview.message)}</p>
        `;
    }

    try {
        const data = await apiClient.get("/api/prescriptions/current/");
        ui.renderSummaryCards("prescriptionSummary", data.summary_cards);
        renderRadarChart(data.radar);
        renderScheduleChart(data.schedule);
        ui.renderTable("prescriptionTable", [
            { label: "地块", key: "block_code" },
            { label: "策略", key: "strategy" },
            { label: "建议水量", key: "water" },
            { label: "肥液配比", key: "fertilizer" },
            { label: "执行窗口", key: "window" },
        ], data.zones);
        renderDispatchPreview(data.dispatch_preview);
        ui.renderTodoList("prescriptionTodos", data.todo_modules);
    } catch (error) {
        alert(error.message);
    }
});
