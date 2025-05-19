#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

DIR_HOME="$(dirname "$SCRIPT_DIR")"
FILE_ENV_DOCKER="${DIR_HOME}/gitlab-srv-install/.env.example"
FILE_ENV_PYTHON="${DIR_HOME}/gitlab-api/.env.example"

ENV_DOCKER="${DIR_HOME}/gitlab-srv-install/"
ENV_PYTHON="${DIR_HOME}/gitlab-api/"

check_file_exists() {
    local file="$1"
    if [[ -f "$file" ]]; then
        return 0
    else
        return 1
    fi
}

main() {
    # Обработка Docker .env
    target_docker_env="${ENV_DOCKER}/.env"
    if ! check_file_exists "$target_docker_env"; then
        if check_file_exists "$FILE_ENV_DOCKER"; then
            mv "$FILE_ENV_DOCKER" "$target_docker_env"
            echo "Создан файл .env для Docker: ${target_docker_env}"
        else
            echo "Ошибка: исходный файл Docker .env.example не найден [${FILE_ENV_DOCKER}]"
        fi
    else
        echo "Файл Docker .env уже существует: ${target_docker_env}"
    fi

    # Обработка Python .env
    target_python_env="${ENV_PYTHON}/.env"
    if ! check_file_exists "$target_python_env"; then
        if check_file_exists "$FILE_ENV_PYTHON"; then
            mv "$FILE_ENV_PYTHON" "$target_python_env"
            echo "Создан файл .env для Python: ${target_python_env}"
        else
            echo "Ошибка: исходный файл Python .env.example не найден [${FILE_ENV_PYTHON}]"
        fi
    else
        echo "Файл Python .env уже существует: ${target_python_env}"
    fi
}

main "$@"