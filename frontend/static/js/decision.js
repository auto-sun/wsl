function createDecisionGradeOption(distribution) {
    const { getLegend } = window.chartUtils;
    return {
        animationDuration: 600,
        tooltip: { trigger: "item" },
        legend: getLegend({ bottom: 6 }),
        series: [
            {
                type: "pie",
                radius: ["42%", "68%"],
                center: ["50%", "45%"],
                data: distribution.labels.map((label, index) => ({
                    name: label,
                    value: distribution.values[index],
                })),
                label: { color: "#eef8ff" },
                itemStyle: {
                    borderColor: "#081723",
                    borderWidth: 4,
                },
                color: ["#32d1c0", "#72d8ff", "#ff5f7a"],
            },
        ],
    };
}

async function initDecisionPage() {
    const { escapeHtml, renderState, renderErrorState, setButtonLoading } = window.pageUtils;
    const { setChartOption } = window.chartUtils;

    const blockSelectButton = document.getElementById("decisionBlockSelectButton");
    const blockSelectMenu = document.getElementById("decisionBlockSelectMenu");
    const generateButton = document.getElementById("generatePlanButton");
    const dispatchButton = document.getElementById("dispatchPlanButton");
    const summaryNode = document.getElementById("decisionSummary");
    const metricsNode = document.getElementById("planMetrics");
    const statusTag = document.getElementById("planStatusTag");
    const gradeTag = document.getElementById("planGradeTag");
    const historyNode = document.getElementById("decisionHistoryTable");
    const futureNode = document.getElementById("futureExtensions");
    const dispatchPlaceholderNode = document.getElementById("dispatchPlaceholder");
    const decisionShell = document.querySelector(".decision-shell");

    let plansPayload = null;
    let selectedBlock = "";
    let decisionMap = null;
    let decisionPopup = null;
    let blockOptions = [];

    function getActivePlan() {
        if (!plansPayload || !plansPayload.plans.length) {
            return null;
        }
        return plansPayload.plans.find((item) => item.block_code === selectedBlock) || plansPayload.plans[0];
    }

    function updateBlockOptions(blocks) {
        blockOptions = blocks.map((item) => ({
            value: item.code,
            label: `${item.code} · ${item.name}`,
        }));
        renderBlockDropdown();
    }

    function getSelectedBlockLabel() {
        const selectedOption = blockOptions.find((item) => item.value === selectedBlock);
        return selectedOption ? selectedOption.label : "请选择地块";
    }

    function closeBlockDropdown() {
        blockSelectMenu?.classList.remove("is-open");
        blockSelectButton?.setAttribute("aria-expanded", "false");
    }

    function toggleBlockDropdown() {
        const isOpen = blockSelectMenu?.classList.contains("is-open");
        blockSelectMenu?.classList.toggle("is-open", !isOpen);
        blockSelectButton?.setAttribute("aria-expanded", String(!isOpen));
    }

    function setSelectedBlock(value) {
        selectedBlock = value;
        renderBlockDropdown();
        render();
    }

    function renderBlockDropdown() {
        if (!blockSelectButton || !blockSelectMenu) {
            return;
        }
        blockSelectButton.textContent = getSelectedBlockLabel();
        blockSelectMenu.innerHTML = blockOptions.map((item) => `
            <button
                type="button"
                class="decision-select-option ${item.value === selectedBlock ? "is-active" : ""}"
                data-value="${escapeHtml(item.value)}"
                role="option"
                aria-selected="${item.value === selectedBlock ? "true" : "false"}"
            >
                ${escapeHtml(item.label)}
            </button>
        `).join("");
    }

    function setStatusTag(status) {
        statusTag.textContent = status;
    }

    function setGradeTag(grade) {
        gradeTag.className = "grade-badge";
        if (grade === "A") {
            gradeTag.classList.add("grade-a");
        } else if (grade === "B") {
            gradeTag.classList.add("grade-b");
        } else if (grade === "C") {
            gradeTag.classList.add("grade-c");
        } else {
            gradeTag.classList.add("grade-neutral");
        }
        gradeTag.textContent = `处方 ${grade}级`;
    }

    function renderSummary(plan) {
        summaryNode.innerHTML = `
            <div class="summary-card">
                <h5>${escapeHtml(plan.block_code)} · ${escapeHtml(plan.block_name)}</h5>
                <p>${escapeHtml(plan.growth_summary)}</p>
            </div>
            <div class="summary-card">
                <h5>风险摘要</h5>
                <p>${escapeHtml(plan.risk_summary)}</p>
            </div>
            <div class="summary-card">
                <h5>控制建议</h5>
                <p>${escapeHtml(plan.control_hint)}</p>
            </div>
        `;
    }

    function renderMetrics(plan) {
        metricsNode.innerHTML = `
            <div class="metric-card">
                <span>建议灌溉量</span>
                <strong>${escapeHtml(plan.irrigation_amount)} m3</strong>
            </div>
            <div class="metric-card">
                <span>建议施肥量</span>
                <strong>${escapeHtml(plan.fertilizer_amount)} kg/亩</strong>
            </div>
            <div class="metric-card">
                <span>执行时段建议</span>
                <strong>${escapeHtml(plan.execution_window)}</strong>
            </div>
            <div class="metric-card">
                <span>肥液配方</span>
                <strong>${escapeHtml(plan.fertilizer_formula)}</strong>
            </div>
        `;
    }

    function renderHistory(rows) {
        const filteredRows = rows.filter((row) => row.block_code === selectedBlock);
        const targetRows = filteredRows.length ? filteredRows : rows;
        if (!targetRows.length) {
            renderState(historyNode, "当前暂无历史策略记录", "decision-empty");
            return;
        }

        historyNode.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>策略编号</th>
                        <th>地块</th>
                        <th>处方等级</th>
                        <th>灌溉量</th>
                        <th>施肥量</th>
                        <th>状态</th>
                        <th>生成时间</th>
                    </tr>
                </thead>
                <tbody>
                    ${targetRows.map((row) => `
                        <tr>
                            <td>${escapeHtml(row.plan_code)}</td>
                            <td>${escapeHtml(row.block_code)}</td>
                            <td>${escapeHtml(row.prescription_grade)}级</td>
                            <td>${escapeHtml(row.irrigation_amount)} m3</td>
                            <td>${escapeHtml(row.fertilizer_amount)} kg/亩</td>
                            <td><span class="status-tag ${row.status.includes("已下发") ? "status-ready" : "status-pending"}">${escapeHtml(row.status)}</span></td>
                            <td>${escapeHtml(row.created_at)}</td>
                        </tr>
                    `).join("")}
                </tbody>
            </table>
        `;
    }

    function renderFuture(items, placeholder) {
        dispatchPlaceholderNode.innerHTML = `
            <h5>下发策略按钮说明</h5>
            <p>${escapeHtml(placeholder.message)}</p>
            <p>预留对接对象：${escapeHtml(placeholder.controller)}、${escapeHtml(placeholder.executor)}。</p>
        `;
        futureNode.innerHTML = items.map((item) => `
            <div class="future-item">
                <span>预留接口</span>
                <p>${escapeHtml(item)}</p>
            </div>
        `).join("");
    }

    function renderGradeChart(distribution) {
        setChartOption(
            "gradeDistributionChart",
            createDecisionGradeOption(distribution),
            { emptyClass: "decision-empty", emptyText: "图表组件未加载" },
        );
    }

    function updateMapHighlight() {
        if (!decisionMap || !decisionMap.getSource("decision-blocks")) {
            return;
        }
        decisionMap.getSource("decision-blocks").setData(plansPayload.map.geojson);
        if (decisionMap.getLayer("decision-highlight")) {
            decisionMap.setFilter("decision-highlight", ["==", ["get", "block_code"], selectedBlock]);
        }
    }

    function initMap(mapData) {
        const mapNode = document.getElementById("decisionMap");
        if (!mapNode) {
            return;
        }
        if (!window.mapboxgl) {
            renderState(mapNode, "地图组件未加载", "decision-empty");
            return;
        }

        mapboxgl.accessToken = "";
        decisionMap = new mapboxgl.Map({
            container: "decisionMap",
            center: mapData.center,
            zoom: mapData.zoom,
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

        decisionMap.addControl(new mapboxgl.NavigationControl(), "top-right");
        decisionPopup = new mapboxgl.Popup({
            closeButton: false,
            closeOnClick: false,
            offset: 12,
        });

        decisionMap.on("load", () => {
            decisionMap.addSource("decision-blocks", {
                type: "geojson",
                data: mapData.geojson,
            });

            decisionMap.addLayer({
                id: "decision-fill",
                type: "fill",
                source: "decision-blocks",
                paint: {
                    "fill-color": [
                        "match",
                        ["get", "grade"],
                        "A", "#32d1c0",
                        "B", "#72d8ff",
                        "C", "#ff5f7a",
                        "#7f69ff",
                    ],
                    "fill-opacity": 0.32,
                },
            });

            decisionMap.addLayer({
                id: "decision-line",
                type: "line",
                source: "decision-blocks",
                paint: {
                    "line-color": "#eef8ff",
                    "line-width": 1.5,
                    "line-opacity": 0.7,
                },
            });

            decisionMap.addLayer({
                id: "decision-highlight",
                type: "line",
                source: "decision-blocks",
                paint: {
                    "line-color": "#ffffff",
                    "line-width": 3,
                    "line-opacity": 0.95,
                },
                filter: ["==", ["get", "block_code"], selectedBlock],
            });

            decisionMap.on("mouseenter", "decision-fill", (event) => {
                decisionMap.getCanvas().style.cursor = "pointer";
                const feature = event.features && event.features[0];
                if (!feature) {
                    return;
                }
                const center = feature.geometry.coordinates[0][0];
                decisionPopup
                    .setLngLat(center)
                    .setHTML(
                        `<strong>${escapeHtml(feature.properties.block_code)} · ${escapeHtml(feature.properties.block_name)}</strong><br>` +
                        `处方等级：${escapeHtml(feature.properties.grade)}级<br>` +
                        `灌溉量：${escapeHtml(feature.properties.irrigation)} m3<br>` +
                        `施肥量：${escapeHtml(feature.properties.fertilizer)} kg/亩`,
                    )
                    .addTo(decisionMap);
            });

            decisionMap.on("mouseleave", "decision-fill", () => {
                decisionMap.getCanvas().style.cursor = "";
                decisionPopup.remove();
            });
        });
    }

    function render() {
        if (!plansPayload) {
            return;
        }
        const plan = getActivePlan();
        if (!plan) {
            renderState(summaryNode, "当前暂无策略数据", "decision-empty");
            return;
        }
        setStatusTag(plan.status);
        setGradeTag(plan.prescription_grade);
        renderSummary(plan);
        renderMetrics(plan);
        renderHistory(plansPayload.history);
        renderFuture(plansPayload.future_extensions, plansPayload.dispatch_placeholder);
        renderGradeChart(plansPayload.grade_distribution);
        updateMapHighlight();
    }

    async function loadPlans() {
        window.appUI?.setLoading(true, "正在加载水肥处方策略...");
        plansPayload = await apiClient.get("/api/decision/plans");
        if (!selectedBlock || !plansPayload.plans.some((item) => item.block_code === selectedBlock)) {
            selectedBlock = plansPayload.selected_block;
        }
        updateBlockOptions(plansPayload.blocks);
        render();
        if (!decisionMap) {
            initMap(plansPayload.map);
        }
        window.appUI?.setLoading(false);
    }

    blockSelectButton?.addEventListener("click", toggleBlockDropdown);

    blockSelectMenu?.addEventListener("click", (event) => {
        const optionButton = event.target.closest(".decision-select-option");
        if (!optionButton) {
            return;
        }
        setSelectedBlock(optionButton.dataset.value);
        closeBlockDropdown();
    });

    document.addEventListener("click", (event) => {
        if (!event.target.closest(".decision-select-wrap")) {
            closeBlockDropdown();
        }
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeBlockDropdown();
        }
    });

    generateButton.addEventListener("click", async () => {
        setButtonLoading(generateButton, true, "生成中...");
        try {
            window.appUI?.setLoading(true, `正在为 ${selectedBlock} 生成新策略...`);
            const data = await apiClient.postJson("/api/decision/generate", {
                block_code: selectedBlock,
            });
            plansPayload = data.plans_payload;
            render();
            window.appUI?.notify(`${selectedBlock} 的新策略已生成，当前结果为 mock 决策输出。`, "success", "策略生成完成");
        } catch (error) {
            window.appUI?.notify(error.message, "error", "策略生成失败");
        } finally {
            window.appUI?.setLoading(false);
            setButtonLoading(generateButton, false);
        }
    });

    dispatchButton.addEventListener("click", async () => {
        const activePlan = getActivePlan();
        if (!activePlan) {
            return;
        }
        setButtonLoading(dispatchButton, true, "下发中...");
        try {
            window.appUI?.setLoading(true, `正在下发 ${activePlan.plan_code} 策略预览...`);
            const data = await apiClient.postJson("/api/decision/dispatch", {
                plan_code: activePlan.plan_code,
            });
            plansPayload = data.plans_payload;
            render();
            window.appUI?.notify("策略已进入下发预留状态，当前未连接真实控制系统。", "success", "策略下发占位成功");
        } catch (error) {
            window.appUI?.notify(error.message, "error", "策略下发失败");
        } finally {
            window.appUI?.setLoading(false);
            setButtonLoading(dispatchButton, false);
        }
    });

    try {
        await loadPlans();
    } catch (error) {
        window.appUI?.setLoading(false);
        window.appUI?.notify(error.message, "error", "策略数据加载失败");
        renderErrorState(decisionShell, error.message, "decision-empty");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    initDecisionPage().catch((error) => {
        window.appUI?.setLoading(false);
        window.appUI?.notify(error.message || "页面初始化失败", "error", "策略页初始化失败");
    });
});
