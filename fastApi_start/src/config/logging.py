import logging
import sys
import os
from loguru import logger

def setup_logging():
    # Получаем уровень логирования из переменных окружения (по умолчанию INFO)
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    # Удаляем все стандартные обработчики logging
    logging.root.handlers = []

    # Настраиваем перехват логов стандартной библиотеки logging
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Получаем соответствующий уровень loguru, если он существует
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Находим место, откуда пришло сообщение
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

    # Устанавливаем наш обработчик для корня
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # Настраиваем логирование для uvicorn
    for logger_name in ("uvicorn", "uvicorn.access", "uvicorn.error"):
        mod_logger = logging.getLogger(logger_name)
        mod_logger.handlers = [InterceptHandler()]
        mod_logger.propagate = False

    # Настраиваем формат вывода для loguru
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level
    )

    logger.info(f"Logging has been successfully configured with level: {log_level}")
