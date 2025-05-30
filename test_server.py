#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
import pwd
from urllib.parse import parse_qs, urlparse

class TestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/get_known_wifi_networks':
            self.handle_get_known_wifi_networks()
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/add_wifi_network':
            self.handle_add_wifi_network()
        elif self.path == '/remove_wifi_network':
            self.handle_remove_wifi_network()
        else:
            self.send_response(404)
            self.end_headers()
    
    def handle_get_known_wifi_networks(self):
        try:
            # Определяем домашнюю папку пользователя
            if os.environ.get('SUDO_USER'):
                home_dir = pwd.getpwnam(os.environ['SUDO_USER']).pw_dir
            else:
                home_dir = os.path.expanduser('~')
            
            wifi_file = os.path.join(home_dir, 'wifi_net.txt')
            networks = []
            
            if os.path.exists(wifi_file):
                with open(wifi_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if ':' in line:
                            ssid, password = line.split(':', 1)
                            networks.append({'ssid': ssid, 'password': password})
            
            response = {'success': True, 'networks': networks}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception as e:
            response = {'success': False, 'message': str(e)}
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def handle_add_wifi_network(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            ssid = data.get('ssid', '').strip()
            password = data.get('password', '').strip()
            
            if not ssid or not password:
                raise ValueError("SSID и пароль обязательны")
            
            if len(ssid) > 32:
                raise ValueError("SSID не может быть длиннее 32 символов")
            
            if len(password) > 63:
                raise ValueError("Пароль не может быть длиннее 63 символов")
            
            # Определяем домашнюю папку пользователя
            if os.environ.get('SUDO_USER'):
                home_dir = pwd.getpwnam(os.environ['SUDO_USER']).pw_dir
            else:
                home_dir = os.path.expanduser('~')
            
            wifi_file = os.path.join(home_dir, 'wifi_net.txt')
            
            # Проверяем, существует ли уже такая сеть
            existing_networks = []
            if os.path.exists(wifi_file):
                with open(wifi_file, 'r', encoding='utf-8') as f:
                    existing_networks = f.readlines()
            
            network_line = f"{ssid}:{password}\n"
            for line in existing_networks:
                if line.strip().startswith(f"{ssid}:"):
                    raise ValueError(f"Сеть {ssid} уже существует")
            
            # Добавляем новую сеть
            with open(wifi_file, 'a', encoding='utf-8') as f:
                f.write(network_line)
            
            # Устанавливаем права доступа
            os.chmod(wifi_file, 0o600)
            
            response = {'success': True, 'message': f'Сеть {ssid} добавлена'}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception as e:
            response = {'success': False, 'message': str(e)}
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def handle_remove_wifi_network(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            ssid = data.get('ssid', '').strip()
            
            if not ssid:
                raise ValueError("SSID обязателен")
            
            # Определяем домашнюю папку пользователя
            if os.environ.get('SUDO_USER'):
                home_dir = pwd.getpwnam(os.environ['SUDO_USER']).pw_dir
            else:
                home_dir = os.path.expanduser('~')
            
            wifi_file = os.path.join(home_dir, 'wifi_net.txt')
            
            if not os.path.exists(wifi_file):
                raise ValueError("Файл с сетями не найден")
            
            # Читаем существующие сети
            with open(wifi_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Фильтруем сети, исключая удаляемую
            new_lines = []
            found = False
            for line in lines:
                if not line.strip().startswith(f"{ssid}:"):
                    new_lines.append(line)
                else:
                    found = True
            
            if not found:
                raise ValueError(f"Сеть {ssid} не найдена")
            
            # Записываем обновленный список
            with open(wifi_file, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            
            response = {'success': True, 'message': f'Сеть {ssid} удалена'}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception as e:
            response = {'success': False, 'message': str(e)}
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

if __name__ == "__main__":
    os.chdir('/workspace/Bjorn_rus/web')
    PORT = 12000
    with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()