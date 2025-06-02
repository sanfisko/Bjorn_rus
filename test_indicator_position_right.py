#!/usr/bin/env python3
"""
Тест позиционирования WiFi индикатора максимально справа
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageDraw, ImageFont
import json

def test_indicator_position():
    """Тестирует позицию индикатора максимально справа"""
    
    # Размеры экрана
    width, height = 122, 250
    scale_factor_x = width / 122
    scale_factor_y = height / 250
    
    # Создаем изображение
    image = Image.new('1', (width, height), 255)
    draw = ImageDraw.Draw(image)
    
    # Рисуем границы экрана
    draw.rectangle((0, 0, width-1, height-1), outline=0)
    draw.line((0, 20, width-1, 20), fill=0)
    draw.line((0, 59, width-1, 59), fill=0)
    draw.line((0, 87, width-1, 87), fill=0)
    
    # Позиция IDLE текста (примерно)
    try:
        font = ImageFont.load_default()
    except:
        font = None
    
    if font:
        draw.text((8, 65), "IDLE", font=font, fill=0)
    
    # Новая позиция индикатора (максимально справа)
    indicator_x = int(110 * scale_factor_x)
    indicator_y = int(65 * scale_factor_y)
    
    # Рисуем индикатор (квадрат 10x10)
    draw.rectangle((indicator_x, indicator_y, indicator_x+10, indicator_y+10), fill=0)
    draw.text((indicator_x+2, indicator_y+2), "W", fill=255)
    
    # Показываем координаты
    print(f"Размеры экрана: {width}x{height}")
    print(f"Позиция индикатора: ({indicator_x}, {indicator_y})")
    print(f"Расстояние от правого края: {width - indicator_x - 10} пикселей")
    
    # Сохраняем изображение
    image.save('test_indicator_right_position.png')
    print("Тестовое изображение сохранено как test_indicator_right_position.png")
    
    return indicator_x, indicator_y

if __name__ == "__main__":
    test_indicator_position()