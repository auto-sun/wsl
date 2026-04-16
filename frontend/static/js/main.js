document.addEventListener("DOMContentLoaded", () => {
    const timeNode = document.getElementById("currentTime");
    const toastStack = document.getElementById("appToastStack");
    const loadingNode = document.getElementById("globalLoading");
    const loadingTextNode = document.getElementById("globalLoadingText");
    const modalOverlay = document.getElementById("appModalOverlay");
    const modalTitle = document.getElementById("appModalTitle");
    const modalBody = document.getElementById("appModalBody");
    const modalClose = document.getElementById("appModalClose");
    const modalConfirm = document.getElementById("appModalConfirm");

    function renderTime() {
        if (!timeNode) {
            return;
        }
        const now = new Date();
        const value = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}-${String(now.getDate()).padStart(2, "0")} ${String(now.getHours()).padStart(2, "0")}:${String(now.getMinutes()).padStart(2, "0")}:${String(now.getSeconds()).padStart(2, "0")}`;
        timeNode.textContent = value;
    }

    function notify(message, type = "info", title = "系统提示") {
        if (!toastStack) {
            return;
        }
        const toast = document.createElement("div");
        toast.className = `app-toast ${type}`;
        const titleNode = document.createElement("strong");
        const messageNode = document.createElement("p");
        titleNode.textContent = title;
        messageNode.textContent = message;
        toast.appendChild(titleNode);
        toast.appendChild(messageNode);
        toastStack.appendChild(toast);
        window.setTimeout(() => {
            toast.remove();
        }, 3200);
    }

    function setLoading(visible, text = "加载中...") {
        if (!loadingNode || !loadingTextNode) {
            return;
        }
        loadingTextNode.textContent = text;
        loadingNode.classList.toggle("is-hidden", !visible);
    }

    function closeModal() {
        if (!modalOverlay) {
            return;
        }
        modalOverlay.classList.add("is-hidden");
        modalConfirm.onclick = null;
    }

    function openModal(title, message, onConfirm = null) {
        if (!modalOverlay || !modalTitle || !modalBody || !modalConfirm) {
            return;
        }
        modalTitle.textContent = title;
        modalBody.textContent = message;
        modalOverlay.classList.remove("is-hidden");
        modalConfirm.onclick = () => {
            if (typeof onConfirm === "function") {
                onConfirm();
            }
            closeModal();
        };
    }

    modalClose?.addEventListener("click", closeModal);
    modalOverlay?.addEventListener("click", (event) => {
        if (event.target === modalOverlay) {
            closeModal();
        }
    });

    renderTime();
    window.setInterval(renderTime, 1000);

    window.appUI = {
        notify,
        setLoading,
        openModal,
        closeModal,
    };
});
