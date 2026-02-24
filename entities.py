from datetime import datetime

class Client:
    def __init__(self, id: int, first_name: str, last_name: str, tax_id: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.tax_id = tax_id

    def __str__(self):
        return f"[Client] ID: {self.id}, Name: {self.first_name} {self.last_name}, TaxID: {self.tax_id}"

    def to_dict(self):
        return self.__dict__


class Account:
    def __init__(self, id: int, client_id: int, currency: str, balance: float = 0.0):
        self.id = id
        self.client_id = client_id
        self.currency = currency
        self.balance = balance

    def __str__(self):
        return f"[Account] ID: {self.id}, ClientID: {self.client_id}, Balance: {self.balance} {self.currency}"

    def to_dict(self):
        return self.__dict__


class Transaction:
    def __init__(self, id: int, from_account_id: int, to_account_id: int, amount: float, timestamp: str = None):
        self.id = id
        self.from_account_id = from_account_id
        self.to_account_id = to_account_id
        self.amount = amount
        self.timestamp = timestamp if timestamp else datetime.now().isoformat()

    def __str__(self):
        return f"[Transaction] ID: {self.id}, From: {self.from_account_id} -> To: {self.to_account_id}, Amount: {self.amount}, Time: {self.timestamp}"

    def to_dict(self):
        return self.__dict__