import django_filters

from apps.accounts.models import PlatformUserProfile


class PlatformUserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name="user__username", lookup_expr="icontains")
    email = django_filters.CharFilter(field_name="user__email", lookup_expr="icontains")
    is_active = django_filters.BooleanFilter(field_name="user__is_active")
    platform_role = django_filters.NumberFilter(field_name="role_id")

    class Meta:
        model = PlatformUserProfile
        fields = ["is_super_admin", "role", "is_active", "platform_role"]
