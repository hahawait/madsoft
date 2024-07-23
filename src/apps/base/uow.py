from tortoise.transactions import in_transaction


class BaseUOW:
    def __init__(self):
        self.transaction = in_transaction
