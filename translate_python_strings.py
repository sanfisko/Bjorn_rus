#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

# Словарь переводов для сообщений в Python файлах
python_translations = {
    # Основные сообщения
    "Waiting for startup delay": "Ожидание задержки запуска",
    "seconds": "секунд",
    "Waiting for Wi-Fi connection to start Orchestrator": "Ожидание Wi-Fi соединения для запуска Оркестратора",
    "Starting Orchestrator thread": "Запуск потока Оркестратора",
    "Orchestrator thread started, automatic mode activated": "Поток Оркестратора запущен, автоматический режим активирован",
    "Orchestrator thread is already running": "Поток Оркестратора уже запущен",
    "Cannot start Orchestrator: Wi-Fi is not connected": "Невозможно запустить Оркестратор: Wi-Fi не подключен",
    "Stop button pressed. Manual mode activated & Stopping Orchestrator": "Нажата кнопка остановки. Активирован ручной режим и остановка Оркестратора",
    "Stopping Orchestrator thread": "Остановка потока Оркестратора",
    "Orchestrator thread stopped": "Поток Оркестратора остановлен",
    
    # Веб-сервер
    "Serving at port": "Сервер запущен на порту",
    "Port {} is in use, trying the next port": "Порт {} используется, пробуем следующий порт",
    "Error in web server": "Ошибка в веб-сервере",
    "Web server closed": "Веб-сервер закрыт",
    "Web server shutdown initiated": "Инициировано выключение веб-сервера",
    "Server shutting down": "Сервер выключается",
    "Web server thread started": "Поток веб-сервера запущен",
    "An exception occurred during web server start": "Произошло исключение при запуске веб-сервера",
    
    # Сканирование и сеть
    "Scanning network": "Сканирование сети",
    "Found host": "Найден хост",
    "Scanning ports": "Сканирование портов",
    "Open port found": "Найден открытый порт",
    "Service detected": "Обнаружен сервис",
    "Vulnerability found": "Найдена уязвимость",
    "Attack successful": "Атака успешна",
    "Attack failed": "Атака неудачна",
    "Connection established": "Соединение установлено",
    "Connection failed": "Соединение неудачно",
    "Authentication successful": "Аутентификация успешна",
    "Authentication failed": "Аутентификация неудачна",
    "Brute force attack": "Атака перебора",
    "Password cracked": "Пароль взломан",
    "File downloaded": "Файл скачан",
    "Data extracted": "Данные извлечены",
    
    # Статусы и состояния
    "Starting": "Запуск",
    "Running": "Работает",
    "Stopping": "Остановка",
    "Stopped": "Остановлен",
    "Connected": "Подключен",
    "Disconnected": "Отключен",
    "Active": "Активен",
    "Inactive": "Неактивен",
    "Idle": "Ожидание",
    "Busy": "Занят",
    "Ready": "Готов",
    "Error": "Ошибка",
    "Warning": "Предупреждение",
    "Success": "Успех",
    "Failed": "Неудача",
    
    # Файлы и данные
    "Loading configuration": "Загрузка конфигурации",
    "Configuration loaded": "Конфигурация загружена",
    "Saving data": "Сохранение данных",
    "Data saved": "Данные сохранены",
    "File not found": "Файл не найден",
    "Permission denied": "Доступ запрещён",
    "Invalid format": "Неверный формат",
    "Backup created": "Резервная копия создана",
    "Restore completed": "Восстановление завершено",
    
    # Дисплей
    "Display initialized": "Дисплей инициализирован",
    "Display updated": "Дисплей обновлён",
    "Display error": "Ошибка дисплея",
    "Screen refresh": "Обновление экрана",
    
    # Общие термины
    "host": "хост",
    "port": "порт",
    "service": "сервис",
    "protocol": "протокол",
    "timeout": "таймаут",
    "retry": "повтор",
    "attempt": "попытка",
    "target": "цель",
    "source": "источник",
    "destination": "назначение",
    "username": "имя пользователя",
    "password": "пароль",
    "credential": "учётные данные",
    "session": "сессия",
    "thread": "поток",
    "process": "процесс",
    "module": "модуль",
    "action": "действие",
    "result": "результат",
    "output": "вывод",
    "input": "ввод",
    "log": "лог",
    "debug": "отладка",
    "info": "информация",
    "warning": "предупреждение",
    "error": "ошибка",
    "critical": "критическая ошибка",
}

def translate_python_strings(content):
    """Переводит строки в Python коде"""
    
    # Переводим строки в logger вызовах
    def translate_logger_string(match):
        quote_char = match.group(1)  # " или '
        string_content = match.group(2)
        
        # Переводим содержимое строки
        translated = translate_text(string_content)
        
        return f'logger.{match.group(0).split(".")[1].split("(")[0]}({quote_char}{translated}{quote_char}'
    
    # Паттерн для logger вызовов
    logger_pattern = r'logger\.\w+\((["\'])(.*?)\1'
    content = re.sub(logger_pattern, translate_logger_string, content)
    
    # Переводим обычные строки в print вызовах
    def translate_print_string(match):
        quote_char = match.group(1)
        string_content = match.group(2)
        translated = translate_text(string_content)
        return f'print({quote_char}{translated}{quote_char}'
    
    print_pattern = r'print\((["\'])(.*?)\1'
    content = re.sub(print_pattern, translate_print_string, content)
    
    return content

def translate_text(text):
    """Переводит текст используя словарь переводов"""
    if not text.strip():
        return text
    
    # Прямой перевод
    if text in python_translations:
        return python_translations[text]
    
    # Поиск частичных совпадений и замена
    translated = text
    for english, russian in python_translations.items():
        if english.lower() in translated.lower():
            translated = translated.replace(english, russian)
    
    return translated

def translate_python_files():
    """Переводит пользовательские строки в основных Python файлах"""
    
    # Основные файлы для перевода
    main_files = [
        'Bjorn.py',
        'webapp.py', 
        'orchestrator.py',
        'display.py',
        'shared.py'
    ]
    
    for filename in main_files:
        filepath = f'/workspace/Bjorn_rus/{filename}'
        if os.path.exists(filepath):
            print(f"Переводим {filename}...")
            
            # Читаем файл
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Переводим строки
            translated_content = translate_python_strings(content)
            
            # Записываем обратно только если есть изменения
            if translated_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(translated_content)
                print(f"✓ {filename} переведён")
            else:
                print(f"- {filename} не требует перевода")
        else:
            print(f"⚠ Файл {filename} не найден")

if __name__ == '__main__':
    translate_python_files()
    print("Перевод Python файлов завершён!")