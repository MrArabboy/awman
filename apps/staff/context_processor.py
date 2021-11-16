from .models import OrganizationType, RewardType, Organization, Reward


def filter_processor(request):
    min_date = Reward.objects.order_by("date_of_issue").first().date_of_issue or 1991
    max_date = Reward.objects.order_by("-date_of_issue").first().date_of_issue or 2021
    reward_types = RewardType.objects.all()
    organizations = Organization.objects.all()
    organization_types = OrganizationType.objects.all()

    return {
        "min_date": min_date,
        "max_date": max_date,
        "reward_types": reward_types,
        "organizations": organizations,
        "organization_types": organization_types,
    }
