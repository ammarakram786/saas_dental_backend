from apps.billing.adapters.cash import CashPaymentHandler
from apps.billing.adapters.jazzcash import JazzCashAdapter


class PaymentGatewayFactory:
    @staticmethod
    def get(method: str):
        if method == "jazzcash":
            return JazzCashAdapter()
        if method == "cash":
            return CashPaymentHandler()
        raise ValueError(f"Unsupported payment method: {method}")
