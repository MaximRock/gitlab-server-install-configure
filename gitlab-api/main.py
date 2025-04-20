from config_api.config_api import ConfigApiGitlab
from config_api.config_project import ConfigProjectGitlab
from config_api.config_ssh import ConnectSshRemoteHost
from data.data import DefaultBodyRequest
from paramiko.channel import ChannelFile, ChannelStderrFile, ChannelStdinFile
from config_api.logger import Logger


class ApiGitlabServer(ConfigApiGitlab):

    def __init__(self):
        """
        Инициализирует основной класс с настройками и атрибутами по умолчанию.

        Attributes:
            projects (str): Конечная точка для проектов GitLab.
            users (str): Конечная точка для пользователей GitLab.
            user (str): Конечная точка для одного пользователя GitLab.
            runners (str): Конечная точка для раннеров GitLab.
            personal_access_tokens (str): Конечная точка для персональных токенов 
                доступа.
            body_request (DefaultBodyRequest): Объект для формирования тела запроса.
            user_id (str): ID пользователя (по умолчанию None).
            project_id (int): ID проекта (по умолчанию None).
            gitlab_runner_token (str): Токен для раннера GitLab (по умолчанию None).
            client (ConnectSshRemoteHost): SSH-клиент для подключения к удаленному 
                хосту.
            config_project (ConfigProjectGitlab): Объект конфигурации для проектов 
            GitLab.
            content_type (dict[str, str]): HTTP-заголовки для типа содержимого.
            initialize_with_readme (dict[str, str]): Параметр для инициализации проекта 
                с README.
            old_string (str): Строка для замены в конфигурации раннера.
            new_string (str): Строка-замена для конфигурации раннера.
            sudo_command (str): Команда для изменения владельца с использованием sudo.
            user_root (str): Корневой пользователь системы.
            command_replace_string_in_runner (str): Команда для замены строки в 
            конфигурации раннера (по умолчанию None).
            home_path_dir (list[str]): Компоненты пути к файлу конфигурации в 
                домашней директории.
            host_path_dir (str): Путь к файлу конфигурации раннера на хосте.
            logger (Logger): Экземпляр логгера для записи сообщений.
        """
        super().__init__()
        self.projects: str = "projects/"
        self.users: str = "users/"
        self.user: str = "user"
        self.runners: str = "/runners"
        self.personal_access_tokens: str = "/personal_access_tokens"
        self.body_request = DefaultBodyRequest()
        self.user_id: str = None
        self.project_id: int = None
        self.gitlab_runner_token: str = None
        self.client: ConnectSshRemoteHost = ConnectSshRemoteHost(
            host="vagrant.max-rock.ru",
            username="vagrant",
            ssh_path=[".ssh", "id_ed25519"],
        )
        self.config_project = ConfigProjectGitlab()

        self.content_type: dict[str, str] = {"Content-Type": "application/json"}
        self.initialize_with_readme: dict[str, str] = {"initialize_with_readme": "true"}
        self.old_string: str = '    volumes = ["/cache"]'
        self.new_string: str = (
            '    volumes = ["/var/run/docker.sock:/var/run/docker.sock", "/cache"]'
        )
        self.sudo_command: str = "sudo chown"
        self.user_root: str = "root"
        self.command_replace_string_in_runner: str = None
        self.home_path_dir: list[str] = ["file", "config.toml"]
        self.host_path_dir: str = "/srv/gitlab-runner/config/config.toml"
        self.logger = Logger().get_logger(__name__)

    def get_all_projects(self):
        """
        Получает все проекты из API GitLab.

        Этот метод отправляет GET-запрос к API GitLab для получения всех проектов,
        связанных с аутентифицированным пользователем или группой. Ответ логируется
        и возвращается в формате JSON с отступами для удобства чтения.

        Returns:
            str: Строка в формате JSON, представляющая все проекты, с отступами 
            для читаемости.

        Raises:
            Exception: Если запрос завершился неудачно или ответ не может быть 
            разобран как JSON.
        """

        r = self.make_request(
            "GET", self.projects, headers=self.get_default_headers()
        ).json()
        self.logger.info("Все проекты")
        return self.to_json(r, indent_level=4)

    def get_all_users(self):
        """
        Получает всех пользователей из API GitLab.

        Выполняет GET-запрос к конечной точке users с использованием
        стандартных заголовков, логирует операцию и возвращает ответ
        в формате JSON с отступами для удобства чтения.

        Returns:
            str: Строка в формате JSON, содержащая данные всех пользователей,
            с отступами для читаемости.
        """
        r = self.make_request(
            "GET", self.users, headers=self.get_default_headers()
        ).json()
        self.logger.info("Все пользователи")
        return self.to_json(r, indent_level=4)

    def create_user(self):
        """
        Создает нового пользователя, отправляя POST-запрос с данными пользователя, 
        и получает ID пользователя.

        Этот метод выполняет следующие шаги:
        1. Подготавливает данные пользователя из тела запроса.
        2. Отправляет POST-запрос для создания пользователя.
        3. Логирует процесс создания.
        4. Пытается получить ID пользователя на основе его имени пользователя.
        5. Логирует полученный ID пользователя или ошибку, если получение не удалось.
        6. Возвращает ответ от запроса на создание пользователя в формате JSON.

        Returns:
            str: Ответ от запроса на создание пользователя в формате JSON.

        Raises:
            Exception: Если возникает ошибка при получении ID пользователя.
        """
        data = self.body_request.data_user()
        r = self.make_request(
            "POST", self.users, headers=self.get_default_headers(), data=data
        ).json()
        self.logger.info("Создание пользователя")

        try:
            # получаем данные по ключу username и сохраняем значение
            # по ключу id в переменную self.user_id
            self.user_id = self.search_values_by_key_in_json(
                self.body_request.user_username,
                self.get_all_users(),
                json_key="username",
                target_json="id",
            )
            self.logger.info(f"ID пользователя: {self.user_id}")
        except Exception as error:
            self.logger.error(f"Ошибка: {error}")

        return self.to_json(r, indent_level=4)

    def create_token_for_user(self):
        """
        Создает персональный токен доступа для пользователя.

        Этот метод отправляет POST-запрос к API GitLab для создания персонального
        токена доступа для конкретного пользователя. Токен генерируется на основе
        данных, предоставленных в теле запроса.

        Returns:
            str: Строка в формате JSON, содержащая ответ от API,
            с отступами для удобства чтения.

        Logs:
            Логирует действие создания токена пользователя.

        Raises:
            Любые исключения, возникшие во время выполнения запроса к API,
            будут переданы вызывающему коду.
        """
        data = self.body_request.data_user_tokens()
        r = self.make_request(
            "POST",
            f"{self.users}{self.user_id}{self.personal_access_tokens}",
            self.get_default_headers(),
            data=data,
        ).json()
        self.logger.info("Создание токена пользователя")
        return self.to_json(r, indent_level=4)

    def create_project_for_user(self):
        """
        Создает новый проект для пользователя на сервере GitLab.

        Этот метод отправляет POST-запрос к API GitLab для создания проекта
        для указанного пользователя. Также он получает ID вновь созданного проекта
        и логирует его.

        Returns:
            str: Строка в формате JSON, содержащая ответ от API.

        Raises:
            Exception: Если запрос к API GitLab завершился неудачно или если
                   не удалось получить ID проекта.

        Attributes:
            self.body_request.data_user_projects: Метод для генерации данных
            для создания проекта, инициализированного с файлом README.
            self.projects: Базовый URL для проектов в API GitLab.
            self.user: Имя пользователя, для которого создается проект.
            self.user_id: ID пользователя, для которого создается проект.
            self.get_default_headers: Метод для получения стандартных заголовков
            для API-запроса.
            self.make_request: Метод для отправки HTTP-запросов к API GitLab.
            self.search_values_by_key_in_json: Метод для поиска определенного
            значения в JSON-ответе.
            self.get_all_projects: Метод для получения всех проектов из API GitLab.
            self.logger.info: Метод для логирования информационных сообщений.
            self.to_json: Метод для форматирования ответа API в виде строки JSON.
        """
        data = self.body_request.data_user_projects(**self.initialize_with_readme)
        r = self.make_request(
            "POST",
            f"{self.projects}{self.user}/{self.user_id}",
            self.get_default_headers(),
            data=data,
        ).json()
        self.project_id = self.search_values_by_key_in_json(
            self.body_request.project_name,
            self.get_all_projects(),
            json_key="name",
            target_json="id",
        )
        self.logger.info(f"ID проекта: {self.project_id}")

        return self.to_json(r, indent_level=4)

    def create_runner_for_project(self):
        """
        Создает GitLab раннер для определенного проекта.

        Этот метод отправляет POST-запрос к API GitLab для создания раннера,
        связанного с указанным проектом. Токен раннера извлекается из ответа API
        и логируется для справки.

        Returns:
            str: Строка в формате JSON, представляющая ответ API.

        Raises:
            Exception: Если запрос к API завершился неудачно или ответ не содержит
                   ожидаемого ключа "token".

        Logs:
            - Информация о создании раннера для проекта.
            - Токен раннера, полученный из ответа API.
        """
        data = self.body_request.data_runner_project_for_user(
            self.project_id
        )  # {"project_id": self.project_id}

        r = self.make_request(
            method="POST",
            endpoint=f"{self.user}{self.runners}",
            headers=self.get_default_headers(),
            data=data,
        ).json()
        self.logger.info("Создание раннера проекта")
        self.gitlab_runner_token = self.get_json_key(data=r, key="token")
        self.logger.info(f"Токен раннера: {self.gitlab_runner_token}")
        return self.to_json(r, indent_level=4)

    def registration_gitlab_runner_on_server(self):
        """
        Регистрирует GitLab Runner на сервере с использованием Docker.

        Этот метод выполняет команду для регистрации GitLab Runner с указанным
        доменным именем и токеном. Раннер настраивается для использования Docker
        executor с образом "docker:dind" и получает описание "docker-runner".

        Returns:
            tuple[ChannelStdinFile, ChannelFile, ChannelStderrFile]: Кортеж, содержащий
            стандартный ввод, вывод и ошибки из выполненной команды.

        Raises:
            Любые исключения, возникающие во время выполнения команды SSH или
            проблемы с подключением клиента.

        Side effects:
            - Логирует процесс регистрации.
            - Отключает SSH-клиент после выполнения команды.
        """
        command = f"""
            docker exec -i gitlab-runner gitlab-runner register \
                --non-interactive \
                --url {self.domain_name}/ \
                --token {self.gitlab_runner_token} \
                --executor "docker" \
                --docker-image docker:dind \
                --description "docker-runner"
            """
        commannd_regist: tuple[ChannelStdinFile, ChannelFile, ChannelStderrFile] = (
            self.client.exec_command(command)
        )
        self.logger.info("Регистрация раннера на сервере")
        self.client.disconnect(self.client.ssh_connect())

        return commannd_regist

    def replace_in_config_runner(self) -> bool:
        """
        Заменяет определенную строку в файле конфигурации GitLab Runner (config.toml)
        на удаленном сервере и обновляет файл с измененным содержимым.

        Этот метод выполняет следующие шаги:
        1. Выполняет команду на удаленном сервере для подготовки файла конфигурации.
        2. Загружает файл конфигурации с удаленного сервера с использованием SFTP.
        3. Заменяет указанную строку в загруженном файле конфигурации.
        4. Загружает измененный файл конфигурации обратно на удаленный сервер 
            с использованием SFTP.
        5. Выполняет команду на удаленном сервере для применения изменений прав 
            собственности к файлу.
        6. Удаляет локальную копию файла конфигурации.
        7. Логирует успешное обновление конфигурации.
        8. Отключает соединения SFTP и SSH.

        Returns:
            bool: True, если обновление конфигурации выполнено успешно.

        Raises:
            Exception: Если возникает ошибка в процессе, она логируется и в
            ыбрасывается исключение.

        Note:
            - Этот метод предполагает, что объекты `self.client`, `self.config_project` 
                и `self.logger` правильно инициализированы и настроены.
            - Атрибуты `self.sudo_command`, `self.host_path_dir`, `self.home_path_dir`, 
                `self.old_string`, `self.new_string` и `self.user_root` 
                должны быть установлены перед вызовом этого метода.

        Side effects:
            - Изменяет удаленный файл конфигурации GitLab Runner.
            - Изменяет права собственности удаленного файла конфигурации.
            - Удаляет локальную временную копию файла конфигурации.
            - Логирует информацию и ошибки в процессе выполнения.
            - Отключает активные соединения SFTP и SSH.
        """
        # command = "sudo chown vagrant:vagrant /srv/gitlab-runner/config/config.toml"
        try:
            self.client.exec_command(
                self.client.command(
                    command=self.sudo_command, path_to_file=self.host_path_dir
                )
            )

            self.client.make_sftp(
                "get",
                self.host_path_dir,
                self.config_project.project_path_to_file(*self.home_path_dir),
            )

            self.config_project.replace_in_file(
                file_path=self.config_project.project_path_to_file(*self.home_path_dir),
                old_string=self.old_string,
                new_string=self.new_string,
            )

            self.client.make_sftp(
                "put",
                self.config_project.project_path_to_file(*self.home_path_dir),
                self.host_path_dir,
            )

            self.client.exec_command(
                self.client.command(
                    command=self.sudo_command,
                    user_owner=self.user_root,
                    path_to_file=self.host_path_dir,
                )
            )

            self.config_project.delete_in_file("file", "config.toml")

            self.logger.info("Конфигурация файла config.toml")

            self.client.disconnect(self.client.sftp_connect())
            self.client.disconnect(self.client.ssh_connect())
            return True
        except Exception as error:
            self.logger.error(f"Ошибка: {error}")
            raise Exception(f"Error: {error}")


if __name__ == "__main__":
    api_gitlab = ApiGitlabServer()
    methode_name: list[str] = [
        # "get_all_users",
        # "get_all_projects",
        "create_user",
        "create_token_for_user",
        "create_project_for_user",
        "create_runner_for_project",
        "registration_gitlab_runner_on_server",
        "replace_in_config_runner",
    ]

    for name in methode_name:
        method = getattr(api_gitlab, name)()
        print(method)
