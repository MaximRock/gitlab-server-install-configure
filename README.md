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

Проект установки и первичной конфигурации Gitlab Server с использованием API.

### Content
- [Описание](#описание)
  - [Навигация_по_проекту](#Навигация_по_проекту)
- [Требования](#тебования)
- [Насторойка](#настройка)
- [Установка](#установка)
- [Использование](#использование)
- [Функциональность](#функциональность)
- [Лицнзия](#лицензия)
- [Контакты](#контакты)

### Описание
Установка сервера производится на виртуальную машину развернутую с использованием Vagrant.  Настройка и первоначальная конфигурация производится с применением Ansible или python скрипта. Установка GitLab sever и GitLab Runner устанавливается в docker.

  

### Требования
При создании проекта использовались следующие инструменты:

1. ОС - Linux Ubuntu - 22.04
2. VM:
    - VirtualBox v7.0.24
    - Vagrant v2.4.3
3. Python - v3.12
4. Ansible - core 2.17.8

### Насторойка
1. Клонируем репозиторий
```bash
git clone https://github.com/MaximRock/gitlab-server-install-configure.git
```
2. Переходим в директорию
```bash
cd gitlab-server-install-configure
```
3. Переименовываем файлы .env.example в .env
Для этого используем скрипт из директории scripts/ rename_file.sh
```bash
./scripts/rename_file.sh
```

### Установка

1. Установка сервер VAGRANT
    - Подготовим Vagrantfile запускаем скрипт
      ```bash
      ./scripts/config_vagrantfile.sh 
      ```
    - Вам будет предложенно ввести данные для конфигурации сервера, а имено:
      - IP-адрес VM
      - сетевой интерфейс VM
      - hostname VM
      - оперативную память VM (МБ) - рекомендуется не менее 4 Gb
      - количество ядер процессора VM

    - Подготовим docker compose.yml для установки GitLab servera в docker:
      ```bash
      ./scripts/config_var_docker_compose.sh
      ```
      - Введите директорию сервера на VM
      - Введите пароль root на сервере VM
      - Введите доменное имя сервера
      - Введите image tag gitlab сервера
      - Для настройки сервера в Vagrant введите 'yes' или 'no' для удаленного сервера

    - Запускаем установку сервера:
      ```bash
      vagrant up
      ```

### Использование
