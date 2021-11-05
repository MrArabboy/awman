from .models import OrganizationType, RewardType, Organization, Reward


def filter_processor(request):
    min_date = Reward.objects.order_by("date_of_issue")[0].date_of_issue
    max_date = Reward.objects.order_by("-date_of_issue")[0].date_of_issue
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
