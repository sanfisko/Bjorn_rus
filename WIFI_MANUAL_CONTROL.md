# WiFi Manual Control Feature

## Overview
Added manual WiFi script control functionality to complement the existing auto-connect service.

## Features Added

### 1. Manual Script Control Toggle
- **Parameter**: `wifi_script_running`
- **Location**: config.html WiFi Settings section
- **Function**: Start/stop WiFi auto-connect script manually
- **Independent**: Works independently of the systemd service

### 2. Real-time Status Updates
- **Endpoint**: `/get_wifi_script_status`
- **Function**: Returns actual script running status
- **Auto-update**: Status refreshes automatically after toggle changes

### 3. Process Management
- **Start**: Uses `subprocess.Popen()` to run script in background
- **Stop**: Uses `pkill -f wifi_auto_connect.sh` to terminate process
- **Verification**: Checks actual process status with `pgrep`

## Usage

### Two Independent Controls:
1. **wifi_auto_connect**: Enable/disable systemd service (auto-start with system)
2. **wifi_script_running**: Manual start/stop of script (immediate control)

### Scenarios:
- **Service enabled + Manual off**: Script starts with system, can be stopped manually
- **Service disabled + Manual on**: Script runs only when manually started
- **Both enabled**: Script runs with system and shows as manually running
- **Both disabled**: Script is completely off

## Technical Implementation

### Backend Changes:
- `shared.py`: Added default config parameters
- `utils.py`: Added manual script management logic
- `webapp.py`: Added status endpoint
- `config/shared_config.json`: Added new parameters

### Frontend Changes:
- `config.js`: Added status update functions and event handlers
- Real-time status synchronization
- Automatic refresh after configuration changes

## Security Considerations:
- Script output redirected to DEVNULL
- Proper error handling and logging
- Process verification before status updates
- Safe process termination methods