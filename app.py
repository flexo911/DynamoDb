from flask import Flask, jsonify
from main import *

app = Flask(__name__)


# Маршрут для отримання даних з DynamoDB
@app.route('/', methods=['GET'])
def get_items_():
    if table_exists('ExampleTable'):
        return get_db_items()
    else:
        return {'message': "table not isset"}

#  Створення таблиці в DynamoDB
@app.route('/create-table', methods=['GET'])
def create_table():
    return create_db_table()

#  Вставка 5 екземплярів з різними типами полів
@app.route('/add_items', methods=['GET'])
def add_items():
    if table_exists('ExampleTable'):
        return add_db_items()

    else:
        return {'message': "table not isset"}

# Оновлення даних
@app.route('/edit-item', methods=['GET'])
def edit_item():
    if table_exists('ExampleTable'):
        return edit_db_item()

    else:
        return {'message': "table not isset"}

# Додавання нового запису
@app.route('/add_item', methods=['GET'])
def add_item():
    if table_exists('ExampleTable'):
        return add_db_item()

    else:
        return {'message': "table not isset"}

# Отримання всього рядка за Partition Key та Sort Key
@app.route('/get_sorted_items', methods=['GET'])
def get_sorted_items():
    if table_exists('ExampleTable'):
        return get_db_sorted_items()

    else:
        return {'message': "table not isset"}


# Сканування всієї таблиці
@app.route('/get_scan_table', methods=['GET'])
def get_scan_table():
    if table_exists('ExampleTable'):
        return get_db_scan_table()

    else:
        return {'message': "table not isset"}

# фільтрація
@app.route('/get_filtered_table', methods=['GET'])
def get_filtered_table():
    if table_exists('ExampleTable'):
        return get_db_filtered_table()

    else:
        return {'message': "table not isset"}

if __name__ == '__main__':
    # Запуск Flask сервера на порту 5000
    app.run(host='0.0.0.0', port=9000)
