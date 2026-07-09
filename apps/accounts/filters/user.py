import django_filters
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr="icontains")
    email = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ["is_active", "is_staff", "is_superuser"]
