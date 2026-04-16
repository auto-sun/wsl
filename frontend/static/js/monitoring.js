function createMonitoringGradeOption(gradeDistribution) {
    const { getGrid, getCategoryAxis, getValueAxis } = window.chartUtils;
    return {
        animationDuration: 600,
        tooltip: { trigger: "axis" },
        grid: getGrid({ left: 40, right: 26, top: 30 }),
        xAxis: getCategoryAxis(gradeDistribution.labels),
        yAxis: getValueAxis(),
        series: [
            {
                data: gradeDistribution.values,
                type: "bar",
                barWidth: 24,
                itemStyle: {
                    borderRadius: [10, 10, 0, 0],
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: "#72d8ff" },
                        { offset: 0.55, color: "#7f69ff" },
                        { offset: 1, color: "#ff5f7a" },
                    ]),
                },
            },
        ],
    };
}

function createMonitoringTrendOption(trendData) {
    const { getGrid, getLegend, getCategoryAxis, getValueAxis } = window.chartUtils;
    return {
        animationDuration: 700,
        tooltip: { trigger: "axis" },
        legend: getLegend({ right: 10 }),
        grid: getGrid({ left: 42, right: 30, top: 46 }),
        xAxis: getCategoryAxis(trendData.dates, { boundaryGap: false }),
        yAxis: [
            getValueAxis({ name: "指数" }),
            getValueAxis({ name: "墒情%", splitLine: { show: false } }),
        ],
        series: [
            {
                name: "长势指数",
                type: "line",
                smooth: true,
                data: trendData.growth_index,
                symbolSize: 7,
                lineStyle: { width: 3, color: "#50e3ff" },
                areaStyle: { color: "rgba(80, 227, 255, 0.12)" },
            },
            {
                name: "健康指数",
                type: "line",
                smooth: true,
                data: trendData.health_index,
                symbolSize: 7,
                lineStyle: { width: 3, color: "#8f7cff" },
                areaStyle: { color: "rgba(143,124,255,.08)" },
            },
            {
                name: "墒情",
                type: "bar",
                yAxisIndex: 1,
                data: trendData.moisture,
                barWidth: 16,
                itemStyle: {
                    borderRadius: [8, 8, 0, 0],
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: "#ff5f7a" },
                        { offset: 1, color: "#ae2d5d" },
                    ]),
                },
            },
        ],
    };
}

function createMonitoringNdviOption(ndviData) {
    const { getGrid, getLegend, getCategoryAxis, getValueAxis } = window.chartUtils;
    return {
        animationDuration: 700,
        tooltip: { trigger: "axis" },
        legend: getLegend({ right: 8 }),
        grid: getGrid({ left: 42, right: 28, top: 44 }),
        xAxis: getCategoryAxis(ndviData.dates, { boundaryGap: false }),
        yAxis: [
            getValueAxis({ name: "NDVI", min: 0.4, max: 1 }),
            getValueAxis({ name: "指数/覆盖率", splitLine: { show: false } }),
        ],
        series: [
            {
                name: "NDVI",
                type: "line",
                smooth: true,
                data: ndviData.ndvi,
                symbolSize: 7,
                lineStyle: { width: 3, color: "#32d1c0" },
                areaStyle: { color: "rgba(50, 209, 192, 0.12)" },
            },
            {
                name: "健康指数",
                type: "line",
                smooth: true,
                yAxisIndex: 1,
                data: ndviData.health_index,
                symbolSize: 7,
                lineStyle: { width: 3, color: "#72d8ff" },
            },
            {
                name: "冠层覆盖",
                type: "line",
                smooth: true,
                yAxisIndex: 1,
                data: ndviData.canopy_cover,
                symbolSize: 7,
                lineStyle: { width: 3, color: "#ff5f7a" },
                areaStyle: { color: "rgba(255,95,122,.08)" },
            },
        ],
    };
}

