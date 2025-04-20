import logging
import sys


# class RequestLogger:
#     def __init__(self):
#         self.logger = logging.getLogger(__name__)
#         self.logger.setLevel(logging.DEBUG)

#     # def setup_logger(self):

#         formatter = logging.Formatter(
#             "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
#         )

#         console_handler = logging.StreamHandler(sys.stdout)
#         console_handler.setLevel(logging.DEBUG)
#         console_handler.setFormatter(formatter)

#         file_handler = logging.FileHandler("logs/request.log", mode="w")
#         file_handler.setLevel(logging.DEBUG)
#         file_handler.setFormatter(formatter)

#         self.logger.addHandler(console_handler)
#         self.logger.addHandler(file_handler)

#     def debug(self, message):
#         self.logger.debug(message)

#     def info(self, message):
#         self.logger.info(message)

#     def warning(self, message):
#         self.logger.warning(message)

#     def error(self, message):
#         self.logger.error(message)

#     def exeption(self, message):
#         self.logger.error(message, exc_info=True)


import logging

class ColorFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self._colors = {
            logging.DEBUG: self.fmt,
            logging.INFO: f"\033[36m{self.fmt}\033[0m",
            logging.WARNING: f"\033[33m{self.fmt}\033[0m",
            logging.ERROR: f"\033[31m{self.fmt}\033[0m",
            logging.CRITICAL: f"\033[1m\033[35m{self.fmt}\033[0m",
        }

    def format(self, record):
        log_fmt = self._colors.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Форматтер для файла БЕЗ цветов
    # file_formatter = logging.Formatter(
    #     fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    # )

    # Создаем обработчик для вывода логов в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColorFormatter())
    logger.addHandler(console_handler)

    # Создаем обработчик для записи логов в файл
    file_handler = logging.FileHandler("logs/request.log", mode="w")
    file_handler.setFormatter(ColorFormatter())
    logger.addHandler(file_handler)
    return logger

logger: logging.Logger = setup_logger()

def debug(message):
    logger.debug(message)

def info(message):
    logger.info(message)

def warning(message):
    logger.warning(message)

def error(message):
    logger.error(message)

def exception(message):
    logger.error(message, exc_info=True)

