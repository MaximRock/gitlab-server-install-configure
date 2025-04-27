#!/bin/bash

# Получаем директорию, где находится скрипт
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

DIR_HOME="$(dirname "$SCRIPT_DIR")"
FILE_ENV_DOCKER="${DIR_HOME}/gitlab-srv-install/.env"
TMP_FILE_DOCKER="${DIR_HOME}/gitlab-srv-install/env_docker.tmp"

YES="yes"
NO="no"

# Проверка, что переменная не пустая
check_not_empty() {
    local var_name="$1"
    local var_value="$2"
    if [[ -z "$var_value" ]]; then
        echo "Ошибка: Значение '$var_name' не может быть пустым!" >&2
        return 1
    fi
    return 0
}

# Откат изменений при прерывании
cleanup() {
    if [[ -f "$TMP_FILE_DOCKER" ]]; then
        rm -f "$TMP_FILE_DOCKER"
    fi
    exit 1
}

trap "cleanup" SIGINT SIGTERM ERR

main() {
    # Создаем директорию, если она не существует
    mkdir -p "$(dirname "$FILE_ENV_DOCKER")" || { echo "Не удалось создать директорию" >&2; exit 1; }

    if [[ ! -f "$FILE_ENV_DOCKER" ]]; then
        echo "Ошибка: Исходный файл $FILE_ENV_DOCKER не найден!" >&2
        exit 1
    fi

    cp "$FILE_ENV_DOCKER" "$TMP_FILE_DOCKER" || { echo "Ошибка копирования файла" >&2; exit 1; }

    read -p "Введите директорию сервера на VM: " SERVER_DIR
    check_not_empty "SERVER_DIR" "$SERVER_DIR" || cleanup

    read -p "Введите пароль root на сервере VM: " ROOT_PASSWORD
    check_not_empty "ROOT_PASSWORD" "$ROOT_PASSWORD" || cleanup

    read -p "Введите доменное имя сервера: " SERVER_DOMAIN
    check_not_empty "SERVER_DOMAIN" "$SERVER_DOMAIN" || cleanup

    read -p "Введите image tag gitlab сервера: " GITLAB_IMAGE_TAG
    check_not_empty "GITLAB_IMAGE_TAG" "$GITLAB_IMAGE_TAG" || cleanup

    read -p "Для настройки сервера в Vagrant введите 'yes' или 'no' для удаленного сервера: " ANSWER

    # Применяем все замены
    sed -i "1s|\"\"|$SERVER_DIR|" "$TMP_FILE_DOCKER"
    sed -i "2s|\"\"|$ROOT_PASSWORD|" "$TMP_FILE_DOCKER"
    sed -i "3s|\"\"|$SERVER_DOMAIN|" "$TMP_FILE_DOCKER"
    sed -i "4s|\"\"|$GITLAB_IMAGE_TAG|" "$TMP_FILE_DOCKER"

    if [[ "${ANSWER,,}" = "${YES,,}" ]]; then
        echo "Настройка для Vagrant"
    elif [[ "${ANSWER,,}" = "${NO,,}" ]]; then
        echo "Настройка для удаленного сервера"
        sed -i 's/^# HTTPS=https/HTTPS=https/' "$TMP_FILE_DOCKER"
    else
        echo "Выберите yes или no!" >&2
        cleanup
    fi

    if ! mv "$TMP_FILE_DOCKER" "$FILE_ENV_DOCKER"; then
        echo "Ошибка при перемещении временного файла" >&2
        cleanup
        return 1
    fi

    echo "Изменения успешно применены!"
    return 0
}

main "$@"