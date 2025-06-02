#!/usr/bin/env python3
"""
Тестовый скрипт для проверки индикатора статуса WiFi автоподключения
"""

import json
import time
import os

def create_test_status(status, message):
    """Создать тестовый файл статуса"""
    status_file = "/tmp/wifi_auto_connect_status"
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    
    status_data = {
        "status": status,
        "message": message,
        "timestamp": timestamp
    }
    
    with open(status_file, 'w') as f:
        json.dump(status_data, f)
    
    print(f"Создан статус: {status} - {message}")

def test_all_statuses():
    """Протестировать все возможные статусы"""
    statuses = [
        ("running", "Скрипт WiFi автоподключения запущен"),
        ("scanning", "Сканирование WiFi сетей"),
        ("connecting", "Подключение к TestNetwork"),
        ("connected", "Подключено к TestNetwork"),
        ("failed", "Не удалось подключиться к TestNetwork"),
        ("waiting", "Ожидание 30 сек перед следующей попыткой"),
        ("idle", "Ожидание следующей проверки"),
        ("stopped", "Процесс остановлен")
    ]
    
    print("Тестирование всех статусов WiFi автоподключения:")
    print("=" * 50)
    
    for status, message in statuses:
        create_test_status(status, message)
        print(f"Статус установлен: {status}")
        input("Нажмите Enter для следующего статуса...")
    
    # Удаляем файл статуса в конце
    status_file = "/tmp/wifi_auto_connect_status"
    if os.path.exists(status_file):
        os.remove(status_file)
        print("Файл статуса удален")

if __name__ == "__main__":
    test_all_statuses()