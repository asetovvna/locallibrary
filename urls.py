# locallibrary/locallibrary/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "catalog/", include("catalog.urls")
    ),  # <-- все URL приложения catalog начинаются с /catalog/
    path(
        "", include("catalog.urls")
    ),  # <-- опционально: сделать catalog домашним (http://127.0.0.1:8000/)
    path("accounts/", include("django.contrib.auth.urls")),  # ← эта строка обязательна!
]
