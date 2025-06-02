
function generateConfigForm(config) {
    const formElement = document.querySelector(".config-form");
    formElement.innerHTML = ''; // Clear the form
    
    const leftColumn = document.createElement('div');
    leftColumn.classList.add('left-column');
    
    const rightColumn = document.createElement('div');
    rightColumn.classList.add('right-column');
    
    // Описания для всплывающих подсказок
    const tooltips = {
        "manual_mode": "Ручной режим - отключает автоматическое выполнение действий",
        "websrv": "Веб-сервер - включает/отключает веб-интерфейс",
        "web_increment": "Инкремент веб-страницы - автоматическое обновление данных",
        "debug_mode": "Режим отладки - включает подробное логирование",
        "scan_vuln_running": "Сканирование уязвимостей - запускает поиск уязвимостей",
        "retry_success_actions": "Повтор успешных действий - повторяет успешно выполненные атаки",
        "retry_failed_actions": "Повтор неудачных действий - повторяет неудачные попытки атак",
        "blacklistcheck": "Проверка черного списка - исключает заблокированные IP/MAC",
        "displaying_csv": "Отображение CSV - показывает данные в табличном формате",
        "log_debug": "Логи отладки - записывает отладочную информацию",
        "log_info": "Информационные логи - записывает общую информацию",
        "log_warning": "Логи предупреждений - записывает предупреждения",
        "log_error": "Логи ошибок - записывает ошибки",
        "log_critical": "Критические логи - записывает критические ошибки",
        "startup_delay": "Задержка запуска (сек) - время ожидания перед началом работы",
        "web_delay": "Задержка веб-интерфейса (сек) - интервал обновления веб-страницы",
        "screen_delay": "Задержка экрана (сек) - интервал обновления дисплея",
        "comment_delaymin": "Мин. задержка комментариев (мин) - минимальное время показа комментариев",
        "comment_delaymax": "Макс. задержка комментариев (мин) - максимальное время показа комментариев",
        "livestatus_delay": "Задержка статуса (сек) - интервал обновления статуса",
        "image_display_delaymin": "Мин. задержка изображений (сек) - минимальное время показа изображений",
        "image_display_delaymax": "Макс. задержка изображений (сек) - максимальное время показа изображений",
        "scan_interval": "Интервал сканирования (сек) - частота сканирования сети",
        "scan_vuln_interval": "Интервал сканирования уязвимостей (сек) - частота поиска уязвимостей",
        "failed_retry_delay": "Задержка повтора неудач (сек) - время ожидания перед повтором неудачной атаки",
        "success_retry_delay": "Задержка повтора успехов (сек) - время ожидания перед повтором успешной атаки",
        "ref_width": "Ширина экрана (пикс) - ширина e-paper дисплея",
        "ref_height": "Высота экрана (пикс) - высота e-paper дисплея",
        "epd_type": "Тип дисплея - модель e-paper дисплея",
        "portlist": "Список портов - порты для сканирования (через запятую)",
        "mac_scan_blacklist": "Черный список MAC - исключенные MAC-адреса (через запятую)",
        "ip_scan_blacklist": "Черный список IP - исключенные IP-адреса (через запятую)",
        "steal_file_names": "Имена файлов для кражи - конкретные имена файлов (через запятую)",
        "steal_file_extensions": "Расширения файлов для кражи - типы файлов для поиска (через запятую)",
        "nmap_scan_aggressivity": "Агрессивность nmap - параметр скорости сканирования (-T0 до -T5)",
        "portstart": "Начальный порт - первый порт диапазона для сканирования",
        "portend": "Конечный порт - последний порт диапазона для сканирования",
        "timewait_smb": "Ожидание SMB (сек) - задержка между SMB-атаками",
        "timewait_ssh": "Ожидание SSH (сек) - задержка между SSH-атаками",
        "timewait_telnet": "Ожидание Telnet (сек) - задержка между Telnet-атаками",
        "timewait_ftp": "Ожидание FTP (сек) - задержка между FTP-атаками",
        "timewait_sql": "Ожидание SQL (сек) - задержка между SQL-атаками",
        "timewait_rdp": "Ожидание RDP (сек) - задержка между RDP-атаками",
        "wifi_auto_connect": "Автоподключение WiFi - автоматически подключается к известным сетям",
        "wifi_script_running": "Скрипт WiFi активен - включает/отключает WiFi-скрипт"
    };
    
    for (const [key, value] of Object.entries(config)) {
        if (key.startsWith("__title_")) {
            rightColumn.innerHTML += `<div class="section-title"><b>${value}</b></div>`;
        } else if (typeof value === "boolean") {
            const checked = value ? "checked" : "";
            const tooltip = tooltips[key] || key;
            leftColumn.innerHTML += `
    
                <div class="label-switch" title="${tooltip}">
                    <label class="switch" title="${tooltip}">
                        <input type="checkbox" id="${key}" name="${key}" ${checked} title="${tooltip}">
                        <span class="slider round" title="${tooltip}"></span>
                    </label>
                    <label for="${key}" title="${tooltip}">${key}</label>
                </div>
            `;
        } else if (Array.isArray(value)) {
            const listValue = value.join(',');
            const tooltip = tooltips[key] || key;
            rightColumn.innerHTML += `
                <div class="section-item">
                    <label for="${key}" title="${tooltip}">${key}:</label>
                    <input type="text" id="${key}" name="${key}" value="${listValue}" title="${tooltip}">
                </div>
            `;
        } else if (!isNaN(value) && !key.toLowerCase().includes("ip") && !key.toLowerCase().includes("mac")) {
            const tooltip = tooltips[key] || key;
            rightColumn.innerHTML += `
                <div class="section-item">
                    <label for="${key}" title="${tooltip}">${key}:</label>
                    <input type="number" id="${key}" name="${key}" value="${value}" title="${tooltip}">
                </div>
            `;
        } else {
            const tooltip = tooltips[key] || key;
            rightColumn.innerHTML += `
                <div class="section-item">
                    <label for="${key}" title="${tooltip}">${key}:</label>
                    <input type="text" id="${key}" name="${key}" value="${value}" title="${tooltip}">
                </div>
            `;
        }
    }
    
    formElement.appendChild(leftColumn);
    formElement.appendChild(rightColumn);
    
    // Add a spacer div at the end for better scrolling experience
    formElement.innerHTML += '<div style="height: 50px;"></div>';
    }
    
    
    function saveConfig() {
        console.log("Saving configuration...");
        const formElement = document.querySelector(".config-form");
    
        if (!formElement) {
            console.error("Form element not found.");
            return;
        }
    
        const formData = new FormData(formElement);
        const formDataObj = {};
        // Each of these fields contains an array of data.  Lets track these so we can ensure the format remains an array for the underlying structure.
        const arrayFields = [
            "portlist",
            "mac_scan_blacklist",
            "ip_scan_blacklist",
            "steal_file_names",
            "steal_file_extensions",
        ];

        formData.forEach((value, key) => {
            // Check if the input from the user contains a `,` character or is a known array field
            if (value.includes(',') || arrayFields.includes(key)) {
                formDataObj[key] = value.split(',').map(item => {
                    const trimmedItem = item.trim();
                    return isNaN(trimmedItem) || trimmedItem == "" ? trimmedItem : parseFloat(trimmedItem);
                });
            } else {
                formDataObj[key] = value === 'on' ? true : (isNaN(value) ? value : parseFloat(value));
            }
        });
    
        formElement.querySelectorAll('input[type="checkbox"]').forEach((checkbox) => {
            if (!formData.has(checkbox.name)) {
                formDataObj[checkbox.name] = false;
            }
        });
    
        console.log("Form data:", formDataObj);
    
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/save_config", true);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4) {
                console.log("Response status: " + xhr.status);
                if (xhr.status == 200) {
                    loadConfig();
                } else {
                    console.error("Failed to save configuration");
                    alert("Failed to save configuration");
                }
            }
        };
        xhr.send(JSON.stringify(formDataObj));
    }
    
    function restoreDefault() {
        fetch('/restore_default_config').then(response => response.json()).then(data => {
            generateConfigForm(data);
        });
    }
    
    function loadConfig() {
        fetch('/load_config').then(response => response.json()).then(data => {
            generateConfigForm(data);
            // Update WiFi script status after form is generated
            setTimeout(updateWifiScriptStatus, 100);
        });
    }
    
    function closeWifiPanel() {
        let wifiPanel = document.getElementById('wifi-panel');
        wifiPanel.style.display = 'none';
    }
    
    
    let wifiIntervalId;
    
    function scanWifi(update = false) {
        fetch('/scan_wifi')
            .then(response => response.json())
            .then(data => {
                console.log("Current SSID:", data.current_ssid); // Debugging
                let wifiPanel = document.getElementById('wifi-panel');
                let wifiList = document.getElementById('wifi-list');
                wifiList.innerHTML = '';
                data.networks.forEach(network => {
                    let li = document.createElement('li');
                    li.innerText = network;
                    li.setAttribute('data-ssid', network);
                    li.onclick = () => connectWifi(network);
                    if (network === data.current_ssid) {
                        li.classList.add('current-wifi'); // Apply the class if it's the current SSID
                        li.innerText += " ✅"; // Add the checkmark icon
                    }
                    wifiList.appendChild(li);
                });
                if (data.networks.length > 0) {
                    wifiPanel.style.display = 'block';
                    if (update) {
                        clearInterval(wifiIntervalId);
                        wifiIntervalId = setInterval(() => scanWifi(true), 5000);
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
    
    
    
    function connectWifi(ssid) {
        let password = prompt("Enter the password for " + ssid);
        if (password) {
            fetch('/connect_wifi', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ ssid: ssid, password: password }),
            })
            .then(response => response.json())
            .then(data => alert(data.message))
            .catch(error => alert('Error: ' + error));
        }
    }
    
    
        
    
    function adjustFormPadding() {
        const toolbarHeight = document.querySelector('.toolbar').offsetHeight;
        const formElement = document.querySelector('.config-form');
        formElement.style.paddingBottom = toolbarHeight + 'px';
    }
    
    window.addEventListener('load', () => {
        adjustFormPadding();
    });
    window.addEventListener('resize', () => {
        adjustFormPadding();
    }); // Adjust size on window resize
    
    document.addEventListener("DOMContentLoaded", function() {
        loadConfig();
        
        // Ensure WiFi panel is hidden on page load
        const wifiPanel = document.getElementById('wifi-panel');
        if (wifiPanel) {
            wifiPanel.style.display = 'none';
        }
        
        // Add event listener for wifi_script_running toggle
        document.addEventListener('change', function(event) {
            if (event.target.id === 'wifi_script_running') {
                // Immediately apply the WiFi script toggle
                toggleWifiScript(event.target.checked);
                // Update status after toggle
                setTimeout(updateWifiScriptStatus, 1500);
            }
        });
    });

    let fontSize = 12;

    // Adjust font size based on device type
    if (/Mobi|Android/i.test(navigator.userAgent)) {
        fontSize = 7; // size for mobile devices
    }
    
    function adjustConfigFontSize(change) {
        fontSize += change;
        
        // Retrieve all elements with the class 'section-item'
        var sectionItems = document.getElementsByClassName('section-item');
        
        // Loop through each element and apply the style
        for (var i = 0; i < sectionItems.length; i++) {
            // Apply the style to the section element
            sectionItems[i].style.fontSize = fontSize + 'px';
            
            // Retrieve all inputs inside this section element
            var inputs = sectionItems[i].getElementsByTagName('input');
            
            // Loop through each input and apply the style
            for (var j = 0; j < inputs.length; j++) {
                inputs[j].style.fontSize = fontSize + 'px';
            }
            
            // Retrieve all elements with the class 'switch' inside this section element
            var switches = sectionItems[i].getElementsByClassName('switch');
            
            // Loop through each switch and apply the style
            for (var k = 0; k < switches.length; k++) {
                switches[k].style.fontSize = fontSize + 'px';
            }
    
            // Retrieve all elements with the class 'slider round' inside this section element
            var sliders = sectionItems[i].getElementsByClassName('slider round');
            
            // Loop through each slider and apply the style
            for (var l = 0; l < sliders.length; l++) {
                sliders[l].style.width = fontSize * 2 + 'px';  // Adjust width based on fontSize
                sliders[l].style.height = fontSize + 'px';  // Adjust height based on fontSize
                sliders[l].style.borderRadius = fontSize / 2 + 'px';  // Adjust border-radius based on fontSize
            }
        }
    
        // Retrieve all elements with the class 'section-title'
        var sectionTitles = document.getElementsByClassName('section-title');
        
        // Loop through each element and apply the style
        for (var i = 0; i < sectionTitles.length; i++) {
            sectionTitles[i].style.fontSize = fontSize + 'px';
        }
    
        // Retrieve all elements with the class 'label-switch'
        var labelSwitches = document.getElementsByClassName('label-switch');
        
        // Loop through each element and apply the style
        for (var i = 0; i < labelSwitches.length; i++) {
            labelSwitches[i].style.fontSize = fontSize + 'px';
        }
        
        // Apply the style to the element with the class 'config-form'
        document.querySelector('.config-form').style.fontSize = fontSize + 'px';
    }
    

    

function toggleConfigToolbar() {
    const mainToolbar = document.querySelector('.toolbar');
    const toggleButton = document.getElementById('toggle-toolbar')
    const toggleIcon = document.getElementById('toggle-icon');
    if (mainToolbar.classList.contains('hidden')) {
        mainToolbar.classList.remove('hidden');
        toggleIcon.src = 'images/hide.png';
        toggleButton.setAttribute('data-open', 'false');
    } else {
        mainToolbar.classList.add('hidden');
        toggleIcon.src = 'images/reveal.png';
        toggleButton.setAttribute('data-open', 'true');

    }
}

function updateWifiScriptStatus() {
    fetch('/get_wifi_script_status')
        .then(response => response.json())
        .then(data => {
            const wifiScriptCheckbox = document.getElementById('wifi_script_running');
            if (wifiScriptCheckbox) {
                wifiScriptCheckbox.checked = data.wifi_script_running;
            }
        })
        .catch(error => {
            console.error('Error fetching WiFi script status:', error);
        });
}

// WiFi network management functions

function showWifiStatus(message, type) {
    const statusDiv = document.getElementById('wifi-add-status');
    statusDiv.textContent = message;
    statusDiv.className = `wifi-status ${type}`;
    
    // Clear status after 5 seconds
    setTimeout(() => {
        statusDiv.textContent = '';
        statusDiv.className = 'wifi-status';
    }, 5000);
}

function loadKnownNetworks() {
    fetch('/get_known_wifi_networks')
        .then(response => response.json())
        .then(data => {
            const knownList = document.getElementById('wifi-known-list');
            knownList.innerHTML = '';
            
            if (data.networks && data.networks.length > 0) {
                data.networks.forEach(network => {
                    const li = document.createElement('li');
                    li.innerHTML = `
                        <span>${network.ssid}</span>
                        <button class="wifi-remove-btn" onclick="removeWifiNetwork('${network.ssid}')">Удалить</button>
                    `;
                    knownList.appendChild(li);
                });
            } else {
                const li = document.createElement('li');
                li.textContent = 'Нет сохраненных сетей';
                li.style.fontStyle = 'italic';
                li.style.color = '#aaa';
                knownList.appendChild(li);
            }
        })
        .catch(error => {
            console.error('Error loading known networks:', error);
            const knownList = document.getElementById('wifi-known-list');
            knownList.innerHTML = '<li style="color: #f44336;">Ошибка загрузки сетей</li>';
        });
}

function removeWifiNetwork(ssid) {
    if (!confirm(`Удалить сеть "${ssid}" из списка известных?`)) {
        return;
    }
    
    fetch('/remove_wifi_network', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            ssid: ssid
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showWifiStatus(`Сеть "${ssid}" удалена`, 'success');
            loadKnownNetworks();
        } else {
            showWifiStatus(data.message || 'Ошибка при удалении сети', 'error');
        }
    })
    .catch(error => {
        console.error('Error removing WiFi network:', error);
        showWifiStatus('Ошибка соединения с сервером', 'error');
    });
}

