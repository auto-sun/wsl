(function () {
    function getCsrfToken() {
        const meta = document.querySelector('meta[name="csrf-token"]');
        if (meta && meta.content && meta.content !== "NOTPROVIDED") {
            return meta.content;
        }

        const match = document.cookie.match(/csrftoken=([^;]+)/);
        return match ? decodeURIComponent(match[1]) : "";
    }

    async function request(url, options = {}) {
        const method = (options.method || "GET").toUpperCase();
        const headers = new Headers(options.headers || {});
        const config = {
            credentials: "same-origin",
            ...options,
            method,
            headers,
        };

        if (!(config.body instanceof FormData) && config.body && !headers.has("Content-Type")) {
            headers.set("Content-Type", "application/json");
        }

        if (!["GET", "HEAD", "OPTIONS"].includes(method)) {
            const token = getCsrfToken();
            if (token) {
                headers.set("X-CSRFToken", token);
            }
        }

        const response = await fetch(url, config);
        const rawText = await response.text();
        let payload = null;

        try {
            payload = rawText ? JSON.parse(rawText) : {};
        } catch (error) {
            throw new Error("接口返回非 JSON 响应，可能是登录状态失效或服务异常。");
        }

        if (!response.ok || payload.code !== 0) {
            throw new Error(payload.message || "请求失败");
        }

        return payload.data;
    }

    async function getJson(url) {
        return request(url);
    }

    window.apiClient = {
        get: getJson,
        postJson(url, payload) {
            return request(url, {
                method: "POST",
                body: JSON.stringify(payload),
            });
        },
        postForm(url, formData) {
            return request(url, {
                method: "POST",
                body: formData,
            });
        },
    };
})();
