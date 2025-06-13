import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла (если существует)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Определяем окружение
env = os.environ.get('FLASK_ENV') or 'default'

# Импортируем приложение
from app import app

if __name__ == '__main__':
    # Запускаем приложение напрямую только в режиме отладки
    app.run(host='0.0.0.0', port=8000) 