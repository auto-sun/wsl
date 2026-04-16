async function initDevicesPage() {
    const { escapeHtml, getAccentClass, renderState, renderErrorState, setButtonLoading } = window.pageUtils;

    const summaryNode = document.getElementById("deviceSummaryCards");
    const boundaryNode = document.getElementById("boundaryNotice");
    const overviewNode = document.getElementById("deviceStatusOverview");
    const typeNode = document.getElementById("deviceTypeCards");
    const tableNode = document.getElementById("deviceTable");
    const infoNode = document.getElementById("selectedDeviceInfo");
    const actionResultNode = document.getElementById("actionResult");
    const logsNode = document.getElementById("deviceLogs");
    const extensionNode = document.getElementById("extensionCards");
    const devicesShell = document.querySelector(".devices-shell");

    let deviceList = [];
    let selectedDeviceCode = "CAM-01";

    function getSelectedDevice() {
        return deviceList.find((item) => item.device_code === selectedDeviceCode) || deviceList[0];
    }

    function statusClass(status) {
        if (status === "在线") {
            return "status-online";
        }
        if (status === "离线") {
            return "status-offline";
        }
        return "status-maintain";
    }

    function riskClass(level) {
        if (level === "高") {
            return "risk-high";
        }
        if (level === "中") {
            return "risk-medium";
        }
        return "risk-low";
    }

    function renderSummary(cards) {
        summaryNode.innerHTML = cards.map((card) => `
            <article class="device-summary-card ${getAccentClass(card.accent)}">
                <div>${escapeHtml(card.label)}</div>
                <div class="device-summary-main">
                    <strong>${escapeHtml(card.value)}</strong>
                    <span>${escapeHtml(card.unit || "")}</span>
                </div>
            </article>
        `).join("");
    }

    function renderOverview(overview) {
        overviewNode.innerHTML = `
            <div class="overview-card">
                <span>在线设备数量</span>
                <strong>${escapeHtml(overview.online_count)} 台</strong>
                <p>当前为 mock 状态同步结果。</p>
            </div>
            <div class="overview-card">
                <span>离线设备数量</span>
                <strong>${escapeHtml(overview.offline_count)} 台</strong>
                <p>后续可接入 Redis 实时状态缓存。</p>
            </div>
        `;
    }

    function renderTypeCards(cards) {
        typeNode.innerHTML = cards.map((item) => `
            <article class="type-card">
                <span>${escapeHtml(item.type)}</span>
                <strong>${escapeHtml(item.count)} 台</strong>
                <p>${escapeHtml(item.status)}</p>
                <p>${escapeHtml(item.hint)}</p>
            </article>
        `).join("");
    }

    function renderSelectedDevice() {
        const device = getSelectedDevice();
        if (!device) {
            renderState(infoNode, "当前暂无设备数据", "app-empty-state");
            return;
        }
        infoNode.innerHTML = `
            <span>当前选中设备</span>
            <strong>${escapeHtml(device.device_code)} · ${escapeHtml(device.name)}</strong>
            <p>类型：${escapeHtml(device.type)}，状态：${escapeHtml(device.status)}，最近心跳：${escapeHtml(device.heartbeat_at)}</p>
            <p>电量/信号：${escapeHtml(device.battery)} / ${escapeHtml(device.signal)}</p>
            <p>MQTT 主题：${escapeHtml(device.mqtt_topic)}</p>
        `;
    }

    function renderActionResult(title, message) {
        actionResultNode.innerHTML = `
            <span>动作反馈</span>
            <strong>${escapeHtml(title)}</strong>
            <p>${escapeHtml(message)}</p>
        `;
    }

    function renderLogs(logs, message) {
        logsNode.innerHTML = [
            `<div class="log-item"><strong>日志说明</strong><p>${escapeHtml(message)}</p></div>`,
            ...logs.map((item) => `
                <div class="log-item">
                    <strong>${escapeHtml(item.level)} · ${escapeHtml(item.time)}</strong>
                    <p>${escapeHtml(item.message)}</p>
                </div>
            `),
        ].join("");
    }

    function renderExtensions(extensions) {
        extensionNode.innerHTML = `
            <div class="extension-item">
                <span>设备状态 service</span>
                <p>${escapeHtml(extensions.device_status_service.message)}</p>
                <p>Key 约定：${escapeHtml(extensions.device_status_service.key_patterns.join(" / "))}</p>
            </div>
            <div class="extension-item">
                <span>MQTT topic 约定</span>
                <p>Heartbeat: ${escapeHtml(extensions.mqtt_topics.heartbeat)}</p>
                <p>State: ${escapeHtml(extensions.mqtt_topics.state)}</p>
                <p>Command: ${escapeHtml(extensions.mqtt_topics.command)}</p>
                <p>${escapeHtml(extensions.mqtt_topics.note)}</p>
            </div>
            <div class="extension-item">
                <span>实时推送接口预留</span>
                <p>当前模式：${escapeHtml(extensions.realtime_push.current_mode)}</p>
                <p>轮询：${escapeHtml(extensions.realtime_push.polling_endpoint)}</p>
                <p>WebSocket 预留：${escapeHtml(extensions.realtime_push.websocket_placeholder)}</p>
                <p>${escapeHtml(extensions.realtime_push.message)}</p>
            </div>
        `;
    }

    function renderTable(rows) {
        if (!rows.length) {
            renderState(tableNode, "当前暂无设备数据", "app-empty-state");
            return;
        }

        tableNode.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>设备编号</th>
                        <th>设备名称</th>
                        <th>类型</th>
                        <th>状态</th>
                        <th>风险等级</th>
                        <th>最近心跳</th>
                        <th>电量</th>
                        <th>信号</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    ${rows.map((row) => `
                        <tr data-device-code="${escapeHtml(row.device_code)}">
                            <td>${escapeHtml(row.device_code)}</td>
                            <td>${escapeHtml(row.name)}</td>
                            <td><span class="type-tag">${escapeHtml(row.type)}</span></td>
                            <td><span class="status-tag ${statusClass(row.status)}">${escapeHtml(row.status)}</span></td>
                            <td><span class="risk-tag ${riskClass(row.risk)}">${escapeHtml(row.risk)}</span></td>
                            <td>${escapeHtml(row.heartbeat_at)}</td>
                            <td>${escapeHtml(row.battery)}</td>
                            <td>${escapeHtml(row.signal)}</td>
                            <td>
                                <div class="action-btn-group">
                                    <button class="mini-btn" data-action="test" data-device="${escapeHtml(row.device_code)}">连接测试</button>
                                    <button class="mini-btn" data-action="logs" data-device="${escapeHtml(row.device_code)}">查看日志</button>
                                    <button class="mini-btn" data-action="command" data-device="${escapeHtml(row.device_code)}">下发命令</button>
                                </div>
                            </td>
                        </tr>
                    `).join("")}
                </tbody>
            </table>
        `;
    }

    async function loadLogs(deviceCode) {
        const data = await apiClient.get(`/api/devices/logs?device_code=${encodeURIComponent(deviceCode)}`);
        renderLogs(data.logs, data.message);
    }

    async function loadDevices() {
        window.appUI?.setLoading(true, "正在加载设备状态与日志...");
        const [status, list] = await Promise.all([
            apiClient.get("/api/devices/status"),
            apiClient.get("/api/devices/list"),
        ]);
        deviceList = list.devices;
        boundaryNode.innerHTML = `<p>${escapeHtml(status.boundary_notice)}</p>`;
        renderSummary(status.summary_cards);
        renderOverview(status.status_overview);
        renderTypeCards(status.status_overview.status_cards);
        renderTable(deviceList);
        renderExtensions(status.extensions);
        renderSelectedDevice();
        renderActionResult("系统边界说明", "当前所有按钮均为占位动作，不会与真实硬件建立连接。");
        await loadLogs(selectedDeviceCode);
        window.appUI?.setLoading(false);
    }

    tableNode.addEventListener("click", async (event) => {
        const button = event.target.closest("button[data-action]");
        if (!button) {
            return;
        }
        const action = button.dataset.action;
        const deviceCode = button.dataset.device;
        selectedDeviceCode = deviceCode;
        renderSelectedDevice();

        setButtonLoading(button, true, "处理中...");
        try {
            if (action === "test") {
                window.appUI?.setLoading(true, `正在执行 ${deviceCode} 连接测试...`);
                const data = await apiClient.postJson("/api/devices/test", { device_code: deviceCode });
                renderActionResult(`${deviceCode} 连接测试`, data.message);
                window.appUI?.notify(data.message, "success", "连接测试完成");
            } else if (action === "logs") {
                window.appUI?.setLoading(true, `正在加载 ${deviceCode} 日志...`);
                await loadLogs(deviceCode);
                renderActionResult(`${deviceCode} 查看日志`, "已加载 mock 日志输出。");
                window.appUI?.notify("已加载 mock 日志输出。", "info", "日志查看完成");
            } else if (action === "command") {
                window.appUI?.setLoading(true, `正在生成 ${deviceCode} 命令下发预览...`);
                const data = await apiClient.postJson("/api/devices/command", {
                    device_code: deviceCode,
                    command: "status_sync",
                });
                renderActionResult(`${deviceCode} 下发命令`, data.message);
                window.appUI?.notify(data.message, "success", "命令占位已提交");
            }
        } catch (error) {
            window.appUI?.notify(error.message, "error", "设备操作失败");
            renderActionResult("操作失败", error.message);
        } finally {
            window.appUI?.setLoading(false);
            setButtonLoading(button, false);
        }
    });

    try {
        await loadDevices();
    } catch (error) {
        window.appUI?.setLoading(false);
        window.appUI?.notify(error.message, "error", "设备数据加载失败");
        renderErrorState(devicesShell, error.message, "app-error-state");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    initDevicesPage().catch((error) => {
        window.appUI?.setLoading(false);
        window.appUI?.notify(error.message || "页面初始化失败", "error", "设备页初始化失败");
    });
});
