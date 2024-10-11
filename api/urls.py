from django.urls import path

from api import views

app_name = "api"

urlpatterns = [
    path("", views.TestView.as_view(), name="test_view"),
    path('groups/<int:pk>/summary', views.GroupPaymentSummary.as_view(), name="transaction_group_summary"),
]
