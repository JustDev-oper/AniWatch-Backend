import logging
import logging.handlers
import os
from datetime import datetime

# Создаем директорию для логов, если её нет
LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Формат логов
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Настройка основного логгера
logger = logging.getLogger("AniWatch")
logger.setLevel(logging.INFO)

# Форматтер
formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

# Обработчик для файла (с ротацией)
file_handler = logging.handlers.RotatingFileHandler(
    os.path.join(LOGS_DIR, "anilist_api.log"),
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# Обработчик для консоли
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Добавляем обработчики к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Предотвращаем дублирование логов в случае вложенности
logger.propagate = False

# Экспортируем логгер
__all__ = ['logger']