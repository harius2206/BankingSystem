from interfaces import IUnitOfWork
from data_context import DataContext
from repositories import ClientRepository, AccountRepository, TransactionRepository

class FileUnitOfWork(IUnitOfWork):
    def __init__(self, data_context: DataContext):
        self._context = data_context
        self._clients_repo = ClientRepository(self._context.clients)
        self._accounts_repo = AccountRepository(self._context.accounts)
        self._transactions_repo = TransactionRepository(self._context.transactions)

    @property
    def clients(self):
        return self._clients_repo

    @property
    def accounts(self):
        return self._accounts_repo

    @property
    def transactions(self):
        return self._transactions_repo

    def save(self):
        """Викликає метод збереження у контексті даних"""
        self._context.save_changes()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass