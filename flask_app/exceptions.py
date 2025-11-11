class OrderNotFound(Exception):
    def __init__(self, detail: str | None = None):
        self.detail = detail
        super().__init__(detail or "Order not found")


class InvalidPayment(Exception):
    def __init__(self, detail: str | None = None):
        self.detail = detail
        super().__init__(detail or "Invalid payment")
