(function () {
    const chartRegistry = new Map();

    function getGrid(overrides = {}) {
        return {
            left: 42,
            right: 28,
            top: 46,
            bottom: 28,
            ...overrides,
        };
    }

    function getLegend(overrides = {}) {
        return {
            textStyle: { color: "rgba(236,247,255,.72)" },
            ...overrides,
        };
    }

    function getCategoryAxis(data, overrides = {}) {
        return {
            type: "category",
            data,
            axisLine: { lineStyle: { color: "rgba(255,255,255,.14)" } },
            axisLabel: { color: "rgba(236,247,255,.72)" },
            ...overrides,
        };
    }

    function getValueAxis(overrides = {}) {
        return {
            type: "value",
            axisLabel: { color: "rgba(236,247,255,.68)" },
            splitLine: { lineStyle: { color: "rgba(255,255,255,.06)" } },
            ...overrides,
        };
    }

    function getOrCreateChart(nodeId, options = {}) {
        const node = typeof nodeId === "string" ? document.getElementById(nodeId) : nodeId;
        if (!node) {
            return null;
        }

        if (!window.echarts) {
            window.pageUtils?.renderState(
                node,
                options.emptyText || "图表库未加载",
                options.emptyClass || "app-empty-state",
            );
            return null;
        }

        const registryKey = node.id || String(nodeId);
        if (chartRegistry.has(registryKey)) {
            return chartRegistry.get(registryKey);
        }

        const chart = echarts.init(node);
        chartRegistry.set(registryKey, chart);
        window.addEventListener("resize", () => chart.resize());
        return chart;
    }

    function setChartOption(nodeId, option, options = {}) {
        const chart = getOrCreateChart(nodeId, options);
        if (!chart) {
            return null;
        }
        chart.setOption(option);
        return chart;
    }

    window.chartUtils = {
        getGrid,
        getLegend,
        getCategoryAxis,
        getValueAxis,
        getOrCreateChart,
        setChartOption,
    };
})();
