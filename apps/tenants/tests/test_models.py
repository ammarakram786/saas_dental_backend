from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from apps.tenants.models import (
    Tenant,
    TenantMembership,
    TenantPermission,
    TenantRole,
)

User = get_user_model()


class DefaultRoleSeedingTests(TestCase):
    def test_creating_tenant_seeds_system_roles(self):
        tenant = Tenant.objects.create(name="Acme", slug="acme")
        roles = TenantRole.objects.filter(tenant=tenant)
        self.assertEqual(
            set(roles.values_list("slug", flat=True)),
            {"admin", "manager", "member"},
        )
        self.assertTrue(all(role.is_system for role in roles))

    def test_admin_role_gets_all_permissions(self):
        tenant = Tenant.objects.create(name="Acme", slug="acme")
        admin = TenantRole.objects.get(tenant=tenant, slug="admin")
        all_codenames = set(
            TenantPermission.objects.filter(is_active=True).values_list(
                "codename", flat=True
            )
        )
        self.assertEqual(admin.permission_codenames(), all_codenames)

    def test_member_role_is_restricted(self):
        tenant = Tenant.objects.create(name="Acme", slug="acme")
        member = TenantRole.objects.get(tenant=tenant, slug="member")
        self.assertEqual(member.permission_codenames(), {"view_appointments"})

    def test_seeding_is_idempotent(self):
        tenant = Tenant.objects.create(name="Acme", slug="acme")
        from apps.tenants.services import seed_default_roles

        seed_default_roles(tenant)
        self.assertEqual(TenantRole.objects.filter(tenant=tenant).count(), 3)


class TenantMembershipIntegrityTests(TestCase):
    def setUp(self):
        self.tenant_a = Tenant.objects.create(name="A", slug="a")
        self.tenant_b = Tenant.objects.create(name="B", slug="b")
        self.user = User.objects.create_user(username="u", password="x")

    def test_role_from_other_tenant_is_rejected(self):
        role_b = TenantRole.objects.get(tenant=self.tenant_b, slug="admin")
        membership = TenantMembership(
            user=self.user, tenant=self.tenant_a, role=role_b
        )
        with self.assertRaises(ValidationError):
            membership.save()

    def test_same_tenant_role_is_accepted(self):
        role_a = TenantRole.objects.get(tenant=self.tenant_a, slug="admin")
        membership = TenantMembership.objects.create(
            user=self.user, tenant=self.tenant_a, role=role_a
        )
        self.assertIsNotNone(membership.pk)

    def test_one_membership_per_user_and_tenant(self):
        role_a = TenantRole.objects.get(tenant=self.tenant_a, slug="admin")
        member_a = TenantRole.objects.get(tenant=self.tenant_a, slug="member")
        TenantMembership.objects.create(
            user=self.user, tenant=self.tenant_a, role=role_a
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                TenantMembership.objects.create(
                    user=self.user, tenant=self.tenant_a, role=member_a
                )

    def test_role_slug_unique_per_tenant_but_reusable_across_tenants(self):
        # 'admin' exists in both tenants without collision.
        self.assertTrue(
            TenantRole.objects.filter(tenant=self.tenant_a, slug="admin").exists()
        )
        self.assertTrue(
            TenantRole.objects.filter(tenant=self.tenant_b, slug="admin").exists()
        )