async function initMonitoringPage() {
    const { escapeHtml, renderState, renderErrorState, getAccentClass, setSelectOptions } = window.pageUtils;
    const { setChartOption } = window.chartUtils;

    const blockFilter = document.getElementById("blockFilter");
    const startDateInput = document.getElementById("startDate");
    const endDateInput = document.getElementById("endDate");
    const filterStatus = document.getElementById("monitoringFilterStatus");
    const summaryCardsNode = document.getElementById("monitoringSummaryCards");
    const futureExtensionsNode = document.getElementById("futureExtensions");
    const recordListNode = document.getElementById("inspectionRecordList");
    const droneInfoNode = document.getElementById("droneInfoCard");
    const droneStatusTag = document.getElementById("droneStatusTag");
    const applyButton = document.getElementById("applyMonitoringFilter");
    const resetButton = document.getElementById("resetMonitoringFilter");
    const monitoringShell = document.querySelector(".monitoring-shell");

    let summaryData = null;
    let heatmapData = null;
    let monitoringMap = null;
    let monitoringPopup = null;

    function formatShortDate(dateText) {
        return dateText.slice(5);
    }

    function initFilters(filters) {
        setSelectOptions(
            blockFilter,
            filters.blocks.map((item) => ({
                value: item.code,
                label: `${item.code} · ${item.name}`,
            })),
            filters.default_block || "ALL",
            [{ value: "ALL", label: "全部地块" }],
        );
        startDateInput.value = filters.default_start;
        endDateInput.value = filters.default_end;
    }

    function renderSummaryCards(cards) {
        summaryCardsNode.innerHTML = cards.map((card) => `
            <article class="monitoring-summary-card ${getAccentClass(card.accent)}">
                <div class="summary-card-label">${escapeHtml(card.label)}</div>
                <div class="monitoring-summary-main">
                    <strong>${escapeHtml(card.value)}</strong>
                    <span>${escapeHtml(card.unit || "")}</span>
                </div>
                <div class="monitoring-summary-trend">变化 ${escapeHtml(card.trend)}</div>
            </article>
        `).join("");
    }

    function renderFutureNotes(items) {
        futureExtensionsNode.innerHTML = items.map((item) => `
            <div class="future-note-item">
                <span class="future-note-title">预留扩展</span>
                <div>${escapeHtml(item)}</div>
            </div>
        `).join("");
    }

    function renderDroneInfo(droneInfo) {
        droneStatusTag.textContent = droneInfo.status;
        droneInfoNode.innerHTML = `
            <div class="drone-highlight">
                <span class="future-note-title">当前巡检任务</span>
                <strong>${escapeHtml(droneInfo.mission_name)}</strong>
                <p>${escapeHtml(droneInfo.route)}</p>
            </div>
            <div class="drone-metric-grid">
                <div class="drone-metric">
                    <span>无人机编号</span>
                    <strong>${escapeHtml(droneInfo.uav_code)}</strong>
                </div>
                <div class="drone-metric">
                    <span>飞手</span>
                    <strong>${escapeHtml(droneInfo.pilot)}</strong>
                </div>
                <div class="drone-metric">
                    <span>飞行时长</span>
                    <strong>${escapeHtml(droneInfo.flight_time)}</strong>
                </div>
                <div class="drone-metric">
                    <span>覆盖面积</span>
                    <strong>${escapeHtml(droneInfo.covered_area)}</strong>
                </div>
                <div class="drone-metric">
                    <span>挂载能力</span>
                    <strong>${escapeHtml(droneInfo.payload)}</strong>
                </div>
                <div class="drone-metric">
                    <span>后续接入</span>
                    <strong>${escapeHtml(droneInfo.next_task)}</strong>
                </div>
            </div>
        `;
    }

    function renderRecords(records) {
        if (!records.length) {
            renderState(recordListNode, "当前筛选条件下暂无巡检记录", "monitoring-empty");
            return;
        }
        recordListNode.innerHTML = records.map((record) => `
            <article class="inspection-item">
                <div class="inspection-item-header">
                    <div>
                        <h5>${escapeHtml(record.block_code)} · ${escapeHtml(record.block_name)}</h5>
                        <div class="inspection-time">${escapeHtml(record.recorded_at)}</div>
                    </div>
                    <span class="inspection-route">${escapeHtml(record.route)}</span>
                </div>
                <p>${escapeHtml(record.summary)}</p>
                <p>处理建议：${escapeHtml(record.result)}</p>
            </article>
        `).join("");
    }

    function getFilteredGeoJson(selectedBlock) {
        const features = selectedBlock === "ALL"
            ? heatmapData.geojson.features
            : heatmapData.geojson.features.filter((feature) => feature.properties.block_code === selectedBlock);

        return {
            type: "FeatureCollection",
            features,
        };
    }

    function updateMapFeatures(selectedBlock) {
        if (!monitoringMap || !monitoringMap.getSource("monitoring-heat")) {
            return;
        }
        monitoringMap.getSource("monitoring-heat").setData(getFilteredGeoJson(selectedBlock));
    }

    function initMap(mapConfig) {
        const mapNode = document.getElementById("monitoringMap");
        if (!mapNode) {
            return;
        }
        if (!window.mapboxgl) {
            renderState(mapNode, "地图组件未加载", "monitoring-empty");
            return;
        }

        mapboxgl.accessToken = "";
        monitoringMap = new mapboxgl.Map({
            container: "monitoringMap",
            center: mapConfig.center,
            zoom: mapConfig.zoom,
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

        monitoringMap.addControl(new mapboxgl.NavigationControl(), "top-right");
        monitoringPopup = new mapboxgl.Popup({
            closeButton: false,
            closeOnClick: false,
            offset: 12,
        });

        monitoringMap.on("load", () => {
            monitoringMap.addSource("monitoring-heat", {
                type: "geojson",
                data: getFilteredGeoJson(blockFilter.value || "ALL"),
            });

            monitoringMap.addLayer({
                id: "monitoring-heat-layer",
                type: "heatmap",
                source: "monitoring-heat",
                maxzoom: 16,
                paint: {
                    "heatmap-weight": ["interpolate", ["linear"], ["get", "intensity"], 0, 0, 1, 1],
                    "heatmap-intensity": 0.95,
                    "heatmap-radius": 30,
                    "heatmap-opacity": 0.78,
                    "heatmap-color": [
                        "interpolate",
                        ["linear"],
                        ["heatmap-density"],
                        0, "rgba(50,209,192,0)",
                        0.35, "#32d1c0",
                        0.65, "#7f69ff",
                        1, "#ff5f7a",
                    ],
                },
            });

            monitoringMap.addLayer({
                id: "monitoring-points",
                type: "circle",
                source: "monitoring-heat",
                paint: {
                    "circle-radius": 8,
                    "circle-color": [
                        "interpolate",
                        ["linear"],
                        ["get", "intensity"],
                        0.58, "#ff5f7a",
                        0.72, "#7f69ff",
                        0.84, "#32d1c0",
                    ],
                    "circle-stroke-width": 1.5,
                    "circle-stroke-color": "#eef8ff",
                },
            });

            monitoringMap.on("mouseenter", "monitoring-points", (event) => {
                monitoringMap.getCanvas().style.cursor = "pointer";
                const feature = event.features && event.features[0];
                if (!feature) {
                    return;
                }
                monitoringPopup
                    .setLngLat(feature.geometry.coordinates)
                    .setHTML(
                        `<strong>${escapeHtml(feature.properties.block_code)} · ${escapeHtml(feature.properties.block_name)}</strong><br>` +
                        `长势等级：${escapeHtml(feature.properties.growth_grade)}<br>` +
                        `NDVI：${escapeHtml(feature.properties.ndvi)}`,
                    )
                    .addTo(monitoringMap);
            });

            monitoringMap.on("mouseleave", "monitoring-points", () => {
                monitoringMap.getCanvas().style.cursor = "";
                monitoringPopup.remove();
            });
        });
    }

    function sliceSeriesByDate(series, startDate, endDate) {
        const selectedDates = [];
        const indexes = [];

        series.dates.forEach((dateText, index) => {
            if (dateText >= startDate && dateText <= endDate) {
                selectedDates.push(dateText);
                indexes.push(index);
            }
        });

        if (!selectedDates.length) {
            return { ...series };
        }

        const nextSeries = { dates: selectedDates.map(formatShortDate) };
        Object.keys(series).forEach((key) => {
            if (key === "dates") {
                return;
            }
            nextSeries[key] = indexes.map((index) => series[key][index]);
        });
        return nextSeries;
    }

    function filterRecords(records, selectedBlock, startDate, endDate) {
        return records.filter((record) => {
            const recordDate = record.recorded_at.slice(0, 10);
            const byBlock = selectedBlock === "ALL" || record.block_code === selectedBlock;
            const byDate = recordDate >= startDate && recordDate <= endDate;
            return byBlock && byDate;
        });
    }

    function getActiveProfile(selectedBlock) {
        if (selectedBlock === "ALL") {
            return {
                summary_cards: summaryData.summary_cards,
                grade_distribution: summaryData.grade_distribution,
                growth_trend: summaryData.growth_trend,
                ndvi_chart: summaryData.ndvi_chart,
                drone_info: summaryData.drone_info,
            };
        }
        return summaryData.block_profiles.find((item) => item.code === selectedBlock);
    }

    function updateFilterStatus(selectedBlock, startDate, endDate) {
        const blockInfo = summaryData.filters.blocks.find((item) => item.code === selectedBlock) || {};
        const blockText = selectedBlock === "ALL" ? "全部地块" : `${selectedBlock} · ${blockInfo.name || ""}`;
        filterStatus.textContent = `${blockText} / ${startDate} 至 ${endDate}`;
    }

    function renderCharts(activeProfile, startDate, endDate) {
        setChartOption(
            "growthGradeChart",
            createMonitoringGradeOption(activeProfile.grade_distribution),
            { emptyClass: "monitoring-empty", emptyText: "图表库未加载" },
        );
        setChartOption(
            "growthTrendChart",
            createMonitoringTrendOption(sliceSeriesByDate(activeProfile.growth_trend, startDate, endDate)),
            { emptyClass: "monitoring-empty", emptyText: "图表库未加载" },
        );
        setChartOption(
            "ndviChart",
            createMonitoringNdviOption(sliceSeriesByDate(activeProfile.ndvi_chart, startDate, endDate)),
            { emptyClass: "monitoring-empty", emptyText: "图表库未加载" },
        );
    }

    function applyFilters() {
        const selectedBlock = blockFilter.value || "ALL";
        let startDate = startDateInput.value || summaryData.filters.default_start;
        let endDate = endDateInput.value || summaryData.filters.default_end;

        if (startDate > endDate) {
            [startDate, endDate] = [endDate, startDate];
            startDateInput.value = startDate;
            endDateInput.value = endDate;
        }

        const activeProfile = getActiveProfile(selectedBlock);
        updateFilterStatus(selectedBlock, startDate, endDate);
        renderSummaryCards(activeProfile.summary_cards);
        renderCharts(activeProfile, startDate, endDate);
        renderDroneInfo(activeProfile.drone_info);
        renderRecords(filterRecords(summaryData.inspection_records, selectedBlock, startDate, endDate));
        updateMapFeatures(selectedBlock);
        renderFutureNotes(summaryData.future_extensions);
    }

    function bindEvents() {
        applyButton.addEventListener("click", applyFilters);
        resetButton.addEventListener("click", () => {
            blockFilter.value = summaryData.filters.default_block || "ALL";
            startDateInput.value = summaryData.filters.default_start;
            endDateInput.value = summaryData.filters.default_end;
            applyFilters();
        });
    }

    try {
        window.appUI?.setLoading(true, "正在加载长势监测数据...");
        const [summary, heatmap] = await Promise.all([
            apiClient.get("/api/monitoring/growth-summary"),
            apiClient.get("/api/monitoring/heatmap-data"),
        ]);
        summaryData = summary;
        heatmapData = heatmap;
        initFilters(summary.filters);
        bindEvents();
        initMap(heatmap.map);
        applyFilters();
        window.appUI?.setLoading(false);
    } catch (error) {
        window.appUI?.setLoading(false);
        window.appUI?.notify(error.message, "error", "长势监测加载失败");
        renderErrorState(monitoringShell, error.message, "monitoring-empty");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    initMonitoringPage().catch((error) => {
        window.appUI?.setLoading(false);
        window.appUI?.notify(error.message || "页面初始化失败", "error", "长势监测初始化失败");
    });
});
