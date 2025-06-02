#!/usr/bin/env python3
"""
Демонстрация работы индикатора статуса WiFi автоподключения
"""

import json
import time
import os
from PIL import Image, ImageDraw, ImageFont

def create_status(status, message):
    """Создать файл статуса"""
    status_file = "/tmp/wifi_auto_connect_status"
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    
    status_data = {
        "status": status,
        "message": message,
        "timestamp": timestamp
    }
    
    with open(status_file, 'w') as f:
        json.dump(status_data, f)

def create_demo_image():
    """Создать демонстрационное изображение с индикаторами"""
    # Размер изображения
    width, height = 400, 300
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Заголовок
    draw.text((10, 10), "Индикатор статуса WiFi автоподключения", fill='black')
    draw.text((10, 30), "=" * 50, fill='black')
    
    # Загружаем иконки
    icons_dir = "/workspace/Bjorn_rus/resources/images/static"
    statuses = [
        ("running", "Работает"),
        ("scanning", "Сканирование"),
        ("connecting", "Подключение"),
        ("connected", "Подключено"),
        ("failed", "Ошибка"),
        ("waiting", "Ожидание"),
        ("stopped", "Остановлен")
    ]
    
    y_pos = 60
    for status, description in statuses:
        # Пытаемся загрузить иконку
        icon_path = os.path.join(icons_dir, f"wifi_auto_{status}.png")
        if os.path.exists(icon_path):
            try:
                icon = Image.open(icon_path)
                # Увеличиваем иконку для лучшей видимости
                icon = icon.resize((32, 32), Image.Resampling.NEAREST)
                img.paste(icon, (20, y_pos))
            except Exception as e:
                print(f"Ошибка загрузки иконки {icon_path}: {e}")
                # Рисуем простой квадрат вместо иконки
                draw.rectangle([20, y_pos, 52, y_pos + 32], outline='black', width=2)
        
        # Текст описания
        draw.text((60, y_pos + 8), f"{status}: {description}", fill='black')
        y_pos += 40
    
    # Сохраняем изображение
    demo_path = "/workspace/Bjorn_rus/wifi_indicator_demo.png"
    img.save(demo_path)
    print(f"Демонстрационное изображение сохранено: {demo_path}")
    
    return demo_path

def simulate_wifi_connection():
    """Симуляция процесса подключения к WiFi"""
    print("Симуляция работы WiFi автоподключения:")
    print("=" * 40)
    
    scenarios = [
        ("running", "Скрипт WiFi автоподключения запущен", 2),
        ("scanning", "Сканирование WiFi сетей", 3),
        ("connecting", "Подключение к TestNetwork", 4),
        ("connected", "Подключено к TestNetwork", 5),
        ("idle", "Ожидание следующей проверки", 3),
        ("scanning", "Повторное сканирование", 2),
        ("connecting", "Подключение к AnotherNetwork", 3),
        ("failed", "Не удалось подключиться", 2),
        ("waiting", "Ожидание 30 сек перед следующей попыткой", 3),
        ("stopped", "Скрипт остановлен", 2)
    ]
    
    for status, message, duration in scenarios:
        create_status(status, message)
        print(f"[{time.strftime('%H:%M:%S')}] {status.upper()}: {message}")
        time.sleep(duration)
    
    # Удаляем файл статуса
    status_file = "/tmp/wifi_auto_connect_status"
    if os.path.exists(status_file):
        os.remove(status_file)
    
    print("\nСимуляция завершена!")

if __name__ == "__main__":
    print("Демонстрация индикатора статуса WiFi автоподключения")
    print("=" * 55)
    
    # Создаем демонстрационное изображение
    demo_path = create_demo_image()
    
    print("\n1. Создано демонстрационное изображение с иконками")
    print(f"   Путь: {demo_path}")
    
    print("\n2. Запуск симуляции работы WiFi автоподключения...")
    print("   (Файл статуса будет создаваться в /tmp/wifi_auto_connect_status)")
    
    input("\nНажмите Enter для начала симуляции...")
    simulate_wifi_connection()