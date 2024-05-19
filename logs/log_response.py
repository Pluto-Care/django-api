class LogResponse:
    def __init__(self, status, message=None):
        self.status = status
        self.message = message

    def serialize(self):
        result = {"s": self.status}
        if self.message:
            result["m"] = self.message
        return result
