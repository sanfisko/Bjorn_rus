#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re

# Словарь переводов для часто встречающихся фраз
translations = {
    # Основные фразы
    "I'm bored": "Мне скучно",
    "Nothing to do": "Нечего делать", 
    "Tired": "Устал",
    "Life is tough": "Жизнь тяжела",
    "This is boring": "Это скучно",
    "So, what's up?": "Ну, как дела?",
    "I'm waiting": "Я жду",
    "I'm just hanging out": "Я просто тусуюсь",
    "I'm just chilling": "Я просто расслабляюсь",
    "Netflix and chill?": "Netflix и расслабон?",
    "Hi!": "Привет!",
    "Hello!": "Привет!",
    "Ready when you are!": "Готов, когда ты готов!",
    "Just hanging out": "Просто тусуюсь",
    "Let's get to work!": "Давайте приступим к работе!",
    "Standing by": "В ожидании",
    "Try harder!": "Старайся сильнее!",
    "Hack the planet!": "Взломай планету!",
    "Hello, Neo. Time to wake up.": "Привет, Нео. Время просыпаться.",
    
    # Хакерские фразы
    "hack": "взломать",
    "hacking": "хакинг",
    "hacker": "хакер",
    "cyber": "кибер",
    "system": "система",
    "planet": "планета",
    "matrix": "матрица",
    "waiting": "жду",
    "ready": "готов",
    "bored": "скучно",
    "idle": "бездействую",
    "IDLE": "БЕЗДЕЙСТВУЮ",
    "mission": "миссия",
    "task": "задача",
    "adventure": "приключение",
    "challenge": "вызов",
    "target": "цель",
    "vulnerability": "уязвимость",
    "exploit": "эксплойт",
    "code": "код",
    "data": "данные",
    "network": "сеть",
    "server": "сервер",
    "firewall": "файрвол",
    "password": "пароль",
    "security": "безопасность",
    
    # Фильмы и персонажи
    "Neo": "Нео",
    "Matrix": "Матрица",
    "Mr. Robot": "Мистер Робот",
    "Zero Cool": "Зеро Кул",
    "Lisbeth Salander": "Лисбет Саландер",
    "Kevin Mitnick": "Кевин Митник",
    "Hackers": "Хакеры",
    "WarGames": "Военные игры",
    "Sneakers": "Взломщики",
    "Tron": "Трон",
    "Swordfish": "Рыба-меч",
    "Blackhat": "Чёрная шляпа",
    "Fight Club": "Бойцовский клуб",
    "Live Free or Die Hard": "Крепкий орешек 4.0",
    "Ghost in the Shell": "Призрак в доспехах",
    "The Girl with the Dragon Tattoo": "Девушка с татуировкой дракона",
    
    # Общие фразы
    "What's next": "Что дальше",
    "Any tasks for me?": "Есть задачи для меня?",
    "Give me a task": "Дай мне задачу",
    "Time to": "Время",
    "Let's": "Давайте",
    "I feel like": "Чувствую себя как",
    "Feeling like": "Чувствую себя как",
    "Inspired by": "Вдохновлён",
    "Channeling": "Направляю",
    "Wondering": "Интересно",
    "Thinking": "Думаю",
    "Remembering": "Вспоминаю",
    "Looking for": "Ищу",
    "Scanning for": "Сканирую в поисках",
    "Waiting for": "Жду",
    "Ready for": "Готов к",
    "In the mood for": "В настроении для",
    "Can we": "Можем ли мы",
    "Shall we": "Начнём ли мы",
    "Do you think": "Думаешь",
    "Did you know": "Знал ли ты",
    "Ever watched": "Смотрел когда-нибудь",
    "Remember": "Помнишь",
    "Like in": "Как в",
    "Just like": "Прямо как",
    "style": "стиле",
    "level": "уровня",
    "today": "сегодня",
    "next": "следующий",
    "big": "большой",
    "epic": "эпический",
    "ultimate": "абсолютный",
    "inner": "внутренний",
    "digital": "цифровой",
    "virtual": "виртуальный",
    "electronic": "электронный",
    "online": "онлайн",
    "offline": "оффлайн",
}

def translate_phrase(phrase):
    """Переводит фразу на русский язык"""
    # Сначала проверяем точные совпадения
    if phrase in translations:
        return translations[phrase]
    
    # Затем переводим по словам
    result = phrase
    for eng, rus in translations.items():
        # Используем регулярные выражения для замены слов с учётом границ слов
        pattern = r'\b' + re.escape(eng) + r'\b'
        result = re.sub(pattern, rus, result, flags=re.IGNORECASE)
    
    return result

def translate_comments_file(input_file, output_file):
    """Переводит файл комментариев"""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if 'IDLE' in data:
        translated_comments = []
        for comment in data['IDLE']:
            translated = translate_phrase(comment)
            translated_comments.append(translated)
        
        data['IDLE'] = translated_comments
    
    with open(output_file, 'w', encoding='utf-8', ensure_ascii=False) as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # Переводим основной файл
    translate_comments_file(
        '/workspace/Bjorn_rus/resources/comments/comments.json',
        '/workspace/Bjorn_rus/resources/comments/comments.json'
    )
    
    # Переводим кэш файл
    translate_comments_file(
        '/workspace/Bjorn_rus/resources/comments/comments.json.cache',
        '/workspace/Bjorn_rus/resources/comments/comments.json.cache'
    )
    
    print("Перевод файлов комментариев завершён!")