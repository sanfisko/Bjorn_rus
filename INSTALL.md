## 🔧 Установка и конфигурация

<p align="center">
  <img src="https://github.com/user-attachments/assets/c5eb4cc1-0c3d-497d-9422-1614651a84ab" alt="thumbnail_IMG_0546" width="98">
</p>

## 📚 Содержание

- [Предварительные требования](#-предварительные-требования)
- [Быстрая установка](#-быстрая-установка)
- [Ручная установка](#-ручная-установка)
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
# Скачайте и запустите установщик
wget https://raw.githubusercontent.com/sanfisko/Bjorn_rus/refs/heads/main/install_bjorn.sh
sudo chmod +x install_bjorn.sh && sudo ./install_bjorn.sh
# Выберите вариант 1 для автоматической установки. Это может занять некоторое время, так как будет установлено много пакетов и модулей. В конце необходимо перезагрузиться.
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

Для полного удаления Bjorn:

```bash
sudo ./uninstall_bjorn.sh
```

## 📜 Лицензия

Этот проект лицензирован под лицензией MIT - см. файл [LICENSE](LICENSE) для подробностей.