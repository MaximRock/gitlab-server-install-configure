import logging


class ColorFormatter(logging.Formatter):
    """
    ColorFormatter - это пользовательский форматтер для логирования, 
    который добавляет цвет к сообщениям журнала в зависимости от их уровня серьезности. 
    Он использует ANSI-коды для применения цветов к сообщениям журнала, 
    делая их более визуально различимыми в консоли.

    Атрибуты:
        COLORS (dict): Сопоставление уровней логирования с соответствующими ANSI-кодами
            цветов. Уровни и их цвета:
            - DEBUG: Белый
            - INFO: Голубой
            - WARNING: Желтый
            - ERROR: Красный
            - CRITICAL: Жирный пурпурный
        RESET (str): ANSI-код для сброса цветового форматирования.

    Методы:
        format(record):
            Форматирует запись журнала, применяя соответствующий цвет в зависимости
            от уровня логирования и добавляя код сброса в конце.
            Переопределяет метод `format` базового класса `logging.Formatter`.
    """
    COLORS = {
        logging.DEBUG: "\033[37m",  # white
        logging.INFO: "\033[36m",  # cyan
        logging.WARNING: "\033[33m",  # yellow
        logging.ERROR: "\033[31m",  # red
        logging.CRITICAL: "\033[1m\033[35m",  # bold magenta
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelno, "")
        message = super().format(record)
        return f"{color}{message}{self.RESET}"


class Logger:
    """
    Класс Logger предоставляет централизованный механизм логирования с поддержкой
    как консольного, так и файлового логирования. Он позволяет настраивать формат
    логов и уровень логирования.

    Методы:
        get_stream_handler():
            Создает и возвращает обработчик потоков для логирования в консоль.
            Обработчик использует цветной форматтер для улучшения читаемости.

        get_file_handler():
            Создает и возвращает обработчик для логирования в файл.
            Логи добавляются в файл 'logs/request.log' с указанным форматом.

        get_logger(name):
            Создает и возвращает экземпляр логгера с указанным именем.
            Логгер настраивается с обработчиками для консоли и файла, а также
            имеет уровень логирования DEBUG.
    """

    def __init__(self):
        self._log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"

    def get_stream_handler(self):
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(ColorFormatter(self._log_format))
        return stream_handler

    def get_file_handler(self):
        file_handler = logging.FileHandler("logs/request.log", mode="a")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(self._log_format))
        return file_handler

    def get_logger(self, name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.get_file_handler())
        logger.addHandler(self.get_stream_handler())
        logger.propagate = False
        return logger
