from django.urls import path
from .views import (
    EmployeeListView,
    EmployeeDetailView,
    EmployeeBiographyView,
    search_autocomplete,
    qs_json,
)

urlpatterns = [
    path("", EmployeeListView.as_view(), name="employees"),
    path("<int:pk>/biography", EmployeeBiographyView.as_view(), name="biography"),
    path("<int:pk>/detail", EmployeeDetailView.as_view(), name="detail"),
    path("search_hints/", search_autocomplete, name="search_hints"),
    path("qs/", qs_json),
]
