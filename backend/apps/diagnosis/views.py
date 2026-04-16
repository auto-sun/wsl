from django.shortcuts import render


def diagnosis_view(request):
    return render(
        request,
        "diagnosis.html",
        {
            "page_title": "病虫害检测",
            "page_key": "diagnosis",
            "page_description": "上传病虫害图片、执行 mock AI 诊断、查看结果与历史记录。",
        },
    )
