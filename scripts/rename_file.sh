#!/bin/bash


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

DIR_HOME="$(dirname "$SCRIPT_DIR")"
FILE_ENV_DOCKER="${DIR_HOME}/gitlab-srv-install/.env.example"
FILE_ENV_PYTHON="${DIR_HOME}/gitlab-api/.env.example"


check_existence_file () {
    local file="$1"
    if [[ -f "$file" ]]; then
        return 0
    else
        echo "Файл не найден"
        return 1
    fi
}

main () {
    file_env_for_docker="$FILE_ENV_DOCKER"
    check_existence_file "$file_env_for_docker" || return 0
    mv "$file_env_for_docker" "gitlab-srv-install/.env"

    file_env_for_python="$FILE_ENV_PYTHON"
    check_existence_file "$file_env_for_python" || return 0
    mv "$file_env_for_python" "gitlab-api/.env"
}

main "$@"