#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

DIR_HOME="$(dirname "$SCRIPT_DIR")"
# "${DIR_HOME}/gitlab-srv-install/.env.example"

#!/bin/bash

# Проверка количества аргументов
if [ $# -ne 1 ]; then
    echo "Использование: $0 [vagrant|remoute]"
    exit 1
fi

ARG=$1

# Проверка допустимости аргумента
if [ "$ARG" != "vagrant" ] && [ "$ARG" != "remoute" ]; then
    echo "Ошибка: Некорректный аргумент. Используйте 'vagrant' или 'remoute'."
    exit 1
fi

# Путь к файлу .env
ENV_FILE="${DIR_HOME}/gitlab-srv-install/.env"

# Проверка существования файла
if [ ! -f "$ENV_FILE" ]; then
    echo "Ошибка: Файл $ENV_FILE не найден."
    exit 1
fi

# Проверка прав на запись
if [ ! -w "$ENV_FILE" ]; then
    echo "Ошибка: Нет прав на запись в файл $ENV_FILE."
    exit 1
fi

# Закомментировать целевые строки, если они не закомментированы (только для незакомментированных)
sed -i.bak '/^[[:space:]]*#/! {/GITLAB_HOME=\/home\/vagrant\/gitlab-docker/s/^/#/}' "$ENV_FILE"
sed -i.bak '/^[[:space:]]*#/! {/GITLAB_HOME=\/home\/gitlab\/gitlab-docker/s/^/#/}' "$ENV_FILE"
sed -i.bak '/^[[:space:]]*#/! {/HTTPS=https/s/^/#/}' "$ENV_FILE"

# Раскомментировать строки в зависимости от аргумента
case $ARG in
    "vagrant")
        sed -i.bak 's/^#[[:space:]]*\(GITLAB_HOME=\/home\/vagrant\/gitlab-docker\)/\1/' "$ENV_FILE"
        ;;
    "remoute")
        sed -i.bak 's/^#[[:space:]]*\(GITLAB_HOME=\/home\/gitlab\/gitlab-docker\)/\1/' "$ENV_FILE"
        sed -i.bak 's/^#[[:space:]]*\(HTTPS=https\)/\1/' "$ENV_FILE"
        ;;
esac

# Удаляем резервную копию (если не нужна)
rm -f "$ENV_FILE.bak"

echo "Настройки для $ARG применены. Проверьте файл $ENV_FILE."