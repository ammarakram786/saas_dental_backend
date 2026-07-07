from django.conf import settings

from apps.notifications.adapters.lifetime_sms import LifetimeSmsAdapter
from apps.notifications.adapters.veer_sms import VeerSmsAdapter


class SmsGatewayFactory:
    @staticmethod
    def get():
        provider = getattr(settings, "SMS_PROVIDER", "lifetimesms")
        if provider == "veersms":
            return VeerSmsAdapter()
        return LifetimeSmsAdapter()
