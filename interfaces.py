from abc import ABC, abstractmethod
from typing import List, Optional
from entities import Client, Account, Transaction



class IRepository(ABC):
    """Базовий інтерфейс для всіх репозиторіїв"""

    @abstractmethod
    def get_all(self) -> List[object]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[object]:
        pass

    @abstractmethod
    def add(self, item: object):
        pass

    @abstractmethod
    def update(self, item: object):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass


class IClientRepository(IRepository):
    """Специфічні методи для клієнтів можна додати сюди"""
    pass


class IAccountRepository(IRepository):
    pass


class ITransactionRepository(IRepository):
    pass


class IUnitOfWork(ABC):
    @property
    @abstractmethod
    def clients(self) -> IClientRepository:
        pass

    @property
    @abstractmethod
    def accounts(self) -> IAccountRepository:
        pass

    @property
    @abstractmethod
    def transactions(self) -> ITransactionRepository:
        pass

    @abstractmethod
    def save(self):
        """Зберігає всі зміни"""
        pass

    @abstractmethod
    def __enter__(self):
        """Для підтримки контекстного менеджера (аналог IDisposable)"""
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Для підтримки контекстного менеджера"""
        pass