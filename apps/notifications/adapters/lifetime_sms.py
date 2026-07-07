from apps.notifications.adapters.base import BaseSmsAdapter


class LifetimeSmsAdapter(BaseSmsAdapter):
    def send_sms(self, *, to: str, message: str, sender_id: str = "DNTLDOODLE") -> dict:
        return {"provider": "lifetimesms", "to": to, "message": message, "sender_id": sender_id}
