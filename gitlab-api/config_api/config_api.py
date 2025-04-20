import json
import os
import requests

from requests.exceptions import HTTPError
from urllib.parse import urljoin

from dotenv import load_dotenv
from config_api.logger import Logger


# from config_api.logger import RequestLogger


class ConfigApiGitlab:
    def __init__(self):
        """
        Инициализирует класс конфигурации API.

        Этот конструктор выполняет следующие действия:
        - Загружает переменные окружения из файла .env с использованием 
            функции `load_dotenv`.
        - Устанавливает доменное имя для API.
        - Определяет конечную точку API и версию.
        - Инициализирует контейнер для хранения данных.
        - Настраивает логгер для класса.

        Attributes:
            load_dotenv (bool): Указывает, были ли успешно загружены 
                переменные окружения.
            domain_name (str): Базовый URL API.
            api (str): Название конечной точки API.
            version (str): Версия API.
            data (None): Контейнер для хранения данных.
            logger (Logger): Экземпляр логгера для записи сообщений.
        """
        self.load_dotenv = load_dotenv()
        self.domain_name = "http://vagrant.max-rock.ru"
        self.api = "api"
        self.version = "v4"
        self.data = None
        self.logger = Logger().get_logger(__name__)


    def gitlab_token(self) -> str | None:
        """
        Извлекает токен GitLab из переменной окружения "GITLAB-TOKEN".
        Returns:
            str | None: Токен GitLab, если переменная окружения установлена.
        It calls:
            ValueError: Если переменная окружения "GITLAB-TOKEN" не установлена.
        """
        if not os.getenv("GITLAB-TOKEN"):
            raise ValueError('Environment variable "GITLAB-TOKEN not set!"')
        else:
            return os.getenv("GITLAB-TOKEN")

    def _validate_url_components(self) -> str:
        """
        Проверяет и формирует базовый URL из предоставленных компонентов.

        Этот метод выполняет следующие проверки:
        1. Убеждается, что обязательные компоненты (`domain_name`, `api` и `version`) 
            присутствуют.
           Если какой-либо из этих компонентов отсутствует, вызывается `ValueError` 
            с перечислением отсутствующих полей.
        2. Проверяет, что `domain_name` начинается с "http://" или "https://".
           Если это не так, вызывается `ValueError`.

        После проверки метод формирует и возвращает нормализованный базовый URL, 
        объединяя компоненты `domain_name`, `api` и `version`.

        Returns:
            str: Сформированный и нормализованный базовый URL.

        It calls:
            ValueError: Если какой-либо обязательный компонент отсутствует или 
            если `domain_name` не начинается с "http://" или "https://".
        """

        # Проверка обязательных полей
        if not all([self.domain_name, self.api, self.version]):
            missing = []
            if not self.domain_name:
                missing.append("domain_name")
            if not self.api:
                missing.append("api")
            if not self.version:
                missing.append("version")
            raise ValueError(
                f"Missing environment variables: {', '.join(missing)}"
            )  # Выводит список отсутствующих полей

        # Проверка формата domian_name
        if not self.domain_name.startswith(("http://", "https://")):
            raise ValueError('Domain must start with http:// or https://"')

        # Нормализация URL компонентов
        base_url: str = urljoin(
            urljoin(f"{self.domain_name}/", f"{self.api}/"), f"{self.version}/"
        )

        return base_url

    def base_url_api_gitlab(self, endpoint: str) -> str:
        """
        Формирует полный URL для API GitLab на основе указанного endpoint.
        Arguments:
            endpoint (str): Конкретный endpoint API, который нужно добавить 
                к базовому URL.
        Returns:
            str: Полный URL для указанного endpoint API GitLab.
        """
        url: str = f"{self._validate_url_components()}{endpoint}"
        return url

    def get_default_headers(self, **kwargs):
        """
        Генерирует заголовки по умолчанию для запросов к API GitLab.

        Этот метод создает словарь заголовков, которые будут использоваться 
            в запросах к API.
        Он включает приватный токен для аутентификации и позволяет добавлять 
        дополнительные заголовки через переданные аргументы.

        Arguments:
            **kwargs: Произвольные именованные аргументы, представляющие дополнительные
                  заголовки, которые нужно включить в запрос.

        Returns:
            dict: Словарь, содержащий заголовки по умолчанию, объединенные с любыми
              дополнительными заголовками, переданными в метод.
        """
        base_headers = {
            "PRIVATE-TOKEN": self.gitlab_token(),
            # "Content-Type": "application/json"
        }
        return {**base_headers, **kwargs}

    def make_request(self, method: str, endpoint: str, headers, **kwargs):
        """
        Отправляет HTTP-запрос к указанному endpoint, используя предоставленный метод, 
        заголовки и дополнительные параметры.

        Arguments:
            method (str): HTTP-метод для выполнения запроса 
                (например, 'GET', 'POST', 'PUT', 'DELETE').
            endpoint (str): Endpoint API, который нужно добавить к базовому URL.
            headers (dict): Словарь HTTP-заголовков, которые нужно включить в запрос.
            **kwargs: Дополнительные именованные аргументы, 
                передаваемые в метод `requests.request` (например, data, params, json).

        Returns:
            Response: Объект HTTP-ответа, возвращаемый библиотекой `requests`.

        Raises:
            HTTPError: Если HTTP-запрос возвращает неуспешный статус-код.
            Exception: Для любых других исключений, возникающих во время 
                выполнения запроса.

        Logs:
            - Debug: Логирует сформированный URL перед выполнением запроса.
            - Exception: Логирует любые HTTPError или другие исключения.
            - Info: Логирует статус-код ответа, если запрос выполнен успешно.
        """
        url = self.base_url_api_gitlab(endpoint)

        try:
            self.logger.debug(f"URL: {url}")
            response = requests.request(
                method=method.upper(), url=url, headers=headers, **kwargs
            )
            response.raise_for_status()
        except HTTPError as http_err:
            self.logger.exception(http_err)
        except Exception as err:
           self.logger.exception(err)
        else:
            self.logger.info(f"Status code: {response.status_code}")

        return response

    def to_json(self, data: json, indent_level: int) -> json:
        """
        Преобразует предоставленные данные в строку в формате JSON 
        с указанным уровнем отступа.

        Arguments:
            data (json): Данные, которые нужно преобразовать в формат JSON.
            indent_level (int): Количество пробелов для отступов в строке JSON.

        Returns:
            json: Строковое представление данных в формате JSON.
        """
        self.data = data
        json_dumps: str = json.dumps(self.data, indent=indent_level)
        return json_dumps

    def search_values_by_key_in_json(
        
        self, json_value: str, data: list, json_key: str, target_json: str
    ):
        """
        Ищет определенное значение в списке JSON-объектов и извлекает значение, 
        связанное с целевым ключом в совпадающем объекте.

        Arguments:
            json_value (str): Значение, которое нужно найти в JSON-объектах.
            data (list): Список JSON-объектов, представленных в виде строки.
            json_key (str): Ключ, по которому выполняется сравнение с `json_value` 
                в каждом JSON-объекте.
            target_json (str): Ключ, значение которого нужно вернуть 
                из совпадающего объекта.

        Returns:
            Any: Значение, связанное с `target_json` в совпадающем JSON-объекте, 
            или None, если совпадение не найдено.

        Raises:
            json.JSONDecodeError: Если строка `data` не является допустимым 
                JSON-форматом.
        """
        json_data = json.loads(data)
        for item in json_data:
            if json_value == (item[json_key]):
                return item[target_json]
        return None

    def get_json_key(self, data: dict, key: str) -> str:
        """
        Извлекает значение, связанное с указанным ключом, из словаря.

        Arguments:
            data (dict): Словарь, в котором нужно искать ключ.
            key (str): Ключ, значение которого нужно извлечь.

        Returns:
            str: Значение, связанное с ключом, если оно существует, иначе None.
        """
        if key in data:
            return data[key]
        else:
            return None
