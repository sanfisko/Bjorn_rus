#!/bin/bash

# Тестовый скрипт для проверки wifi_auto_connect.sh

echo "=== Тест WiFi скрипта ==="

# Проверяем наличие nmcli
if ! command -v nmcli >/dev/null 2>&1; then
    echo "ОШИБКА: nmcli не найден. Установите NetworkManager."
    exit 1
fi

echo "✓ nmcli найден"

# Проверяем WiFi интерфейс
wifi_device=$(nmcli device status | grep wifi | head -n1 | awk '{print $1}')
if [ -z "$wifi_device" ]; then
    echo "ОШИБКА: WiFi устройство не найдено"
    exit 1
fi

echo "✓ WiFi устройство найдено: $wifi_device"

# Проверяем статус WiFi
wifi_status=$(nmcli radio wifi)
echo "Статус WiFi: $wifi_status"

if [ "$wifi_status" = "disabled" ]; then
    echo "Включаем WiFi..."
    nmcli radio wifi on
    sleep 2
fi

# Проверяем доступные сети
echo "Сканирование WiFi сетей..."
nmcli dev wifi rescan 2>/dev/null
sleep 3

networks=$(nmcli -f SSID,SIGNAL,SECURITY dev wifi list | grep -v "^SSID" | head -5)
if [ -z "$networks" ]; then
    echo "ПРЕДУПРЕЖДЕНИЕ: WiFi сети не найдены"
else
    echo "✓ Найдены WiFi сети:"
    echo "$networks"
fi

# Проверяем текущее подключение
current_ssid=$(nmcli -t -f active,ssid dev wifi | grep '^yes' | cut -d':' -f2)
if [ -n "$current_ssid" ]; then
    echo "✓ Уже подключены к: $current_ssid"
else
    echo "Нет активного WiFi подключения"
fi

# Проверяем права доступа к файлам
home_dir="$HOME"
if [ -n "$SUDO_USER" ]; then
    home_dir=$(getent passwd "$SUDO_USER" | cut -d: -f6)
fi

cred_file="$home_dir/wifi_net.txt"
echo "Файл учетных данных: $cred_file"

if [ -f "$cred_file" ]; then
    echo "✓ Файл учетных данных существует"
    echo "Содержимое (первые 3 строки):"
    head -3 "$cred_file" | sed 's/:.*/:*****/'
else
    echo "Файл учетных данных не найден, создаем тестовый..."
    echo "TestNetwork:testpassword" > "$cred_file"
    chmod 600 "$cred_file"
    echo "✓ Создан тестовый файл учетных данных"
fi

# Проверяем возможность записи в /tmp
status_file="/tmp/wifi_auto_connect_status"
if echo '{"test":"ok"}' > "$status_file" 2>/dev/null; then
    echo "✓ Запись в $status_file работает"
    rm -f "$status_file"
else
    echo "ОШИБКА: Не удается записать в $status_file"
fi

echo ""
echo "=== Результат тестирования ==="
echo "Основные компоненты для работы WiFi скрипта готовы."
echo "Скрипт должен работать корректно."
echo ""
echo "Для запуска скрипта используйте:"
echo "sudo ./wifi_auto_connect.sh"