document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("loginForm");
    const message = document.getElementById("loginMessage");

    if (!form) {
        return;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        message.textContent = "正在校验账号并进入系统...";

        try {
            const formData = new FormData(form);
            const payload = {
                username: formData.get("username"),
                password: formData.get("password"),
            };
            const data = await apiClient.postJson("/api/auth/login/", payload);
            message.textContent = `登录成功，正在跳转至 ${data.user.display_name} 的控制台...`;
            window.location.href = data.redirect || "/dashboard/";
        } catch (error) {
            message.textContent = error.message;
        }
    });
});
