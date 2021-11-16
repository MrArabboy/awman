from django.shortcuts import render
from django.template import RequestContext
from django.utils.translation import templatize
from django.views.generic import ListView, DetailView
from .models import Employee, GENDER_CHOICES, Reward, RewardType, EmployeeTranslation
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.db.models import CharField, Value as V
from django.db.models.functions import Concat


def handler404(request, exception):
    response = render(request, "staff/404.html", status=404)
    return response


class EmployeeListView(ListView):
    model = Employee
    context_object_name = "employees"
    template_name = "staff/employees.html"
    paginate_by = 8

    def get_queryset(self):
        queryset = Employee.objects.all()  # EmployeeTranslation.objects.all()
        search = self.request.GET.get("search", None)
        gender = self.request.GET.getlist("gender", None)
        reward_type = self.request.GET.getlist("reward_type", None)
        organization = self.request.GET.getlist("organization", None)
        org_type = self.request.GET.getlist("org_type", None)
        min_year = self.request.GET.get("min_year", None)
        max_year = self.request.GET.get("max_year", None)

        if search:
            search = search.title()
            search = list(search.split(" "))
            if len(search) == 1:
                search = search[0]
            queryset = queryset.filter(
                Q(translations__first_name__contains=search)
                | Q(translations__last_name__contains=search)
                | Q(translations__middle_name__contains=search)
                | Q(translations__first_name__in=search)
                | Q(translations__last_name__in=search)
                | Q(translations__middle_name__in=search)
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
    search = request.GET.get("search", None)
    queryset = Employee.objects.all()
    if search:
        search = search.title()
        search = list(search.split(" "))
        if len(search) == 1:
            search = search[0]
        queryset = queryset.filter(
            Q(translations__first_name__contains=search)
            | Q(translations__last_name__contains=search)
            | Q(translations__middle_name__contains=search)
            | Q(translations__first_name__in=search)
            | Q(translations__last_name__in=search)
            | Q(translations__middle_name__in=search)
        ).distinct()[:7]
        result = [
            (q.last_name + " " + q.first_name + " " + q.middle_name) for q in queryset
        ]
    else:
        result = []

    return JsonResponse({"employees": result})


def qs_json(request):
    gender = request.GET.getlist("gender", None)
    reward_type = request.GET.getlist("reward_type", None)
    organization = request.GET.getlist("organization", None)
    org_type = request.GET.getlist("org_type", None)
    min_year = request.GET.get("min_year", None)
    max_year = request.GET.get("max_year", None)

    queryset = Employee.objects.all()
    if gender:
        queryset = Employee.objects.filter(gender__in=gender)
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
    data = list(
        queryset.values()
    )  # wrap in list(), because QuerySet is not JSON serializable
    return JsonResponse(
        {"employees": data}, safe=False
    )  # or JsonResponse({'data': data})
