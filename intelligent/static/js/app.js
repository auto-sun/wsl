(function () {
    function formatValue(value, unit = "") {
        return `${value}${unit || ""}`;
    }

    function escapeHtml(value) {
        return String(value)
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#39;");
    }

    function setCurrentTime() {
        const target = document.getElementById("currentTime");
        if (!target) {
            return;
        }
        const now = new Date();
        target.textContent = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}-${String(now.getDate()).padStart(2, "0")} ${String(now.getHours()).padStart(2, "0")}:${String(now.getMinutes()).padStart(2, "0")}:${String(now.getSeconds()).padStart(2, "0")}`;
    }

    function statusClass(statusText) {
        const text = String(statusText || "");
        if (["高", "告警", "离线"].some((word) => text.includes(word))) {
            return "alert";
        }
        if (["中", "待执行", "执行中", "异常"].some((word) => text.includes(word))) {
            return "warn";
        }
        return "";
    }

    function renderSummaryCards(containerId, cards) {
        const container = document.getElementById(containerId);
        if (!container) {
            return;
        }
        container.innerHTML = cards.map((card) => `
            <article class="summary-card">
                <span>${escapeHtml(card.label)}</span>
                <div class="status-number">
                    <strong>${escapeHtml(card.value)}</strong>
                    <span class="unit">${escapeHtml(card.unit || "")}</span>
                </div>
                <div class="trend">变化 ${escapeHtml(card.trend || card.delta || "--")}</div>
            </article>
        `).join("");
    }

    function renderStackList(containerId, items, formatter) {
        const container = document.getElementById(containerId);
        if (!container) {
            return;
        }
        if (!items || !items.length) {
            container.innerHTML = '<div class="empty-state">暂无数据</div>';
            return;
        }
        container.innerHTML = items.map((item) => formatter(item)).join("");
    }

    function renderTable(containerId, columns, rows) {
        const container = document.getElementById(containerId);
        if (!container) {
            return;
        }

        const head = columns.map((column) => `<th>${escapeHtml(column.label)}</th>`).join("");
        const body = rows.map((row) => `
            <tr>
                ${columns.map((column) => `<td>${column.render ? column.render(row) : escapeHtml(row[column.key] ?? "--")}</td>`).join("")}
            </tr>
        `).join("");

        container.innerHTML = `
            <table>
                <thead>
                    <tr>${head}</tr>
                </thead>
                <tbody>${body}</tbody>
            </table>
        `;
    }

    function renderTodoList(containerId, items) {
        const container = document.getElementById(containerId);
        if (!container) {
            return;
        }
        container.innerHTML = items.map((item) => `
            <div class="todo-item">
                <strong>TODO / 预留说明</strong>
                <p>${escapeHtml(item)}</p>
            </div>
        `).join("");
    }

    const FALLBACK_COLORS = ["#2de2b6", "#1da7d9", "#ffcf5c", "#ff6b6b", "#7c8cff", "#b3ff66"];

    function ensureEchartsCompatibility() {
        window.echarts = window.echarts || {};
        window.echarts.graphic = window.echarts.graphic || {};

        if (typeof window.echarts.graphic.LinearGradient !== "function") {
            window.echarts.graphic.LinearGradient = function LinearGradientStub(x0, y0, x1, y1, colorStops = []) {
                return { x0, y0, x1, y1, colorStops };
            };
        }
    }

    function normalizeColor(color, fallbackColor = FALLBACK_COLORS[0]) {
        if (!color) {
            return fallbackColor;
        }
        if (typeof color === "string") {
            return color;
        }
        if (Array.isArray(color) && color.length) {
            return normalizeColor(color[0], fallbackColor);
        }
        if (typeof color === "object") {
            const stops = color.colorStops || color.stops;
            if (Array.isArray(stops) && stops.length) {
                const firstStop = stops[0];
                return normalizeColor(firstStop?.color, fallbackColor);
            }
        }
        return fallbackColor;
    }

    function getSeriesColor(series, index, option = {}) {
        const paletteColor = normalizeColor(option.color?.[index], FALLBACK_COLORS[index % FALLBACK_COLORS.length]);
        return normalizeColor(
            series.lineStyle?.color ||
            series.itemStyle?.color ||
            series.areaStyle?.color ||
            series.color,
            paletteColor,
        );
    }

    function getNumericValue(item) {
        if (typeof item === "number") {
            return item;
        }
        if (item && typeof item === "object" && "value" in item) {
            return Number(item.value) || 0;
        }
        return Number(item) || 0;
    }

    function getVizDimensions(target, minHeight = 320) {
        return {
            width: Math.max(target.clientWidth || 0, 320),
            height: Math.max(target.clientHeight || 0, minHeight),
        };
    }

    function buildFallbackLegend(seriesList, option) {
        const visibleSeries = (seriesList || []).filter((series) => series?.name);
        if (!visibleSeries.length) {
            return "";
        }
        return `
            <div class="fallback-legend">
                ${visibleSeries.map((series, index) => `
                    <span class="fallback-legend-item">
                        <i class="fallback-legend-dot" style="background:${escapeHtml(getSeriesColor(series, index, option))}"></i>
                        ${escapeHtml(series.name)}
                    </span>
                `).join("")}
            </div>
        `;
    }

    function renderFallbackCartesianChart(target, option) {
        const seriesList = (option.series || []).filter((series) => ["line", "bar"].includes(series.type));
        if (!seriesList.length) {
            target.innerHTML = '<div class="empty-state">暂无图表数据</div>';
            return;
        }

        const xAxis = Array.isArray(option.xAxis) ? option.xAxis[0] : option.xAxis;
        const categories = xAxis?.data || seriesList[0].data.map((_, index) => `${index + 1}`);
        const { width, height } = getVizDimensions(target, target.classList.contains("chart-tall") ? 430 : 320);
        const padding = { top: 22, right: 20, bottom: 54, left: 44 };
        const plotWidth = Math.max(width - padding.left - padding.right, 120);
        const plotHeight = Math.max(height - padding.top - padding.bottom, 120);
        const categoryBand = categories.length ? plotWidth / categories.length : plotWidth;
        const lineCenterOffset = categoryBand / 2;
        const axisMaxMap = {};

        seriesList.forEach((series) => {
            const axisIndex = series.yAxisIndex || 0;
            const values = (series.data || []).map(getNumericValue);
            axisMaxMap[axisIndex] = Math.max(axisMaxMap[axisIndex] || 1, ...values, 1);
        });

        const barSeries = seriesList.filter((series) => series.type === "bar");
        const lineSeries = seriesList.filter((series) => series.type === "line");
        const barWidth = barSeries.length ? (categoryBand * 0.66) / barSeries.length : 0;
        const gridLines = Array.from({ length: 5 }, (_, index) => {
            const y = padding.top + (plotHeight / 4) * index;
            return `<line x1="${padding.left}" y1="${y}" x2="${padding.left + plotWidth}" y2="${y}" class="fallback-grid-line"></line>`;
        }).join("");

        const barShapes = barSeries.map((series, seriesIndex) => {
            const color = getSeriesColor(series, seriesIndex, option);
            const axisMax = axisMaxMap[series.yAxisIndex || 0] || 1;
            return (series.data || []).map((item, itemIndex) => {
                const value = getNumericValue(item);
                const safeHeight = axisMax ? (value / axisMax) * plotHeight : 0;
                const x = padding.left + categoryBand * itemIndex + (categoryBand - barWidth * barSeries.length) / 2 + seriesIndex * barWidth;
                const y = padding.top + plotHeight - safeHeight;
                const widthValue = Math.max(barWidth - 6, 10);
                return `
                    <rect
                        x="${x + 3}"
                        y="${y}"
                        width="${widthValue}"
                        height="${safeHeight}"
                        rx="8"
                        fill="${escapeHtml(color)}"
                        opacity="0.86"
                    ></rect>
                `;
            }).join("");
        }).join("");

        const lineShapes = lineSeries.map((series, seriesIndex) => {
            const color = getSeriesColor(series, barSeries.length + seriesIndex, option);
            const axisMax = axisMaxMap[series.yAxisIndex || 0] || 1;
            const points = (series.data || []).map((item, itemIndex) => {
                const value = getNumericValue(item);
                const x = padding.left + categoryBand * itemIndex + lineCenterOffset;
                const y = padding.top + plotHeight - (value / axisMax) * plotHeight;
                return { x, y, value };
            });
            const polylinePoints = points.map((point) => `${point.x},${point.y}`).join(" ");
            const markers = points.map((point) => `
                <circle cx="${point.x}" cy="${point.y}" r="4" fill="${escapeHtml(color)}" stroke="#071b22" stroke-width="2"></circle>
            `).join("");
            return `
                <polyline
                    points="${polylinePoints}"
                    fill="none"
                    stroke="${escapeHtml(color)}"
                    stroke-width="3"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                ></polyline>
                ${markers}
            `;
        }).join("");

        const xLabels = categories.map((label, index) => {
            const x = padding.left + categoryBand * index + lineCenterOffset;
            return `<text x="${x}" y="${height - 18}" text-anchor="middle" class="fallback-axis-label">${escapeHtml(label)}</text>`;
        }).join("");

        target.innerHTML = `
            <div class="fallback-chart-shell">
                <div class="fallback-viz-meta">
                    <span class="fallback-viz-badge">本地图表渲染</span>
                    ${buildFallbackLegend(seriesList, option)}
                </div>
                <svg class="fallback-chart-svg" viewBox="0 0 ${width} ${height}" aria-label="图表降级渲染">
                    ${gridLines}
                    <line x1="${padding.left}" y1="${padding.top + plotHeight}" x2="${padding.left + plotWidth}" y2="${padding.top + plotHeight}" class="fallback-axis-line"></line>
                    ${barShapes}
                    ${lineShapes}
                    ${xLabels}
                </svg>
            </div>
        `;
    }

    function renderFallbackPieChart(target, option) {
        const series = option.series?.[0];
        const items = series?.data || [];
        if (!items.length) {
            target.innerHTML = '<div class="empty-state">暂无图表数据</div>';
            return;
        }

        const total = items.reduce((sum, item) => sum + getNumericValue(item.value ?? item), 0) || 1;
        let offset = 0;
        const gradient = items.map((item, index) => {
            const color = normalizeColor(
                item.itemStyle?.color || option.color?.[index],
                FALLBACK_COLORS[index % FALLBACK_COLORS.length],
            );
            const value = getNumericValue(item.value ?? item);
            const start = offset;
            offset += (value / total) * 100;
            return `${color} ${start}% ${offset}%`;
        }).join(", ");

        target.innerHTML = `
            <div class="fallback-chart-shell">
                <div class="fallback-viz-meta">
                    <span class="fallback-viz-badge">本地图表渲染</span>
                    ${buildFallbackLegend(items.map((item) => ({ name: item.name })), { color: option.color || FALLBACK_COLORS })}
                </div>
                <div class="fallback-donut-layout">
                    <div class="fallback-donut" style="background: conic-gradient(${gradient});">
                        <div class="fallback-donut-core">
                            <strong>${escapeHtml(total)}</strong>
                            <span>设备总计</span>
                        </div>
                    </div>
                    <div class="fallback-pie-list">
                        ${items.map((item, index) => {
                            const color = normalizeColor(option.color?.[index], FALLBACK_COLORS[index % FALLBACK_COLORS.length]);
                            const value = getNumericValue(item.value ?? item);
                            return `
                                <div class="fallback-pie-item">
                                    <span class="fallback-pie-label">
                                        <i class="fallback-legend-dot" style="background:${escapeHtml(color)}"></i>
                                        ${escapeHtml(item.name)}
                                    </span>
                                    <strong>${escapeHtml(value)}</strong>
                                </div>
                            `;
                        }).join("")}
                    </div>
                </div>
            </div>
        `;
    }

    function renderFallbackRadarChart(target, option) {
        const radar = option.radar || {};
        const indicators = radar.indicator || [];
        const seriesValues = option.series?.[0]?.data?.[0]?.value || [];

        if (!indicators.length || !seriesValues.length) {
            target.innerHTML = '<div class="empty-state">暂无图表数据</div>';
            return;
        }

        const { width, height } = getVizDimensions(target, target.classList.contains("chart-tall") ? 430 : 320);
        const cx = width / 2;
        const cy = height / 2 + 8;
        const radius = Math.min(width, height) * 0.28;
        const levels = [0.25, 0.5, 0.75, 1];
        const angleStep = (Math.PI * 2) / indicators.length;
        const seriesColor = getSeriesColor(option.series[0], 0, option);

        function getPoint(index, ratio) {
            const angle = -Math.PI / 2 + angleStep * index;
            return {
                x: cx + Math.cos(angle) * radius * ratio,
                y: cy + Math.sin(angle) * radius * ratio,
            };
        }

        const gridPolygons = levels.map((level) => {
            const points = indicators.map((_, index) => {
                const point = getPoint(index, level);
                return `${point.x},${point.y}`;
            }).join(" ");
            return `<polygon points="${points}" class="fallback-radar-grid"></polygon>`;
        }).join("");

        const axes = indicators.map((indicator, index) => {
            const point = getPoint(index, 1);
            const labelPoint = getPoint(index, 1.18);
            return `
                <line x1="${cx}" y1="${cy}" x2="${point.x}" y2="${point.y}" class="fallback-radar-axis"></line>
                <text x="${labelPoint.x}" y="${labelPoint.y}" text-anchor="middle" class="fallback-axis-label">${escapeHtml(indicator.name)}</text>
            `;
        }).join("");

        const dataPoints = indicators.map((indicator, index) => {
            const max = indicator.max || 100;
            const ratio = Math.max(0, Math.min(1, getNumericValue(seriesValues[index]) / max));
            const point = getPoint(index, ratio);
            return `${point.x},${point.y}`;
        }).join(" ");

        target.innerHTML = `
            <div class="fallback-chart-shell">
                <div class="fallback-viz-meta">
                    <span class="fallback-viz-badge">本地图表渲染</span>
                    ${buildFallbackLegend([{ name: "策略权重" }], { color: [seriesColor] })}
                </div>
                <svg class="fallback-chart-svg" viewBox="0 0 ${width} ${height}" aria-label="雷达图降级渲染">
                    ${gridPolygons}
                    ${axes}
                    <polygon points="${dataPoints}" fill="${escapeHtml(seriesColor)}" fill-opacity="0.18" stroke="${escapeHtml(seriesColor)}" stroke-width="3"></polygon>
                </svg>
            </div>
        `;
    }

    function renderFallbackChart(target, option) {
        const series = option?.series || [];
        const chartTypes = new Set(series.map((item) => item.type));

        if (chartTypes.has("pie")) {
            renderFallbackPieChart(target, option);
            return;
        }

        if (chartTypes.has("radar")) {
            renderFallbackRadarChart(target, option);
            return;
        }

        renderFallbackCartesianChart(target, option);
    }

    function createFallbackChart(target) {
        return {
            option: null,
            setOption(option) {
                this.option = option;
                renderFallbackChart(target, option);
            },
            resize() {
                if (this.option) {
                    renderFallbackChart(target, this.option);
                }
            },
            dispose() {
                target.innerHTML = "";
                this.option = null;
            },
        };
    }

    function safeChart(containerId) {
        const target = document.getElementById(containerId);
        if (!target) {
            return null;
        }
        if (!window.echarts || typeof window.echarts.init !== "function") {
            return createFallbackChart(target);
        }
        try {
            return echarts.init(target);
        } catch (error) {
            return createFallbackChart(target);
        }
    }

    function createPopupHtml(properties) {
        return `
            <div style="min-width: 160px;">
                <strong>${escapeHtml(properties.block_code || "地块")}</strong>
                <div style="margin-top: 8px; color: rgba(237,247,243,.78); font-size: 13px;">
                    长势指数：${escapeHtml(properties.vigor)}<br>
                    墒情：${escapeHtml(properties.moisture)}%<br>
                    温度：${escapeHtml(properties.temperature)}℃
                </div>
            </div>
        `;
    }

    function createOrchardMap(containerId, geojson, options = {}) {
        const target = document.getElementById(containerId);
        if (!target) {
            return null;
        }

        const features = geojson?.features || [];
        const preferMapbox = options.preferMapbox === true;

        function renderFallbackMap() {
            if (!features.length) {
                target.innerHTML = '<div class="empty-state">暂无地图数据</div>';
                return null;
            }

            const { width, height } = getVizDimensions(target, target.classList.contains("map-tall") ? 430 : 320);
            const stageHeight = Math.max(height - 110, 240);
            const padding = 44;
            const coordinates = features.map((feature) => feature.geometry?.coordinates || [0, 0]);
            const lngValues = coordinates.map((item) => item[0]);
            const latValues = coordinates.map((item) => item[1]);
            const minLng = Math.min(...lngValues);
            const maxLng = Math.max(...lngValues);
            const minLat = Math.min(...latValues);
            const maxLat = Math.max(...latValues);
            const spanLng = Math.max(maxLng - minLng, 0.0001);
            const spanLat = Math.max(maxLat - minLat, 0.0001);
            const plotWidth = width - padding * 2;
            const plotHeight = stageHeight - padding * 2;

            function projectPoint(coordinate) {
                const [lng, lat] = coordinate;
                return {
                    x: padding + ((lng - minLng) / spanLng) * plotWidth,
                    y: stageHeight - padding - ((lat - minLat) / spanLat) * plotHeight,
                };
            }

            const gridLines = Array.from({ length: 5 }, (_, index) => {
                const y = padding + (plotHeight / 4) * index;
                const x = padding + (plotWidth / 4) * index;
                return `
                    <line x1="${padding}" y1="${y}" x2="${padding + plotWidth}" y2="${y}" class="fallback-grid-line"></line>
                    <line x1="${x}" y1="${padding}" x2="${x}" y2="${padding + plotHeight}" class="fallback-grid-line"></line>
                `;
            }).join("");

            const pointMarks = features.map((feature) => {
                const point = projectPoint(feature.geometry.coordinates);
                const intensity = Number(feature.properties?.intensity || feature.properties?.vigor || 0);
                const color = intensity >= 0.8 ? "#2de2b6" : intensity >= 0.74 ? "#ffcf5c" : "#ff6b6b";
                const radius = 7 + Math.max(0, intensity - 0.65) * 18;
                return `
                    <g>
                        <circle cx="${point.x}" cy="${point.y}" r="${radius + 7}" fill="${color}" opacity="0.12"></circle>
                        <circle cx="${point.x}" cy="${point.y}" r="${radius}" fill="${color}" stroke="#d8fff1" stroke-width="1.5">
                            <title>${escapeHtml(feature.properties?.block_code || "地块")} 长势 ${escapeHtml(feature.properties?.vigor)} 墒情 ${escapeHtml(feature.properties?.moisture)}%</title>
                        </circle>
                        <text x="${point.x}" y="${point.y - radius - 10}" text-anchor="middle" class="fallback-axis-label">${escapeHtml(feature.properties?.block_code || "--")}</text>
                    </g>
                `;
            }).join("");

            target.innerHTML = `
                <div class="fallback-map-shell">
                    <div class="fallback-viz-meta">
                        <span class="fallback-viz-badge">本地地图渲染</span>
                        <span class="fallback-map-note">已切换为离线地块热区视图，不依赖在线底图</span>
                    </div>
                    <div class="fallback-map-stage">
                        <svg class="fallback-map-svg" viewBox="0 0 ${width} ${stageHeight}" aria-label="园区地块分布图">
                            ${gridLines}
                            ${pointMarks}
                        </svg>
                    </div>
                    <div class="fallback-map-list">
                        ${features.map((feature) => `
                            <article class="fallback-map-card">
                                <strong>${escapeHtml(feature.properties?.block_code || "--")}</strong>
                                <span>长势 ${escapeHtml(feature.properties?.vigor)}</span>
                                <span>墒情 ${escapeHtml(feature.properties?.moisture)}%</span>
                                <span>温度 ${escapeHtml(feature.properties?.temperature)}℃</span>
                            </article>
                        `).join("")}
                    </div>
                </div>
            `;

            return {
                resize() {
                    renderFallbackMap();
                },
            };
        }

        // Default to the local orchard renderer so the dashboard remains usable
        // even when CDN, WebGL, or external map resources are unreliable.
        if (!preferMapbox || !window.mapboxgl) {
            return renderFallbackMap();
        }

        let map = null;

        try {
            map = new mapboxgl.Map({
                container: containerId,
                center: options.center || [107.3662, 22.4011],
                zoom: options.zoom || 13.5,
                style: {
                    version: 8,
                    sources: {},
                    layers: [
                        {
                            id: "orchard-background",
                            type: "background",
                            paint: {
                                "background-color": "#071b22",
                            },
                        },
                    ],
                },
            });
        } catch (error) {
            return renderFallbackMap();
        }

        map.addControl(new mapboxgl.NavigationControl({ visualizePitch: false }), "top-right");

        map.on("load", () => {
            if (!geojson) {
                return;
            }

            map.addSource("orchard-heat-source", {
                type: "geojson",
                data: geojson,
            });

            map.addLayer({
                id: "orchard-heat-layer",
                type: "heatmap",
                source: "orchard-heat-source",
                maxzoom: 16,
                paint: {
                    "heatmap-weight": ["interpolate", ["linear"], ["get", "intensity"], 0, 0, 1, 1],
                    "heatmap-intensity": 0.8,
                    "heatmap-radius": 28,
                    "heatmap-opacity": 0.72,
                    "heatmap-color": [
                        "interpolate",
                        ["linear"],
                        ["heatmap-density"],
                        0, "rgba(45, 226, 182, 0)",
                        0.3, "#2de2b6",
                        0.6, "#ffcf5c",
                        1, "#ff6b6b",
                    ],
                },
            });

            map.addLayer({
                id: "orchard-point-layer",
                type: "circle",
                source: "orchard-heat-source",
                paint: {
                    "circle-radius": [
                        "interpolate",
                        ["linear"],
                        ["zoom"],
                        10, 6,
                        15, 11,
                    ],
                    "circle-color": [
                        "interpolate",
                        ["linear"],
                        ["get", "intensity"],
                        0.65, "#ff6b6b",
                        0.8, "#ffcf5c",
                        1, "#2de2b6",
                    ],
                    "circle-stroke-width": 1.5,
                    "circle-stroke-color": "#d8fff1",
                    "circle-opacity": 0.92,
                },
            });

            const popup = new mapboxgl.Popup({
                closeButton: false,
                closeOnClick: false,
                offset: 12,
            });

            map.on("mouseenter", "orchard-point-layer", (event) => {
                map.getCanvas().style.cursor = "pointer";
                const feature = event.features?.[0];
                if (!feature) {
                    return;
                }
                popup
                    .setLngLat(feature.geometry.coordinates)
                    .setHTML(createPopupHtml(feature.properties))
                    .addTo(map);
            });

            map.on("mouseleave", "orchard-point-layer", () => {
                map.getCanvas().style.cursor = "";
                popup.remove();
            });
        });

        return map;
    }

    ensureEchartsCompatibility();

    function bindLogout() {
        const button = document.getElementById("logoutButton");
        if (!button || !window.apiClient) {
            return;
        }
        button.addEventListener("click", async () => {
            try {
                const data = await apiClient.postJson("/api/auth/logout/", {});
                window.location.href = data.redirect || "/login/";
            } catch (error) {
                alert(error.message);
            }
        });
    }

    function bindFullscreenButton() {
        const button = document.getElementById("fullscreenButton");
        if (!button) {
            return;
        }

        function getFullscreenElement() {
            return document.fullscreenElement || document.webkitFullscreenElement || null;
        }

        function updateFullscreenButton() {
            const isFullscreen = Boolean(getFullscreenElement());
            button.textContent = isFullscreen ? "退出全屏" : "进入全屏";
            button.setAttribute("aria-pressed", isFullscreen ? "true" : "false");
        }

        async function requestFullscreen(target) {
            if (typeof target.requestFullscreen === "function") {
                await target.requestFullscreen();
                return;
            }
            if (typeof target.webkitRequestFullscreen === "function") {
                target.webkitRequestFullscreen();
                return;
            }
            throw new Error("当前浏览器不支持全屏模式。");
        }

        async function exitFullscreen() {
            if (typeof document.exitFullscreen === "function") {
                await document.exitFullscreen();
                return;
            }
            if (typeof document.webkitExitFullscreen === "function") {
                document.webkitExitFullscreen();
                return;
            }
            throw new Error("当前浏览器不支持退出全屏。");
        }

        const fullscreenEnabled = Boolean(
            document.fullscreenEnabled ||
            document.webkitFullscreenEnabled ||
            document.documentElement.requestFullscreen ||
            document.documentElement.webkitRequestFullscreen
        );

        if (!fullscreenEnabled) {
            button.disabled = true;
            button.textContent = "全屏不可用";
            return;
        }

        button.addEventListener("click", async () => {
            try {
                if (getFullscreenElement()) {
                    await exitFullscreen();
                } else {
                    await requestFullscreen(document.documentElement);
                }
            } catch (error) {
                window.alert(error.message || "切换全屏失败，请检查浏览器权限。");
            } finally {
                updateFullscreenButton();
            }
        });

        document.addEventListener("fullscreenchange", updateFullscreenButton);
        document.addEventListener("webkitfullscreenchange", updateFullscreenButton);
        updateFullscreenButton();
    }

    window.SmartAgriUI = {
        escapeHtml,
        formatValue,
        renderSummaryCards,
        renderStackList,
        renderTable,
        renderTodoList,
        safeChart,
        createOrchardMap,
        statusClass,
    };

    document.addEventListener("DOMContentLoaded", () => {
        setCurrentTime();
        window.setInterval(setCurrentTime, 1000);
        bindFullscreenButton();
        bindLogout();
    });
})();
