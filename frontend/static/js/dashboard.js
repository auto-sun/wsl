function createDashboardGrowthTrendOption(config) {
    const { getGrid, getLegend, getCategoryAxis, getValueAxis } = window.chartUtils;
    return {
        animationDuration: 700,
        tooltip: { trigger: "axis" },
        legend: getLegend({ right: 10 }),
        grid: getGrid({ left: 44, top: 48, bottom: 32 }),
        xAxis: getCategoryAxis(config.dates, { boundaryGap: false }),
        yAxis: [
            getValueAxis({ name: "指数" }),
            getValueAxis({ name: "墒情%", splitLine: { show: false } }),
        ],
        series: [
            {
                name: "长势指数",
                type: "line",
                smooth: true,
                data: config.growth_index,
                symbolSize: 7,
                lineStyle: { width: 3, color: "#50e3ff" },
                areaStyle: { color: "rgba(80, 227, 255, 0.12)" },
            },
            {
                name: "开花指数",
                type: "line",
                smooth: true,
                data: config.flower_index,
                symbolSize: 7,
                lineStyle: { width: 3, color: "#8f7cff" },
                areaStyle: { color: "rgba(143, 124, 255, 0.09)" },
            },
            {
                name: "土壤墒情",
                type: "bar",
                yAxisIndex: 1,
                data: config.moisture,
                barWidth: 18,
                itemStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: "#ff5f7a" },
                        { offset: 1, color: "#ad2d5e" },
                    ]),
                    borderRadius: [8, 8, 0, 0],
                },
            },
        ],
    };
}

function createDashboardDiagnosisStatsOption(config) {
    const { getLegend } = window.chartUtils;
    return {
        animationDuration: 700,
        tooltip: { trigger: "item" },
        legend: getLegend({ bottom: 8 }),
        series: [
            {
                type: "pie",
                radius: ["42%", "68%"],
                center: ["50%", "45%"],
                data: config.labels.map((label, index) => ({
                    name: label,
                    value: config.values[index],
                })),
                label: { color: "#eef8ff" },
                labelLine: { lineStyle: { color: "rgba(255,255,255,.24)" } },
                itemStyle: {
                    borderColor: "#081723",
                    borderWidth: 4,
                },
                color: ["#32d1c0", "#7f69ff", "#ff5f7a", "#72d8ff"],
            },
        ],
    };
}

function createDashboardStrategyOverviewOption(config) {
    const { getGrid, getLegend, getCategoryAxis, getValueAxis } = window.chartUtils;
    return {
        animationDuration: 700,
        tooltip: { trigger: "axis" },
        legend: getLegend({ top: 6 }),
        grid: getGrid({ left: 42, top: 50 }),
        xAxis: getCategoryAxis(config.zones),
        yAxis: [
            getValueAxis({ name: "水量 / EC" }),
            getValueAxis({ name: "完成率%", splitLine: { show: false } }),
        ],
        series: [
            {
                name: "灌溉计划量",
                type: "bar",
                data: config.water_plan,
                barWidth: 16,
                itemStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: "#72d8ff" },
                        { offset: 1, color: "#2a6eff" },
                    ]),
                    borderRadius: [8, 8, 0, 0],
                },
            },
            {
                name: "施肥浓度",
                type: "line",
                smooth: true,
                data: config.fertilizer_plan,
                lineStyle: { width: 3, color: "#8f7cff" },
                symbolSize: 7,
            },
            {
                name: "策略完成率",
                type: "line",
                yAxisIndex: 1,
                smooth: true,
                data: config.completion,
                lineStyle: { width: 3, color: "#ff5f7a" },
                areaStyle: { color: "rgba(255,95,122,.08)" },
                symbolSize: 7,
            },
        ],
    };
}

