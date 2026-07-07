from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from apps.clinical.models import ClinicalNote


@shared_task
def lock_stale_notes():
    cutoff = timezone.now() - timedelta(hours=24)
    return ClinicalNote.objects.filter(
        is_locked=False,
        created_at__lte=cutoff,
    ).update(is_locked=True, locked_at=timezone.now())
