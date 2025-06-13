from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
import json
from datetime import datetime
from functools import wraps
from pymongo import MongoClient
import random
import time
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = "каЙфМесС_СеКрЕтНыЙ_КлЮч_B_3_4аСа_Н04и"
app.jinja_env.globals.update(len=len, list=list)

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['kayfmess']
users = db['users']
messages = db['messages']
energy_logs = db['energy_logs']  # Логи "энергетика"

# Инициализация Flask-Mail
mail = Mail(app)

# Конфигурация из файла config.py
if os.environ.get('FLASK_ENV') == 'docker':
    from config import config
    app.config.from_object(config['docker'])
else:
    from config import config
    app.config.from_object(config['development'])

mail.init_app(app)

# Смешные сообщения для отображения при загрузке страницы
FUNNY_LOADING_MESSAGES = [
    "Загружаем байты кайфа...",
    "Будим сервер, он еще спит...",
    "Открываем банку энергетика для сервера...",
    "Синхронизируемся с космосом...",
    "Переводим клавиатуру в ночной режим...",
    "Проверяем уровень кайфа в системе...",
    "Выводим разработчика из-под кайфа..."
]

# Имитация задержек типа "я писал это в 3 часа ночи"
def random_delay():
    """Имитирует случайные лаги, как будто код писался в 3 часа ночи"""
    if random.random() < 0.1:  # 10% шанс на "баг" 
        time.sleep(random.uniform(0.2, 0.5))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        random_delay()  # Добавляем случайную задержку
        if "username" not in session:
            flash("Сначала войдите в систему, товарищ! Или вы слишком под кайфом?", "danger")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    random_delay()  # Имитация бага
    return redirect(url_for("messages_page"))

