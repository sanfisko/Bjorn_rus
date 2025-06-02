#!/usr/bin/env python3
"""
Проверка системы индикатора статуса WiFi автоподключения
"""

import os
import json
import sys

def check_files():
    """Проверить наличие всех необходимых файлов"""
    print("Проверка файлов системы индикатора WiFi:")
    print("=" * 45)
    
    files_to_check = [
        ("wifi_auto_connect.sh", "Скрипт автоподключения"),
        ("shared.py", "Общие данные"),
        ("display.py", "Модуль дисплея"),
        ("resources/images/static/wifi_auto_running.png", "Иконка 'работает'"),
        ("resources/images/static/wifi_auto_scanning.png", "Иконка 'сканирование'"),
        ("resources/images/static/wifi_auto_connecting.png", "Иконка 'подключение'"),
        ("resources/images/static/wifi_auto_connected.png", "Иконка 'подключено'"),
        ("resources/images/static/wifi_auto_failed.png", "Иконка 'ошибка'"),
        ("resources/images/static/wifi_auto_waiting.png", "Иконка 'ожидание'"),
        ("resources/images/static/wifi_auto_stopped.png", "Иконка 'остановлен'"),
    ]
    
    all_ok = True
    for file_path, description in files_to_check:
        if os.path.exists(file_path):
            print(f"✓ {description}: {file_path}")
        else:
            print(f"✗ {description}: {file_path} - НЕ НАЙДЕН")
            all_ok = False
    
    return all_ok

def check_shared_py():
    """Проверить изменения в shared.py"""
    print("\nПроверка изменений в shared.py:")
    print("=" * 35)
    
    try:
        with open("shared.py", 'r') as f:
            content = f.read()
        
        checks = [
            ("wifi_auto_status", "Переменная статуса"),
            ("wifi_auto_message", "Переменная сообщения"),
            ("wifi_auto_timestamp", "Переменная времени"),
            ("wifi_auto_running", "Загрузка иконки 'работает'"),
            ("wifi_auto_scanning", "Загрузка иконки 'сканирование'"),
            ("wifi_auto_connecting", "Загрузка иконки 'подключение'"),
            ("wifi_auto_connected", "Загрузка иконки 'подключено'"),
            ("wifi_auto_failed", "Загрузка иконки 'ошибка'"),
            ("wifi_auto_waiting", "Загрузка иконки 'ожидание'"),
            ("wifi_auto_stopped", "Загрузка иконки 'остановлен'"),
            ("get_wifi_auto_icon", "Метод получения иконки"),
        ]
        
        all_ok = True
        for check, description in checks:
            if check in content:
                print(f"✓ {description}")
            else:
                print(f"✗ {description} - НЕ НАЙДЕНО")
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print(f"✗ Ошибка чтения shared.py: {e}")
        return False

def check_display_py():
    """Проверить изменения в display.py"""
    print("\nПроверка изменений в display.py:")
    print("=" * 35)
    
    try:
        with open("display.py", 'r') as f:
            content = f.read()
        
        checks = [
            ("update_wifi_auto_status", "Метод обновления статуса"),
            ("get_wifi_auto_icon", "Вызов метода получения иконки"),
            ("wifi_auto_icon", "Переменная иконки"),
        ]
        
        all_ok = True
        for check, description in checks:
            if check in content:
                print(f"✓ {description}")
            else:
                print(f"✗ {description} - НЕ НАЙДЕНО")
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print(f"✗ Ошибка чтения display.py: {e}")
        return False

def check_wifi_script():
    """Проверить изменения в wifi_auto_connect.sh"""
    print("\nПроверка изменений в wifi_auto_connect.sh:")
    print("=" * 42)
    
    try:
        with open("wifi_auto_connect.sh", 'r') as f:
            content = f.read()
        
        checks = [
            ("STATUS_FILE", "Переменная файла статуса"),
            ("update_status", "Функция обновления статуса"),
            ("init_status", "Функция инициализации статуса"),
            ("/tmp/wifi_auto_connect_status", "Путь к файлу статуса"),
        ]
        
        all_ok = True
        for check, description in checks:
            if check in content:
                print(f"✓ {description}")
            else:
                print(f"✗ {description} - НЕ НАЙДЕНО")
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print(f"✗ Ошибка чтения wifi_auto_connect.sh: {e}")
        return False

def test_status_file():
    """Протестировать создание файла статуса"""
    print("\nТестирование файла статуса:")
    print("=" * 30)
    
    status_file = "/tmp/wifi_auto_connect_status"
    
    # Создаем тестовый файл статуса
    test_data = {
        "status": "testing",
        "message": "Тестирование системы",
        "timestamp": "2025-06-02 16:51:00"
    }
    
    try:
        with open(status_file, 'w') as f:
            json.dump(test_data, f)
        print(f"✓ Файл статуса создан: {status_file}")
        
        # Читаем файл обратно
        with open(status_file, 'r') as f:
            read_data = json.load(f)
        
        if read_data == test_data:
            print("✓ Файл статуса читается корректно")
        else:
            print("✗ Ошибка чтения файла статуса")
            return False
        
        # Удаляем тестовый файл
        os.remove(status_file)
        print("✓ Тестовый файл статуса удален")
        
        return True
        
    except Exception as e:
        print(f"✗ Ошибка работы с файлом статуса: {e}")
        return False

def main():
    """Основная функция проверки"""
    print("ПРОВЕРКА СИСТЕМЫ ИНДИКАТОРА СТАТУСА WiFi АВТОПОДКЛЮЧЕНИЯ")
    print("=" * 60)
    
    checks = [
        ("Файлы", check_files),
        ("shared.py", check_shared_py),
        ("display.py", check_display_py),
        ("wifi_auto_connect.sh", check_wifi_script),
        ("Файл статуса", test_status_file),
    ]
    
    all_passed = True
    results = []
    
    for name, check_func in checks:
        result = check_func()
        results.append((name, result))
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    print("ИТОГОВЫЕ РЕЗУЛЬТАТЫ:")
    print("=" * 60)
    
    for name, result in results:
        status = "✓ ПРОЙДЕНО" if result else "✗ ОШИБКА"
        print(f"{name:20} {status}")
    
    print("=" * 60)
    if all_passed:
        print("🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!")
        print("\nСистема индикатора статуса WiFi автоподключения готова к работе.")
        print("\nДля тестирования запустите:")
        print("  python3 run_wifi_simulation.py")
        return 0
    else:
        print("❌ ОБНАРУЖЕНЫ ОШИБКИ!")
        print("\nНеобходимо исправить указанные проблемы.")
        return 1

if __name__ == "__main__":
    sys.exit(main())