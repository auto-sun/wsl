from django.shortcuts import render


def devices_view(request):
    return render(
        request,
        "devices.html",
        {
            "page_title": "设备管理",
            "page_key": "devices",
            "page_description": "展示设备状态、连接测试与控制链路预留，当前不连接真实硬件。",
        },
    )