async function initDashboardPage() {
    const { escapeHtml, getAccentClass, renderErrorState } = window.pageUtils;
    const { setChartOption } = window.chartUtils;

    const overviewCardsNode = document.getElementById("overviewCards");
    const quickLinksNode = document.getElementById("quickLinks");
    const alertsNode = document.getElementById("recentAlerts");
    const cameraVideoNode = document.getElementById("cameraVideo");
    const cameraFreezeFrameNode = document.getElementById("cameraFreezeFrame");
    const startCameraButton = document.getElementById("startCameraButton");
    const pauseCameraButton = document.getElementById("pauseCameraButton");
    const stopCameraButton = document.getElementById("stopCameraButton");
    const cameraStatusBadge = document.getElementById("cameraStatusBadge");
    const cameraMessage = document.getElementById("cameraMessage");
    const cameraFrameNode = document.querySelector(".camera-frame");
    const dashboardShell = document.querySelector(".dashboard-shell");
    const freezeFrameContext = cameraFreezeFrameNode?.getContext("2d");

    let cameraStream = null;
    let isCameraPaused = false;

    function renderOverviewCards(cards) {
        overviewCardsNode.innerHTML = cards.map((card) => `
            <article class="overview-card ${getAccentClass(card.accent)}">
                <div class="overview-card-label">${escapeHtml(card.label)}</div>
                <div class="overview-card-main">
                    <strong>${escapeHtml(card.value)}</strong>
                    <span>${escapeHtml(card.unit || "")}</span>
                </div>
                <div class="overview-card-trend">较昨日 ${escapeHtml(card.trend)}</div>
            </article>
        `).join("");
    }

    function renderAlerts(alerts) {
        alertsNode.innerHTML = alerts.map((alertItem) => {
            let levelClass = "alert-low";
            if (alertItem.level === "高") {
                levelClass = "alert-high";
            } else if (alertItem.level === "中") {
                levelClass = "alert-medium";
            }
            return `
                <article class="alert-item">
                    <div class="alert-item-header">
                        <h5>${escapeHtml(alertItem.title)}</h5>
                        <span class="alert-level ${levelClass}">${escapeHtml(alertItem.level)}级</span>
                    </div>
                    <div class="alert-meta">${escapeHtml(alertItem.time)}</div>
                    <p>${escapeHtml(alertItem.detail)}</p>
                </article>
            `;
        }).join("");
    }

    function renderQuickLinks(links) {
        quickLinksNode.innerHTML = links.map((link) => `
            <a href="${escapeHtml(link.path)}" class="quick-link-card">
                <div>
                    <strong>${escapeHtml(link.label)}</strong>
                    <p>${escapeHtml(link.description)}</p>
                </div>
                <span class="quick-link-arrow">↗</span>
            </a>
        `).join("");
    }

    function renderTitle(payload) {
        document.getElementById("dashboardSystemTitle").textContent = payload.system_title;
        document.getElementById("dashboardSystemSubtitle").textContent = payload.system_subtitle;
        document.getElementById("droneMissionName").textContent = payload.drone_status.mission_name;
        document.getElementById("droneMissionRoute").textContent = payload.drone_status.route;
        document.getElementById("droneMissionMessage").textContent = payload.drone_status.message;
        document.getElementById("droneMissionProgress").style.width = `${payload.drone_status.progress}%`;
    }

    function renderCharts(payload) {
        setChartOption(
            "growthTrendChart",
            createDashboardGrowthTrendOption(payload.growth_trend),
            { emptyClass: "dashboard-empty", emptyText: "图表库未加载" },
        );
        setChartOption(
            "diagnosisStatsChart",
            createDashboardDiagnosisStatsOption(payload.diagnosis_stats),
            { emptyClass: "dashboard-empty", emptyText: "图表库未加载" },
        );
        setChartOption(
            "strategyOverviewChart",
            createDashboardStrategyOverviewOption(payload.strategy_overview),
            { emptyClass: "dashboard-empty", emptyText: "图表库未加载" },
        );
    }

    function buildMap(config) {
        const mapNode = document.getElementById("orchardMap");
        if (!mapNode) {
            return;
        }

        if (!window.mapboxgl) {
            window.pageUtils.renderState(mapNode, "地图组件未加载", "dashboard-empty");
            return;
        }

        mapboxgl.accessToken = "";
        const map = new mapboxgl.Map({
            container: "orchardMap",
            center: config.center,
            zoom: config.zoom,
            style: {
                version: 8,
                sources: {
                    osm: {
                        type: "raster",
                        tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
                        tileSize: 256,
                        attribution: "OpenStreetMap",
                    },
                },
                layers: [{ id: "osm", type: "raster", source: "osm" }],
            },
        });

        map.addControl(new mapboxgl.NavigationControl(), "top-right");

        map.on("load", () => {
            map.addSource("orchard-heat", {
                type: "geojson",
                data: config.geojson,
            });

            map.addLayer({
                id: "orchard-heat-layer",
                type: "heatmap",
                source: "orchard-heat",
                maxzoom: 16,
                paint: {
                    "heatmap-weight": ["interpolate", ["linear"], ["get", "intensity"], 0, 0, 1, 1],
                    "heatmap-intensity": 0.9,
                    "heatmap-radius": 28,
                    "heatmap-opacity": 0.78,
                    "heatmap-color": [
                        "interpolate",
                        ["linear"],
                        ["heatmap-density"],
                        0, "rgba(50,209,192,0)",
                        0.3, "#32d1c0",
                        0.6, "#7f69ff",
                        1, "#ff5f7a",
                    ],
                },
            });

            map.addLayer({
                id: "orchard-points",
                type: "circle",
                source: "orchard-heat",
                paint: {
                    "circle-radius": 8,
                    "circle-color": [
                        "interpolate",
                        ["linear"],
                        ["get", "intensity"],
                        0.6, "#ff5f7a",
                        0.75, "#7f69ff",
                        0.85, "#32d1c0",
                    ],
                    "circle-stroke-width": 1.5,
                    "circle-stroke-color": "#eef8ff",
                },
            });

            const popup = new mapboxgl.Popup({
                closeButton: false,
                closeOnClick: false,
                offset: 12,
            });

            map.on("mouseenter", "orchard-points", (event) => {
                map.getCanvas().style.cursor = "pointer";
                const feature = event.features && event.features[0];
                if (!feature) {
                    return;
                }
                popup
                    .setLngLat(feature.geometry.coordinates)
                    .setHTML(
                        `<strong>${escapeHtml(feature.properties.block)}</strong><br>` +
                        `长势：${escapeHtml(feature.properties.growth)}<br>` +
                        `墒情：${escapeHtml(feature.properties.moisture)}%`,
                    )
                    .addTo(map);
            });

            map.on("mouseleave", "orchard-points", () => {
                map.getCanvas().style.cursor = "";
                popup.remove();
            });
        });
    }

    function setCameraStatusBadge(text, tone = "default") {
        cameraStatusBadge.textContent = text;
        cameraStatusBadge.classList.remove("panel-chip-danger", "panel-chip-warning");

        if (tone === "danger") {
            cameraStatusBadge.classList.add("panel-chip-danger");
        } else if (tone === "warning") {
            cameraStatusBadge.classList.add("panel-chip-warning");
        }
    }

    function resetFrozenFrame(options = {}) {
        const { disablePauseButton = false } = options;

        isCameraPaused = false;
        cameraFrameNode?.classList.remove("is-paused");

        if (cameraFreezeFrameNode) {
            cameraFreezeFrameNode.hidden = true;
            cameraFreezeFrameNode.width = 0;
            cameraFreezeFrameNode.height = 0;
        }

        if (pauseCameraButton) {
            pauseCameraButton.textContent = "暂停画面";
            pauseCameraButton.classList.remove("is-active");
            pauseCameraButton.setAttribute("aria-pressed", "false");

            if (disablePauseButton) {
                pauseCameraButton.disabled = true;
            }
        }
    }

    function captureFrozenFrame() {
        if (!cameraVideoNode || !cameraFreezeFrameNode || !freezeFrameContext) {
            return false;
        }

        if (
            cameraVideoNode.readyState < HTMLMediaElement.HAVE_CURRENT_DATA ||
            !cameraVideoNode.videoWidth ||
            !cameraVideoNode.videoHeight
        ) {
            return false;
        }

        const frameWidth = cameraVideoNode.videoWidth;
        const frameHeight = cameraVideoNode.videoHeight;
        cameraFreezeFrameNode.width = frameWidth;
        cameraFreezeFrameNode.height = frameHeight;
        freezeFrameContext.clearRect(0, 0, frameWidth, frameHeight);

        // Draw the current live frame onto an overlay canvas so the paused state keeps the last image visible.
        freezeFrameContext.drawImage(cameraVideoNode, 0, 0, frameWidth, frameHeight);
        cameraFreezeFrameNode.hidden = false;
        return true;
    }

    function resumeCameraPlayback() {
        if (!cameraStream || !cameraVideoNode?.srcObject) {
            resetFrozenFrame({ disablePauseButton: true });
            return;
        }

        resetFrozenFrame();
        setCameraStatusBadge("采集中");
        cameraMessage.textContent = "摄像头已连接，正在显示实时视频流。";
    }

    function toggleCameraPause() {
        if (!cameraStream || !cameraVideoNode?.srcObject) {
            resetFrozenFrame({ disablePauseButton: true });
            cameraMessage.textContent = "请先开启摄像头后再使用暂停画面。";
            window.appUI?.notify("请先开启摄像头，再使用暂停画面功能。", "info", "摄像头未开启");
            return;
        }

        if (isCameraPaused) {
            resumeCameraPlayback();
            return;
        }

        if (!captureFrozenFrame()) {
            cameraMessage.textContent = "实时画面尚未就绪，请稍后再试。";
            window.appUI?.notify("实时画面尚未准备好，暂时无法暂停。", "info", "画面未就绪");
            return;
        }

        isCameraPaused = true;
        cameraFrameNode?.classList.add("is-paused");
        pauseCameraButton.textContent = "继续播放";
        pauseCameraButton.classList.add("is-active");
        pauseCameraButton.setAttribute("aria-pressed", "true");
        setCameraStatusBadge("已暂停", "warning");
        cameraMessage.textContent = "画面已冻结在当前帧，点击“继续播放”恢复实时视频。";
    }

    async function startCamera() {
        if (cameraStream) {
            if (isCameraPaused) {
                resumeCameraPlayback();
            }
            return;
        }

        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            setCameraStatusBadge("不支持", "danger");
            cameraMessage.textContent = "当前浏览器不支持 getUserMedia。";
            resetFrozenFrame({ disablePauseButton: true });
            window.appUI?.notify("当前浏览器不支持摄像头实时采集，请更换现代浏览器。", "error", "摄像头不可用");
            return;
        }

        try {
            cameraStream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                },
                audio: false,
            });
            cameraVideoNode.srcObject = cameraStream;
            await cameraVideoNode.play();
            resetFrozenFrame();
            setCameraStatusBadge("采集中");
            cameraMessage.textContent = "摄像头已连接，正在显示实时视频流。";
            startCameraButton.disabled = true;
            pauseCameraButton.disabled = false;
            stopCameraButton.disabled = false;
            window.appUI?.notify("浏览器摄像头已开启，正在显示实时画面。", "success", "摄像头已连接");
        } catch (error) {
            stopCamera();
            setCameraStatusBadge("开启失败", "danger");
            cameraMessage.textContent = "摄像头授权失败或设备不可用。";
            window.appUI?.notify("摄像头授权失败或设备不可用，请检查浏览器权限。", "error", "摄像头开启失败");
        }
    }

    function stopCamera() {
        if (cameraStream) {
            cameraStream.getTracks().forEach((track) => track.stop());
            cameraStream = null;
        }
        cameraVideoNode.srcObject = null;
        resetFrozenFrame({ disablePauseButton: true });
        setCameraStatusBadge("已关闭", "danger");
        cameraMessage.textContent = "摄像头已关闭。";
        startCameraButton.disabled = false;
        stopCameraButton.disabled = true;
    }

    async function loadDashboardData() {
        window.appUI?.setLoading(true, "正在加载首页驾驶舱数据...");
        const payload = await apiClient.get("/api/dashboard/overview");
        renderTitle(payload);
        renderOverviewCards(payload.overview_cards);
        renderAlerts(payload.alerts);
        renderQuickLinks(payload.quick_links);
        renderCharts(payload);
        buildMap(payload.map);
        window.appUI?.setLoading(false);
    }

    startCameraButton?.addEventListener("click", startCamera);
    pauseCameraButton?.addEventListener("click", toggleCameraPause);
    stopCameraButton?.addEventListener("click", stopCamera);
    window.addEventListener("beforeunload", stopCamera);

    try {
        await loadDashboardData();
    } catch (error) {
        window.appUI?.setLoading(false);
        window.appUI?.notify(error.message, "error", "首页数据加载失败");
        renderErrorState(dashboardShell, error.message, "dashboard-empty");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    initDashboardPage().catch((error) => {
        window.appUI?.setLoading(false);
        window.appUI?.notify(error.message || "系统初始化失败", "error", "首页初始化失败");
    });
});
