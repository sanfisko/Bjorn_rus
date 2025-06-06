## 🔧 Установка и конфигурация

<p align="center">
  <img src="https://github.com/user-attachments/assets/c5eb4cc1-0c3d-497d-9422-1614651a84ab" alt="thumbnail_IMG_0546" width="98">
</p>

## 📚 Содержание

- [Предварительные требования](#-предварительные-требования)
- [Быстрая установка](#-быстрая-установка)
- [Ручная установка](#-ручная-установка)
- [Устранение неполадок](#️-устранение-неполадок)
- [Обновление](#-обновление)
- [Удаление](#️-удаление)
- [Лицензия](#-лицензия)

Используйте Raspberry Pi Imager для установки вашей ОС
https://www.raspberrypi.com/software/

### 📌 Предварительные требования для RPI zero W (32 бита)
![image](https://github.com/user-attachments/assets/3980ec5f-a8fc-4848-ab25-4356e0529639)

- Установленная Raspberry Pi OS. 
    - Стабильная:
      - Система: 32-битная
      - Версия ядра: 6.6
      - Версия Debian: 12 (bookworm) '2024-10-22-raspios-bookworm-armhf-lite'
- Имя пользователя и имя хоста установлены как `bjorn`.
- 2.13-дюймовый e-Paper HAT подключен к GPIO пинам.

### 📌 Предварительные требования для RPI zero W2 (64 бита)

![image](https://github.com/user-attachments/assets/e8d276be-4cb2-474d-a74d-b5b6704d22f5)

Я не разрабатывал Bjorn для raspberry pi zero w2 64 бита, но несколько отзывов подтвердили, что установка работает идеально.

- Установленная Raspberry Pi OS. 
    - Стабильная:
      - Система: 64-битная
      - Версия ядра: 6.6
      - Версия Debian: 12 (bookworm) '2024-10-22-raspios-bookworm-arm64-lite'
- Имя пользователя и имя хоста установлены как `bjorn`.
- 2.13-дюймовый e-Paper HAT подключен к GPIO пинам.



На данный момент протестированы и реализованы экраны v2 и v4.
Я просто надеюсь, что V1 и V3 будут работать так же.
 
### ⚡ Быстрая установка

Самый быстрый способ установить Bjorn - использовать скрипт автоматической установки:

```bash
# Интерактивная установка
curl https://raw.githubusercontent.com/sanfisko/Bjorn_rus/refs/heads/main/install_bjorn.sh | sudo bash

# Неинтерактивная установка с автоматическим выбором дисплея
curl https://raw.githubusercontent.com/sanfisko/Bjorn_rus/refs/heads/main/install_bjorn.sh | sudo bash -s -- --epd-version 4

# Доступные параметры установки:
# --epd-version 1-5    : Версия дисплея
#   1 = epd2in13
#   2 = epd2in13_V2  
#   3 = epd2in13_V3
#   4 = epd2in13_V4 (по умолчанию)
#   5 = epd2in7
# --auto-reboot        : Принудительная автоматическая перезагрузка
# --no-reboot          : Пропустить перезагрузку (перезагрузить вручную)
# --help               : Показать справку

# Примеры использования:
curl https://raw.githubusercontent.com/sanfisko/Bjorn_rus/refs/heads/main/install_bjorn.sh | sudo bash -s -- --epd-version 4 --auto-reboot
curl https://raw.githubusercontent.com/sanfisko/Bjorn_rus/refs/heads/main/install_bjorn.sh | sudo bash -s -- --no-reboot

# Установка может занять некоторое время, так как будет установлено много пакетов и модулей. В конце необходимо перезагрузиться.
```

### 🛠️ Ручная установка

Если вы предпочитаете ручную установку или хотите понять процесс установки:

#### Шаг 1: Обновление системы

```bash
sudo apt update && sudo apt upgrade -y
```

#### Шаг 2: Установка зависимостей

```bash
sudo apt install -y python3 python3-pip git
```

#### Шаг 3: Клонирование репозитория

```bash
git clone https://github.com/sanfisko/Bjorn_rus.git
cd Bjorn_rus
```

#### Шаг 4: Установка Python зависимостей

```bash
pip3 install -r requirements.txt
```

#### Шаг 5: Настройка разрешений

```bash
sudo chmod +x install_bjorn.sh
sudo chmod +x uninstall_bjorn.sh
```

#### Шаг 6: Запуск установки

```bash
sudo ./install_bjorn.sh
```

**Альтернативно**, вы можете использовать одну команду для скачивания и запуска:

```bash
# Интерактивная установка
curl https://raw.githubusercontent.com/sanfisko/Bjorn_rus/refs/heads/main/install_bjorn.sh | sudo bash

# Неинтерактивная установка с автоматическим выбором дисплея
curl https://raw.githubusercontent.com/sanfisko/Bjorn_rus/refs/heads/main/install_bjorn.sh | sudo bash -s -- --epd-version 4
```

### 🔧 Конфигурация

После установки вы можете настроить Bjorn через:

1. **Веб-интерфейс**: Откройте браузер и перейдите по IP-адресу вашего Raspberry Pi
2. **Файлы конфигурации**: Отредактируйте файлы в папке `config/`
3. **E-Paper дисплей**: Используйте физические кнопки (если подключены)

### 🚀 Первый запуск

После установки и перезагрузки:

1. Bjorn автоматически запустится как сервис
2. Веб-интерфейс будет доступен по адресу `http://[IP_АДРЕС_RASPBERRY_PI]:8000`
3. E-Paper дисплей покажет текущий статус

### 🔍 Проверка установки

Чтобы убедиться, что Bjorn работает правильно:

```bash
# Проверка статуса сервиса
sudo systemctl status bjorn

# Проверка логов
sudo journalctl -u bjorn -f

# Проверка процессов
ps aux | grep bjorn
```

### 🛠️ Устранение неполадок

Если у вас возникли проблемы с установкой:

1. **Проверьте подключение к интернету**
2. **Убедитесь, что у вас достаточно места на диске**
3. **Проверьте, что все зависимости установлены**
4. **Обратитесь к [Руководству по устранению неполадок](TROUBLESHOOTING.md)**

### 🔄 Обновление

Для обновления Bjorn до последней версии:

```bash
cd /path/to/Bjorn
git pull origin main
pip3 install -r requirements.txt --upgrade
sudo systemctl restart bjorn
```

### 🗑️ Удаление

Для полного удаления Bjorn используйте скрипт автоматического удаления:

```bash
# Автоматическое удаление (рекомендуется)
# Все запросы автоматически подтверждаются через 5 секунд
sudo chmod +x ./Bjorn_rus/uninstall_bjorn.sh && sudo ./Bjorn_rus/uninstall_bjorn.sh

# Интерактивный режим (ручное подтверждение каждого шага)
sudo chmod +x ./Bjorn_rus/uninstall_bjorn.sh && sudo ./Bjorn_rus/uninstall_bjorn.sh --interactive

# Изменить таймаут автоподтверждения (например, 10 секунд)
sudo chmod +x ./Bjorn_rus/uninstall_bjorn.sh && sudo ./Bjorn_rus/uninstall_bjorn.sh --timeout 10

# Показать справку по параметрам
chmod +x ./Bjorn_rus/uninstall_bjorn.sh && ./Bjorn_rus/uninstall_bjorn.sh --help
```

**Возможности скрипта удаления:**

- 🚀 **Автоматический режим**: Все запросы подтверждаются через 5 секунд по умолчанию
- ⏱️ **Визуальный обратный отсчет**: Показывает оставшееся время до автоподтверждения  
- ❌ **Возможность отмены**: Нажмите 'n' в любой момент для отмены действия
- 🎛️ **Гибкие настройки**: Настройка таймаута и интерактивного режима
- 🎨 **Цветовая индикация**: Понятный интерфейс с цветовыми подсказками
- 🛡️ **Безопасное удаление**: Сохраняет пользователя bjorn и системные пакеты

**Что удаляется:**
- Все файлы и каталоги Bjorn
- Сервисы systemd (bjorn.service, bjorn-web.service)
- Конфигурационные файлы
- Логи и временные файлы
- Python зависимости (опционально)

**Что сохраняется:**
- Пользователь bjorn
- Системные пакеты (Python, Git, etc.)
- Настройки SSH и сети

## 📜 Лицензия

Этот проект лицензирован под лицензией MIT - см. файл [LICENSE](LICENSE) для подробностей.