#!/usr/bin/env python3
"""
Создание иконок для индикатора статуса WiFi автоподключения
"""

from PIL import Image, ImageDraw
import os

def create_wifi_status_icons():
    """Создает иконки для различных статусов WiFi автоподключения"""
    
    # Размер иконок
    size = (16, 16)
    
    # Папка для сохранения иконок
    icons_dir = "/workspace/Bjorn_rus/resources/images"
    os.makedirs(icons_dir, exist_ok=True)
    
    # Статус: Работает (зеленая точка)
    img_running = Image.new('1', size, 255)  # Белый фон
    draw = ImageDraw.Draw(img_running)
    draw.ellipse([4, 4, 12, 12], fill=0)  # Черная точка (на e-ink это будет видно)
    img_running.save(os.path.join(icons_dir, "wifi_auto_running.png"))
    
    # Статус: Подключение (мигающая точка - полузаполненная)
    img_connecting = Image.new('1', size, 255)
    draw = ImageDraw.Draw(img_connecting)
    draw.ellipse([4, 4, 12, 12], outline=0, width=2)  # Контур точки
    draw.arc([6, 6, 10, 10], 0, 180, fill=0, width=2)  # Половина заполнена
    img_connecting.save(os.path.join(icons_dir, "wifi_auto_connecting.png"))
    
    # Статус: Подключено (точка с галочкой)
    img_connected = Image.new('1', size, 255)
    draw = ImageDraw.Draw(img_connected)
    draw.ellipse([2, 2, 14, 14], fill=0)  # Большая точка
    # Маленькая галочка внутри (белая на черном фоне)
    draw.line([5, 8, 7, 10], fill=255, width=1)
    draw.line([7, 10, 11, 6], fill=255, width=1)
    img_connected.save(os.path.join(icons_dir, "wifi_auto_connected.png"))
    
    # Статус: Ошибка (крестик)
    img_failed = Image.new('1', size, 255)
    draw = ImageDraw.Draw(img_failed)
    draw.ellipse([2, 2, 14, 14], outline=0, width=2)  # Контур
    # Крестик
    draw.line([5, 5, 11, 11], fill=0, width=2)
    draw.line([11, 5, 5, 11], fill=0, width=2)
    img_failed.save(os.path.join(icons_dir, "wifi_auto_failed.png"))
    
    # Статус: Ожидание (пустая точка)
    img_waiting = Image.new('1', size, 255)
    draw = ImageDraw.Draw(img_waiting)
    draw.ellipse([4, 4, 12, 12], outline=0, width=2)  # Только контур
    img_waiting.save(os.path.join(icons_dir, "wifi_auto_waiting.png"))
    
    # Статус: Сканирование (точка с волнами)
    img_scanning = Image.new('1', size, 255)
    draw = ImageDraw.Draw(img_scanning)
    draw.ellipse([6, 6, 10, 10], fill=0)  # Центральная точка
    # Волны вокруг
    draw.ellipse([3, 3, 13, 13], outline=0, width=1)
    draw.ellipse([1, 1, 15, 15], outline=0, width=1)
    img_scanning.save(os.path.join(icons_dir, "wifi_auto_scanning.png"))
    
    # Статус: Остановлен (пустой квадрат)
    img_stopped = Image.new('1', size, 255)
    draw = ImageDraw.Draw(img_stopped)
    draw.rectangle([4, 4, 12, 12], outline=0, width=2)  # Пустой квадрат
    img_stopped.save(os.path.join(icons_dir, "wifi_auto_stopped.png"))
    
    print("Иконки статуса WiFi автоподключения созданы в:", icons_dir)
    print("Созданные файлы:")
    for status in ["running", "connecting", "connected", "failed", "waiting", "scanning", "stopped"]:
        print(f"  - wifi_auto_{status}.png")

if __name__ == "__main__":
    create_wifi_status_icons()