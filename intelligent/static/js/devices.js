document.addEventListener("DOMContentLoaded", async () => {
    const ui = window.SmartAgriUI;

    function renderStatusChart(items) {
        const chart = ui.safeChart("deviceStatusChart");
        if (!chart) {
            return;
        }
        chart.setOption({
            tooltip: { trigger: "item" },
            legend: {
                bottom: 0,
                textStyle: { color: "#edf7f3" },
            },
            series: [
                {
                    type: "pie",
                    radius: ["44%", "68%"],
                    data: items,
                    itemStyle: {
                        borderColor: "#071b22",
                        borderWidth: 4,
                    },
                    label: { color: "#edf7f3" },
                    color: ["#2de2b6", "#ffcf5c", "#ff6b6b"],
                },
            ],
        });
    }

    function renderInfrastructure(list) {
        ui.renderStackList("infrastructureList", list, (item) => `
            <div class="list-card">
                <div class="list-card-top">
                    <h4>${ui.escapeHtml(item.name)}</h4>
                    <span class="status-badge ${item.enabled ? "" : "warn"}">${item.enabled ? "已配置" : "预留中"}</span>
                </div>
                <p>${ui.escapeHtml(item.summary)}</p>
                <p style="margin-top:6px;">${ui.escapeHtml(item.todo)}</p>
            </div>
        `);
    }

    try {
        const data = await apiClient.get("/api/devices/");
        ui.renderSummaryCards("deviceSummary", data.summary);
        renderStatusChart(data.status_distribution);
        renderInfrastructure(data.infrastructure.services);
        ui.renderTable("deviceTable", [
            { label: "设备编码", key: "device_code" },
            { label: "设备名称", key: "name" },
            { label: "类型", key: "type" },
            {
                label: "状态",
                key: "status",
                render: (row) => `<span class="status-badge ${ui.statusClass(row.status)}">${ui.escapeHtml(row.status)}</span>`,
            },
            { label: "信号", key: "signal" },
            { label: "电量", key: "battery" },
            { label: "最后心跳", key: "last_seen" },
        ], data.devices);
        ui.renderTodoList("networkLinks", data.network_links);
    } catch (error) {
        alert(error.message);
    }
});
