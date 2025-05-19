#!/bin/bash
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
DIR_HOME="$(dirname "$SCRIPT_DIR")"

# NAME_FOLDER="mykeys"
FOLDER="${DIR_HOME}/mykeys"

# Проверка существования папки
if [ ! -d "$FOLDER" ]; then
    echo "Создаю папку для ключей: $FOLDER"
    mkdir -p "$FOLDER"
    cd "$FOLDER"
    
    echo "Генерация SSH-ключей..."
    ssh-keygen -m PEM -t ed25519 -b 4096 -f myansible.key -N "" -C "root@srv" -q
    
    echo "Ключи успешно созданы в: $FOLDER"
else
    echo "Папка с ключами уже существует: $FOLDER"
    echo "Дополнительные действия не требуются"
fi