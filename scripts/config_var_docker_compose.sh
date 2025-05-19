#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
DIR_HOME="$(dirname "$SCRIPT_DIR")"
FILE_ENV_DOCKER="${DIR_HOME}/gitlab-srv-install/.env"
TMP_FILE_DOCKER="${DIR_HOME}/gitlab-srv-install/env_docker.tmp"

check_not_empty() {
    local var_name="$1"
    local var_value="$2"
    if [[ -z "$var_value" ]]; then
        echo "Ошибка: Значение '$var_name' не может быть пустым!" >&2
        return 1
    fi
    return 0
}

cleanup() {
    if [[ -f "$TMP_FILE_DOCKER" ]]; then
        rm -f "$TMP_FILE_DOCKER"
    fi
    exit 1
}

trap "cleanup" SIGINT SIGTERM ERR

main() {
    mkdir -p "$(dirname "$FILE_ENV_DOCKER")" || { echo "Не удалось создать директорию" >&2; exit 1; }

    if [[ ! -f "$FILE_ENV_DOCKER" ]]; then
        echo "Ошибка: Исходный файл $FILE_ENV_DOCKER не найден!" >&2
        exit 1
    fi

    cp "$FILE_ENV_DOCKER" "$TMP_FILE_DOCKER" || { echo "Ошибка копирования файла" >&2; exit 1; }

    read -p "Введите пароль root на сервере VM: " ROOT_PASSWORD
    check_not_empty "ROOT_PASSWORD" "$ROOT_PASSWORD" || cleanup

    read -p "Введите доменное имя сервера: " SERVER_DOMAIN
    check_not_empty "SERVER_DOMAIN" "$SERVER_DOMAIN" || cleanup

    read -p "Введите image tag gitlab сервера: " GITLAB_IMAGE_TAG
    check_not_empty "GITLAB_IMAGE_TAG" "$GITLAB_IMAGE_TAG" || cleanup

    # Экранирование специальных символов
    ROOT_PASSWORD_ESC=$(sed 's/[&/\]/\\&/g' <<<"$ROOT_PASSWORD")
    SERVER_DOMAIN_ESC=$(sed 's/[&/\]/\\&/g' <<<"$SERVER_DOMAIN")
    GITLAB_IMAGE_TAG_ESC=$(sed 's/[&/\]/\\&/g' <<<"$GITLAB_IMAGE_TAG")

    # Замена значений переменных
    sed -i "s|^GITLAB_ROOT_PASSWORD=.*|GITLAB_ROOT_PASSWORD=$ROOT_PASSWORD_ESC|" "$TMP_FILE_DOCKER"
    sed -i "s|^DOMIAN_NAME=.*|DOMIAN_NAME=$SERVER_DOMAIN_ESC|" "$TMP_FILE_DOCKER"
    sed -i "s|^GITLAB_TAG=.*|GITLAB_TAG=$GITLAB_IMAGE_TAG_ESC|" "$TMP_FILE_DOCKER"

    if ! mv "$TMP_FILE_DOCKER" "$FILE_ENV_DOCKER"; then
        echo "Ошибка при перемещении временного файла" >&2
        cleanup
        return 1
    fi

    echo "Изменения успешно применены!"
    return 0
}

main "$@"