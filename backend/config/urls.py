from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from apps.common.views import not_found_view
from apps.user.views import logout_view


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/monitoring/", include("apps.monitoring.api_urls")),
    path("api/diagnosis/", include("apps.diagnosis.api_urls")),
    path("api/decision/", include("apps.decision.api_urls")),
    path("api/devices/", include("apps.device.api_urls")),
    path("", include("apps.common.urls")),
    path("login", include("apps.user.urls")),
    path("monitoring", include("apps.monitoring.urls")),
    path("diagnosis", include("apps.diagnosis.urls")),
    path("decision", include("apps.decision.urls")),
    path("devices", include("apps.device.urls")),
    path("logout", logout_view, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path("<path:unknown_path>", not_found_view, name="not-found"),
]

handler404 = "apps.common.views.custom_404"
