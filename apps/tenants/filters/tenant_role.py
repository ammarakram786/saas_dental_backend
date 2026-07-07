import django_filters

from apps.tenants.models import TenantRole


class TenantRoleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = TenantRole
        fields = ["slug", "is_active", "is_system"]
