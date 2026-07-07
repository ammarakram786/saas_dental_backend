from __future__ import annotations

from abc import ABC, abstractmethod


class BasePaymentAdapter(ABC):
    @abstractmethod
    def create_payment(self, *, amount, reference: str, metadata: dict | None = None) -> dict:
        raise NotImplementedError
