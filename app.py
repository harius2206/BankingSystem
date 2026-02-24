from flask import Flask, render_template, g, request, redirect, url_for
from data_context import DataContext
from unit_of_work import FileUnitOfWork
from view_models import ClientBrowsingModel, ClientEditingModel

app = Flask(__name__)



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



@app.route('/')
def index():
    return render_template('index.html', title="Головна")


@app.route('/about')
def about():
    return render_template('about.html', title="Про сайт")



@app.route('/clients')
def clients_index():
    uow = get_uow()
    raw_clients = uow.clients.get_all()

    browsing_models = [ClientBrowsingModel(c) for c in raw_clients]

    return render_template('clients/index.html',
                           clients=browsing_models,
                           title="Список клієнтів")


@app.route('/clients/details/<int:id>')
def clients_details(id):
    uow = get_uow()
    client = uow.clients.get_by_id(id)
    if not client:
        return "Клієнта не знайдено", 404

    model = ClientEditingModel(client)
    return render_template('clients/details.html', model=model, title="Деталі клієнта")


@app.route('/clients/create', methods=['GET', 'POST'])
def clients_create():
    if request.method == 'POST':
        model = ClientEditingModel()
        model.load_from_form(request.form)

        uow = get_uow()
        new_client = model.to_entity()
        uow.clients.add(new_client)
        uow.save()

        return redirect(url_for('clients_index'))

    model = ClientEditingModel()  # Порожня модель
    return render_template('clients/create.html', model=model, title="Створити клієнта")


@app.route('/clients/edit/<int:id>', methods=['GET', 'POST'])
def clients_edit(id):
    uow = get_uow()
    client = uow.clients.get_by_id(id)

    if not client:
        return "Клієнта не знайдено", 404

    if request.method == 'POST':
        model = ClientEditingModel()
        model.load_from_form(request.form)
        model.id = id

        updated_entity = model.to_entity()
        uow.clients.update(updated_entity)
        uow.save()

        return redirect(url_for('clients_index'))

    model = ClientEditingModel(client)
    return render_template('clients/edit.html', model=model, title="Редагування клієнта")


# Task 5: Delete (Видалення)
@app.route('/clients/delete/<int:id>', methods=['GET', 'POST'])
def clients_delete(id):
    uow = get_uow()
    client = uow.clients.get_by_id(id)

    if not client:
        return "Клієнта не знайдено", 404

    if request.method == 'POST':
        uow.clients.delete(id)
        uow.save()
        return redirect(url_for('clients_index'))

    model = ClientBrowsingModel(client)
    return render_template('clients/delete.html', model=model, title="Видалення клієнта")



@app.context_processor
def utility_processor():
    def get_client_accounts(client_id):
        uow = get_uow()
        all_accounts = uow.accounts.get_all()
        return [acc for acc in all_accounts if acc.client_id == client_id]

    return dict(get_client_accounts=get_client_accounts)


if __name__ == '__main__':
    app.run(debug=True)