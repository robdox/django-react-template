from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounts.views import (
    ConfirmEmailView,
    ResetPasswordView,
    UserViewSet,
)


router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("confirm-email/<str:key>/", ConfirmEmailView.as_view(), name="confirm-email"),
    path(
        "password/reset/<str:email>/",
        ResetPasswordView.as_view(),
        name="password_reset_confirm",
    ),
]
