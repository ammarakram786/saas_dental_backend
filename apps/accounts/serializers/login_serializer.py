from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class EmailOrUsernameTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Allow obtaining a token pair using either a username or an email.

    If the submitted identifier looks like an email, it is resolved to the
    matching user's username before the standard JWT authentication runs.
    """

    def validate(self, attrs):
        identifier = attrs.get(self.username_field)
        if identifier and "@" in identifier:
            match = (
                User.objects.filter(email__iexact=identifier)
                .order_by("id")
                .first()
            )
            if match is not None:
                attrs[self.username_field] = match.get_username()
        return super().validate(attrs)
