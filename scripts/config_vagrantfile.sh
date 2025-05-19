#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
DIR_HOME="$(dirname "$SCRIPT_DIR")"
VAGRANT_FILE="${DIR_HOME}/Vagrantfile"
TMP_FILE="${DIR_HOME}/Vagrantfile.tmp"

validate_format() {
    local value="$1"
    if [[ "$value" =~ [^0-9.:] ]]; then
        echo "Ошибка: Недопустимые символы в значении!"
        return 1
    fi
    return 0
}

validate_ipv4() {
    local ip="$1"
    if [[ ! "$ip" =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        echo "Ошибка: Неверный формат IPv4!"
        return 1
    fi
    return 0
}

check_not_empty() {
    local var_name="$1"
    local var_value="$2"
    if [[ -z "$var_value" ]]; then
        echo "Ошибка: Значение '$var_name' не может быть пустым!"
        return 1
    fi
    return 0
}

cleanup() {
    if [[ -f "$TMP_FILE" ]]; then
        rm -f "$TMP_FILE"
    fi
    exit 1
}

trap cleanup SIGINT SIGTERM ERR

main() {
    cp "$VAGRANT_FILE" "$TMP_FILE" || { echo "Ошибка копирования файла"; exit 1; }

    read -p "Введите IP-адрес сервера: " ip_address
    check_not_empty "ip_address" "$ip_address" || return 1
    validate_format "$ip_address" || return 1
    validate_ipv4 "$ip_address" || return 1

    read -p "Введите сетевой интерфейс: " network_interface
    check_not_empty "network_interface" "$network_interface" || return 1

    read -p "Введите hostname VM: " network_hostname
    check_not_empty "network_hostname" "$network_hostname" || return 1

    read -p "Введите оперативную память VM (МБ): " vm_memory
    check_not_empty "vm_memory" "$vm_memory" || return 1
    validate_format "$vm_memory" || return 1

    read -p "Введите количество ядер процессора VM: " vm_cpus
    check_not_empty "vm_cpus" "$vm_cpus" || return 1
    validate_format "$vm_cpus" || return 1

    # Модифицированные команды замены
    sed -i "s/^\(PRIVATE_NETWORK_IP\s*=\s*\).*/\1\"${ip_address}\"/" "$TMP_FILE"
    sed -i "s/^\(NETWORK_BRIDGE\s*=\s*\).*/\1\"${network_interface}\"/" "$TMP_FILE"
    sed -i "s/^\(HOSTNAME\s*=\s*\).*/\1\"${network_hostname}\"/" "$TMP_FILE"
    sed -i "s/^\(VB_MEMORY\s*=\s*\).*/\1${vm_memory}/" "$TMP_FILE"
    sed -i "s/^\(VB_CPUS\s*=\s*\).*/\1${vm_cpus}/" "$TMP_FILE"

    mv "$TMP_FILE" "$VAGRANT_FILE"
    echo "Изменения успешно применены!"
    echo "VAGRANT_IP='$ip_address'" > "${MENU_DIR}/vagrant.cfg"
}

main "$@"