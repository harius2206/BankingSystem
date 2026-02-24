
from typing import List, Optional
from interfaces import IClientRepository, IAccountRepository, ITransactionRepository
from entities import Client, Account, Transaction

class BaseRepository:
    """Базовий клас для реалізації спільної логіки CRUD"""
    def __init__(self, collection: list):
        self._collection = collection

    def get_all(self) -> List[object]:
        return self._collection

    def get_by_id(self, id: int) -> Optional[object]:
        return next((item for item in self._collection if item.id == id), None)

    def delete(self, id: int):
        item = self.get_by_id(id)
        if item:
            self._collection.remove(item)

    def _generate_id(self) -> int:
        if not self._collection:
            return 1
        return max(item.id for item in self._collection) + 1


class ClientRepository(BaseRepository, IClientRepository):
    def add(self, item: Client):
        item.id = self._generate_id()
        self._collection.append(item)

    def update(self, item: Client):
        existing = self.get_by_id(item.id)
        if existing:
            existing.first_name = item.first_name
            existing.last_name = item.last_name
            existing.tax_id = item.tax_id


class AccountRepository(BaseRepository, IAccountRepository):
    def add(self, item: Account):
        item.id = self._generate_id()
        self._collection.append(item)

    def update(self, item: Account):
        existing = self.get_by_id(item.id)
        if existing:
            existing.client_id = item.client_id
            existing.currency = item.currency
            existing.balance = item.balance


class TransactionRepository(BaseRepository, ITransactionRepository):
    def add(self, item: Transaction):
        item.id = self._generate_id()
        self._collection.append(item)

    def update(self, item: Transaction):
        existing = self.get_by_id(item.id)
        if existing:
            existing.amount = item.amount
            existing.timestamp = item.timestamp