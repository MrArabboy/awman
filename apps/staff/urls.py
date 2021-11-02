from django.urls import path
from .views import EmployeeListView, EmployeeDetailView, EmployeeBiographyView, main

urlpatterns = [
    path("", EmployeeListView.as_view(), name="employees"),
    path("<int:pk>/biography", EmployeeBiographyView.as_view(), name="biography"),
    path("<int:pk>/detail", EmployeeDetailView.as_view(), name="detail"),
    path("history/", main, name="history"),
]
