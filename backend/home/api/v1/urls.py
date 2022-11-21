from django.urls import path, include


urlpatterns = [
    path("users/", include("home.api.v1.users.urls", namespace="users"))
]
