#!/usr/bin/env python3
"""
Демонстрация полного цикла работы WiFi индикатора
Показывает: запуск -> работа -> остановка
"""

import os
import sys
import time
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont

# Добавляем путь к модулям проекта
sys.path.append('/workspace/Bjorn_rus')

import shared

def create_demo_display():
    """Создает демонстрационное изображение с индикатором WiFi"""
    
    # Размеры дисплея
    width, height = 250, 122
    scale_x = width / 250
    scale_y = height / 122
    
    # Создаем изображение
    image = Image.new('1', (width, height), 1)  # 1-битное изображение, белый фон
    draw = ImageDraw.Draw(image)
    
    # Загружаем шрифт
    try:
        font = ImageFont.truetype("/workspace/Bjorn_rus/resources/fonts/DejaVuSans.ttf", 12)
    except:
        font = ImageFont.load_default()
    
    # Рисуем текст IDLE
    idle_text = "IDLE"
    draw.text((10, 65), idle_text, font=font, fill=0)
    
    # Позиция для WiFi индикатора (справа от IDLE)
    wifi_x = int(70 * scale_x)
    wifi_y = int(65 * scale_y)
    
    # Читаем статус WiFi
    status_file = "/tmp/wifi_auto_connect_status"
    wifi_status = "stopped"  # по умолчанию
    wifi_message = "Нет данных"
    
    if os.path.exists(status_file):
        try:
            with open(status_file, 'r') as f:
                status_data = json.load(f)
                wifi_status = status_data.get('status', 'stopped')
                wifi_message = status_data.get('message', 'Нет данных')
        except:
            pass
    
    # Загружаем соответствующую иконку
    icon_path = f"/workspace/Bjorn_rus/resources/images/static/wifi_auto_connect_{wifi_status}.bmp"
    
    if os.path.exists(icon_path):
        try:
            wifi_icon = Image.open(icon_path)
            # Вставляем иконку
            image.paste(wifi_icon, (wifi_x, wifi_y))
            print(f"Показан индикатор: {wifi_status}")
        except Exception as e:
            print(f"Ошибка загрузки иконки {icon_path}: {e}")
            # Рисуем простой квадрат как fallback
            draw.rectangle([wifi_x, wifi_y, wifi_x+10, wifi_y+10], fill=0)
    else:
        print(f"Иконка не найдена: {icon_path}")
        # Рисуем простой квадрат как fallback
        draw.rectangle([wifi_x, wifi_y, wifi_x+10, wifi_y+10], fill=0)
    
    # Добавляем информацию о статусе
    status_text = f"WiFi: {wifi_status}"
    draw.text((10, 90), status_text, font=font, fill=0)
    
    # Добавляем сообщение (обрезаем если слишком длинное)
    if len(wifi_message) > 30:
        wifi_message = wifi_message[:27] + "..."
    draw.text((10, 105), wifi_message, font=font, fill=0)
    
    return image, wifi_status, wifi_message

def demo_full_cycle():
    """Демонстрирует полный цикл работы индикатора"""
    
    print("=== Демонстрация полного цикла WiFi индикатора ===\n")
    
    # 1. Показываем начальное состояние
    print("1. Начальное состояние:")
    image, status, message = create_demo_display()
    image.save("/workspace/Bjorn_rus/demo_cycle_initial.png")
    print(f"   Статус: {status}")
    print(f"   Сообщение: {message}")
    print("   Сохранено: demo_cycle_initial.png\n")
    
    # 2. Запускаем скрипт
    print("2. Запуск WiFi скрипта...")
    script_path = "/workspace/Bjorn_rus/wifi_auto_connect.sh"
    
    try:
        process = subprocess.Popen(['sudo', script_path], 
                                  stdout=subprocess.DEVNULL, 
                                  stderr=subprocess.DEVNULL)
        print("   Скрипт запущен в фоне")
        
        # Ждем немного для инициализации
        time.sleep(3)
        
        # Показываем состояние после запуска
        image, status, message = create_demo_display()
        image.save("/workspace/Bjorn_rus/demo_cycle_started.png")
        print(f"   Статус: {status}")
        print(f"   Сообщение: {message}")
        print("   Сохранено: demo_cycle_started.png\n")
        
        # 3. Ждем и показываем рабочее состояние
        print("3. Рабочее состояние (через 5 секунд):")
        time.sleep(5)
        
        image, status, message = create_demo_display()
        image.save("/workspace/Bjorn_rus/demo_cycle_working.png")
        print(f"   Статус: {status}")
        print(f"   Сообщение: {message}")
        print("   Сохранено: demo_cycle_working.png\n")
        
        # 4. Останавливаем скрипт
        print("4. Остановка WiFi скрипта...")
        result = subprocess.run("sudo pkill -f wifi_auto_connect.sh", 
                               shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   Скрипт остановлен")
        else:
            print("   Скрипт уже был остановлен или не найден")
        
        # Ждем обновления статуса
        time.sleep(3)
        
        # Показываем финальное состояние
        image, status, message = create_demo_display()
        image.save("/workspace/Bjorn_rus/demo_cycle_stopped.png")
        print(f"   Статус: {status}")
        print(f"   Сообщение: {message}")
        print("   Сохранено: demo_cycle_stopped.png\n")
        
    except Exception as e:
        print(f"   Ошибка при запуске скрипта: {e}")
    
    print("=== Демонстрация завершена ===")
    print("\nСозданы файлы:")
    print("- demo_cycle_initial.png (начальное состояние)")
    print("- demo_cycle_started.png (скрипт запущен)")
    print("- demo_cycle_working.png (рабочее состояние)")
    print("- demo_cycle_stopped.png (скрипт остановлен)")
    
    # Показываем финальный статус
    status_file = "/tmp/wifi_auto_connect_status"
    if os.path.exists(status_file):
        try:
            with open(status_file, 'r') as f:
                status_data = json.load(f)
                print(f"\nФинальный статус файла:")
                print(f"  Статус: {status_data.get('status', 'неизвестно')}")
                print(f"  Сообщение: {status_data.get('message', 'нет')}")
                print(f"  Время: {status_data.get('timestamp', 'нет')}")
        except Exception as e:
            print(f"\nОшибка чтения файла статуса: {e}")
    else:
        print(f"\nФайл статуса не найден: {status_file}")

if __name__ == "__main__":
    demo_full_cycle()