<div id="header" align="center">
  <h3>
    Installation and configuration 
    <br>GitLab Server using API
  </h3>
  <div id="badges">
    <img src="https://img.shields.io/badge/Python-v3.12-%233776AB?style=flat&logo=python&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/Ansible-core%202.17.8-%23EE0000?style=flat&logo=ansible">
    <img src="https://img.shields.io/badge/Vagrant-v2.4.3-%231868F2?style=flat&logo=vagrant">
    <img src="https://img.shields.io/badge/GitLab%20API-v4-%23FC6D26?style=flat&logo=gitlab&logoColor=white">
    <hr>
  </div>
</div>

Установка и первичная конфигурация Gitlab Server с использованием API.

### Content
- [Описание](#описание)
- [Требования](#требования)
- [Настройка](#настройка)
- [Установка](#установка)
- [Использование](#использование)
  - [Ansible](#ansible)
  - [Python](#python)

### Описание
Установка сервера производится на виртуальную машину развернутую с использованием Vagrant.  Настройка и первоначальная конфигурация производится с применением Ansible или Python скрипта. Установка GitLab sever и GitLab Runner в docker.

### Требования
При создании проекта использовались следующие инструменты:

1. ОС - Linux Ubuntu - 22.04
2. VM:
    - VirtualBox v7.0.24
    - Vagrant v2.4.3
3. Python - v3.12
4. Ansible - core 2.17.8

### Настройка
1. Клонируем репозиторий
```bash
git clone https://github.com/MaximRock/gitlab-server-install-configure.git
```
2. Переходим в директорию
```bash
cd gitlab-server-install-configure
```
3. Запускаем настройку проекта 
```bash
./scripts/setup.sh
```
  - Вам будет предложено два варианта настройки
    - 1 > Установка с использованием Vagrant
    - 2 > Установка на удаленный сервер

### Установка

1. Установка сервера *VAGRANT*

    - Этап 1:
      - Переименовываем файлы .env

    - Этап 2:
      - Сконфигурируем Vagrantfile:
        - Вам будет предложенно ввести данные для конфигурации сервера, а имено:
          - IP-адрес VM
          - сетевой интерфейс VM
          - hostname VM
          - оперативную память VM (МБ) - рекомендуется не менее 4 Gb
          - количество ядер процессора VM

    - Этап 3:
      - Подготовим docker-compose.yml для установки GitLab servera в docker:
        - Введите директорию сервера на VM
        - Введите пароль root на сервере VM
        - Введите доменное имя сервера
        - Введите image tag gitlab сервера

    - Этап 4:
      - Подготовим файл inventory_vgrant.ini для насторойки GitLab сервера    

- Запускаем установку сервера:
  ```bash
  vagrant up
  ```
2. Установка на удаленный сервер
    - Этап 1:
      - Переименовываем файлы .env

    - Этап 2:
      - Подготовим docker-compose.yml для установки GitLab servera в docker:
        - Введите директорию сервера на VM
        - Введите пароль root на сервере VM
        - Введите доменное имя сервера
        - Введите image tag gitlab сервера

    - Этап 3:
      - Подготовим SSH key (создадим дерикторию mykeys)

    - Этап 4:
      - Подготовим inventory_remoute.ini файл для Ansible

- Запускаем установку сервера с использованием ansible:
  - user_name_become_user - им пользователя из под которого Вы работаете в системе (Ваш пользователь в Ubuntu)
  - user_password - пароль для пользователя gitlab на сервере 
```bash
ansible-playbook play.yml -i ./inventories/inventory_remoute.ini -e "user_name_become_user=<username>" -e "user_password=<password>"
```

### Использование
После запуска сервера GitLab необходимо создать токен для насторойки сервера.
Копируем наш токен.

Настройка GitLab сервера может осуществлятся двумя способами, с использованием:
1. *Ansible role*
2. *Python скрипта*

#### Ansible
*Ansible role* - создает проект, создает раннер, регистрирует раннер. 
Отредактируйте переменные для *Ansible*:
```bash
nano ./ansible-roles/gitlab-config-ci/defaults/main.yml
```

Для передачи токена будем использовать *ansible-vault*.
Переименуйте файл *.vault_pass.example* для хранения пароля для *ansible-vault*
```bash
mv .vault_pass.example .vault_pass
```
Отредактируйте файл, введите свой пароль для *ansible-vault*, для этого расшифруем файл *vault.yml*
```bash
ansible-vault decrypt ./ansible-roles/gitlab-config-ci/vars/vault.yml
```
Введите свой токен (имя переменной не меняйте, важно!)

`vault_gitlab_api_token: "<token>"`

Зашифруйте файл *vault.yml*:
```bash
ansible-vault encrypt ansible-roles/gitlab-config-ci/vars/vault.yml --vault-password-file .vault_pass
```
Если Вы используете *Vagrant* выполните команду:
```bash
ansible-playbook play-gitlab-config.yml -i ./inventories/inventory_vagrant.ini
```
Если Вы используете *Remoute server* запустите *ansible role*:
```bash
ansible-playbook play-gitlab-config.yml -i ./inventories/inventory_remoute.ini
```

#### Python
*Python script* - создает пользователя, проект, раннер для проекта, регистрирует раннер.

Отредактируем файл *.env*
```bash
nano ./gitlab-api/.env
```
```
GITLAB-TOKEN=<token>
GITLAB-USER-PASSWORD=<password>
```
  - GITLAB-TOKEN - созданный токен
  - GITLAB-USER-PASSWORD - пароль для пользователя GitLab


Для использования необходимо заменить значение переменных на свои.
1. Файл *main.py*
```bash
nano ./gitlab-api/main.py
```
```python
        self.gitlab_runner_token: str = None
        self.client: ConnectSshRemoteHost = ConnectSshRemoteHost(
            host="<domian_name>",
            username="<username>",
            ssh_path=[".ssh", "id_ed25519"],
        )
        self.config_project = ConfigProjectGitlab()
```
  - host - доменное имя;
  - username - имя пользователя (для *Vagrant* пользователь *vagrant*)

```bash
nano ./gitlab-api/config_api/config_api.py 
```
```python
        self.load_dotenv = load_dotenv()
        self.domain_name = "http://<domian_name>"
        self.api = "api"
        self.version = "v4"
```
  - self.domain_name - доменное имя

```bash
nano ./gitlab-api/data/data.py
```
```python
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
```
  - self.user_name - полное имя пользователя
  - self.user_username - имя пользователя
  - self.user_email - почта пользователя
  - self.user_name_tokens - имя для токена
  - self.user_token_expires_at - дата истечения срока действия
  - self.user_token_expires_at - список всех доступных областей       действия для токенов пользователя.
  - self.project_name - имя проекта
