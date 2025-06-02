#!/usr/bin/env python3
"""
Тест переключателя WiFi автоподключения
"""

import json
import os
import sys
import subprocess
import time

# Добавляем путь к модулям
sys.path.append('/workspace/Bjorn_rus')

def test_wifi_switch():
    """Тестировать переключатель WiFi"""
    try:
        from utils import WebUtils
        from shared import SharedData
        from logger import Logger
        import logging
        
        # Создаем экземпляры
        shared_data = SharedData()
        logger = Logger(name="test_wifi_switch", level=logging.DEBUG)
        web_utils = WebUtils(shared_data, logger)
        
        print("=== Тест переключателя WiFi автоподключения ===")
        
        # Проверяем текущий статус
        result = subprocess.run("pgrep -f wifi_auto_connect.sh", shell=True, capture_output=True, text=True)
        initial_running = result.returncode == 0
        print(f"Начальный статус скрипта: {'Работает' if initial_running else 'Остановлен'}")
        
        # Тест 1: Включение скрипта
        print("\n--- Тест 1: Включение скрипта ---")
        params = {'wifi_script_running': True}
        
        # Симулируем обработку параметров как в save_configuration
        with open(shared_data.shared_config_json, 'r') as f:
            current_config = json.load(f)
        
        # Обновляем конфигурацию
        for key, value in params.items():
            current_config[key] = value
        
        # Сохраняем конфигурацию
        with open(shared_data.shared_config_json, 'w') as f:
            json.dump(current_config, f, indent=4)
        
        # Обрабатываем wifi_script_running
        if 'wifi_script_running' in params:
            try:
                if params['wifi_script_running']:
                    # Start the script manually in background with sudo
                    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wifi_auto_connect.sh')
                    subprocess.Popen(['sudo', script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    print("WiFi auto-connect script started manually with sudo")
                else:
                    # Stop the script by killing the process
                    subprocess.run("sudo pkill -f wifi_auto_connect.sh", shell=True, check=False)
                    print("WiFi auto-connect script stopped manually")
                
                # Wait a moment and check the actual status
                time.sleep(1)
                result = subprocess.run("pgrep -f wifi_auto_connect.sh", shell=True, capture_output=True, text=True)
                actual_status = result.returncode == 0
                current_config['wifi_script_running'] = actual_status
                print(f"WiFi script actual status: {actual_status}")
                
            except Exception as e:
                print(f"Failed to manage wifi script manually: {e}")
                current_config['wifi_script_running'] = False
        
        # Проверяем статус через 2 секунды
        time.sleep(2)
        result = subprocess.run("pgrep -f wifi_auto_connect.sh", shell=True, capture_output=True, text=True)
        script_running = result.returncode == 0
        print(f"Статус после включения: {'Работает' if script_running else 'Остановлен'}")
        
        # Проверяем файл статуса
        if os.path.exists("/tmp/wifi_auto_connect_status"):
            with open("/tmp/wifi_auto_connect_status", 'r') as f:
                status_data = json.load(f)
            print(f"Файл статуса: {status_data}")
        else:
            print("Файл статуса не найден")
        
        # Тест 2: Выключение скрипта
        print("\n--- Тест 2: Выключение скрипта ---")
        params = {'wifi_script_running': False}
        
        # Симулируем обработку параметров как в save_configuration
        with open(shared_data.shared_config_json, 'r') as f:
            current_config = json.load(f)
        
        # Обновляем конфигурацию
        for key, value in params.items():
            current_config[key] = value
        
        # Сохраняем конфигурацию
        with open(shared_data.shared_config_json, 'w') as f:
            json.dump(current_config, f, indent=4)
        
        # Обрабатываем wifi_script_running
        if 'wifi_script_running' in params:
            try:
                if params['wifi_script_running']:
                    # Start the script manually in background with sudo
                    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wifi_auto_connect.sh')
                    subprocess.Popen(['sudo', script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    print("WiFi auto-connect script started manually with sudo")
                else:
                    # Stop the script by killing the process
                    subprocess.run("sudo pkill -f wifi_auto_connect.sh", shell=True, check=False)
                    print("WiFi auto-connect script stopped manually")
                
                # Wait a moment and check the actual status
                time.sleep(1)
                result = subprocess.run("pgrep -f wifi_auto_connect.sh", shell=True, capture_output=True, text=True)
                actual_status = result.returncode == 0
                current_config['wifi_script_running'] = actual_status
                print(f"WiFi script actual status: {actual_status}")
                
            except Exception as e:
                print(f"Failed to manage wifi script manually: {e}")
                current_config['wifi_script_running'] = False
        
        # Проверяем статус через 2 секунды
        time.sleep(2)
        result = subprocess.run("pgrep -f wifi_auto_connect.sh", shell=True, capture_output=True, text=True)
        script_running = result.returncode == 0
        print(f"Статус после выключения: {'Работает' if script_running else 'Остановлен'}")
        
        # Проверяем файл статуса
        if os.path.exists("/tmp/wifi_auto_connect_status"):
            with open("/tmp/wifi_auto_connect_status", 'r') as f:
                status_data = json.load(f)
            print(f"Файл статуса: {status_data}")
        else:
            print("Файл статуса не найден")
        
        print("\n=== Тест завершен ===")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_wifi_switch()