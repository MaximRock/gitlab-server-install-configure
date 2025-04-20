from paramiko import Channel, Ed25519Key, SFTPClient, SSHClient, AutoAddPolicy
from paramiko.channel import ChannelFile, ChannelStderrFile, ChannelStdinFile
from config_api.config_project import ConfigProjectGitlab

from config_api.logger import Logger


class ConnectSshRemoteHost:
    def __init__(self, host: str, username: str, ssh_path: list):
        """
        Инициализирует конфигурацию для SSH-доступа.

        Arguments:
            host (str): Имя хоста или IP-адрес сервера 
                    (например, "vagrant.max-rock.ru").
            username (str): Имя пользователя для SSH-доступа (например, "vagrant").
            ssh_path (list): Список, представляющий путь к приватному SSH-ключу 
                    (например, [".ssh", "id_ed25519"]).

        Attributes:
            project_path (ConfigProjectGitlab): Экземпляр ConfigProjectGitlab 
                для конфигурации проекта.
            host (str): Имя хоста или IP-адрес сервера.
            username (str): Имя пользователя для SSH-доступа.
            ssh_path (list): Компоненты пути к приватному SSH-ключу.
            private_key_path (str): Полный путь к приватному SSH-ключу.
            logger (Logger): Экземпляр логгера для записи сообщений.
        """
        self.project_path = ConfigProjectGitlab()
        self.host = host  # "vagrant.max-rock.ru"
        self.username = username  # "vagrant"
        self.ssh_path: list = ssh_path  # [".ssh", "id_ed25519"]
        self.private_key_path = self.project_path.path_to_file(*self.ssh_path)
        self.logger = Logger().get_logger(__name__)

    def ssh_connect(self) -> SSHClient:
        """
        Устанавливает SSH-соединение с удалённым сервером, используя предоставленный 
            приватный ключ.
        Returns:
            SSHClient: Активное SSH-соединение с удалённым сервером.
        Raises:
            Exception: Если произошла ошибка при загрузке приватного ключа
             или подключении к серверу.
        Note:
            - Метод использует `Ed25519Key` для загрузки приватного ключа
             из указанного пути.
            - Если приватный ключ недействителен или подключение не удалось,
                 соответствующие исключения записываются в лог.
            - Возвращает `None`, если подключение к SSH-серверу не удалось.
        """
        ssh_client = SSHClient()
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())

        try:
            key: Ed25519Key = Ed25519Key.from_private_key_file(self.private_key_path)
            # self.logger.debug("Key Saccessful!")
        except Exception as err:
            self.logger.exception(f"Key Error: {err}")
            raise Exception(err)

        try:
            ssh_client.connect(hostname=self.host, username=self.username, pkey=key)
            # self.logger.info("Connect to ssh server")
        except Exception as err:
            self.logger.exception(f"Connect to ssh Error: {err}")
            return None

        return ssh_client

    def sftp_connect(self) -> SSHClient:
        """
        Устанавливает соединение SFTP с использованием SSH-клиента.

        Этот метод подключается к SFTP-серверу, сначала устанавливая SSH-соединение,
        а затем открывая SFTP-сессию. Также устанавливается тайм-аут для канала SFTP.
        Returns:
            SFTPClient: Экземпляр SFTP-клиента, используемого для подключения.
        Raises:
            Exception: Логирует и обрабатывает любые исключения, возникающие
             в процессе подключения.
        """

        try:
            sftp: SFTPClient = self.ssh_connect().open_sftp()
            channel: Channel | None = sftp.get_channel()
            channel.settimeout(3)
            # self.logger.info("Connect to sftp server")
        except Exception as err:
            self.logger.exception(f"Sftp Error: {err}")
        return sftp

    def exec_command(
        self, command: str
    ) -> tuple[ChannelStdinFile, ChannelFile, ChannelStderrFile]:
        """
        Выполняет команду на удалённом сервере через SSH и возвращает потоки ввода,
        вывода и ошибок.
        Arguments:
            command (str): Команда для выполнения на удалённом сервере.
        Returns:
            tuple[ChannelStdinFile, ChannelFile, ChannelStderrFile]: Кортеж, содержащий
            стандартный ввод, стандартный вывод и стандартный поток ошибок 
            выполненной команды.
        Side effects:
            Выводит стандартный вывод и стандартный поток ошибок выполненной команды
            в консоль.
        """
        stdin, stdout, stderr = self.ssh_connect().exec_command(command)
        print(stdout.read().decode())
        print(stderr.read().decode())
        return stdin, stdout, stderr

    def command(self, command: str, path_to_file: str, user_owner: str = None) -> str:
        """
        Формирует строку команды для выполнения указанной команды над файлом с заданным владельцем.
        Arguments:
            command (str): Команда для выполнения.
            path_to_file (str): Путь к целевому файлу.
            user_owner (str, optional): Имя пользователя-владельца файла.
                 По умолчанию используется атрибут `username` экземпляра.
        Returns:
            str: Сформированная строка команды.
        """
        user_owner = user_owner or self.username
        return f"{command} {user_owner}:{user_owner} {path_to_file}"

    def make_sftp(self, method_name: str, *args, **kwargs) -> any:
        """
        Выполняет указанный метод на SFTP-соединении с переданными аргументами.
        Arguments:
            method_name (str): Имя метода, который нужно вызвать на SFTP-соединении.
            *args: Позиционные аргументы, передаваемые в указанный метод.
            **kwargs: Именованные аргументы, передаваемые в указанный метод.
        Returns:
            any: Результат выполнения указанного метода на SFTP-соединении.
        """
        return getattr(self.sftp_connect(), method_name)(*args, **kwargs)

    def disconnect(self, client: SSHClient | SFTPClient):
        """
        Отключает указанный SSH или SFTP клиент.
        Этот метод закрывает соединение для предоставленного клиента, 
            если он не равен None.
        Arguments:
            client (SSHClient | SFTPClient): SSH или SFTP клиент для отключения.
        Returns:
            None
        """
        if client:
            return client.close()
