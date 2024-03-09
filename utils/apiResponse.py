class ApiResponse:
    def __init__(self, status, message, data):
        self.status = status
        self.message = message
        self.data = data

    def __str__(self):
        return f"status: {self.status}, message: {self.message}, data: {self.data}"

    def convert_to_dict(self):
        return {"status": self.status, "message": self.message, "data": self.data}
