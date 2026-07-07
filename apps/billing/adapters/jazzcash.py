from apps.billing.adapters.base import BasePaymentAdapter


class JazzCashAdapter(BasePaymentAdapter):
    def create_payment(self, *, amount, reference: str, metadata: dict | None = None) -> dict:
        return {
            "provider": "jazzcash",
            "reference": reference,
            "amount": str(amount),
            "status": "pending",
            "metadata": metadata or {},
        }
