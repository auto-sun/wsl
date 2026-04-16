(function () {
    const accentClassMap = {
        cyan: "accent-cyan",
        blue: "accent-blue",
        violet: "accent-violet",
        red: "accent-red",
    };

    function escapeHtml(value) {
        return String(value)
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#39;");
    }

    function renderState(node, message, className = "app-empty-state") {
        if (!node) {
            return;
        }
        node.innerHTML = `<div class="${className}">${escapeHtml(message)}</div>`;
    }

    function renderEmptyState(node, message, extraClass = "") {
        renderState(node, message, `app-empty-state ${extraClass}`.trim());
    }

    function renderErrorState(node, message, extraClass = "") {
        renderState(node, message, `app-error-state ${extraClass}`.trim());
    }

    function getAccentClass(accent) {
        return accentClassMap[accent] || accentClassMap.cyan;
    }

    function setButtonLoading(button, loading, loadingText = "处理中...") {
        if (!button) {
            return;
        }
        if (!button.dataset.defaultText) {
            button.dataset.defaultText = button.textContent.trim();
        }
        button.disabled = loading;
        button.textContent = loading ? loadingText : button.dataset.defaultText;
    }

    function setSelectOptions(selectNode, options, selectedValue, extraOptions = []) {
        if (!selectNode) {
            return;
        }
        const merged = [...extraOptions, ...options];
        selectNode.innerHTML = merged.map((item) => (
            `<option value="${escapeHtml(item.value)}">${escapeHtml(item.label)}</option>`
        )).join("");
        if (selectedValue !== undefined && selectedValue !== null) {
            selectNode.value = selectedValue;
        }
    }

    window.pageUtils = {
        escapeHtml,
        renderState,
        renderEmptyState,
        renderErrorState,
        getAccentClass,
        setButtonLoading,
        setSelectOptions,
    };
})();
