from django.urls import path

from api import views

app_name = "api"

urlpatterns = [
    path("", views.TestView.as_view(), name="test_view"),
]
