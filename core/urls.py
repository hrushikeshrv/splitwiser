from django.urls import path

from core import views

app_name = "core"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path(
        "group/<int:pk>",
        views.TransactionGroupDetailView.as_view(),
        name="transaction_group_detail",
    ),
    path("__test_view__/", views.test_view, name="test_view"),
]
