from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/station/", include("station.urls", namespace="station")),
    path("api/user/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/user/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/user/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/doc/", SpectacularAPIView.as_view(), name="schema"),
    path("api/doc/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
