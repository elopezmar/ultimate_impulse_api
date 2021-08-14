class BusinessError(Exception):
    def __init__(self, message, status_code):
        self.message = {'message': message}, status_code
