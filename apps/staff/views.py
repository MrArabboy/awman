from django.shortcuts import render
from django.utils.translation import templatize
from django.views.generic import ListView, DetailView
from .models import Employee, GENDER_CHOICES, Reward
from django.db.models import Q
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION


class EmployeeListView(ListView):
    model = Employee
    context_object_name = "employees"
    template_name = "staff/index.html"
    paginate_by = 10

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


class EmployeeBiographyView(DetailView):
    model = Employee
    template_name = "staff/biography.html"
    context_object_name = "employee"


def main(request):

    logs = LogEntry.objects.exclude(change_message="No fields changed.").order_by(
        "-action_time"
    )[:20]
    logCount = (
        LogEntry.objects.exclude(change_message="No fields changed.")
        .order_by("-action_time")[:20]
        .count()
    )

    return render(request, "staff/main.html", {"logs": logs, "logCount": logCount})
