import django_filters

from apps.tenants.models import Tenant


class TenantFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    slug = django_filters.CharFilter(lookup_expr="icontains")
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Tenant
        fields = ["is_active"]
