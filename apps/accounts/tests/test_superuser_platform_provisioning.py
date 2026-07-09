from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.accounts.models import PlatformUserProfile

User = get_user_model()


class SuperuserPlatformProvisioningTests(TestCase):
    def test_createsuperuser_provisions_platform_profile(self):
        user = User.objects.create_superuser(
            username="admin",
            password="secret",
            email="admin@test.com",
        )

        profile = PlatformUserProfile.objects.get(user=user)
        self.assertTrue(profile.is_super_admin)

    def test_revoking_superuser_clears_platform_super_admin_flag(self):
        user = User.objects.create_superuser(
            username="admin2",
            password="secret",
            email="admin2@test.com",
        )
        user.is_superuser = False
        user.save()

        profile = PlatformUserProfile.objects.get(user=user)
        self.assertFalse(profile.is_super_admin)
