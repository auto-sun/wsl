document.addEventListener("DOMContentLoaded", async () => {
    const ui = window.SmartAgriUI;
    const cameraStatus = document.getElementById("cameraStatus");
    const cameraVideo = document.getElementById("dashboardCamera");
    const cameraFreezeFrame = document.getElementById("cameraFreezeFrame");
    const cameraMessage = document.getElementById("cameraMessage");
    const cameraStage = document.querySelector(".camera-stage");
    const startCameraButton = document.getElementById("startCameraButton");
    const pauseCameraButton = document.getElementById("pauseCameraButton");
    const stopCameraButton = document.getElementById("stopCameraButton");
    const freezeFrameContext = cameraFreezeFrame?.getContext("2d");
    let streamRef = null;
    let isCameraPaused = false;

    function renderTrendChart(trend) {
        const chart = ui.safeChart("growthTrendChart");
        if (!chart) {
            return;
        }
        chart.setOption({
            tooltip: { trigger: "axis" },
            legend: { textStyle: { color: "#edf7f3" } },
            grid: { left: 36, right: 20, top: 48, bottom: 30 },
            xAxis: {
                type: "category",
                data: trend.dates,
                axisLine: { lineStyle: { color: "rgba(255,255,255,.2)" } },
                axisLabel: { color: "rgba(237,247,243,.7)" },
            },
            yAxis: {
                type: "value",
                axisLine: { show: false },
                splitLine: { lineStyle: { color: "rgba(255,255,255,.08)" } },
                axisLabel: { color: "rgba(237,247,243,.7)" },
            },
            series: [
                { name: "冠层覆盖", type: "line", smooth: true, data: trend.canopy, lineStyle: { color: "#2de2b6" }, areaStyle: { color: "rgba(45,226,182,.12)" } },
                { name: "开花同步", type: "line", smooth: true, data: trend.flowering, lineStyle: { color: "#ffcf5c" }, areaStyle: { color: "rgba(255,207,92,.1)" } },
                { name: "坐果指数", type: "line", smooth: true, data: trend.fruiting, lineStyle: { color: "#ff6b6b" }, areaStyle: { color: "rgba(255,107,107,.08)" } },
            ],
        });
    }

    function renderWaterChart(payload) {
        const chart = ui.safeChart("waterFertilizerChart");
        if (!chart) {
            return;
        }
        chart.setOption({
            tooltip: { trigger: "axis" },
            legend: { textStyle: { color: "#edf7f3" } },
            grid: { left: 40, right: 20, top: 46, bottom: 28 },
            xAxis: {
                type: "category",
                data: payload.zones,
                axisLabel: { color: "rgba(237,247,243,.72)" },
                axisLine: { lineStyle: { color: "rgba(255,255,255,.16)" } },
            },
            yAxis: [
                {
                    type: "value",
                    name: "m3",
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
                    name: "灌溉量",
                    type: "bar",
                    data: payload.water,
                    itemStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: "#2de2b6" },
                            { offset: 1, color: "#0f836c" },
                        ]),
                        borderRadius: [8, 8, 0, 0],
                    },
                },
                {
                    name: "施肥浓度",
                    type: "line",
                    yAxisIndex: 1,
                    smooth: true,
                    data: payload.fertilizer,
                    lineStyle: { color: "#ff6b6b" },
                    symbolSize: 8,
                },
            ],
        });
    }

    function renderTasks(tasks) {
        ui.renderStackList("droneTaskList", tasks, (task) => `
            <div class="list-card">
                <div class="list-card-top">
                    <h4>${ui.escapeHtml(task.name)}</h4>
                    <span class="status-badge ${ui.statusClass(task.status)}">${ui.escapeHtml(task.status)}</span>
                </div>
                <p>计划时间：${ui.escapeHtml(task.time)}</p>
            </div>
        `);
    }

    function renderAlerts(alerts) {
        ui.renderStackList("alertList", alerts, (alertItem) => `
            <div class="list-card">
                <div class="list-card-top">
                    <h4>${ui.escapeHtml(alertItem.title)}</h4>
                    <span class="status-badge ${ui.statusClass(alertItem.level)}">${ui.escapeHtml(alertItem.level)}级</span>
                </div>
                <p>${ui.escapeHtml(alertItem.detail)}</p>
            </div>
        `);
    }

    function setCameraStatus(text, tone = "default") {
        cameraStatus.textContent = text;
        cameraStatus.classList.remove("panel-tag-danger", "panel-tag-warning");

        if (tone === "danger") {
            cameraStatus.classList.add("panel-tag-danger");
        } else if (tone === "warning") {
            cameraStatus.classList.add("panel-tag-warning");
        }
    }

    function resetFrozenFrame(options = {}) {
        const { disablePauseButton = false } = options;

        isCameraPaused = false;
        cameraStage?.classList.remove("is-paused");

        if (cameraFreezeFrame) {
            cameraFreezeFrame.hidden = true;
            cameraFreezeFrame.width = 0;
            cameraFreezeFrame.height = 0;
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
        if (!cameraVideo || !cameraFreezeFrame || !freezeFrameContext) {
            return false;
        }

        if (
            cameraVideo.readyState < HTMLMediaElement.HAVE_CURRENT_DATA ||
            !cameraVideo.videoWidth ||
            !cameraVideo.videoHeight
        ) {
            return false;
        }

        const frameWidth = cameraVideo.videoWidth;
        const frameHeight = cameraVideo.videoHeight;
        cameraFreezeFrame.width = frameWidth;
        cameraFreezeFrame.height = frameHeight;
        freezeFrameContext.clearRect(0, 0, frameWidth, frameHeight);

        // Freeze the current frame on a canvas overlay so the paused state does not fall back to a black screen.
        freezeFrameContext.drawImage(cameraVideo, 0, 0, frameWidth, frameHeight);
        cameraFreezeFrame.hidden = false;
        return true;
    }

    function resumeCameraPlayback() {
        if (!streamRef || !cameraVideo?.srcObject) {
            resetFrozenFrame({ disablePauseButton: true });
            return;
        }

        resetFrozenFrame();
        setCameraStatus("实时采集中");
        cameraMessage.textContent = "摄像头已连接，正在显示实时视频流。";
    }

    function toggleCameraPause() {
        if (!streamRef || !cameraVideo?.srcObject) {
            resetFrozenFrame({ disablePauseButton: true });
            cameraMessage.textContent = "请先开启摄像头后再使用暂停画面。";
            return;
        }

        if (isCameraPaused) {
            resumeCameraPlayback();
            return;
        }

        if (!captureFrozenFrame()) {
            cameraMessage.textContent = "实时画面尚未就绪，请稍后再试。";
            return;
        }

        isCameraPaused = true;
        cameraStage?.classList.add("is-paused");
        pauseCameraButton.textContent = "继续播放";
        pauseCameraButton.classList.add("is-active");
        pauseCameraButton.setAttribute("aria-pressed", "true");
        setCameraStatus("画面已暂停", "warning");
        cameraMessage.textContent = "画面已冻结在当前帧，点击“继续播放”恢复实时视频。";
    }

    async function startCamera() {
        if (streamRef) {
            if (isCameraPaused) {
                resumeCameraPlayback();
            }
            return;
        }

        if (!cameraVideo || !navigator.mediaDevices?.getUserMedia) {
            setCameraStatus("当前浏览器不支持", "danger");
            cameraMessage.textContent = "当前浏览器不支持摄像头实时采集。";
            startCameraButton.disabled = true;
            stopCameraButton.disabled = true;
            resetFrozenFrame({ disablePauseButton: true });
            return;
        }

        try {
            streamRef = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                },
                audio: false,
            });
            cameraVideo.srcObject = streamRef;
            await cameraVideo.play();
            resetFrozenFrame();
            setCameraStatus("实时采集中");
            cameraMessage.textContent = "摄像头已连接，正在显示实时视频流。";
            startCameraButton.disabled = true;
            pauseCameraButton.disabled = false;
            stopCameraButton.disabled = false;
        } catch (error) {
            stopCamera();
            setCameraStatus("授权失败", "danger");
            cameraMessage.textContent = "摄像头授权失败或设备不可用，请检查浏览器权限。";
        }
    }

    function stopCamera() {
        if (streamRef) {
            streamRef.getTracks().forEach((track) => track.stop());
            streamRef = null;
        }

        if (cameraVideo) {
            cameraVideo.srcObject = null;
        }

        resetFrozenFrame({ disablePauseButton: true });
        setCameraStatus("已关闭", "danger");
        cameraMessage.textContent = "摄像头已关闭。";
        startCameraButton.disabled = false;
        stopCameraButton.disabled = true;
    }

    startCameraButton?.addEventListener("click", startCamera);
    pauseCameraButton?.addEventListener("click", toggleCameraPause);
    stopCameraButton?.addEventListener("click", stopCamera);
    window.addEventListener("beforeunload", stopCamera);

    try {
        const [overview, heatmap] = await Promise.all([
            apiClient.get("/api/dashboard/overview/"),
            apiClient.get("/api/monitoring/heatmap/"),
        ]);

        ui.renderSummaryCards("summaryCards", overview.summary_cards);
        renderTrendChart(overview.growth_trend);
        renderWaterChart(overview.water_fertilizer);
        renderTasks(overview.drone_tasks);
        renderAlerts(overview.alerts);
        ui.createOrchardMap("dashboardMap", heatmap.geojson, heatmap.map);
        startCamera();
    } catch (error) {
        alert(error.message);
    }
});
