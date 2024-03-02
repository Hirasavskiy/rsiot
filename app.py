from flask import Flask, request, jsonify, render_template, redirect
from models.database import execute_query, execute_non_query

app = Flask(__name__)

# Функция для проверки существования транспортного средства с заданным ID
def vehicle_exists(vehicle_id):
    query = "SELECT COUNT(*) FROM vehicles WHERE id = ?"
    # Формируем запрос с параметрами
    params = (vehicle_id,)
    result = execute_query(query, params).fetchone()
    return result[0] > 0


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/delete_vehicle', methods=['GET', 'POST'])
def delete_vehicle():
    if request.method == 'POST':
        vehicle_id = request.form.get('vehicle_id')
        # Проверяем существование транспортного средства с заданным ID
        if not vehicle_exists(vehicle_id):
            return "Vehicle with provided ID does not exist", 404

        # Выполняем удаление транспортного средства с заданным ID
        query = "DELETE FROM vehicles WHERE id = ?"
        params = (vehicle_id,)
        execute_non_query(query, params)

        return redirect('/vehicles')  # Перенаправляем пользователя на страницу с транспортными средствами

    return render_template('delete_vehicle.html')

@app.route('/add_vehicle')
def add_vehicle_form():
    return render_template('add_vehicle.html')

@app.route('/edit_vehicle')
def edit_vehicle_form():
    return render_template('edit_vehicle.html')

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    query = "SELECT * FROM vehicles"
    cursor = execute_query(query)
    vehicles = cursor.fetchall()
    return render_template('vehicles.html', vehicles=vehicles)

# Маршрут для добавления нового транспортного средства
@app.route('/vehicles', methods=['POST'])
def add_vehicle():
    data = request.get_json()
    brand = data['brand']
    model = data['model']
    year = data['year']
    license_plate = data['license_plate']
    vehicle_type = data['vehicle_type']

    query = "INSERT INTO vehicles (brand, model, year, license_plate, vehicle_type) VALUES (?, ?, ?, ?, ?)"
    params = (brand, model, year, license_plate, vehicle_type)
    execute_non_query(query, params)
    return redirect('/vehicles')
    #return 'Vehicle added successfully', 201

@app.route('/edit_vehicle', methods=['POST'])
def edit_vehicle():
    data = request.form
    vehicle_id = data['vehicle_id']
    brand = data['brand']
    model = data['model']
    year = data['year']
    license_plate = data['license_plate']
    vehicle_type = data['vehicle_type']

    query = "UPDATE vehicles SET brand = ?, model = ?, year = ?, license_plate = ?, vehicle_type = ? WHERE id = ?"
    params = (brand, model, year, license_plate, vehicle_type, vehicle_id)
    execute_non_query(query, params)

    return redirect('/vehicles')

if __name__ == '__main__':
    app.run(debug=True)
