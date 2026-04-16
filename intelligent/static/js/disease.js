document.addEventListener("DOMContentLoaded", async () => {
    const ui = window.SmartAgriUI;
    const form = document.getElementById("diseaseForm");
    const input = document.getElementById("diseaseImageInput");
    const preview = document.getElementById("diseasePreview");
    const fileName = document.getElementById("selectedFileName");
    const resultContainer = document.getElementById("detectionResult");
    const statusTag = document.getElementById("detectionStatus");
    const boxesLayer = document.getElementById("diseaseBoxes");

    function renderBoxes(boxes) {
        boxesLayer.innerHTML = (boxes || []).map((box) => `
            <div class="detection-box" style="left:${box.x}%;top:${box.y}%;width:${box.w}%;height:${box.h}%;">
                <span>${ui.escapeHtml(box.label)}</span>
            </div>
        `).join("");
    }

    function renderResult(result) {
        statusTag.textContent = result.severity;
        resultContainer.innerHTML = `
            <div class="result-grid">
                <div>
                    <p class="eyebrow">检测结论</p>
                    <h4>${ui.escapeHtml(result.disease_name)}</h4>
                    <p>${ui.escapeHtml(result.remarks)}</p>
                </div>
                <div class="result-highlight">
                    <div class="result-cell">
                        <span>风险等级</span>
                        <strong>${ui.escapeHtml(result.severity)}</strong>
                    </div>
                    <div class="result-cell">
                        <span>置信度</span>
                        <strong>${ui.escapeHtml((result.confidence * 100).toFixed(1))}%</strong>
                    </div>
                    <div class="result-cell">
                        <span>疑似面积</span>
                        <strong>${ui.escapeHtml(result.detected_area)}</strong>
                    </div>
                </div>
                <div class="narrative-card">
                    <h4>任务信息</h4>
                    <p>任务编号：${ui.escapeHtml(result.task_code)}</p>
                    <p>地块编号：${ui.escapeHtml(result.plot_code)}</p>
                    <p>采集时间：${ui.escapeHtml(result.capture_time)}</p>
                </div>
                <div class="narrative-card">
                    <h4>处置建议</h4>
                    <p>${result.suggestions.map((item) => `• ${ui.escapeHtml(item)}`).join("<br>")}</p>
                </div>
                <div class="narrative-card">
                    <h4>模型接口占位</h4>
                    <p>${ui.escapeHtml(result.inference.message)}</p>
                </div>
            </div>
        `;
        renderBoxes(result.boxes);
    }

    function renderHistory(history) {
        ui.renderTable("detectionHistory", [
            { label: "任务编号", key: "task_code" },
            { label: "文件名", key: "image_name" },
            { label: "地块", key: "plot_code" },
            { label: "结果", key: "disease_name" },
            {
                label: "风险",
                key: "severity",
                render: (row) => `<span class="status-badge ${ui.statusClass(row.severity)}">${ui.escapeHtml(row.severity)}</span>`,
            },
            {
                label: "置信度",
                key: "confidence",
                render: (row) => `${ui.escapeHtml((row.confidence * 100).toFixed(1))}%`,
            },
            { label: "时间", key: "created_at" },
        ], history);
    }

    input?.addEventListener("change", () => {
        const [file] = input.files;
        boxesLayer.innerHTML = "";
        if (!file) {
            preview.style.display = "none";
            fileName.textContent = "尚未选择图片";
            return;
        }
        preview.src = URL.createObjectURL(file);
        preview.style.display = "block";
        fileName.textContent = file.name;
    });

    form?.addEventListener("submit", async (event) => {
        event.preventDefault();
        if (!input.files?.length) {
            alert("请先选择病虫害图片。");
            return;
        }

        statusTag.textContent = "检测中";
        resultContainer.innerHTML = `
            <div class="placeholder-block">
                <h4>任务提交成功</h4>
                <p>正在按真实业务流程调用后端接口并等待 mock 推理结果返回。</p>
            </div>
        `;

        try {
            const formData = new FormData(form);
            const result = await apiClient.postForm("/api/disease-detections/", formData);
            renderResult(result);
            const latestHistory = await apiClient.get("/api/disease-detections/");
            renderHistory(latestHistory.history);
        } catch (error) {
            statusTag.textContent = "失败";
            resultContainer.innerHTML = `
                <div class="placeholder-block">
                    <h4>检测失败</h4>
                    <p>${ui.escapeHtml(error.message)}</p>
                </div>
            `;
        }
    });

    try {
        const data = await apiClient.get("/api/disease-detections/");
        renderHistory(data.history);
    } catch (error) {
        alert(error.message);
    }
});
