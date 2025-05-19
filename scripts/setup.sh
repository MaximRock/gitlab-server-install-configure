#!/bin/bash

MENU_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
DIR_HOME="$(dirname "$MENU_DIR")"

# Пути к скриптам 
RENAME_FILE="${MENU_DIR}/rename_file.sh"
VAGRANT_SCRIPT="${MENU_DIR}/config_vagrantfile.sh"
DOCKER_COMPOSE_SCRIPT="${MENU_DIR}/config_var_docker_compose.sh"
TOGGLE_COMEMENT="${MENU_DIR}/toggle_comment.sh"
FILE_DOCKER_ENV="${MENU_DIR}/gitlab-srv-install/.env"
INVENTORY_SRV="${MENU_DIR}/inventory_remoute_srv.sh"
GENERATE_SSH_KEY="${MENU_DIR}/generate-ssh-key.sh"

show_menu() {
    clear
    echo "=============================="
    echo "    УПРАВЛЕНИЕ СЕРВЕРАМИ      "
    echo "=============================="
    echo "1. Полная настройка Vagrant"
    echo "2. Настройка удаленного сервера"
    echo "3. Выход"
    echo "=============================="
}

check_script() {
    local script_path="$1"
    local script_name="$(basename "$script_path")"
    
    if [ ! -f "$script_path" ]; then
        echo -e "\n❌ Ошибка: Скрипт ${script_name} не найден!"
        return 1
    fi
    
    if [ ! -x "$script_path" ]; then
        echo -e "\n❌ Ошибка: Скрипт ${script_name} не исполняемый!"
        echo "Исправьте права: chmod +x "$script_path""
        return 1
    fi
    
    return 0
}

run_vagrant_sequence() {

    local config_file="${MENU_DIR}/vagrant.cfg"

    echo -e "\n=== Запуск этапа 1: Подготовим файлы .env ==="
    if check_script "$RENAME_FILE"; then
        (cd "$MENU_DIR" && "$RENAME_FILE")
    else
        return 1
    fi
    
    echo -e "\n=== Запуск этапа 2: Vagrantfile конфигурация ==="
    if check_script "$VAGRANT_SCRIPT"; then
        (cd "$MENU_DIR" && source "$VAGRANT_SCRIPT")
    else
        return 1
    fi
    
    echo -e "\n=== Запуск этапа 3: Docker compose конфигурация ==="
    if check_script "$TOGGLE_COMEMENT"; then
        (cd "$MENU_DIR" && "$TOGGLE_COMEMENT" vagrant)
    else
        return 1
    fi

    if check_script "$DOCKER_COMPOSE_SCRIPT"; then
        (cd "$MENU_DIR" && "$DOCKER_COMPOSE_SCRIPT")
    else
        return 1
    fi

    echo -e "\n=== Запуск этапа 4: inventory_vagrant.ini конфигурация ==="
    if [ -f "$config_file" ]; then
        source "$config_file"
        echo "Загружены параметры:"
        echo "IP-адрес сервера:: $VAGRANT_IP"
        rm -f "$config_file"
    fi
    sed -i "s/^\(ansible_host\s*=\s*\).*/\1\"${VAGRANT_IP}\"/" "${DIR_HOME}/inventories/inventory_vagrant.ini"

    echo -e "\n✅ Все этапы выполнены успешно!"
    return 0
}

run_remote_srv() {

    echo -e "\n=== Запуск этапа 1: Подготовим файлы .env ==="
    if check_script "$RENAME_FILE"; then
        (cd "$MENU_DIR" && "$RENAME_FILE")
    else
        return 1
    fi
    
    echo -e "\n=== Запуск этапа 2: Docker compose конфигурация ==="
    if check_script "$TOGGLE_COMEMENT"; then
        (cd "$MENU_DIR" && "$TOGGLE_COMEMENT" remoute)
    else
        return 1
    fi

    if check_script "$DOCKER_COMPOSE_SCRIPT"; then
        (cd "$MENU_DIR" && "$DOCKER_COMPOSE_SCRIPT")
    else
        return 1
    fi

    echo -e "\n=== Запуск этапа 3: Генерируем ключи доступа ==="
    if check_script "$GENERATE_SSH_KEY"; then
        (cd "$MENU_DIR" && "$GENERATE_SSH_KEY")
    else
        return 1
    fi

    echo -e "\n=== Запуск этапа 4: Подготовка inventory файла ==="
    if check_script "$INVENTORY_SRV"; then
        (cd "$MENU_DIR" && "$INVENTORY_SRV")
    else
        return 1
    fi
    
    echo -e "\n✅ Все этапы выполнены успешно!"
    return 0
}

while true; do
    show_menu
    read -p "Введите номер выбора [1-3]: " choice
    
    case $choice in
        1)
            echo -e "\nЗапуск полной настройки Vagrant..."
            run_vagrant_sequence
            read -p "Нажмите Enter чтобы продолжить..."
            ;;
        2)
            echo -e "\nЗапуск подготовки окружения..."
            run_remote_srv
            read -p "Нажмите Enter чтобы продолжить..."
            ;;
        3)
            echo -e "\nЗавершение работы...\n"
            exit 0
            ;;
        *)
            echo -e "\n⚠️ Ошибка: Некорректный выбор! Используйте цифры 1-3.\n"
            read -p "Нажмите Enter чтобы продолжить..."
            ;;
    esac
done