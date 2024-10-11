from django.urls import path

from core import views

app_name = "core"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path(
        "groups/<int:pk>",
        views.TransactionGroupDetailView.as_view(),
        name="transaction_group_detail",
    ),
    path('groups/<int:pk>/transactions/create', views.TransactionCreateView.as_view(), name="transaction_create"),
    path(
        "groups/",
        views.TransactionGroupListView.as_view(),
        name="transaction_group_list",
    ),
    path(
        "groups/join",
        views.JoinTransactionGroupView.as_view(),
        name="transaction_group_join",
    ),
    path("__test_view__/", views.test_view, name="test_view"),
]
