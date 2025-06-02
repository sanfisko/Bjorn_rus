#!/usr/bin/env python3
import http.server
import socketserver
import json
import os

class SimpleTestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/load_config':
            self.handle_load_config()
        elif self.path == '/restore_default_config':
            self.handle_restore_default_config()
        elif self.path == '/scan_wifi':
            self.handle_scan_wifi()
        elif self.path == '/get_known_wifi_networks':
            self.handle_get_known_wifi_networks()
        elif self.path == '/get_wifi_script_status':
            self.handle_get_wifi_script_status()
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/save_config':
            self.handle_save_config()
        elif self.path == '/add_wifi_network':
            self.handle_add_wifi_network()
        elif self.path == '/remove_wifi_network':
            self.handle_remove_wifi_network()
        elif self.path == '/connect_wifi':
            self.handle_connect_wifi()
        else:
            self.send_response(404)
            self.end_headers()
    
    def handle_load_config(self):
        # Возвращаем тестовую конфигурацию
        test_config = {
            "__title_General": "Общие настройки",
            "debug": True,
            "web_delay": 5,
            "epd_type": "epd2in13_V4",
            "__title_Network": "Сетевые настройки", 
            "portlist": [22, 80, 443, 8080],
            "scan_timeout": 30,
            "max_threads": 10,
            "__title_WiFi": "WiFi настройки",
            "wifi_script_running": False,
            "wifi_auto_connect": True,
            "__title_Security": "Настройки безопасности",
            "steal_file_names": ["passwords.txt", "config.ini"],
            "steal_file_extensions": [".txt", ".log", ".conf"]
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(test_config).encode('utf-8'))
    
    def handle_restore_default_config(self):
        # Возвращаем дефолтную конфигурацию
        default_config = {
            "__title_General": "Общие настройки",
            "debug": False,
            "web_delay": 3,
            "epd_type": "epd2in13_V4",
            "__title_Network": "Сетевые настройки",
            "portlist": [22, 80, 443],
            "scan_timeout": 20,
            "max_threads": 5,
            "__title_WiFi": "WiFi настройки",
            "wifi_script_running": False,
            "wifi_auto_connect": False,
            "__title_Security": "Настройки безопасности",
            "steal_file_names": [],
            "steal_file_extensions": []
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(default_config).encode('utf-8'))
    
    def handle_save_config(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            print("Received config data:", data)
            
            response = {'success': True, 'message': 'Конфигурация сохранена'}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception as e:
            response = {'success': False, 'message': str(e)}
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def handle_scan_wifi(self):
        # Возвращаем тестовые WiFi сети
        wifi_data = {
            'networks': ['TestWiFi', 'HomeNetwork', 'OfficeWiFi', 'GuestNetwork'],
            'current_ssid': 'TestWiFi'
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(wifi_data).encode('utf-8'))
    
    def handle_get_known_wifi_networks(self):
        # Возвращаем тестовые известные сети
        networks_data = {
            'success': True,
            'networks': [
                {'ssid': 'HomeNetwork', 'password': '********'},
                {'ssid': 'OfficeWiFi', 'password': '********'}
            ]
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(networks_data).encode('utf-8'))
    
    def handle_get_wifi_script_status(self):
        # Возвращаем статус WiFi скрипта
        status_data = {
            'wifi_script_running': False
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(status_data).encode('utf-8'))
    
    def handle_add_wifi_network(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            response = {'success': True, 'message': f'Сеть {data.get("ssid")} добавлена'}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception as e:
            response = {'success': False, 'message': str(e)}
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def handle_remove_wifi_network(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            response = {'success': True, 'message': f'Сеть {data.get("ssid")} удалена'}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception as e:
            response = {'success': False, 'message': str(e)}
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def handle_connect_wifi(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            response = {'message': f'Подключение к сети {data.get("ssid")} выполнено'}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception as e:
            response = {'message': f'Ошибка подключения: {str(e)}'}
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

if __name__ == "__main__":
    os.chdir('/workspace/Bjorn_rus/web')
    PORT = 12000
    with socketserver.TCPServer(("", PORT), SimpleTestHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()