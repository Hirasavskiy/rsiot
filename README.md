# Описание структуры проекта
app.y - основной файл проекта
index.html - основной интерфейс
delete_vehicle.html - удаление элемента
add_vehicle.html - добавить элемент

# Запуск проекта

1. Запустить PyCharm
2. Установить нужные библиотеки
3. Создать БД с соответствующим названием
4. Скомпилировать app.py

# Блок заданий
1. **Нумерованный список**: Опишите шаги, необходимые для
приготовления вашего любимого блюда, используя нумерованный список
Markdown.
2.  **Изображения**: Вставьте изображение своего любимого пейзажа
или питомца в документ Markdown.
3. **Горизонтальная линия**: Вставьте горизонтальную линию для
разделения разделов вашего документа.
4. **Блочный код**: Вставьте крупный фрагмент кода в ваш документ,
используя блочное форматирование Markdown
5.**Список объемных текстов**: Вставьте длинный текст, состоящий из
нескольких абзацев, в виде списка с помощью Markdown.



# Рецепт моего любимого блюда: Паста Карбонара

## 1. Приготовление пасты Карбонара

1. Нагрейте кастрюлю с водой до кипения.
2. Добавьте соль в кипящую воду.
3. Положите пасту в кипящую воду и варите до готовности согласно инструкции на упаковке.
4. В то время как паста варится, подготовьте соус.

## 2. Приготовление соуса Карбонара

1. Нагрейте сковороду на среднем огне.
2. Добавьте мелко нарезанный бекон и обжарьте до золотистого цвета.
3. Добавьте нарубленный чеснок и обжаривайте до аромата.
4. В другой миске взбейте яйца, сыр пармезан и черный перец.
5. Откиньте вареную пасту на дуршлаг, затем добавьте ее в сковороду с беконом и чесноком.
6. Перемешайте пасту с беконом и чесноком, затем добавьте смесь яиц и сыра.
7. Постоянно помешивайте, пока соус не загустеет.

---

![Любимое животное](cat.jpg)
*Животное, которое я обожаю*

---

```python
from flask import Flask, request, jsonify, render_template, redirect
from models.database import execute_query, execute_non_query

app = Flask(__name__, template_folder='.')

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

    # Получаем имена столбцов из cursor.description
    columns = [column[0] for column in cursor.description]

    # Преобразуем каждую строку в словарь, используя имена столбцов
    vehicles = []
    for row in cursor:
        vehicle_dict = {}
        for i in range(len(columns)):
            vehicle_dict[columns[i]] = row[i]
        vehicles.append(vehicle_dict)

    return jsonify(vehicles)

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
```
- **Lorem ipsum dolor sit amet, consectetur adipiscing elit.** Donec ultricies dolor ut arcu posuere, nec suscipit libero fringilla.
- **Vestibulum vitae diam id sapien ullamcorper vehicula at a dolor.** Sed at nisi nec enim pharetra convallis sit amet sit amet lectus.
- **Nulla facilisi. Donec non feugiat mauris.** Sed sed mi feugiat, dapibus sapien nec, fringilla eros.