// Toggle WiFi script immediately when checkbox is changed
function toggleWifiScript(enabled) {
    const config = {
        wifi_script_running: enabled
    };
    
    fetch('/save_config', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(config)
    })
    .then(response => response.json())
    .then(data => {
        console.log('WiFi script toggle response:', data);
    })
    .catch(error => {
        console.error('Error toggling WiFi script:', error);
    });
}

// Load known networks when WiFi panel is opened
function toggleWifiPanel() {
    const panel = document.getElementById('wifi-panel');
    if (panel.style.display === 'none' || panel.style.display === '') {
        panel.style.display = 'block';
        loadKnownNetworks();
        scanWifi();
    } else {
        panel.style.display = 'none';
    }
}

// Add WiFi network to known networks file
async function addWifiNetwork() {
    const ssidInput = document.getElementById('wifi-ssid-input');
    const passwordInput = document.getElementById('wifi-password-input');
    const statusDiv = document.getElementById('wifi-add-status');
    
    const ssid = ssidInput.value.trim();
    const password = passwordInput.value.trim();
    
    // Validate input
    if (!ssid) {
        showWifiStatus('Пожалуйста, введите SSID сети', 'error');
        return;
    }
    
    if (!password) {
        showWifiStatus('Пожалуйста, введите пароль сети', 'error');
        return;
    }
    
    // Validate SSID length (max 32 characters for WiFi standard)
    if (ssid.length > 32) {
        showWifiStatus('SSID не может быть длиннее 32 символов', 'error');
        return;
    }
    
    // Validate password length (WPA/WPA2 requires 8-63 characters)
    if (password.length < 8 || password.length > 63) {
        showWifiStatus('Пароль должен содержать от 8 до 63 символов', 'error');
        return;
    }
    
    try {
        const response = await fetch('/add_wifi_network', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ssid: ssid,
                password: password
            })
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            showWifiStatus(`Сеть "${ssid}" успешно добавлена`, 'success');
            // Clear form
            ssidInput.value = '';
            passwordInput.value = '';
            // Reload known networks list
            loadKnownNetworks();
        } else {
            showWifiStatus(result.error || 'Ошибка при добавлении сети', 'error');
        }
    } catch (error) {
        console.error('Error adding WiFi network:', error);
        showWifiStatus('Ошибка соединения с сервером', 'error');
    }
}

