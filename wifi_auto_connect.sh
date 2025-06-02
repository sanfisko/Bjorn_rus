#!/bin/sh

# Определяем домашнюю папку пользователя (учитываем запуск с sudo)
if [ -n "$SUDO_USER" ]; then
    HOME_DIR=$(getent passwd "$SUDO_USER" | cut -d: -f6)
else
    HOME_DIR="$HOME"
fi

# Путь к файлу с WiFi учетными данными
CRED_FILE="$HOME_DIR/wifi_net.txt"
# Путь для монтирования USB
USB_MOUNT="/mnt"
# Альтернативная точка монтирования для автоматического монтирования системой
USB_MEDIA="/media/$SUDO_USER"
# Интервал ожидания между проверками (в секундах)
CHECK_INTERVAL=30
# Файл статуса для отображения на экране
STATUS_FILE="/tmp/wifi_auto_connect_status"

# Функция логирования для отладки
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] $1"
    logger -t wifi_usb_connect "$1"
}

# Функция обновления статуса
update_status() {
    local status="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "{\"status\":\"$status\",\"message\":\"$message\",\"timestamp\":\"$timestamp\"}" > "$STATUS_FILE"
    chmod 666 "$STATUS_FILE" 2>/dev/null || true
}

# Функция для создания начального статуса
init_status() {
    update_status "running" "Скрипт WiFi автоподключения запущен"
}

# Функция для корректного завершения
cleanup() {
    log "Получен сигнал завершения"
    update_status "stopped" "Скрипт WiFi автоподключения остановлен"
    exit 0
}

# Устанавливаем обработчики сигналов
trap cleanup TERM INT QUIT

# Функция проверки подключения к WiFi
check_wifi_connection() {
    active_ssid=$(nmcli -t -f active,ssid dev wifi | grep '^yes' | cut -d':' -f2)
    if [ -n "$active_ssid" ]; then
        log "Уже подключен к WiFi: $active_ssid"
        return 0
    fi
    log "Нет активного WiFi подключения"
    return 1
}

# Функция проверки и монтирования USB
check_usb() {
    # Проверяем, смонтирован ли USB в $USB_MOUNT
    if [ -d "$USB_MOUNT" ] && ls "$USB_MOUNT"/*.txt >/dev/null 2>&1; then
        log "Найден USB с .txt файлами в $USB_MOUNT"
        return 0
    fi

    # Проверяем альтернативную точку монтирования (/media/bjorn/XXXX)
    if [ -d "$USB_MEDIA" ]; then
        for dir in "$USB_MEDIA"/*; do
            if [ -d "$dir" ] && ls "$dir"/*.txt >/dev/null 2>&1; then
                log "Найден USB с .txt файлами в $dir"
                USB_MOUNT="$dir"
                return 0
            fi
        done
    fi

    # Находим USB-разделы через /dev/disk/by-path
    usb_paths=$(find /dev/disk/by-path -type l | grep -E 'usb-.*-part[0-9]+$')
    if [ -n "$usb_paths" ]; then
        usb_partitions=$(echo "$usb_paths" | xargs readlink | sed 's#../../#/dev/#')
    else
        usb_partitions=""
    fi
    if [ -z "$usb_partitions" ]; then
        log "USB-разделы не обнаружены"
        log "Текущие точки монтирования:"
        lsblk -f | while read -r line; do log "  $line"; done
        return 1
    fi

    log "Обнаруженные USB-разделы:"
    for part in $usb_partitions; do
        log "  $part"
    done

    found_usb=false
    for part in $usb_partitions; do
        # Проверяем файловую систему и статус монтирования
        fstype=$(lsblk -o FSTYPE -n "$part")
        mountpoint=$(lsblk -o MOUNTPOINT -n "$part")
        if [ -n "$fstype" ] && [ -z "$mountpoint" ]; then
            log "Обнаружен USB-раздел: $part (файловая система: $fstype), пытаемся смонтировать в $USB_MOUNT"
            [ ! -d "$USB_MOUNT" ] && mkdir -p "$USB_MOUNT"
            if mount "$part" "$USB_MOUNT" 2>/dev/null; then
                if ls "$USB_MOUNT"/*.txt >/dev/null 2>&1; then
                    log "USB успешно смонтирован в $USB_MOUNT, найдены .txt файлы"
                    found_usb=true
                    return 0
                else
                    log "USB смонтирован, но .txt файлы не найдены"
                    umount "$USB_MOUNT" 2>/dev/null
                fi
            else
                log "Не удалось смонтировать $part"
            fi
        elif [ -n "$mountpoint" ]; then
            log "Раздел $part уже смонтирован в $mountpoint"
        fi
    done

    log "USB-раздел не обнаружен или нет .txt файлов"
    log "Текущие точки монтирования:"
    lsblk -f | while read -r line; do log "  $line"; done
    return 1
}

# Функция извлечения WiFi учетных данных из .txt файлов
extract_wifi_credentials() {
    # Создаем файл учетных данных, если он не существует
    [ ! -f "$CRED_FILE" ] && touch "$CRED_FILE" && chmod 600 "$CRED_FILE" && log "Создан файл $CRED_FILE"
    
    # Обрабатываем все .txt файлы на USB
    for file in "$USB_MOUNT"/*.txt; do
        if [ -f "$file" ]; then
            log "Обработка файла $file"
            # Читаем строки в формате SSID:Password
            while IFS=: read -r ssid password; do
                if [ -n "$ssid" ] && [ -n "$password" ]; then
                    # Проверяем, есть ли уже такая сеть в файле
                    if ! grep -Fx "$ssid:$password" "$CRED_FILE" >/dev/null; then
                        log "Добавление сети $ssid в $CRED_FILE"
                        echo "$ssid:$password" >> "$CRED_FILE"
                    else
                        log "Сеть $ssid уже существует в $CRED_FILE"
                    fi
                else
                    log "Пропущена строка в $file: неверный формат (SSID:Password)"
                fi
            done < "$file"
        fi
    done
}

# Функция подключения к WiFi
connect_to_wifi() {
    log "Сканирование WiFi сетей..."
    update_status "scanning" "Сканирование WiFi сетей"
    # Получаем список доступных сетей, исключая заголовок
    nmcli dev wifi rescan 2>/dev/null
    networks=$(nmcli -f SSID,SIGNAL,SECURITY dev wifi list | grep -v "^SSID" | sort -k2 -nr)
    if [ -z "$networks" ]; then
        log "WiFi сети не найдены"
        return 1
    fi
    
    log "Доступные сети (отсортированы по сигналу):"
    echo "$networks" | while read -r line; do log "  $line"; done
    
    # Получаем текущий SSID, если подключены
    current_ssid=$(nmcli -t -f active,ssid dev wifi | grep '^yes' | cut -d':' -f2)
    
    # Проверяем известные сети
    if [ -f "$CRED_FILE" ]; then
        while IFS=: read -r saved_ssid saved_password; do
            if [ -n "$saved_ssid" ]; then
                # Проверяем, доступна ли сеть
                if echo "$networks" | grep -w "$saved_ssid" >/dev/null; then
                    signal=$(echo "$networks" | grep -w "$saved_ssid" | awk '{print $2}' | head -n1)
                    security=$(echo "$networks" | grep -w "$saved_ssid" | awk '{print $3}' | head -n1)
                    log "Обнаружена сеть $saved_ssid (сигнал: $signal%, защита: $security)"
                    # Пропускаем, если уже подключены к этой сети
                    if [ "$saved_ssid" = "$current_ssid" ]; then
                        log "Уже подключены к $saved_ssid, пропускаем"
                        if [ -n "$security" ] && [ "$security" != "--" ]; then
                            log "Подключение к закрытой сети $saved_ssid, завершаем скрипт"
                            exit 0
                        fi
                        return 0
                    fi
                    log "Попытка подключения к $saved_ssid"
                    update_status "connecting" "Подключение к $saved_ssid"
                    if nmcli dev wifi connect "$saved_ssid" password "$saved_password" 2>&1 | logger -t wifi_usb_connect; then
                        log "Успешно подключено к $saved_ssid"
                        update_status "connected" "Подключено к $saved_ssid"
                        if [ -n "$security" ] && [ "$security" != "--" ]; then
                            log "Подключение к закрытой сети $saved_ssid, завершаем скрипт"
                            exit 0
                        fi
                        return 0
                    else
                        log "Не удалось подключиться к $saved_ssid"
                        update_status "failed" "Не удалось подключиться к $saved_ssid"
                    fi
                fi
            fi
        done < "$CRED_FILE"
    else
        log "Файл учетных данных $CRED_FILE не существует"
    fi
    
    # Если нет подходящих известных сетей, ищем открытые
    log "Поиск открытых сетей..."
    while IFS= read -r line; do
        ssid=$(echo "$line" | awk '{print $1}')
        security=$(echo "$line" | awk '{print $3}')
        if [ "$security" = "--" ]; then
            # Пропускаем, если уже подключены к этой открытой сети
            if [ "$ssid" = "$current_ssid" ]; then
                log "Уже подключены к открытой сети $ssid, пропускаем"
                return 0
            fi
            log "Попытка подключения к открытой сети $ssid"
            update_status "connecting" "Подключение к открытой сети $ssid"
            if nmcli dev wifi connect "$ssid" 2>&1 | logger -t wifi_usb_connect; then
                log "Успешно подключено к открытой сети $ssid"
                update_status "connected" "Подключено к открытой сети $ssid"
                return 0
            else
                log "Не удалось подключиться к $ssid"
                update_status "failed" "Не удалось подключиться к $ssid"
            fi
        fi
    done <<EOF
$(echo "$networks" | grep -w -- "--")
EOF
    
    log "Не удалось подключиться к WiFi"
    return 1
}

# Основной процесс
log "Запуск скрипта wifi_auto_connect.sh"
init_status
while true; do
    # Проверяем WiFi-соединение
    if check_usb; then
        extract_wifi_credentials
        if [ "$found_usb" = true ]; then
            umount "$USB_MOUNT" 2>/dev/null
            log "USB размонтирован из $USB_MOUNT"
        fi
    else
        log "Продолжаем без USB"
    fi

    # Всегда проверяем сети и пытаемся подключиться
    if connect_to_wifi; then
        update_status "idle" "Ожидание следующей проверки"
    else
        log "Ожидаем $CHECK_INTERVAL секунд перед следующей попыткой"
        update_status "waiting" "Ожидание $CHECK_INTERVAL сек перед следующей попыткой"
    fi
    
    # Ждем перед следующей итерацией
    sleep "$CHECK_INTERVAL"
done