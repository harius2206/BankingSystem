from entities import Client


class ClientBrowsingModel:
    """Модель для відображення у списку (Task 2)"""

    def __init__(self, entity: Client):
        self.id = entity.id
        self.full_name = f"{entity.first_name} {entity.last_name}"
        self.tax_id = entity.tax_id


class ClientEditingModel:
    """Модель для створення та редагування (Task 3, 4)"""

    def __init__(self, entity: Client = None):
        if entity:
            self.id = entity.id
            self.first_name = entity.first_name
            self.last_name = entity.last_name
            self.tax_id = entity.tax_id
        else:
            self.id = 0
            self.first_name = ""
            self.last_name = ""
            self.tax_id = ""

    def to_entity(self) -> Client:
        """Перетворює модель назад у сутність Client"""
        return Client(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            tax_id=self.tax_id
        )

    def load_from_form(self, form_data):
        """Заповнює модель даними з HTML-форми"""
        self.first_name = form_data.get('first_name')
        self.last_name = form_data.get('last_name')
        self.tax_id = form_data.get('tax_id')
        if form_data.get('id'):
            self.id = int(form_data.get('id'))