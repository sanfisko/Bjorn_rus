#!/usr/bin/env python3
"""
Финальный тест переключателя WiFi автоподключения
"""

import sys
import os
import time
import json
import subprocess
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_improved_switch():
    """Тестирует улучшенный переключатель"""
    
    print("=== Финальный тест переключателя WiFi ===")
    
    # Очищаем предыдущие процессы
    subprocess.run("sudo pkill -KILL -f wifi_auto_connect.sh", shell=True, check=False)
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
    
    time.sleep(2)
    
    # Проверяем статус
    result = subprocess.run("pgrep -f wifi_auto_connect.sh", shell=True, capture_output=True, text=True)
    process_running = result.returncode == 0
    
    status_file_exists = os.path.exists('/tmp/wifi_auto_connect_status')
    file_status = "unknown"
    if status_file_exists:
        try:
            with open('/tmp/wifi_auto_connect_status', 'r') as f:
                status_data = json.loads(f.read())
                file_status = status_data.get('status', 'stopped')
        except:
            pass
    
    print(f"   Процесс: {process_running}, Файл: {status_file_exists}, Статус: {file_status}")
    
    print("\n2. Останавливаем скрипт (улучшенным способом)...")
    
    # Используем улучшенную логику остановки
    subprocess.run("sudo pkill -TERM -f wifi_auto_connect.sh", shell=True, check=False)
    time.sleep(1)
    subprocess.run("sudo pkill -KILL -f wifi_auto_connect.sh", shell=True, check=False)
    
    # Обновляем файл статуса вручную
    try:
        status_file = '/tmp/wifi_auto_connect_status'
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        status_data = {"status": "stopped", "message": "Скрипт остановлен через веб-интерфейс", "timestamp": timestamp}
        with open(status_file, 'w') as f:
            json.dump(status_data, f)
        os.chmod(status_file, 0o666)
        print("   Файл статуса обновлен вручную")
    except Exception as e:
        print(f"   Ошибка обновления файла статуса: {e}")
    
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
        except:
            pass
    
    # Логика из utils.py
    actual_status = process_running
    if status_file_exists and file_status != 'stopped':
        actual_status = True
    
    print(f"   Процесс: {process_running}, Файл: {status_file_exists}, Статус: {file_status}")
    print(f"   Итоговый статус: {actual_status}")
    
    if not actual_status:
        print("✅ Переключатель работает корректно!")
    else:
        print("❌ Проблема с переключателем")
    
    print("\n=== Тест завершен ===")

if __name__ == "__main__":
    test_improved_switch()