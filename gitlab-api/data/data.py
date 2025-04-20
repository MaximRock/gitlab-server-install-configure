import os

from dotenv import load_dotenv


class DefaultBodyRequest:

    def __init__(self) -> None:
        """
        Инициализирует данные конфигурации для взаимодействия с GitLab API.

        Attributes:
            load_dotenv (bool): Указывает, загружены ли переменные окружения из файла
                 .env.
            user_name (str): Полное имя пользователя.
            user_username (str): Имя пользователя.
            user_email (str): Электронная почта пользователя.
            user_password (str): Пароль пользователя, полученный из 
                переменной окружения 'GITLAB-USER-PASSWORD'.
            user_name_tokens (str): Имя, связанное с токеном пользователя.
            user_token_expires_at (str): Дата истечения срока действия
                токена пользователя в формате YYYY-MM-DD.
            true (bool): Логическое значение, установленное в True.
            all_scopes_user_tokens (list): Список всех доступных областей 
                действия для токенов пользователя.
            project_name (str): Имя проекта.
        """
        self.load_dotenv: bool = load_dotenv()
        self.user_name: str = "Max Admin"
        self.user_username: str = "neh_admin"
        self.user_email: str = "example23@com.com"
        self.user_password: str = os.getenv('GITLAB-USER-PASSWORD')
        self.user_name_tokens: str = "mytoken_max"
        self.user_token_expires_at: str = "2025-06-01"
        self.true: bool = True
        self.all_scopes_user_tokens: list = [
                "api",
                "read_user",
                "read_repository",
                "write_repository",
                "read_registry",
                "write_registry",
                "sudo",
                "admin_mode",
                "create_runner",
                "manage_runner",
                "ai_features",
                "k8s_proxy",
                "self_rotate",
                "read_service_ping"
            ]
        self.project_name: str = "project01"

    def data_user(self, **kwargs) -> dict:
        """
        Создает словарь, представляющий пользователя с атрибутами по умолчанию 
            и дополнительными необязательными атрибутами.
        Arguments:
            **kwargs: Произвольные именованные аргументы, представляющие
             дополнительные атрибуты пользователя.
        Returns:
            dict: Словарь, содержащий атрибуты пользователя, включая атрибуты по умолчанию 
              ('name', 'username', 'email', 'password') и любые дополнительные атрибуты, 
              переданные через kwargs.
        """
        user: dict = {
            "name": self.user_name,
            "username": self.user_username,
            "email": self.user_email,
            "password": self.user_password
            }
        return {**user, **kwargs}
    
    def data_user_tokens(self, **kwargs) -> dict:
        """
        Генерирует словарь, содержащий информацию о токене пользователя, 
            и объединяет его с дополнительными именованными аргументами.
        Arguments:
            **kwargs: Произвольные именованные аргументы, 
            которые будут объединены со словарем токена пользователя.
        Returns:
            dict: Словарь, содержащий информацию о токене пользователя, включая:
            - "name": Имя токена пользователя.
            - "expires_at": Дата истечения срока действия токена.
            - "scopes": Области действия, связанные с токеном пользователя.
            Также включаются дополнительные пары ключ-значение из **kwargs.
        """
        user_tokens: dict = {
            "name": self.user_name_tokens,
            "expires_at": self.user_token_expires_at,
            "scopes": self.all_scopes_user_tokens
        }
        return {**user_tokens, **kwargs}
    
    def data_user_projects(self, **kwargs) -> dict:
        """
        Создает словарь, представляющий данные проекта пользователя с значениями 
            по умолчанию  и позволяет добавлять или переопределять данные с помощью 
            дополнительных именованных аргументов.
        Arguments:
            **kwargs: Произвольные именованные аргументы для переопределения 
            или добавления данных проекта.
        Returns:
            dict: Словарь, содержащий данные проекта, включая любые переопределения 
              или дополнительные поля, переданные через kwargs.
        """
        user_projects: dict = {
            "name": self.project_name,
            "description": "Project01",
            "visibility": "public",
            "shared_runners_enabled": self.true
            # "initialize_with_readme": self.true
        }
        return {**user_projects, **kwargs}
    
    def data_runner_project_for_user(self, project_id: int,**kwargs) -> dict:
        """
        Генерирует словарь, представляющий проект-раннер для конкретного пользователя.
        АргуArguments:
            project_id (int): Идентификатор проекта, связанного с раннером.
            **kwargs: Дополнительные пары ключ-значение, которые будут 
                включены в словарь проекта-раннера.
        Returns:
            dict: Словарь, содержащий детали проекта-раннера, включая предоставленный
              идентификатор проекта, тип раннера по умолчанию, описание, список тегов
              и любые дополнительные пары ключ-значение, переданные через kwargs.
        """
        runner_project: dict = {
            "project_id": project_id,
            "runner_type": "project_type",
            "description": "test-runner01",
            "tag_list": "test-docker"
        }
        return {**runner_project, **kwargs}
        
        