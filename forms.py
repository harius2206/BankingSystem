from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange


class ClientForm(FlaskForm):
    """
    Форма для створення/редагування клієнта.
    Аналог ClientEditingModel з атрибутами валідації.
    """
    first_name = StringField('Ім\'я', validators=[
        DataRequired(message="Потрібно заповнити поле 'Ім'я'"),
        Length(min=2, max=50, message="Ім'я має містити від 2 до 50 символів")
    ])

    last_name = StringField('Прізвище', validators=[
        DataRequired(message="Потрібно заповнити поле 'Прізвище'"),
        Length(min=2, max=50, message="Прізвище має містити від 2 до 50 символів")
    ])

    tax_id = StringField('ІПН (Податковий номер)', validators=[
        DataRequired(message="Потрібно заповнити поле 'ІПН'"),
        Length(min=8, max=12, message="ІПН має містити 8-12 цифр"),
        Regexp(r'^\d+$', message="ІПН повинен складатися лише з цифр")
    ])


class AccountForm(FlaskForm):
    """
    Форма для створення рахунку (Завдання 3 - випадаючі списки).
    """
    client_id = SelectField('Клієнт', coerce=int, validators=[
        DataRequired(message="Оберіть клієнта зі списку")
    ])

    currency = SelectField('Валюта', choices=[('UAH', 'Гривня'), ('USD', 'Долар'), ('EUR', 'Євро')], validators=[
        DataRequired()
    ])

    balance = FloatField('Початковий баланс', validators=[
        NumberRange(min=0, message="Баланс не може бути від'ємним")
    ])