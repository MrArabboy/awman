from django.urls import path
from .views import EmployeeListView, EmployeeDetailView

urlpatterns = [
    path("", EmployeeListView.as_view(), name="employees"),
    path("<int:pk>/detail", EmployeeDetailView.as_view(), name="detail"),
]