@app.route("/регистрация", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        
        existing_user = users.find_one({"username": username})
        
        if existing_user:
            flash("Товарищ, это имя уже занято другим кайфовым партийцем!", "danger")
        else:
            users.insert_one({
                "username": username,
                "password": password,
                "email": email,
                "energy_level": random.randint(50, 100),
                "created_at": datetime.now()
            })
            
            # Запись в журнал энергетика
            energy_logs.insert_one({
                "event": "new_user",
                "username": username,
                "timestamp": datetime.now(),
                "note": f"Новый участник вечеринки в 3 часа ночи: {username}"
            })
            
            # Отправляем приветственное письмо
            if email:
                try:
                    welcome_msg = Message(
                        "Добро пожаловать в КайфМесс!",
                        recipients=[email]
                    )
                    welcome_msg.body = f"""
Привет, {username}!

Добро пожаловать в КайфМесс - мессенджер, созданный в 3 часа ночи под энергетиком!

Твой уровень энергии: {random.randint(50, 100)}%

Продолжай кайфовать!
Команда КайфМесс
"""
                    welcome_msg.html = f"""
<h2>Привет, {username}!</h2>
<p>Добро пожаловать в <strong>КайфМесс</strong> - мессенджер, созданный в 3 часа ночи под энергетиком!</p>
<p>Твой уровень энергии: <span style="color: green;">{random.randint(50, 100)}%</span></p>
<p>Продолжай кайфовать!</p>
<p><em>Команда КайфМесс</em></p>
"""
                    mail.send(welcome_msg)
                except Exception as e:
                    print(f"Ошибка отправки email: {str(e)}")
            
            flash("Партбилет выдан успешно! Энергетик вручен. Теперь войдите в систему.", "success")
            return redirect(url_for("login"))
    
    return render_template("register.html", loading_message=random.choice(FUNNY_LOADING_MESSAGES))

@app.route("/вход", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = users.find_one({"username": username, "password": password})
        
        if user:
            session["username"] = username
            session["energy_level"] = user.get("energy_level", 100)
            
            # Понижаем уровень энергетика пользователя при каждом входе
            new_energy = max(10, session["energy_level"] - random.randint(1, 10))
            users.update_one({"username": username}, {"$set": {"energy_level": new_energy}})
            
            flash(f"Товарищ {username}, добро пожаловать в КайфМесс! Ваш уровень энергетика: {new_energy}%", "success")
            return redirect(url_for("messages_page"))
        else:
            flash("Неверное имя или пароль! Или энергетик закончился в 3 часа ночи...", "danger")
    
    return render_template("login.html", loading_message=random.choice(FUNNY_LOADING_MESSAGES))

@app.route("/выход")
def logout():
    if "username" in session:
        username = session.pop("username")
        energy_logs.insert_one({
            "event": "logout",
            "username": username,
            "timestamp": datetime.now(),
            "note": f"Пользователь {username} отключился. Видимо, энергетик кончился."
        })
        flash(f"До свидания, товарищ {username}! Партия будет скучать и продолжать пить энергетики!", "info")
    return redirect(url_for("login"))

@app.route("/сообщения")
@login_required
def messages_page():
    # Добавляем искусственные баги время от времени
    if random.random() < 0.05:  # 5% шанс на "баг"
        time.sleep(random.uniform(0.5, 1.0))
    
    # Получаем все сообщения из базы данных в обратном хронологическом порядке
    message_list = list(messages.find().sort("timestamp", -1))
    
    # Понижаем энергию пользователя
    if "username" in session:
        users.update_one(
            {"username": session["username"]}, 
            {"$inc": {"energy_level": -1}}
        )
        
        # Получаем обновленную энергию
        user = users.find_one({"username": session["username"]})
        session["energy_level"] = user.get("energy_level", 0)
        
        # Случайное забавное событие
        if random.random() < 0.1:  # 10% шанс
            funny_events = [
                "Вы случайно пролили энергетик на клавиатуру!",
                "В вашем энергетике закончился кофеин!",
                "Вы задремали над клавиатурой на 5 секунд!",
                "Вы начали слышать голоса компилятора!"
            ]
            flash(random.choice(funny_events), "warning")
    
    return render_template("messages.html", 
                          messages=message_list,
                          energy_level=session.get("energy_level", 0),
                          loading_message=random.choice(FUNNY_LOADING_MESSAGES))

@app.route("/отправить", methods=["POST"])
@login_required
def send_message():
    content = request.form.get("content")
    if content and content.strip():
        # Иногда "глючим" текст (как будто в 3 часа ночи опечатки)
        if random.random() < 0.15:  # 15% шанс на "опечатку"
            typos = {"а": "о", "о": "а", "е": "и", "и": "е", "т": "д", "с": "з"}
            for char, replacement in typos.items():
                if char in content and random.random() < 0.3:
                    content = content.replace(char, replacement, 1)
        
        # Добавление нового сообщения в MongoDB
        message = {
            "username": session["username"],
            "content": content,
            "timestamp": datetime.now(),
            "likes": 0,
            "dislikes": 0,
            "written_at": "3 часа ночи" if 1 <= datetime.now().hour <= 5 else f"{datetime.now().hour} часов дня/ночи",
            "energy_level": session.get("energy_level", 100)
        }
        
        messages.insert_one(message)
        
        # Если это важное сообщение (содержит ключевые слова), отправляем уведомление админу
        important_keywords = ["срочно", "важно", "критично", "сбой", "ошибка", "падение"]
        if any(keyword in content.lower() for keyword in important_keywords):
            try:
                admin_email = os.environ.get('ADMIN_EMAIL') or 'admin@qndk.fun'
                urgent_msg = Message(
                    "Важное сообщение в КайфМесс!",
                    recipients=[admin_email]
                )
                urgent_msg.body = f"""
Важное сообщение от пользователя {session['username']}:

{content}

Время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
"""
                mail.send(urgent_msg)
            except Exception as e:
                print(f"Ошибка отправки уведомления админу: {str(e)}")
        
        # Если у пользователя мало энергии, добавим энергетик
        if session.get("energy_level", 0) < 30:
            users.update_one(
                {"username": session["username"]},
                {"$inc": {"energy_level": random.randint(20, 50)}}
            )
            flash("Вы выпили еще энергетика! Теперь можно писать дальше!", "success")
        else:
            flash("Ваше послание отправлено в народ под кайфом!", "success")
    else:
        flash("Пустые сообщения запрещены указом партии! Пейте больше энергетиков!", "danger")
    
    return redirect(url_for("messages_page"))

@app.route("/оценить/<message_id>/<action>")
@login_required
def rate_message(message_id, action):
    try:
        from bson.objectid import ObjectId
        
        if action == "like":
            messages.update_one(
                {"_id": ObjectId(message_id)},
                {"$inc": {"likes": 1}}
            )
            flash("Вы выразили одобрение этому кайфу!", "success")
        elif action == "dislike":
            messages.update_one(
                {"_id": ObjectId(message_id)},
                {"$inc": {"dislikes": 1}}
            )
            flash("Осторожно! У разработчика кончается энергетик, возможны перебои!", "warning")
    except Exception as e:
        flash(f"Произошла ошибка: {str(e)}. Видимо, в 3 часа ночи код не работает как надо!", "danger")
    
    return redirect(url_for("messages_page"))

@app.route("/api/messages")
def api_messages():
    """API для получения сообщений в формате JSON"""
    message_list = list(messages.find().sort("timestamp", -1))
    
    # Преобразуем ObjectId в строки для сериализации в JSON
    for msg in message_list:
        msg["_id"] = str(msg["_id"])
        msg["timestamp"] = msg["timestamp"].strftime("%d.%m.%Y %H:%M:%S")
    
    return jsonify(message_list)

@app.route("/api/energy")
def api_energy():
    """API для получения статистики энергетиков"""
    energy_stats = {
        "total_users": users.count_documents({}),
        "average_energy": list(users.aggregate([
            {"$group": {"_id": None, "avg": {"$avg": "$energy_level"}}}
        ]))[0]["avg"],
        "message_count": messages.count_documents({}),
        "night_owl_count": users.count_documents({"created_at": {"$gte": datetime(datetime.now().year, datetime.now().month, datetime.now().day, 1, 0), 
                                                             "$lte": datetime(datetime.now().year, datetime.now().month, datetime.now().day, 5, 0)}})
    }
    return jsonify(energy_stats)

@app.route("/о_нас")
def about():
    stats = {
        "users_count": users.count_documents({}),
        "messages_count": messages.count_documents({}),
        "night_messages": messages.count_documents({"written_at": "3 часа ночи"}),
        "energy_consumed": random.randint(100, 500)
    }
    return render_template("about.html", stats=stats, loading_message=random.choice(FUNNY_LOADING_MESSAGES))

@app.route("/энергетик")
@login_required
def energy_boost():
    """Страница для пополнения энергии"""
    if random.random() < 0.7:  # 70% шанс успеха
        energy_boost = random.randint(30, 70)
        users.update_one(
            {"username": session["username"]},
            {"$inc": {"energy_level": energy_boost}}
        )
        flash(f"Вы выпили энергетик и получили +{energy_boost} к энергии!", "success")
    else:
        flash("Энергетик оказался просроченным! Никакого эффекта.", "danger")
        
    return redirect(url_for("messages_page"))

@app.route("/отправить-тест", methods=["GET"])
@login_required
def send_test_email():
    """Тестовый маршрут для проверки работы Postfix"""
    # Получаем информацию о пользователе
    user = users.find_one({"username": session["username"]})
    
    if user and "email" in user and user["email"]:
        try:
            # Формируем текущее время
            current_time = datetime.now().strftime("%H:%M")
            hour = datetime.now().hour
            time_text = "3 часа ночи" if 1 <= hour <= 5 else f"{hour} часов"
            
            # Отправляем тестовое письмо через функцию уведомлений
            result = send_notification_email(
                to=user["email"],
                subject="Тестовое письмо от КайфМесс",
                template="email/notification",
                sender=session["username"],
                message="Это тестовое сообщение для проверки работы Postfix.<br>Если вы его получили, значит всё работает!",
                timestamp=time_text,
                urgent=False
            )
            
            if result:
                flash("Тестовое письмо отправлено успешно! Проверьте свою почту.", "success")
            else:
                flash("Произошла ошибка при отправке письма. Возможно, сервер слишком под кайфом!", "danger")
        except Exception as e:
            flash(f"Произошла ошибка: {str(e)}", "danger")
    else:
        flash("У вас не указан email. Пожалуйста, обновите свой профиль.", "warning")
    
    return redirect(url_for("messages_page"))

@app.errorhandler(404)
def page_not_found(e):
    error_messages = [
        "Страница потерялась в 3 часа ночи!",
        "Эту страницу съел энергетик!",
        "404 - Кайф не найден!",
        "Разработчик уснул, не дописав эту страницу!"
    ]
    return render_template("404.html", error_message=random.choice(error_messages)), 404

@app.errorhandler(500)
def server_error(e):
    error_messages = [
        "У сервера закончился энергетик!",
        "Сервер прилёг поспать в 3 часа ночи!",
        "500 - Слишком много кайфа для одного сервера!",
        "Перебор с энергетиками! Сервер на перезагрузке!"
    ]
    return render_template("500.html", error_message=random.choice(error_messages)), 500

# Функция для отправки уведомлений по email
def send_notification_email(to, subject, template, **kwargs):
    try:
        msg = Message(subject=subject, recipients=[to])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        
        # Добавляем случайную "фишку" в стиле приложения
        if random.random() < 0.3:  # 30% шанс на "фишку"
            msg.body += "\n\nP.S. Это сообщение было отправлено в 3 часа ночи под энергетиком!"
            msg.html += "<p><em>P.S. Это сообщение было отправлено в 3 часа ночи под энергетиком!</em></p>"
        
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Ошибка отправки email: {str(e)}")
        return False

if __name__ == "__main__":
    app.run(debug=True) 