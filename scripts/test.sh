#!/bin/bash

#!/bin/bash

# Скрипт: setup_inventory.sh
# Интерактивно создаёт inventory-файл для Ansible

set -e  # Завершить скрипт при любой ошибке

# Приветственное сообщение
echo "========================================"
echo " Настройка Ansible inventory для GitLab "
echo "========================================"
echo

# Запрос данных у пользователя
read -p "Введите IP-адрес сервера: " IP_ADDRESS
read -p "Введите SSH-пользователя (по умолчанию root): " SSH_USER

# Установка значений по умолчанию
SSH_USER=${SSH_USER:-root}

# Валидация ввода
if [[ -z "$IP_ADDRESS" ]]; then
  echo "Ошибка: IP-адрес не может быть пустым!"
  exit 1
fi

if ! [[ $IP_ADDRESS =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
  echo "Ошибка: Некорректный формат IP-адреса!"
  exit 1
fi

# Проверка существования ключа
KEY_PATH="./mykeys/myansible.key"
if [ ! -f "$KEY_PATH" ]; then
  echo
  echo "⚠️ Внимание: Файл ключа $KEY_PATH не найден!"
  read -p "Продолжить без проверки ключа? (y/N) " -n 1 -r
  echo
  [[ ! $REPLY =~ ^[Yy]$ ]] && exit 1
fi

# Формирование inventory-файла
INVENTORY_FILE="inventory.ini"

{
  echo "[srv]"
  echo "gitlab ansible_host=\"$IP_ADDRESS\" ansible_user=\"$SSH_USER\" ansible_ssh_private_key_file=$KEY_PATH"
} > "$INVENTORY_FILE"

# Результат
echo
echo "✔️ Inventory-файл успешно создан:"
echo "────────────────────────────────────"
cat "$INVENTORY_FILE"
echo "────────────────────────────────────"
echo "Расположение: $(realpath "$INVENTORY_FILE")"

# #!/bin/bash
# set -e

# PATH_FOLDER=$HOME/github/vagrant-k8s-django-postgresql/src
# NAME_FOLDER=mykeys
# FOLDER=$PATH_FOLDER/$NAME_FOLDER

# if [ ! -d $FOLDER ]
# then
#     mkdir $FOLDER 2>&1
#     cd $FOLDER

#     ssh-keygen -m PEM -t ed25519 -b 4096 -f myansible.key -N "" -C "root@srv" 2>&1

# else
#     cd $PATH_FOLDER
#     rm -rf $FOLDER

# fi 