from flask import Flask, render_template, g
from data_context import DataContext
from unit_of_work import FileUnitOfWork

app = Flask(__name__)



def get_uow():
    """
    Створює або повертає UnitOfWork для поточного запиту.
    У Flask g - це об'єкт для зберігання даних у межах одного запиту.
    """
    if 'uow' not in g:
        context = DataContext("banking_data.json")
        if not context.clients:
            context.create_testing_data()
            context.save_changes()

        g.uow = FileUnitOfWork(context)
    return g.uow


@app.teardown_appcontext
def close_connection(exception):
    """Закриваємо з'єднання (якщо потрібно) після завершення запиту"""
    uow = g.pop('uow', None)



@app.route('/')
def index():
    """Аналог HomeController.Index"""
    return render_template('index.html', title="Головна")


@app.route('/about')
def about():
    """Аналог HomeController.About"""
    return render_template('about.html', title="Про сайт")


@app.route('/clients')
def clients_info():
    """
    Аналог CountriesController.ObjectsInfo.
    Відображає список клієнтів.
    """
    uow = get_uow()
    clients = uow.clients.get_all()
    return render_template('clients.html', clients=clients, title="Клієнти банку")


@app.context_processor
def utility_processor():
    """
    Дозволяє викликати Python-функції прямо з шаблонів.
    Аналог @Html.Action або Partial Method.
    """

    def get_client_accounts(client_id):
        uow = get_uow()
        all_accounts = uow.accounts.get_all()
        return [acc for acc in all_accounts if acc.client_id == client_id]

    return dict(get_client_accounts=get_client_accounts)


if __name__ == '__main__':
    app.run(debug=True)