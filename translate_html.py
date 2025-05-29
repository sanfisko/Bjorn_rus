#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

# Словарь переводов для HTML файлов
translations = {
    # Основные термины
    'Playground': 'Площадка',
    'Config': 'Конфигурация',
    'Configuration': 'Конфигурация',
    'Network': 'Сеть',
    'NetKB': 'База знаний сети',
    'Credentials': 'Учётные данные',
    'Loot': 'Добыча',
    'Actions': 'Действия',
    'Status': 'Статус',
    'Settings': 'Настройки',
    'Home': 'Главная',
    'Dashboard': 'Панель управления',
    
    # Заголовки и описания
    'Bjorn Cyberviking': 'Bjorn Киберваряг',
    'Cyber Viking': 'Киберваряг',
    'Security Tool': 'Инструмент безопасности',
    'Penetration Testing': 'Тестирование на проникновение',
    'Network Scanner': 'Сканер сети',
    'Vulnerability Assessment': 'Оценка уязвимостей',
    
    # Кнопки и действия
    'Start': 'Запуск',
    'Stop': 'Остановка',
    'Restart': 'Перезапуск',
    'Save': 'Сохранить',
    'Load': 'Загрузить',
    'Reset': 'Сброс',
    'Clear': 'Очистить',
    'Refresh': 'Обновить',
    'Download': 'Скачать',
    'Upload': 'Загрузить',
    'Delete': 'Удалить',
    'Edit': 'Редактировать',
    'View': 'Просмотр',
    'Export': 'Экспорт',
    'Import': 'Импорт',
    
    # Статусы
    'Running': 'Работает',
    'Stopped': 'Остановлен',
    'Idle': 'Ожидание',
    'Active': 'Активен',
    'Inactive': 'Неактивен',
    'Connected': 'Подключен',
    'Disconnected': 'Отключен',
    'Online': 'В сети',
    'Offline': 'Не в сети',
    'Success': 'Успех',
    'Failed': 'Неудача',
    'Error': 'Ошибка',
    'Warning': 'Предупреждение',
    'Info': 'Информация',
    
    # Сетевые термины
    'Host': 'Хост',
    'Hosts': 'Хосты',
    'Port': 'Порт',
    'Ports': 'Порты',
    'Service': 'Сервис',
    'Services': 'Сервисы',
    'Protocol': 'Протокол',
    'IP Address': 'IP-адрес',
    'MAC Address': 'MAC-адрес',
    'Subnet': 'Подсеть',
    'Gateway': 'Шлюз',
    'DNS': 'DNS',
    'DHCP': 'DHCP',
    
    # Безопасность
    'Vulnerability': 'Уязвимость',
    'Vulnerabilities': 'Уязвимости',
    'Exploit': 'Эксплойт',
    'Attack': 'Атака',
    'Scan': 'Сканирование',
    'Brute Force': 'Перебор',
    'Password': 'Пароль',
    'Username': 'Имя пользователя',
    'Login': 'Вход',
    'Authentication': 'Аутентификация',
    'Authorization': 'Авторизация',
    
    # Файлы и данные
    'File': 'Файл',
    'Files': 'Файлы',
    'Folder': 'Папка',
    'Directory': 'Директория',
    'Data': 'Данные',
    'Log': 'Лог',
    'Logs': 'Логи',
    'Report': 'Отчёт',
    'Reports': 'Отчёты',
    'Output': 'Вывод',
    'Input': 'Ввод',
    'Result': 'Результат',
    'Results': 'Результаты',
    
    # Интерфейс
    'Menu': 'Меню',
    'Toolbar': 'Панель инструментов',
    'Button': 'Кнопка',
    'Tab': 'Вкладка',
    'Window': 'Окно',
    'Dialog': 'Диалог',
    'Form': 'Форма',
    'Field': 'Поле',
    'Table': 'Таблица',
    'List': 'Список',
    'Tree': 'Дерево',
    'Grid': 'Сетка',
    
    # Время
    'Time': 'Время',
    'Date': 'Дата',
    'Duration': 'Длительность',
    'Timeout': 'Таймаут',
    'Interval': 'Интервал',
    'Schedule': 'Расписание',
    
    # Размеры и количество
    'Size': 'Размер',
    'Count': 'Количество',
    'Total': 'Всего',
    'Available': 'Доступно',
    'Used': 'Использовано',
    'Free': 'Свободно',
    
    # Атрибуты HTML
    'title': 'title',
    'alt': 'alt',
    'placeholder': 'placeholder',
    'value': 'value',
}

def translate_html_content(content):
    """Переводит содержимое HTML файла"""
    
    # Переводим title теги
    content = re.sub(r'<title>(.*?)</title>', 
                    lambda m: f'<title>{translate_text(m.group(1))}</title>', 
                    content, flags=re.IGNORECASE)
    
    # Переводим атрибуты title
    content = re.sub(r'title="([^"]*)"', 
                    lambda m: f'title="{translate_text(m.group(1))}"', 
                    content)
    
    # Переводим атрибуты alt
    content = re.sub(r'alt="([^"]*)"', 
                    lambda m: f'alt="{translate_text(m.group(1))}"', 
                    content)
    
    # Переводим атрибуты placeholder
    content = re.sub(r'placeholder="([^"]*)"', 
                    lambda m: f'placeholder="{translate_text(m.group(1))}"', 
                    content)
    
    # Переводим текст между тегами (простые случаи)
    content = re.sub(r'>([^<>]+)<', 
                    lambda m: f'>{translate_text(m.group(1))}<', 
                    content)
    
    # Меняем lang="en" на lang="ru"
    content = re.sub(r'lang="en"', 'lang="ru"', content)
    
    return content

def translate_text(text):
    """Переводит текст используя словарь переводов"""
    text = text.strip()
    if not text:
        return text
    
    # Прямой перевод
    if text in translations:
        return translations[text]
    
    # Поиск частичных совпадений
    for english, russian in translations.items():
        if english.lower() in text.lower():
            text = text.replace(english, russian)
    
    return text

def translate_html_files():
    """Переводит все HTML файлы в папке web/"""
    web_dir = '/workspace/Bjorn_rus/web'
    
    html_files = [
        'bjorn.html',
        'config.html', 
        'credentials.html',
        'loot.html',
        'netkb.html',
        'network.html'
    ]
    
    for filename in html_files:
        filepath = os.path.join(web_dir, filename)
        if os.path.exists(filepath):
            print(f"Переводим {filename}...")
            
            # Читаем файл
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Переводим содержимое
            translated_content = translate_html_content(content)
            
            # Записываем обратно
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(translated_content)
            
            print(f"✓ {filename} переведён")
        else:
            print(f"⚠ Файл {filename} не найден")

if __name__ == '__main__':
    translate_html_files()
    print("Перевод HTML файлов завершён!")