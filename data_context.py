
import json
import os
from typing import List
from entities import Client, Account, Transaction


class DataContext:
    def __init__(self, filename: str = "banking_data.json"):
        self.filename = filename
        self.clients: List[Client] = []
        self.accounts: List[Account] = []
        self.transactions: List[Transaction] = []

        self.load_data()

    def create_testing_data(self):
        """Створює початкові тестові дані, якщо база порожня"""
        if not self.clients:
            self.clients.append(Client(1, "Іван", "Петренко", "1234567890"))
            self.clients.append(Client(2, "Марія", "Коваленко", "0987654321"))
            self.accounts.append(Account(1, 1, "UAH", 15000.00))
            self.accounts.append(Account(2, 2, "USD", 500.00))
            print("Тестові дані створено.")

    def save_changes(self):
        """Зберігає поточний стан списків у файл (Commit)"""
        data = {
            "clients": [c.to_dict() for c in self.clients],
            "accounts": [a.to_dict() for a in self.accounts],
            "transactions": [t.to_dict() for t in self.transactions]
        }
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Дані успішно збережено у {self.filename}")

    def load_data(self):
        """Завантажує дані з файлу"""
        if not os.path.exists(self.filename):
            return

        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

                self.clients = [Client(**item) for item in data.get("clients", [])]
                self.accounts = [Account(**item) for item in data.get("accounts", [])]
                self.transactions = [Transaction(**item) for item in data.get("transactions", [])]
        except Exception as e:
            print(f"Помилка читання файлу: {e}")