from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Employee, GENDER_CHOICES, Reward
from django.db.models import Q


class EmployeeListView(ListView):
    model = Employee
    context_object_name = "employees"
    template_name = "staff/index.html"

    def get_queryset(self):
        queryset = self.model.objects.all()
        gender = self.request.GET.get("gender", None)
        awarded = self.request.GET.get("awarded", None)
        search = self.request.GET.get("search", None)
        filters = []
        if search:
            queryset = queryset.filter(
                Q(first_name__contains=search)
                | Q(last_name__contains=search)
                | Q(middle_name__contains=search)
            )

        if gender or awarded:
            return queryset.filter(gender=gender)
        else:
            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genders"] = GENDER_CHOICES
        return context


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = "staff/employee_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rewards"] = self.get_object().reward_set.all()
        return context
