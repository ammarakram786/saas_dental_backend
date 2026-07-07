import django_filters

from apps.platform.models import PlatformAuditEvent


class PlatformAuditEventFilter(django_filters.FilterSet):
    actor = django_filters.CharFilter(lookup_expr="icontains")
    action = django_filters.CharFilter(lookup_expr="icontains")
    target = django_filters.CharFilter(lookup_expr="icontains")
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = PlatformAuditEvent
        fields = ["severity", "category"]
