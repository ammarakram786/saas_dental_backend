from __future__ import annotations

from abc import ABC, abstractmethod


class BaseSmsAdapter(ABC):
    @abstractmethod
    def send_sms(self, *, to: str, message: str, sender_id: str = "DNTLDOODLE") -> dict:
        raise NotImplementedError
