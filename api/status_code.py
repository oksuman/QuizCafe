from enum import Enum


class StatusCode(Enum):
    C20000 = (200, "C20000", "OK"),

    C40000 = (400, "C40000", "ERROR"),

    C50000 = (500, "C50000", "System Error"),

    @property
    def code(self):
        return self.value[0][1]

    @property
    def message(self):
        return self.value[0][2]

    def response(self):
        return {
            "response_code": self.code,
            "response_message": self.message
        }
