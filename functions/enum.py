class Repeat:
    def __init__(self):
        pass

    Yes = 1
    No = 0

    @staticmethod
    def validate(value):
        if not (value == Yes or value == No):
            raise ValueError("Repeat value should be Yes = 1 or No = 0")


class TranportType:
    def __init__(self):
        pass

    Email = 1
    WhatsApp = 2
    Messenger = 3
    Sms = 4
    Empty = 0

    @staticmethod
    def validate(value):
        if not (value < 5):
            raise ValueError("Transport value should be 0-Empty, 1-Email, 2-WhatsApp, 3-Messenger, 4-Sms")
