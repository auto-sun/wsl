from django.shortcuts import render


def decision_view(request):
    return render(
        request,
        "decision.html",
        {
            "page_title": "处方图与策略",
            "page_key": "decision",
            "page_description": "展示水肥一体化处方策略、执行预留状态与历史策略记录。",
        },
    )
