from django.shortcuts import render
from django.template import RequestContext
from django.utils.translation import templatize
from django.views.generic import ListView, DetailView
from .models import Employee, GENDER_CHOICES, Reward, RewardType
from django.db.models import Q
from django.http import JsonResponse


def handler404(request, exception):
    response = render(request, "staff/404.html", status=404)
    return response


class EmployeeListView(ListView):
    model = Employee
    context_object_name = "employees"
    template_name = "staff/employees.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model.objects.all()
        search = self.request.GET.get("search", None)
        gender = self.request.GET.getlist("gender", None)
        reward_type = self.request.GET.getlist("reward_type", None)
        organization = self.request.GET.getlist("organization", None)
        org_type = self.request.GET.getlist("org_type", None)
        min_year = self.request.GET.get("min_year", None)
        max_year = self.request.GET.get("max_year", None)

        if search:
            obj_ids = [
                obj.id for obj in self.model.objects.all() if search in obj.full_name
            ]

            queryset = queryset.filter(
                Q(id__in=obj_ids)
                | Q(first_name__contains=search)
                | Q(last_name__contains=search)
                | Q(middle_name__contains=search),
            )

        if gender:
            queryset = queryset.filter(gender__in=gender)

        if org_type:
            queryset = queryset.filter(
                reward__issued_by__type__translations__name__in=org_type
            )
        if reward_type:
            queryset = queryset.filter(
                reward__type__translations__name__in=reward_type
            ).distinct()

        if min_year and max_year:
            queryset = queryset.filter(
                reward__date_of_issue__year__range=[min_year, max_year]
            ).distinct()
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


def search_autocomplete(request):
    value = request.GET.get("search", None)
    queryset = Employee.objects.all()
    if value:
        obj_ids = [obj.id for obj in queryset if value in obj.full_name]
        queryset = queryset.filter(
            Q(id__in=obj_ids)
            | Q(first_name__contains=value)
            | Q(last_name__contains=value)
            | Q(middle_name__contains=value),
        )
        result = [q.full_name for q in queryset]
    else:
        result = []

    return JsonResponse({"employees": result})
