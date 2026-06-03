async function initDiagnosisPage() {
    const { escapeHtml, renderState } = window.pageUtils;

    const form = document.getElementById("diagnosisForm");
    const input = document.getElementById("diagnosisImageInput");
    const dropzone = document.getElementById("uploadDropzone");
    const previewImage = document.getElementById("previewImage");
    const overlayLayer = document.getElementById("overlayLayer");
    const selectedImageName = document.getElementById("selectedImageName");
    const startButton = document.getElementById("startDiagnosisButton");
    const progressShell = document.getElementById("diagnosisProgress");
    const progressBar = document.getElementById("diagnosisProgressBar");
    const progressText = document.getElementById("diagnosisProgressText");
    const resultCard = document.getElementById("diagnosisResultCard");
    const historyList = document.getElementById("diagnosisHistoryList");
    const riskBadge = document.getElementById("riskBadge");
    const fallbackBoxReference = { width: 640, height: 360 };

    let previewUrl = "";
    let progressTimer = null;

    function revokePreview() {
        if (previewUrl) {
            URL.revokeObjectURL(previewUrl);
            previewUrl = "";
        }
    }

    function setRiskBadge(level) {
        riskBadge.className = "risk-badge";
        if (level === "高" || level === "中高") {
            riskBadge.classList.add("risk-high");
        } else if (level === "中") {
            riskBadge.classList.add("risk-medium");
        } else if (level === "低") {
            riskBadge.classList.add("risk-low");
        } else {
            riskBadge.classList.add("risk-neutral");
        }
        riskBadge.textContent = level || "待检测";
    }

    function renderOverlayBoxes(boxes, imageSize = fallbackBoxReference) {
        const referenceWidth = Number(imageSize.width) || fallbackBoxReference.width;
        const referenceHeight = Number(imageSize.height) || fallbackBoxReference.height;
        const canvasWidth = overlayLayer.clientWidth || referenceWidth;
        const canvasHeight = overlayLayer.clientHeight || referenceHeight;
        const scale = Math.min(canvasWidth / referenceWidth, canvasHeight / referenceHeight);
        const renderedWidth = referenceWidth * scale;
        const renderedHeight = referenceHeight * scale;
        const offsetX = (canvasWidth - renderedWidth) / 2;
        const offsetY = (canvasHeight - renderedHeight) / 2;
        overlayLayer.innerHTML = (boxes || []).map((box) => `
            <div class="overlay-box" style="left:${offsetX + box.x * scale}px;top:${offsetY + box.y * scale}px;width:${box.width * scale}px;height:${box.height * scale}px;">
                <span>${escapeHtml(box.label)} ${escapeHtml((box.score * 100).toFixed(1))}%</span>
            </div>
        `).join("");
    }

    function renderPreview(file) {
        revokePreview();
        overlayLayer.innerHTML = "";
        if (!file) {
            previewImage.style.display = "none";
            selectedImageName.textContent = "尚未选择图片";
            startButton.disabled = true;
            return;
        }

        previewUrl = URL.createObjectURL(file);
        previewImage.src = previewUrl;
        previewImage.style.display = "block";
        selectedImageName.textContent = file.name;
        startButton.disabled = false;
    }

    function startProgress() {
        clearInterval(progressTimer);
        progressShell.classList.remove("is-hidden");
        progressBar.style.width = "8%";
        const steps = [
            "正在上传图片并创建检测任务...",
            "AI识别中，优先调用本地 YOLOv8 模型...",
            "正在组装结构化诊断结果...",
        ];
        let index = 0;
        let progress = 8;
        progressText.textContent = steps[0];
        progressTimer = window.setInterval(() => {
            index = Math.min(index + 1, steps.length - 1);
            progress = Math.min(progress + 22, 82);
            progressBar.style.width = `${progress}%`;
            progressText.textContent = steps[index];
        }, 650);
    }

    function stopProgress(success) {
        clearInterval(progressTimer);
        progressBar.style.width = success ? "100%" : "0%";
        progressText.textContent = success ? "识别完成，已返回结构化诊断结果。" : "识别失败，请重试。";
        window.setTimeout(() => {
            progressShell.classList.add("is-hidden");
            progressBar.style.width = "0%";
        }, success ? 900 : 500);
    }

    function renderResult(data) {
        setRiskBadge(data.result.risk_level);
        renderOverlayBoxes(data.result.boxes, data.result.image_size);
        resultCard.innerHTML = `
            <div class="result-grid">
                <div class="result-header">
                    <span class="section-title">诊断结论</span>
                    <strong>${escapeHtml(data.result.disease_name)}</strong>
                    <p>${escapeHtml(data.message)}</p>
                </div>
                <div class="meta-grid">
                    <div class="meta-item">
                        <span>任务 ID</span>
                        <strong>${escapeHtml(data.task_id)}</strong>
                    </div>
                    <div class="meta-item">
                        <span>图片地址</span>
                        <strong>${escapeHtml(data.image_url)}</strong>
                    </div>
                    <div class="meta-item">
                        <span>置信度</span>
                        <strong>${escapeHtml((data.result.confidence * 100).toFixed(1))}%</strong>
                    </div>
                    <div class="meta-item">
                        <span>任务状态</span>
                        <strong>${escapeHtml(data.status)}</strong>
                    </div>
                    <div class="meta-item">
                        <span>推理模式</span>
                        <strong>${escapeHtml(data.inference_mode || "unknown")}</strong>
                    </div>
                    <div class="meta-item">
                        <span>检出目标</span>
                        <strong>${escapeHtml(data.result.detected_count || 0)} 个</strong>
                    </div>
                </div>
                <div class="result-message">
                    <span class="section-title">建议措施</span>
                    <div class="suggestion-list">
                        <div class="suggestion-item">${escapeHtml(data.result.suggestion)}</div>
                    </div>
                </div>
                <div class="result-message">
                    <span class="section-title">风险等级</span>
                    <p>${escapeHtml(data.result.risk_level)}</p>
                </div>
            </div>
        `;
    }

    function renderHistory(records) {
        if (!records.length) {
            renderState(historyList, "当前暂无检测历史记录，可先上传一张火龙果病虫害图片开始演示。", "result-message");
            return;
        }
        historyList.innerHTML = records.map((item) => `
            <article class="history-item">
                <h5>${escapeHtml(item.diagnosis_name)}</h5>
                <div class="history-item-meta">${escapeHtml(item.created_at)} · ${escapeHtml(item.image_name)}</div>
                <p>任务编号：${escapeHtml(item.task_code)}</p>
                <p>风险等级：${escapeHtml(item.risk_level)}，置信度：${escapeHtml((item.confidence * 100).toFixed(1))}%</p>
            </article>
        `).join("");
    }

    async function refreshHistory() {
        try {
            const data = await apiClient.get("/api/diagnosis/history");
            renderHistory(data.history);
        } catch (error) {
            window.appUI?.notify(error.message, "error", "历史记录加载失败");
            renderState(historyList, error.message, "result-message");
        }
    }

    function setInputFiles(files) {
        if (!files || !files.length) {
            return;
        }
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(files[0]);
        input.files = dataTransfer.files;
        renderPreview(files[0]);
    }

    input.addEventListener("change", () => {
        renderPreview(input.files[0]);
    });

    ["dragenter", "dragover"].forEach((eventName) => {
        dropzone.addEventListener(eventName, (event) => {
            event.preventDefault();
            dropzone.classList.add("is-dragover");
        });
    });

    ["dragleave", "drop"].forEach((eventName) => {
        dropzone.addEventListener(eventName, (event) => {
            event.preventDefault();
            dropzone.classList.remove("is-dragover");
        });
    });

    dropzone.addEventListener("drop", (event) => {
        setInputFiles(event.dataTransfer.files);
    });

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        if (!input.files.length) {
            return;
        }

        startButton.disabled = true;
        startProgress();
        setRiskBadge("识别中");
        resultCard.innerHTML = `
            <div class="result-placeholder">
                <h5>AI识别中</h5>
                <p>正在保存图片并调用后端病虫害识别流程，请稍候。</p>
            </div>
        `;

        try {
            window.appUI?.setLoading(true, "正在上传图片并执行 AI 诊断流程...");
            const formData = new FormData();
            formData.append("image", input.files[0]);
            const result = await apiClient.postForm("/api/diagnosis/upload", formData);
            stopProgress(true);
            renderResult(result);
            await refreshHistory();
            window.appUI?.notify("检测任务已完成，结果已写入历史记录。", "success", "AI 诊断完成");
        } catch (error) {
            stopProgress(false);
            setRiskBadge("失败");
            window.appUI?.notify(error.message, "error", "AI 诊断失败");
            resultCard.innerHTML = `
                <div class="result-placeholder">
                    <h5>检测失败</h5>
                    <p>${escapeHtml(error.message)}</p>
                </div>
            `;
        } finally {
            window.appUI?.setLoading(false);
            startButton.disabled = !input.files.length;
        }
    });

    await refreshHistory();
    window.addEventListener("beforeunload", revokePreview);
}

document.addEventListener("DOMContentLoaded", () => {
    initDiagnosisPage().catch((error) => {
        window.appUI?.setLoading(false);
        window.appUI?.notify(error.message || "页面初始化失败", "error", "诊断页初始化失败");
    });
});
