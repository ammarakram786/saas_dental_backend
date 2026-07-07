import django_filters

from apps.tenants.models import TenantMembership


class TenantMembershipFilter(django_filters.FilterSet):
    user_username = django_filters.CharFilter(
        field_name="user__username", lookup_expr="icontains"
    )
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = TenantMembership
        fields = ["user", "role", "is_active"]
