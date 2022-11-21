from django.urls import path, include
from rest_framework.routers import DefaultRouter

import home.api.v1.users.views as views


router = DefaultRouter()
router.register("", views.UserViewSet, basename="crud")

urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("verify-code/", views.VerifyPhoneNumber.as_view(), name="verify-code"),
    path("", include(router.urls))
]

app_name = "users"
