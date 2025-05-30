#!/usr/bin/env python3
"""
Демонстрационный скрипт для показа отображения WiFi и IP информации в заголовке
"""

import time
import socket

def get_demo_wifi_ssid():
    """Демо функция для получения WiFi SSID."""
    return "MyWiFiNetwork"

def get_demo_ip_address():
    """Демо функция для получения IP адреса."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "192.168.1.100"

def demo_header_display():
    """Демонстрация отображения WiFi и IP информации в заголовке (вместо BJORN)."""
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ ОТОБРАЖЕНИЯ WiFi И IP В ЗАГОЛОВКЕ")
    print("=" * 70)
    print("Вместо текста 'BJORN' в верхней части экрана будет отображаться:")
    print("WiFi информация и IP адрес с чередованием каждые 5 секунд")
    print("Нажмите Ctrl+C для выхода")
    print("=" * 70)
    
    wifi_ssid = get_demo_wifi_ssid()
    ip_address = get_demo_ip_address()
    
    show_wifi_info = True
    last_toggle = time.time()
    
    try:
        while True:
            current_time = time.time()
            
            # Переключение каждые 5 секунд
            if current_time - last_toggle >= 5:
                show_wifi_info = not show_wifi_info
                last_toggle = current_time
                print("\n" + "-" * 50)
            
            if show_wifi_info:
                header_text = f"WiFi: {wifi_ssid}"
                icon = "📶"
            else:
                header_text = f"IP: {ip_address}"
                icon = "🌐"
            
            # Показываем время до следующего переключения
            time_left = 5 - (current_time - last_toggle)
            
            # Имитируем отображение заголовка
            print(f"\r{icon} ЗАГОЛОВОК: {header_text:<25} (переключение через {time_left:.1f}с)", end="", flush=True)
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n\nДемонстрация завершена!")
        print("\nТеперь вместо 'BJORN' в верхней части экрана будет отображаться:")
        print(f"• WiFi: {wifi_ssid}")
        print(f"• IP: {ip_address}")
        print("с чередованием каждые 5 секунд")

if __name__ == "__main__":
    demo_header_display()