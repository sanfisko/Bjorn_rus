#!/usr/bin/env python3
"""
Демонстрация визуального индикатора WiFi автоподключения
Показывает как индикатор выглядит на экране в разных состояниях
"""

import sys
import os
from PIL import Image, ImageDraw, ImageFont
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_screen_demo(status, title):
    """Создает демонстрацию экрана с индикатором"""
    
    # Размеры экрана Bjorn
    width, height = 122, 250
    scale_factor_x = width / 122
    scale_factor_y = height / 250
    
    # Создаем изображение
    image = Image.new('1', (width, height), 255)  # Белый фон
    draw = ImageDraw.Draw(image)
    
    # Рисуем границы экрана
    draw.rectangle((0, 0, width-1, height-1), outline=0)
    
    # Рисуем разделители (как на реальном экране)
    draw.line((0, 20, width-1, 20), fill=0)  # Верхняя строка
    draw.line((0, 59, width-1, 59), fill=0)  # Разделитель
    draw.line((0, 87, width-1, 87), fill=0)  # Разделитель
    
    # Загружаем шрифт
    try:
        font = ImageFont.load_default()
    except:
        font = None
    
    # Рисуем заголовок
    draw.text((2, 2), "BJORN WiFi Demo", font=font, fill=0)
    
    # Рисуем основной текст (имитация реального интерфейса)
    draw.text((2, 25), "Status: Active", font=font, fill=0)
    draw.text((2, 40), "Mode: Monitor", font=font, fill=0)
    
    # Рисуем текст IDLE и индикатор WiFi
    draw.text((8, 65), "IDLE", font=font, fill=0)
    
    # Позиция индикатора (максимально справа)
    indicator_x = int(110 * scale_factor_x)
    indicator_y = int(65 * scale_factor_y)
    
    # Рисуем индикатор в зависимости от статуса
    if status == "running":
        # Черный круг с "R"
        draw.ellipse((indicator_x, indicator_y, indicator_x+10, indicator_y+10), fill=0)
        draw.text((indicator_x+3, indicator_y+2), "R", font=font, fill=255)
        status_text = "WiFi script running"
        
    elif status == "connecting":
        # Анимированный индикатор (треугольник)
        points = [(indicator_x+2, indicator_y), (indicator_x+8, indicator_y+5), (indicator_x+2, indicator_y+10)]
        draw.polygon(points, fill=0)
        draw.text((indicator_x+3, indicator_y+3), "→", font=font, fill=255)
        status_text = "Connecting to WiFi"
        
    elif status == "connected":
        # Черный квадрат с "C"
        draw.rectangle((indicator_x, indicator_y, indicator_x+10, indicator_y+10), fill=0)
        draw.text((indicator_x+3, indicator_y+2), "C", font=font, fill=255)
        status_text = "Connected to WiFi"
        
    elif status == "failed":
        # Красный X (имитация черным)
        draw.line((indicator_x+2, indicator_y+2, indicator_x+8, indicator_y+8), fill=0)
        draw.line((indicator_x+8, indicator_y+2, indicator_x+2, indicator_y+8), fill=0)
        draw.rectangle((indicator_x, indicator_y, indicator_x+10, indicator_y+10), outline=0)
        status_text = "Connection failed"
        
    elif status == "waiting":
        # Треугольник с "W"
        points = [(indicator_x, indicator_y+10), (indicator_x+5, indicator_y), (indicator_x+10, indicator_y+10)]
        draw.polygon(points, fill=0)
        draw.text((indicator_x+3, indicator_y+6), "W", font=font, fill=255)
        status_text = "Waiting for retry"
        
    elif status == "scanning":
        # Круг с точками (имитация сканирования)
        draw.ellipse((indicator_x, indicator_y, indicator_x+10, indicator_y+10), outline=0)
        draw.point((indicator_x+3, indicator_y+3), fill=0)
        draw.point((indicator_x+7, indicator_y+3), fill=0)
        draw.point((indicator_x+5, indicator_y+7), fill=0)
        status_text = "Scanning networks"
        
    elif status == "stopped":
        # Пустой квадрат с "S"
        draw.rectangle((indicator_x, indicator_y, indicator_x+10, indicator_y+10), outline=0, fill=255)
        draw.text((indicator_x+3, indicator_y+2), "S", font=font, fill=0)
        status_text = "WiFi script stopped"
    
    # Рисуем статус внизу
    draw.text((2, 95), status_text, font=font, fill=0)
    
    # Рисуем информацию о позиции
    draw.text((2, 110), f"Pos: ({indicator_x}, {indicator_y})", font=font, fill=0)
    draw.text((2, 125), f"Distance from edge: {width - indicator_x - 10}px", font=font, fill=0)
    
    # Рисуем стрелку указывающую на индикатор
    draw.line((indicator_x-15, indicator_y+5, indicator_x-2, indicator_y+5), fill=0)
    draw.polygon([(indicator_x-2, indicator_y+3), (indicator_x-2, indicator_y+7), (indicator_x+1, indicator_y+5)], fill=0)
    
    return image

def main():
    """Создает демонстрацию всех состояний индикатора"""
    
    print("=== Демонстрация визуального индикатора WiFi ===")
    print("Создание изображений для всех состояний...")
    
    # Все возможные состояния
    statuses = [
        ("running", "Скрипт запущен"),
        ("connecting", "Подключение"),
        ("connected", "Подключен"),
        ("failed", "Ошибка"),
        ("waiting", "Ожидание"),
        ("scanning", "Сканирование"),
        ("stopped", "Остановлен")
    ]
    
    # Создаем изображения для каждого состояния
    for status, title in statuses:
        image = create_screen_demo(status, title)
        filename = f"demo_indicator_{status}.png"
        image.save(filename)
        print(f"✅ Создано: {filename} - {title}")
    
    # Создаем сравнительное изображение
    print("\nСоздание сравнительного изображения...")
    
    # Создаем большое изображение для сравнения
    comparison_width = 122 * 4  # 4 изображения в ряд
    comparison_height = 250 * 2  # 2 ряда
    comparison = Image.new('1', (comparison_width, comparison_height), 255)
    
    # Размещаем изображения
    positions = [
        (0, 0), (122, 0), (244, 0), (366, 0),  # Первый ряд
        (0, 250), (122, 250), (244, 250)       # Второй ряд
    ]
    
    for i, (status, title) in enumerate(statuses):
        if i < len(positions):
            image = create_screen_demo(status, title)
            x, y = positions[i]
            comparison.paste(image, (x, y))
    
    comparison.save("demo_all_indicators.png")
    print("✅ Создано: demo_all_indicators.png - Все состояния")
    
    print("\n=== Демонстрация завершена ===")
    print("📍 Позиция индикатора: (110, 65) - максимально справа")
    print("📏 Расстояние от правого края: 2 пикселя")
    print("📱 Размер экрана: 122x250 пикселей")
    print("🎯 Индикатор размером: 10x10 пикселей")
    
    print("\n📄 Созданные файлы:")
    for status, _ in statuses:
        print(f"   - demo_indicator_{status}.png")
    print("   - demo_all_indicators.png")

if __name__ == "__main__":
    main()