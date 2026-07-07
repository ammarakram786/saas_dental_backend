class CashPaymentHandler:
    def create_payment(self, *, amount, reference: str, metadata: dict | None = None) -> dict:
        return {
            "provider": "cash",
            "reference": reference,
            "amount": str(amount),
            "status": "manual",
            "metadata": metadata or {},
        }
