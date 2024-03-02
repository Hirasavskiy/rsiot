import pytest
from selenium import webdriver
from flask_testing import LiveServerTestCase
from app import app
from models.database import execute_query


@pytest.fixture(scope='module')
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_add_vehicle(client):
    data = {
        'brand': 'Toyota',
        'model': 'Camry',
        'year': 2022,
        'license_plate': 'ABC123',
        'vehicle_type': 'Sedan'
    }
    response = client.post('/vehicles', json=data)
    assert response.status_code == 302
    # Дополнительные проверки на успешное добавление данных в базу, если необходимо


def test_delete_vehicle(client):
    # Добавляем транспортное средство для последующего удаления
    data = {
        'brand': 'TestBrand',
        'model': 'TestModel',
        'year': 2023,
        'license_plate': 'TEST123',
        'vehicle_type': 'TestType'
    }
    add_response = client.post('/vehicles', json=data)
    assert add_response.status_code == 302  # Проверяем успешность добавления

    # Получаем id добавленного транспортного средства
    # Мы можем получить его из URL редиректа или из базы данных, если у вас есть доступ к ней
    vehicle_id = get_last_vehicle_id_from_database()  # Функция, возвращающая id последнего добавленного транспортного средства

    # Удаляем добавленное транспортное средство
    delete_response = client.post('/delete_vehicle', data={'vehicle_id': vehicle_id})
    assert delete_response.status_code == 302  # Проверяем успешность удаления

def get_last_vehicle_id_from_database():
    query = "SELECT TOP 1 id FROM vehicles ORDER BY id DESC"
    result = execute_query(query).fetchone()
    if result:
        return result[0]  # Возвращаем последний id
    else:
        return None  # Возвращаем None, если база данных пуста

def test_edit_vehicle(client):
    data = {
        'vehicle_id': 1,
        'brand': 'Toyota',
        'model': 'Corolla',
        'year': 2021,
        'license_plate': 'XYZ456',
        'vehicle_type': 'Sedan'
    }
    response = client.post('/edit_vehicle', data=data)
    assert response.status_code == 302
    # Дополнительные проверки на успешное редактирование данных в базе, если необходимо

def test_get_vehicles(client):
    response = client.get('/vehicles')
    assert response.status_code == 200
    # Дополнительные проверки на корректность списка транспортных средств, если необходимо

def test_interface_display():
    driver = webdriver.Firefox()  # Используйте нужный вам драйвер
    driver.get("http://127.0.0.1:5000/vehicles")  # Предполагаем, что ваше приложение запущено локально
    assert "Список транспортных средств" in driver.title
    # Дополнительные проверки на корректное отображение данных в интерфейсе, если необходимо
    driver.quit()

def test_add_vehicle_page(client):
    response = client.get('/add_vehicle')
    assert response.status_code == 200
    assert "Добавить новое транспортное средство" in response.data.decode('utf-8')  # Проверяем наличие текста "Add Vehicle" на странице
    # Дополнительные проверки на наличие нужных полей в форме, если необходимо

def test_edit_vehicle_page(client):
    response = client.get('/edit_vehicle')
    assert response.status_code == 200
    assert "Изменить транспортное средство" in response.data.decode('utf-8')  # Проверяем наличие текста "Edit Vehicle" на странице
    # Дополнительные проверки на наличие нужных полей в форме и данных для редактирования, если необходимо

def test_delete_vehicle_page(client):
    response = client.get('/delete_vehicle')
    assert response.status_code == 200
    assert "Удалить транспортное средство" in response.data.decode('utf-8')  # Проверяем наличие текста "Delete Vehicle" на странице
    # Дополнительные проверки на наличие нужных элементов на странице, если необходимо
