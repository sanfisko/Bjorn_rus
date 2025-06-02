#!/usr/bin/env python3
"""
Тест позиции индикатора WiFi автоподключения
"""

import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

# Добавляем путь к модулям
sys.path.append('/workspace/Bjorn_rus')

def create_test_status(status, message):
    """Создать тестовый файл статуса"""
    status_file = "/tmp/wifi_auto_connect_status"
    test_data = {
        "status": status,
        "message": message,
        "timestamp": "2025-06-02 19:30:00"
    }
    
    with open(status_file, 'w') as f:
        json.dump(test_data, f)
    print(f"Создан статус: {status} - {message}")

def test_indicator_position():
    """Тестировать позицию индикатора"""
    try:
        # Импортируем модули
        from shared import SharedData
        
        # Создаем экземпляр shared_data
        shared_data = SharedData()
        
        # Создаем тестовое изображение
        width, height = 128, 250
        image = Image.new('1', (width, height), 1)  # Белый фон
        draw = ImageDraw.Draw(image)
        
        # Рисуем рамку
        draw.rectangle((0, 0, width-1, height-1), outline=0)
        
        # Рисуем разделительные линии как в оригинале
        draw.line((1, 20, width-1, 20), fill=0)
        draw.line((1, 59, width-1, 59), fill=0)
        draw.line((1, 87, width-1, 87), fill=0)
        
        # Симулируем текст IDLE в позиции (35, 65)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
        except:
            font = ImageFont.load_default()
        
        draw.text((35, 65), "IDLE", font=font, fill=0)
        draw.text((35, 75), "Status", font=font, fill=0)
        
        # Тестируем разные статусы
        statuses = [
            ("running", "Работает"),
            ("scanning", "Сканирование"),
            ("connecting", "Подключение"),
            ("connected", "Подключено"),
            ("failed", "Ошибка"),
            ("waiting", "Ожидание"),
            ("stopped", "Остановлен")
        ]
        
        for i, (status, message) in enumerate(statuses):
            # Создаем статус
            create_test_status(status, message)
            
            # Обновляем статус вручную
            if os.path.exists("/tmp/wifi_auto_connect_status"):
                try:
                    with open("/tmp/wifi_auto_connect_status", 'r') as f:
                        status_data = json.load(f)
                    shared_data.wifi_auto_status = status_data.get('status', 'stopped')
                    shared_data.wifi_auto_message = status_data.get('message', '')
                    shared_data.wifi_auto_timestamp = status_data.get('timestamp', '')
                except:
                    shared_data.wifi_auto_status = 'stopped'
            
            # Получаем иконку
            wifi_auto_icon = shared_data.get_wifi_auto_icon()
            
            # Создаем копию изображения
            test_image = image.copy()
            test_draw = ImageDraw.Draw(test_image)
            
            # Вставляем иконку в новой позиции (70, 65)
            test_image.paste(wifi_auto_icon, (70, 65))
            
            # Добавляем подпись статуса
            test_draw.text((5, 100 + i*15), f"{status}: {message}", font=font, fill=0)
            
            # Сохраняем изображение
            filename = f"test_indicator_{status}.png"
            test_image.save(filename)
            print(f"Сохранено: {filename}")
        
        print("\nТест завершен! Проверьте созданные изображения:")
        for status, _ in statuses:
            print(f"  test_indicator_{status}.png")
            
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_indicator_position()