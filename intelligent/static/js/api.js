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
        let payload = null;

        try {
            payload = await response.json();
        } catch (error) {
            payload = null;
        }

        if (response.status === 401) {
            window.location.href = "/login/";
            throw new Error("登录已失效，请重新登录。");
        }

        if (!response.ok || !payload || payload.code !== 0) {
            throw new Error(payload?.message || "请求失败，请稍后重试。");
        }

        return payload.data;
    }

    window.apiClient = {
        get(url) {
            return request(url);
        },
        postJson(url, body) {
            return request(url, {
                method: "POST",
                body: JSON.stringify(body),
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
