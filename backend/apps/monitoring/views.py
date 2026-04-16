from django.shortcuts import render


def monitoring_view(request):
    return render(
        request,
        "monitoring.html",
        {
            "page_title": "长势监测",
            "page_key": "monitoring",
            "page_description": "展示火龙果种植区长势、热力分布、巡检记录与无人机监测信息。",
        },
    )
