#!/usr/bin/env python3
"""
Тестовый скрипт для проверки логики переключения WiFi/IP информации
"""
import time

class TestWiFiIPToggle:
    def __init__(self):
        # WiFi and IP display variables
        self.wifi_info_display_time = time.time()
        self.show_wifi_info = True  # Start with WiFi info
        self.wifi_info_toggle_interval = 5  # seconds
        
        # Test data
        self.wifi_ssid = "TestNetwork"
        self.ip_address = "192.168.1.100"
    
    def test_toggle_logic(self, iterations=20):
        """Test the toggle logic for specified iterations"""
        print("Тестирование логики переключения WiFi/IP:")
        print(f"Интервал переключения: {self.wifi_info_toggle_interval} секунд")
        print("-" * 50)
        
        for i in range(iterations):
            current_time = time.time()
            
            # Original logic from display.py
            if current_time - self.wifi_info_display_time >= self.wifi_info_toggle_interval:
                self.show_wifi_info = not self.show_wifi_info
                self.wifi_info_display_time = current_time
                print(f"[{i:2d}] Переключение! Время: {current_time:.1f}")
            
            if self.show_wifi_info:
                header_text = f"WiFi: {self.wifi_ssid}"
            else:
                header_text = f"IP: {self.ip_address}"
            
            time_since_last_toggle = current_time - self.wifi_info_display_time
            print(f"[{i:2d}] {header_text} (прошло: {time_since_last_toggle:.1f}s)")
            
            # Simulate display update delay
            time.sleep(1)  # 1 second delay between iterations

if __name__ == "__main__":
    tester = TestWiFiIPToggle()
    tester.test_toggle_logic()