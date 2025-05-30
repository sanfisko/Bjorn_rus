#!/usr/bin/env python3
"""
Демонстрационный скрипт для показа отображения WiFi и IP информации
"""

import time
import socket

def get_demo_wifi_ssid():
    """Демо функция для получения WiFi SSID."""
    # В реальной среде это будет название WiFi сети
    return "MyWiFiNetwork"

def get_demo_ip_address():
    """Демо функция для получения IP адреса."""
    try:
        # Получаем реальный IP адрес
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "192.168.1.100"

def demo_display():
    """Демонстрация отображения WiFi и IP информации с чередованием."""
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ ОТОБРАЖЕНИЯ WiFi И IP ИНФОРМАЦИИ")
    print("=" * 60)
    print("Информация будет чередоваться каждые 5 секунд")
    print("Нажмите Ctrl+C для выхода")
    print("=" * 60)
    
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
                print("\n" + "-" * 40)
            
            if show_wifi_info:
                display_text = f"📶 WiFi: {wifi_ssid}"
            else:
                display_text = f"🌐 IP: {ip_address}"
            
            # Показываем время до следующего переключения
            time_left = 5 - (current_time - last_toggle)
            
            print(f"\r{display_text:<30} (переключение через {time_left:.1f}с)", end="", flush=True)
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n\nДемонстрация завершена!")

if __name__ == "__main__":
    demo_display()