from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.appointments.models import Appointment
from apps.notifications.tasks import send_appointment_confirmation, send_schedule_change


@receiver(post_save, sender=Appointment)
def appointment_post_save(sender, instance, created, **kwargs):
    if created:
        send_appointment_confirmation.delay(instance.pk)
    else:
        send_schedule_change.delay(instance.pk)
