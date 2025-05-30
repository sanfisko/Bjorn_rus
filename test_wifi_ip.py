#!/usr/bin/env python3
"""
Тестовый скрипт для проверки функций получения WiFi SSID и IP адреса
"""

import subprocess
import re
import time

def get_wifi_ssid():
    """Get the current WiFi SSID."""
    try:
        result = subprocess.Popen(['iwgetid', '-r'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        ssid, error = result.communicate()
        if result.returncode != 0:
            print(f"Error executing 'iwgetid -r': {error}")
            return "Не подключено"
        return ssid.strip() if ssid.strip() else "Не подключено"
    except Exception as e:
        print(f"Error getting WiFi SSID: {e}")
        return "Ошибка"

def get_ip_address():
    """Get the current IP address of the device."""
    try:
        # Last resort: try to get any IP address using socket
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            pass
        
        return "Не найден"
    except Exception as e:
        print(f"Error getting IP address: {e}")
        return "Ошибка"

def test_wifi_ip_display():
    """Test the WiFi and IP display functionality."""
    print("Тестирование функций получения WiFi и IP информации...")
    print("=" * 50)
    
    # Test WiFi SSID
    wifi_ssid = get_wifi_ssid()
    print(f"WiFi SSID: {wifi_ssid}")
    
    # Test IP address
    ip_address = get_ip_address()
    print(f"IP адрес: {ip_address}")
    
    print("\nТестирование чередования отображения (10 секунд)...")
    print("=" * 50)
    
    show_wifi_info = True
    start_time = time.time()
    last_toggle = start_time
    
    while time.time() - start_time < 10:  # Run for 10 seconds
        current_time = time.time()
        
        # Toggle every 5 seconds
        if current_time - last_toggle >= 5:
            show_wifi_info = not show_wifi_info
            last_toggle = current_time
        
        if show_wifi_info:
            display_text = f"WiFi: {wifi_ssid}"
        else:
            display_text = f"IP: {ip_address}"
        
        print(f"\r{display_text:<30}", end="", flush=True)
        time.sleep(0.1)
    
    print("\n\nТест завершен!")

if __name__ == "__main__":
    test_wifi_ip_display()