// Load and display known WiFi networks
async function loadKnownNetworks() {
    try {
        const response = await fetch('/get_known_wifi_networks');
        const result = await response.json();
        
        const knownList = document.getElementById('wifi-known-list');
        knownList.innerHTML = '';
        
        if (response.ok && result.success) {
            if (result.networks && result.networks.length > 0) {
                result.networks.forEach(network => {
                    const li = document.createElement('li');
                    li.innerHTML = `
                        <span class="wifi-ssid">${escapeHtml(network.ssid)}</span>
                        <button class="wifi-remove" onclick="removeWifiNetwork('${escapeHtml(network.ssid)}')">Удалить</button>
                    `;
                    knownList.appendChild(li);
                });
            } else {
                const li = document.createElement('li');
                li.innerHTML = '<span style="color: #aaa; font-style: italic;">Нет сохраненных сетей</span>';
                knownList.appendChild(li);
            }
        } else {
            console.error('Error loading known networks:', result.error);
        }
    } catch (error) {
        console.error('Error loading known networks:', error);
    }
}

// Remove WiFi network from known networks
async function removeWifiNetwork(ssid) {
    if (!confirm(`Удалить сеть "${ssid}" из известных сетей?`)) {
        return;
    }
    
    try {
        const response = await fetch('/remove_wifi_network', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ssid: ssid
            })
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            showWifiStatus(`Сеть "${ssid}" удалена`, 'success');
            // Reload known networks list
            loadKnownNetworks();
        } else {
            showWifiStatus(result.error || 'Ошибка при удалении сети', 'error');
        }
    } catch (error) {
        console.error('Error removing WiFi network:', error);
        showWifiStatus('Ошибка соединения с сервером', 'error');
    }
}

// Show status message
function showWifiStatus(message, type) {
    const statusDiv = document.getElementById('wifi-add-status');
    statusDiv.textContent = message;
    statusDiv.className = `wifi-status ${type}`;
    
    // Hide status after 5 seconds
    setTimeout(() => {
        statusDiv.className = 'wifi-status';
    }, 5000);
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

