#!/usr/bin/env python3
"""
Улучшенный тест переключателя WiFi автоподключения
"""

import sys
import os
import time
import json
import subprocess
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_script_execution():
    """Тестирует запуск и остановку скрипта"""
    
    print("=== Тест улучшенного переключателя WiFi ===")
    
    # Очищаем предыдущие процессы
    subprocess.run("sudo pkill -f wifi_auto_connect.sh", shell=True, check=False)
    time.sleep(1)
    
    # Удаляем старый файл статуса
    if os.path.exists('/tmp/wifi_auto_connect_status'):
        os.remove('/tmp/wifi_auto_connect_status')
    
    print("1. Запускаем скрипт...")
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wifi_auto_connect.sh')
    process = subprocess.Popen(['sudo', script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Ждем создания файла статуса
    for i in range(10):
        if os.path.exists('/tmp/wifi_auto_connect_status'):
            break
        time.sleep(0.5)
    
    # Проверяем статус через 2 секунды (как в utils.py)
    time.sleep(2)
    
    # Проверяем процесс
    result = subprocess.run("pgrep -f wifi_auto_connect.sh", shell=True, capture_output=True, text=True)
    process_running = result.returncode == 0
    
    # Проверяем файл статуса
    status_file_exists = os.path.exists('/tmp/wifi_auto_connect_status')
    file_status = "unknown"
    if status_file_exists:
        try:
            with open('/tmp/wifi_auto_connect_status', 'r') as f:
                status_data = json.loads(f.read())
                file_status = status_data.get('status', 'stopped')
                print(f"   Статус из файла: {file_status}")
                print(f"   Сообщение: {status_data.get('message', 'N/A')}")
        except Exception as e:
            print(f"   Ошибка чтения файла статуса: {e}")
    
    print(f"   Процесс запущен: {process_running}")
    print(f"   Файл статуса существует: {status_file_exists}")
    print(f"   Статус в файле: {file_status}")
    
    # Логика из utils.py
    actual_status = process_running
    if status_file_exists and file_status != 'stopped':
        actual_status = True
    
    print(f"   Итоговый статус: {actual_status}")
    
    print("\n2. Останавливаем скрипт...")
    subprocess.run("sudo pkill -f wifi_auto_connect.sh", shell=True, check=False)
    time.sleep(2)
    
    # Проверяем после остановки
    result = subprocess.run("pgrep -f wifi_auto_connect.sh", shell=True, capture_output=True, text=True)
    process_running = result.returncode == 0
    
    status_file_exists = os.path.exists('/tmp/wifi_auto_connect_status')
    file_status = "unknown"
    if status_file_exists:
        try:
            with open('/tmp/wifi_auto_connect_status', 'r') as f:
                status_data = json.loads(f.read())
                file_status = status_data.get('status', 'stopped')
                print(f"   Статус из файла: {file_status}")
        except Exception as e:
            print(f"   Ошибка чтения файла статуса: {e}")
    
    print(f"   Процесс запущен: {process_running}")
    print(f"   Файл статуса существует: {status_file_exists}")
    print(f"   Статус в файле: {file_status}")
    
    # Логика из utils.py
    actual_status = process_running
    if status_file_exists and file_status != 'stopped':
        actual_status = True
    
    print(f"   Итоговый статус: {actual_status}")
    
    print("\n=== Тест завершен ===")

if __name__ == "__main__":
    test_script_execution()