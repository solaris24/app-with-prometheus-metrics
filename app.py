from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from prometheus_client import start_http_server, Counter, Summary, Gauge
import time
import random

# Запуск HTTP сервера для метрик Prometheus
start_http_server(8000)

# Создание счетчиков метрик
ORDERS_CREATED_COUNTER = Counter('orders_created_total', 'Total number of orders created')
ORDER_CREATION_DURATION = Summary('order_creation_duration_seconds', 'Duration of order creation in seconds')
HTTP_REQUEST_ERRORS = Counter('http_request_errors_total', 'Total number of HTTP request errors')
ACTIVE_REQUESTS = Gauge('active_requests', 'Number of active requests')

# Создание экземпляра Flask-приложения
app = Flask(__name__)

# Настройка подключения к базе данных SQLite в памяти с использованием Flask-SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Создание модели данных для таблицы заказов
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100))
    product_name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)

    def __init__(self, customer_name, product_name, quantity):
        self.customer_name = customer_name
        self.product_name = product_name
        self.quantity = quantity

# Маршрут для создания заказа
@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'GET':
        # Логика обработки GET-запроса на маршрут /order
        return 'This is a GET request to /order'
    elif request.method == 'POST':
        # Логика обработки POST-запроса на маршрут /order
        try:
            data = request.get_json()
            customer_name = data.get('customer_name')
            product_name = data.get('product_name')
            quantity = data.get('quantity')

            start_time = time.time()  # Get the current time before order creation
            
            # Introduce a random delay between 0 and 5 seconds
            delay = random.uniform(0, 5)
            time.sleep(delay)

            with app.app_context():
                order = Order(customer_name=customer_name, product_name=product_name, quantity=quantity)
                db.session.add(order)
                db.session.commit()

                elapsed_time = time.time() - start_time  # Calculate the elapsed time

                ORDERS_CREATED_COUNTER.inc()
                ORDER_CREATION_DURATION.observe(elapsed_time)

            return 'Order created successfully', 200
        except Exception as e:
            HTTP_REQUEST_ERRORS.inc()
            raise e
        finally:
            ACTIVE_REQUESTS.dec()

# Create the database tables
with app.app_context():
    db.create_all()


# Запуск Flask-приложения
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()