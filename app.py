# Файл: app.py
from flask import Flask, render_template, g, request, redirect, url_for, flash
from data_context import DataContext
from unit_of_work import FileUnitOfWork
from view_models import ClientBrowsingModel
from entities import Client, Account  # Додаємо Account
from forms import ClientForm, AccountForm  # Імпортуємо наші форми

app = Flask(__name__)
# SECRET_KEY необхідний для роботи CSRF-захисту у Flask-WTF та flash-повідомлень
app.config['SECRET_KEY'] = 'your_secret_key_here_12345'


# --- Infrastructure ---
def get_uow():
    if 'uow' not in g:
        context = DataContext("banking_data.json")
        if not context.clients:
            context.create_testing_data()
            context.save_changes()
        g.uow = FileUnitOfWork(context)
    return g.uow


@app.teardown_appcontext
def close_connection(exception):
    g.pop('uow', None)


# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html', title="Головна")


@app.route('/about')
def about():
    return render_template('about.html', title="Про сайт")


# --- Clients CRUD ---

@app.route('/clients')
def clients_index():
    uow = get_uow()
    raw_clients = uow.clients.get_all()
    browsing_models = [ClientBrowsingModel(c) for c in raw_clients]
    return render_template('clients/index.html', clients=browsing_models, title="Список клієнтів")


@app.route('/clients/create', methods=['GET', 'POST'])
def clients_create():
    form = ClientForm()

    # form.validate_on_submit() перевіряє, чи це POST запит І чи валідні дані
    # Це аналог ModelState.IsValid у C#
    if form.validate_on_submit():
        uow = get_uow()

        # Створюємо сутність на основі даних форми
        new_client = Client(
            id=0,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            tax_id=form.tax_id.data
        )

        uow.clients.add(new_client)
        uow.save()

        # flash - аналог TempData["message"]
        flash(f"Клієнта '{new_client.first_name} {new_client.last_name}' успішно створено!", "success")
        return redirect(url_for('clients_index'))

    return render_template('clients/create.html', form=form, title="Створити клієнта")


@app.route('/clients/edit/<int:id>', methods=['GET', 'POST'])
def clients_edit(id):
    uow = get_uow()
    client = uow.clients.get_by_id(id)

    if not client:
        flash("Клієнта не знайдено", "danger")
        return redirect(url_for('clients_index'))

    # Заповнюємо форму даними з об'єкта (якщо це GET запит)
    form = ClientForm(obj=client)

    if form.validate_on_submit():
        # Оновлюємо поля сутності
        client.first_name = form.first_name.data
        client.last_name = form.last_name.data
        client.tax_id = form.tax_id.data

        uow.clients.update(client)
        uow.save()

        flash(f"Дані клієнта оновлено!", "success")
        return redirect(url_for('clients_index'))

    return render_template('clients/edit.html', form=form, client_id=id, title="Редагування клієнта")


@app.route('/clients/delete/<int:id>', methods=['GET', 'POST'])
def clients_delete(id):
    uow = get_uow()
    client = uow.clients.get_by_id(id)

    if not client:
        return "Клієнта не знайдено", 404

    if request.method == 'POST':
        uow.clients.delete(id)
        uow.save()
        flash("Клієнта видалено.", "warning")
        return redirect(url_for('clients_index'))

    model = ClientBrowsingModel(client)
    return render_template('clients/delete.html', model=model, title="Видалення клієнта")


# --- Accounts CRUD (Завдання 3: Випадаючі списки) ---

@app.route('/accounts/create', methods=['GET', 'POST'])
def accounts_create():
    uow = get_uow()
    form = AccountForm()

    # ЗАВДАННЯ 3: Заповнення випадаючого списку (Choices)
    # Отримуємо всіх клієнтів для списку
    clients = uow.clients.get_all()
    # Формуємо список кортежів (id, label)
    form.client_id.choices = [(c.id, f"{c.first_name} {c.last_name} ({c.tax_id})") for c in clients]

    if form.validate_on_submit():
        new_account = Account(
            id=0,
            client_id=form.client_id.data,
            currency=form.currency.data,
            balance=form.balance.data
        )
        uow.accounts.add(new_account)
        uow.save()
        flash("Рахунок успішно відкрито!", "success")
        return redirect(url_for('clients_index'))  # Або на список рахунків

    return render_template('accounts/create.html', form=form, title="Відкрити рахунок")


@app.context_processor
def utility_processor():
    def get_client_accounts(client_id):
        uow = get_uow()
        all_accounts = uow.accounts.get_all()
        return [acc for acc in all_accounts if acc.client_id == client_id]

    return dict(get_client_accounts=get_client_accounts)


if __name__ == '__main__':
    app.run(debug=True)