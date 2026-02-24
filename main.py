from data_context import DataContext
from unit_of_work import FileUnitOfWork
from entities import Client, Account, Transaction


def print_collection(collection, title):
    print(f"\n--- {title} ---")
    for item in collection:
        print(item)


def study_uow():
    print("=== Study UOW (Banking System) ===")

    context = DataContext()
    context.create_testing_data()

    with FileUnitOfWork(context) as uow:
        print_collection(uow.clients.get_all(), "Клієнти (Початкові)")
        print_collection(uow.accounts.get_all(), "Рахунки (Початкові)")

        new_client = Client(0, "Олег", "Вінник", "111222333")
        uow.clients.add(new_client)
        print(f"\nДодано нового клієнта: {new_client.first_name}")

        acc1 = uow.accounts.get_by_id(1)
        acc2 = uow.accounts.get_by_id(2)

        if acc1 and acc2:
            amount = 100.0
            acc1.balance -= amount
            acc2.balance += amount * 40

            uow.accounts.update(acc1)
            uow.accounts.update(acc2)

            trans = Transaction(0, acc1.id, acc2.id, amount)
            uow.transactions.add(trans)
            print("\nВиконано транзакцію та оновлено баланси.")

        print_collection(uow.clients.get_all(), "Клієнти (Після змін)")
        print_collection(uow.accounts.get_all(), "Рахунки (Після змін)")
        print_collection(uow.transactions.get_all(), "Транзакції (Нові)")

        print("\nЗбереження даних у файл...")
        uow.save()


def verify_saved_data():
    """Метод для перевірки, що дані дійсно збереглись у файл"""
    print("\n=== Перевірка збережених даних (Новий контекст) ===")
    new_context = DataContext()
    with FileUnitOfWork(new_context) as uow:
        print_collection(uow.clients.get_all(), "Клієнти з файлу")
        print_collection(uow.transactions.get_all(), "Транзакції з файлу")


if __name__ == "__main__":
    study_uow()
    verify_saved_data()