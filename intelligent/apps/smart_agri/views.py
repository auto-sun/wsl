from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import RedirectView, TemplateView

from .services.mock_data import get_navigation_summary


SESSION_FLAG = "smart_agri_authenticated"
SESSION_USER_KEY = "smart_agri_user"


class RootRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        if self.request.session.get(SESSION_FLAG):
            return reverse("dashboard")
        return reverse("login")


class LoginPageView(TemplateView):
    template_name = "login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.session.get(SESSION_FLAG):
            return HttpResponseRedirect(reverse("dashboard"))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "page_title": "登录",
                "page_key": "login",
                "nav_summary": get_navigation_summary(),
            }
        )
        return context


class SessionProtectedTemplateView(TemplateView):
    page_title = ""
    page_key = ""

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get(SESSION_FLAG):
            return HttpResponseRedirect(reverse("login"))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "page_title": self.page_title,
                "page_key": self.page_key,
                "nav_summary": get_navigation_summary(),
                "current_user": self.request.session.get(SESSION_USER_KEY, {}),
            }
        )
        return context


class DashboardPageView(SessionProtectedTemplateView):
    template_name = "dashboard.html"
    page_title = "系统驾驶舱"
    page_key = "dashboard"


class GrowthMonitorPageView(SessionProtectedTemplateView):
    template_name = "growth_monitor.html"
    page_title = "长势监测"
    page_key = "growth"


class DiseaseDetectionPageView(SessionProtectedTemplateView):
    template_name = "disease_detection.html"
    page_title = "病虫害检测"
    page_key = "disease"


class PrescriptionPageView(SessionProtectedTemplateView):
    template_name = "prescription.html"
    page_title = "处方图与策略"
    page_key = "prescription"


class DeviceManagementPageView(SessionProtectedTemplateView):
    template_name = "device_management.html"
    page_title = "设备管理"
    page_key = "devices"


class ApiDocsPageView(SessionProtectedTemplateView):
    template_name = "api_docs.html"
    page_title = "API 文档"
    page_key = "api-docs"
