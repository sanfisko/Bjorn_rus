# 🐛 Известные проблемы и устранение неполадок

<p align="center">
  <img src="https://github.com/user-attachments/assets/c5eb4cc1-0c3d-497d-9422-1614651a84ab" alt="thumbnail_IMG_0546" width="98">
</p>

## 📚 Содержание

- [Текущие проблемы разработки](#-текущие-проблемы-разработки)
- [Шаги по устранению неполадок](#-шаги-по-устранению-неполадок)
- [Часто задаваемые вопросы](#-часто-задаваемые-вопросы)
- [Лицензия](#-лицензия)

## 🪲 Текущие проблемы разработки

### Проблема длительного времени выполнения

- **Проблема**: `OSError: [Errno 24] Too many open files` (Слишком много открытых файлов)
- **Статус**: Частично решено с конфигурацией системных лимитов.
- **Обходной путь**: Реализовано увеличение лимитов файловых дескрипторов.
- **Мониторинг**: Проверьте открытые файлы с помощью `lsof -p $(pgrep -f Bjorn.py) | wc -l`
- На данный момент логи периодически показывают эту информацию как (FD : XXX)

### Проблемы с e-Paper дисплеем

- **Проблема**: Дисплей не обновляется или показывает артефакты
- **Возможные причины**: 
  - Неправильное подключение GPIO
  - Несовместимая версия дисплея
  - Проблемы с питанием
- **Решение**: Проверьте подключение и версию дисплея

## 🛠️ Шаги по устранению неполадок

### Проблемы с сервисом

```bash
# Просмотр логов сервиса bjorn
journalctl -fu bjorn.service

# Проверка статуса сервиса
sudo systemctl status bjorn.service

# Перезапуск сервиса
sudo systemctl restart bjorn.service

# Остановка сервиса
sudo systemctl stop bjorn.service

# Запуск сервиса
sudo systemctl start bjorn.service
```

### Проблемы с сетью

```bash
# Проверка сетевых подключений
netstat -tulpn | grep :8000

# Проверка доступности веб-интерфейса
curl -I http://localhost:8000

# Проверка сетевых интерфейсов
ip addr show
```

### Проблемы с разрешениями

```bash
# Проверка владельца файлов
ls -la /path/to/bjorn/

# Исправление разрешений
sudo chown -R bjorn:bjorn /path/to/bjorn/
sudo chmod +x /path/to/bjorn/Bjorn.py
```

### Проблемы с зависимостями

```bash
# Проверка установленных пакетов Python
pip3 list

# Переустановка зависимостей
pip3 install -r requirements.txt --force-reinstall

# Проверка версии Python
python3 --version
```

### Проблемы с памятью

```bash
# Проверка использования памяти
free -h

# Проверка использования диска
df -h

# Проверка процессов, использующих память
top -p $(pgrep -f Bjorn.py)
```

## ❓ Часто задаваемые вопросы

### Q: Bjorn не запускается после установки
**A**: Проверьте следующее:
1. Все зависимости установлены: `pip3 list | grep -E "(flask|requests|nmap)"`
2. Правильные разрешения: `ls -la Bjorn.py`
3. Логи ошибок: `journalctl -u bjorn.service`

### Q: Веб-интерфейс недоступен
**A**: Убедитесь, что:
1. Сервис запущен: `sudo systemctl status bjorn.service`
2. Порт 8000 не заблокирован: `sudo netstat -tulpn | grep :8000`
3. Firewall не блокирует соединения: `sudo ufw status`

### Q: E-Paper дисплей не работает
**A**: Проверьте:
1. Правильность подключения GPIO пинов
2. Совместимость версии дисплея (v2, v4 поддерживаются)
3. Включён ли SPI: `sudo raspi-config` → Interface Options → SPI

### Q: Сканирование сети не работает
**A**: Убедитесь, что:
1. Nmap установлен: `nmap --version`
2. Bjorn имеет права на сканирование: запуск от root или с sudo
3. Сетевой интерфейс активен: `ip link show`

### Q: Высокое использование CPU/памяти
**A**: Это может быть нормально во время активного сканирования. Если проблема постоянная:
1. Проверьте количество открытых файлов: `lsof -p $(pgrep -f Bjorn.py) | wc -l`
2. Перезапустите сервис: `sudo systemctl restart bjorn.service`
3. Проверьте логи на ошибки: `journalctl -u bjorn.service`

## 🔧 Расширенная диагностика

### Проверка системных ресурсов

```bash
# Проверка лимитов файловых дескрипторов
ulimit -n

# Проверка системных лимитов
cat /proc/sys/fs/file-max

# Проверка использования файловых дескрипторов
cat /proc/sys/fs/file-nr
```

### Отладка Python

```bash
# Запуск Bjorn в режиме отладки
python3 -u Bjorn.py --debug

# Проверка импорта модулей
python3 -c "import flask, requests, nmap; print('Все модули импортированы успешно')"
```

### Проверка GPIO (для e-Paper)

```bash
# Проверка состояния GPIO
gpio readall

# Проверка SPI
ls /dev/spi*

# Проверка I2C
ls /dev/i2c*
```

## 🆘 Получение помощи

Если проблема не решается:

1. **Соберите информацию**:
   ```bash
   # Создайте отчёт о системе
   echo "=== Информация о системе ===" > debug_report.txt
   uname -a >> debug_report.txt
   cat /etc/os-release >> debug_report.txt
   python3 --version >> debug_report.txt
   pip3 list >> debug_report.txt
   
   echo "=== Логи Bjorn ===" >> debug_report.txt
   journalctl -u bjorn.service --no-pager >> debug_report.txt
   
   echo "=== Статус сервиса ===" >> debug_report.txt
   systemctl status bjorn.service >> debug_report.txt
   ```

2. **Создайте issue на GitHub** с:
   - Описанием проблемы
   - Шагами для воспроизведения
   - Содержимым debug_report.txt
   - Скриншотами (если применимо)

3. **Обратитесь в Discord** для быстрой помощи сообщества

## 🔄 Сброс к заводским настройкам

Если ничего не помогает:

```bash
# Остановите сервис
sudo systemctl stop bjorn.service

# Сделайте резервную копию данных
cp -r /path/to/bjorn/data /path/to/backup/

# Переустановите Bjorn
sudo ./uninstall_bjorn.sh
sudo ./install_bjorn.sh

# Восстановите данные (если нужно)
cp -r /path/to/backup/data /path/to/bjorn/
```

## 📊 Мониторинг производительности

```bash
# Создайте скрипт мониторинга
cat << 'EOF' > monitor_bjorn.sh
#!/bin/bash
while true; do
    echo "$(date): CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}'), RAM: $(free | grep Mem | awk '{printf("%.1f%%", $3/$2 * 100.0)}'), FD: $(lsof -p $(pgrep -f Bjorn.py) 2>/dev/null | wc -l)"
    sleep 60
done
EOF

chmod +x monitor_bjorn.sh
./monitor_bjorn.sh
```

---

## 📜 Лицензия

Этот документ является частью проекта Bjorn и распространяется под той же лицензией MIT.