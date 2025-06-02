#!/bin/bash

# BJORN Installation Script
# This script handles the complete installation of BJORN
# Author: infinition
# Version: 1.0 - 071124 - 0954

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging configuration
LOG_DIR="/var/log/bjorn_install"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/bjorn_install_$(date +%Y%m%d_%H%M%S).log"
VERBOSE=false

# Global variables
BJORN_USER="bjorn"
BJORN_PATH="/home/${BJORN_USER}/Bjorn_rus"
CURRENT_STEP=0
TOTAL_STEPS=8

if [[ "$1" == "--help" ]]; then
    echo "Usage: sudo ./install_bjorn.sh"
    echo "Make sure you have the necessary permissions and that all dependencies are met."
    exit 0
fi

# Function to display progress
show_progress() {
    echo -e "${BLUE}Step $CURRENT_STEP of $TOTAL_STEPS: $1${NC}"
}

# Logging function
log() {
    local level=$1
    shift
    local message="[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*"
    echo -e "$message" >> "$LOG_FILE"
    if [ "$VERBOSE" = true ] || [ "$level" != "DEBUG" ]; then
        case $level in
            "ERROR") echo -e "${RED}$message${NC}" ;;
            "SUCCESS") echo -e "${GREEN}$message${NC}" ;;
            "WARNING") echo -e "${YELLOW}$message${NC}" ;;
            "INFO") echo -e "${BLUE}$message${NC}" ;;
            *) echo -e "$message" ;;
        esac
    fi
}

# Error handling function
handle_error() {
    local error_code=$?
    local error_message=$1
    log "ERROR" "An error occurred during: $error_message (Error code: $error_code)"
    log "ERROR" "Check the log file for details: $LOG_FILE"

    echo -e "\n${RED}Would you like to:"
    echo "1. Retry this step"
    echo "2. Skip this step (not recommended)"
    echo "3. Exit installation (default)${NC}"
    echo -e "${YELLOW}Auto-exiting in 30 seconds if no response is given.${NC}"
    read -t 30 -p "Enter your choice (1-3) [auto-exit in 30s]: " choice
    read_exit_code=$?
    
    # Check if read timed out (exit code > 128)
    if [ $read_exit_code -gt 128 ]; then
        choice=3
        echo -e "\n${YELLOW}No response received. Auto-exiting installation for safety...${NC}"
        log "INFO" "Auto-exit initiated after 30 second timeout during error handling."
    fi

    case $choice in
        1) return 1 ;; # Retry
        2) return 0 ;; # Skip
        3) clean_exit 1 ;; # Exit
        *) 
            echo -e "${RED}Invalid choice. Exiting for safety.${NC}"
            clean_exit 1
        ;;
    esac
}

# Function to check command success
check_success() {
    if [ $? -eq 0 ]; then
        log "SUCCESS" "$1"
        return 0
    else
        handle_error "$1"
        return $?
    fi
}

# # Check system compatibility
# check_system_compatibility() {
#     log "INFO" "Checking system compatibility..."
    
#     # Check if running on Raspberry Pi
#     if ! grep -q "Raspberry Pi" /proc/cpuinfo; then
#         log "WARNING" "This system might not be a Raspberry Pi. Continue anyway? (y/n)"
#         read -r response
#         if [[ ! "$response" =~ ^[Yy]$ ]]; then
#             clean_exit 1
#         fi
#     fi
    
#     check_success "System compatibility check completed"
# }
# Check system compatibility
check_system_compatibility() {
    log "INFO" "Checking system compatibility..."
    local should_ask_confirmation=false
    
    # Check if running on Raspberry Pi
    if ! grep -q "Raspberry Pi" /proc/cpuinfo; then
        log "WARNING" "This system might not be a Raspberry Pi"
        should_ask_confirmation=true
    fi

    # Check RAM (Raspberry Pi Zero has 512MB RAM)
    total_ram=$(free -m | awk '/^Mem:/{print $2}')
    if [ "$total_ram" -lt 410 ]; then
        log "WARNING" "Low RAM detected. Required: 512MB (410 With OS Running), Found: ${total_ram}MB"
        echo -e "${YELLOW}Your system has less RAM than recommended. This might affect performance, but you can continue.${NC}"
        should_ask_confirmation=true
    else
        log "SUCCESS" "RAM check passed: ${total_ram}MB available"
    fi

    # Check available disk space
    available_space=$(df -m /home | awk 'NR==2 {print $4}')
    if [ "$available_space" -lt 2048 ]; then
        log "WARNING" "Low disk space. Recommended: 1GB, Found: ${available_space}MB"
        echo -e "${YELLOW}Your system has less free space than recommended. This might affect installation.${NC}"
        should_ask_confirmation=true
    else
        log "SUCCESS" "Disk space check passed: ${available_space}MB available"
    fi

    # Check OS version
    if [ -f "/etc/os-release" ]; then
        source /etc/os-release
        
        # Verify if it's Raspbian
        if [ "$NAME" != "Raspbian GNU/Linux" ]; then
            log "WARNING" "Different OS detected. Recommended: Raspbian GNU/Linux, Found: ${NAME}"
            echo -e "${YELLOW}Your system is not running Raspbian GNU/Linux.${NC}"
            should_ask_confirmation=true
        fi
        
        # Compare versions (expecting Bookworm = 12)
        expected_version="12"
        if [ "$VERSION_ID" != "$expected_version" ]; then
            log "WARNING" "Different OS version detected"
            echo -e "${YELLOW}This script was tested with Raspbian GNU/Linux 12 (bookworm)${NC}"
            echo -e "${YELLOW}Current system: ${PRETTY_NAME}${NC}"
            if [ "$VERSION_ID" -lt "$expected_version" ]; then
                echo -e "${YELLOW}Your system version ($VERSION_ID) is older than recommended ($expected_version)${NC}"
            elif [ "$VERSION_ID" -gt "$expected_version" ]; then
                echo -e "${YELLOW}Your system version ($VERSION_ID) is newer than tested ($expected_version)${NC}"
            fi
            should_ask_confirmation=true
        else
            log "SUCCESS" "OS version check passed: ${PRETTY_NAME}"
        fi
    else
        log "WARNING" "Could not determine OS version (/etc/os-release not found)"
        should_ask_confirmation=true
    fi

    # Check if system is 32-bit ARM (armhf)
    architecture=$(dpkg --print-architecture)
    if [ "$architecture" != "armhf" ]; then
        log "WARNING" "Different architecture detected. Expected: armhf, Found: ${architecture}"
        echo -e "${YELLOW}This script was tested with armhf architecture${NC}"
        should_ask_confirmation=true
    fi
    
    # Additional Pi Zero specific checks if possible
    if ! (grep -q "Pi Zero" /proc/cpuinfo || grep -q "BCM2835" /proc/cpuinfo); then
        log "WARNING" "Could not confirm if this is a Raspberry Pi Zero"
        echo -e "${YELLOW}This script was designed for Raspberry Pi Zero${NC}"
        should_ask_confirmation=true
    else
        log "SUCCESS" "Raspberry Pi Zero detected"
    fi

    if [ "$should_ask_confirmation" = true ]; then
        echo -e "\n${YELLOW}Some system compatibility warnings were detected (see above).${NC}"
        echo -e "${YELLOW}The installation might not work as expected.${NC}"
        echo -e "${YELLOW}Installation will automatically continue in 15 seconds if no response is given.${NC}"
        read -t 15 -p "Do you want to continue anyway? (y/n) [auto-continue in 15s]: " response
        read_exit_code=$?
        
        # Check if read timed out (exit code > 128) or user answered 'y'
        if [ $read_exit_code -gt 128 ] || [[ "$response" =~ ^[Yy]$ ]]; then
            if [ $read_exit_code -gt 128 ]; then
                echo -e "\n${YELLOW}No response received. Automatically continuing installation...${NC}"
                log "INFO" "Auto-continue initiated after 15 second timeout."
            else
                log "INFO" "User confirmed to continue installation."
            fi
        elif [[ "$response" =~ ^[Nn]$ ]]; then
            log "INFO" "Installation aborted by user after compatibility warnings"
            clean_exit 1
        else
            echo -e "${YELLOW}Invalid response. Continuing installation...${NC}"
            log "INFO" "Invalid response received, continuing installation."
        fi
    else
        log "SUCCESS" "All compatibility checks passed"
    fi

    log "INFO" "System compatibility check completed"
    return 0
}



# Install system dependencies
install_dependencies() {
    log "INFO" "Installing system dependencies..."
    
    # Update package list
    apt-get update
    
    # List of required packages based on README
    packages=(
        "python3-pip"
        "wget"
        "lsof"
        "git"
        "libopenjp2-7"
        "nmap"
        "libopenblas-dev"
        "bluez-tools"
        "bluez"
        "dhcpcd5"
        "bridge-utils"
        "python3-pil"
        "libjpeg-dev"
        "zlib1g-dev"
        "libpng-dev"
        "python3-dev"
        "libffi-dev"
        "libssl-dev"
        "libgpiod-dev"
        "libi2c-dev"
        "libatlas-base-dev"
        "build-essential"
    )
    
    # Install packages
    for package in "${packages[@]}"; do
        log "INFO" "Installing $package..."
        apt-get install -y "$package"
        check_success "Installed $package"
    done
    
    # Update nmap scripts
    nmap --script-updatedb
    check_success "Dependencies installation completed"
}

# Configure system limits
configure_system_limits() {
    log "INFO" "Configuring system limits..."

    # Configure /etc/security/limits.conf - check if already configured
    if ! grep -q "* soft nofile 65535" /etc/security/limits.conf; then
        cat >> /etc/security/limits.conf << EOF
* soft nofile 65535
* hard nofile 65535
root soft nofile 65535
root hard nofile 65535
EOF
        log "INFO" "Added nofile limits to limits.conf"
    else
        log "INFO" "nofile limits already configured in limits.conf, skipping"
    fi

    # Configure systemd limits - check if already configured
    if ! grep -q "^DefaultLimitNOFILE=65535" /etc/systemd/system.conf; then
        sed -i '/^#DefaultLimitNOFILE=/d' /etc/systemd/system.conf
        sed -i '/^DefaultLimitNOFILE=/d' /etc/systemd/system.conf
        echo "DefaultLimitNOFILE=65535" >> /etc/systemd/system.conf
        log "INFO" "Added DefaultLimitNOFILE to system.conf"
    else
        log "INFO" "DefaultLimitNOFILE already configured in system.conf, skipping"
    fi
    
    if ! grep -q "^DefaultLimitNOFILE=65535" /etc/systemd/user.conf; then
        sed -i '/^#DefaultLimitNOFILE=/d' /etc/systemd/user.conf
        sed -i '/^DefaultLimitNOFILE=/d' /etc/systemd/user.conf
        echo "DefaultLimitNOFILE=65535" >> /etc/systemd/user.conf
        log "INFO" "Added DefaultLimitNOFILE to user.conf"
    else
        log "INFO" "DefaultLimitNOFILE already configured in user.conf, skipping"
    fi

    # Create /etc/security/limits.d/90-nofile.conf - check if already exists
    if [ ! -f "/etc/security/limits.d/90-nofile.conf" ]; then
        cat > /etc/security/limits.d/90-nofile.conf << EOF
root soft nofile 65535
root hard nofile 65535
EOF
        log "INFO" "Created 90-nofile.conf"
    else
        log "INFO" "90-nofile.conf already exists, skipping"
    fi

    # Configure sysctl - check if fs.file-max already exists
    if ! grep -q "fs.file-max" /etc/sysctl.conf; then
        echo "fs.file-max = 2097152" >> /etc/sysctl.conf
        log "INFO" "Added fs.file-max to sysctl.conf"
    else
        log "INFO" "fs.file-max already configured in sysctl.conf, skipping"
    fi
    sysctl -p

    check_success "System limits configuration completed"
}

# Configure SPI and I2C
configure_interfaces() {
    log "INFO" "Configuring SPI and I2C interfaces..."
    
    # Enable SPI and I2C using raspi-config
    raspi-config nonint do_spi 0
    raspi-config nonint do_i2c 0
    
    check_success "Interface configuration completed"
}

# Setup BJORN
setup_bjorn() {
    log "INFO" "Setting up BJORN..."
    
    # Create BJORN user if it doesn't exist
    if ! id -u $BJORN_USER >/dev/null 2>&1; then
        adduser --disabled-password --gecos "" $BJORN_USER
        check_success "Created BJORN user"
    fi

    # Check for existing BJORN directory
    cd /home/$BJORN_USER
    if [ -d "Bjorn_rus" ]; then
        log "INFO" "Using existing BJORN directory"
        echo -e "${GREEN}Using existing BJORN directory${NC}"
    else
        # No existing directory, proceed with clone
        log "INFO" "Cloning BJORN repository"
        git clone https://github.com/sanfisko/Bjorn_rus.git
        check_success "Cloned BJORN repository"
    fi

    cd Bjorn_rus

    # Update the shared_config.json file with the selected EPD version
    log "INFO" "Updating E-Paper display configuration..."
    if [ -f "config/shared_config.json" ]; then
        sed -i "s/\"epd_type\": \"[^\"]*\"/\"epd_type\": \"$EPD_VERSION\"/" config/shared_config.json
        check_success "Updated E-Paper display configuration to $EPD_VERSION"
    else
        log "ERROR" "Configuration file not found: config/shared_config.json"
        handle_error "E-Paper display configuration update"
    fi

    # Install requirements with --break-system-packages flag
    log "INFO" "Installing Python requirements..."
    
    pip3 install -r requirements.txt --break-system-packages
    check_success "Installed Python requirements"

    # Set correct permissions
    chown -R $BJORN_USER:$BJORN_USER /home/$BJORN_USER/Bjorn_rus
    chmod -R 755 /home/$BJORN_USER/Bjorn_rus
    
    # Add bjorn user to necessary groups
    usermod -a -G spi,gpio,i2c $BJORN_USER
    check_success "Added bjorn user to required groups"
}


# Configure services
setup_services() {
    log "INFO" "Setting up system services..."
    
    # Create kill_port_8000.sh script
    cat > $BJORN_PATH/kill_port_8000.sh << 'EOF'
#!/bin/bash
PORT=8000
PIDS=$(lsof -t -i:$PORT)
if [ -n "$PIDS" ]; then
    echo "Killing PIDs using port $PORT: $PIDS"
    kill -9 $PIDS
fi
EOF
    chmod +x $BJORN_PATH/kill_port_8000.sh

    # Create BJORN service
    cat > /etc/systemd/system/bjorn.service << EOF
[Unit]
Description=Bjorn Service
DefaultDependencies=no
Before=basic.target
After=local-fs.target

[Service]
ExecStartPre=/home/bjorn/Bjorn_rus/kill_port_8000.sh
ExecStart=/usr/bin/python3 /home/bjorn/Bjorn_rus/Bjorn.py
WorkingDirectory=/home/bjorn/Bjorn_rus
StandardOutput=inherit
StandardError=inherit
Restart=always
User=root

# Check open files and restart if it reached the limit (ulimit -n buffer of 1000)
ExecStartPost=/bin/bash -c 'FILE_LIMIT=\$(ulimit -n); THRESHOLD=\$(( FILE_LIMIT - 1000 )); while :; do TOTAL_OPEN_FILES=\$(lsof | wc -l); if [ "\$TOTAL_OPEN_FILES" -ge "\$THRESHOLD" ]; then echo "File descriptor threshold reached: \$TOTAL_OPEN_FILES (threshold: \$THRESHOLD). Restarting service."; systemctl restart bjorn.service; exit 0; fi; sleep 10; done &'

[Install]
WantedBy=multi-user.target
EOF

    # Configure PAM - check if already configured
    if ! grep -q "session required pam_limits.so" /etc/pam.d/common-session; then
        echo "session required pam_limits.so" >> /etc/pam.d/common-session
        log "INFO" "Added pam_limits.so to common-session"
    else
        log "INFO" "pam_limits.so already configured in common-session, skipping"
    fi
    
    if ! grep -q "session required pam_limits.so" /etc/pam.d/common-session-noninteractive; then
        echo "session required pam_limits.so" >> /etc/pam.d/common-session-noninteractive
        log "INFO" "Added pam_limits.so to common-session-noninteractive"
    else
        log "INFO" "pam_limits.so already configured in common-session-noninteractive, skipping"
    fi

    # Create WiFi Auto Connect service
    cp $BJORN_PATH/wifi-auto-connect.service /etc/systemd/system/
    
    # Enable and start services
    systemctl daemon-reload
    systemctl enable bjorn.service
    # Note: wifi-auto-connect.service is not enabled by default - it can be enabled via web interface

    check_success "Services setup completed"
}

# Configure USB Gadget
configure_usb_gadget() {
    log "INFO" "Configuring USB Gadget..."

    # Modify cmdline.txt - check if already configured
    if ! grep -q "modules-load=dwc2,g_ether" /boot/firmware/cmdline.txt; then
        sed -i 's/rootwait/rootwait modules-load=dwc2,g_ether/' /boot/firmware/cmdline.txt
        log "INFO" "Added USB gadget modules to cmdline.txt"
    else
        log "INFO" "USB gadget modules already configured in cmdline.txt, skipping"
    fi

    # Modify config.txt - check if already configured
    if ! grep -q "dtoverlay=dwc2" /boot/firmware/config.txt; then
        echo "dtoverlay=dwc2" >> /boot/firmware/config.txt
        log "INFO" "Added dtoverlay=dwc2 to config.txt"
    else
        log "INFO" "dtoverlay=dwc2 already configured in config.txt, skipping"
    fi

    # Create USB gadget script
    cat > /usr/local/bin/usb-gadget.sh << 'EOF'
#!/bin/bash
set -e

modprobe libcomposite
cd /sys/kernel/config/usb_gadget/
mkdir -p g1
cd g1

echo 0x1d6b > idVendor
echo 0x0104 > idProduct
echo 0x0100 > bcdDevice
echo 0x0200 > bcdUSB

mkdir -p strings/0x409
echo "fedcba9876543210" > strings/0x409/serialnumber
echo "Raspberry Pi" > strings/0x409/manufacturer
echo "Pi Zero USB" > strings/0x409/product

mkdir -p configs/c.1/strings/0x409
echo "Config 1: ECM network" > configs/c.1/strings/0x409/configuration
echo 250 > configs/c.1/MaxPower

mkdir -p functions/ecm.usb0

if [ -L configs/c.1/ecm.usb0 ]; then
    rm configs/c.1/ecm.usb0
fi
ln -s functions/ecm.usb0 configs/c.1/

max_retries=10
retry_count=0

while ! ls /sys/class/udc > UDC 2>/dev/null; do
    if [ $retry_count -ge $max_retries ]; then
        echo "Error: Device or resource busy after $max_retries attempts."
        exit 1
    fi
    retry_count=$((retry_count + 1))
    sleep 1
done

if ! ip addr show usb0 | grep -q "172.20.2.1"; then
    ifconfig usb0 172.20.2.1 netmask 255.255.255.0
else
    echo "Interface usb0 already configured."
fi
EOF

    chmod +x /usr/local/bin/usb-gadget.sh

    # Create USB gadget service
    cat > /etc/systemd/system/usb-gadget.service << EOF
[Unit]
Description=USB Gadget Service
After=network.target

[Service]
ExecStartPre=/sbin/modprobe libcomposite
ExecStart=/usr/local/bin/usb-gadget.sh
Type=simple
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF

    # Configure network interface - check if already configured
    if ! grep -q "allow-hotplug usb0" /etc/network/interfaces; then
        cat >> /etc/network/interfaces << EOF

allow-hotplug usb0
iface usb0 inet static
    address 172.20.2.1
    netmask 255.255.255.0
EOF
        log "INFO" "Added usb0 interface configuration to /etc/network/interfaces"
    else
        log "INFO" "usb0 interface already configured in /etc/network/interfaces, skipping"
    fi

    # Enable and start services
    systemctl daemon-reload
    systemctl enable systemd-networkd
    systemctl enable usb-gadget
    systemctl start systemd-networkd
    systemctl start usb-gadget

    check_success "USB Gadget configuration completed"
}

# Verify installation
verify_installation() {
    log "INFO" "Verifying installation..."
    
    # Check if services are running
    if ! systemctl is-active --quiet bjorn.service; then
        log "WARNING" "BJORN service is not running"
    else
        log "SUCCESS" "BJORN service is running"
    fi
    
    # Check web interface
    sleep 5
    if curl -s http://localhost:8000 > /dev/null; then
        log "SUCCESS" "Web interface is accessible"
    else
        log "WARNING" "Web interface is not responding"
    fi
}

# Clean exit function
clean_exit() {
    local exit_code=$1
    if [ $exit_code -eq 0 ]; then
        log "SUCCESS" "BJORN installation completed successfully!"
        log "INFO" "Log file available at: $LOG_FILE"
    else
        log "ERROR" "BJORN installation failed!"
        log "ERROR" "Check the log file for details: $LOG_FILE"
    fi
    exit $exit_code
}

# Main installation process
main() {
    log "INFO" "Starting BJORN installation..."

    # Check if script is run as root
    if [ "$(id -u)" -ne 0 ]; then
        echo "This script must be run as root. Please use 'sudo'."
        exit 1
    fi

    # Automatically use full installation
    install_option=1
    log "INFO" "Using full installation (recommended)"

    # E-Paper Display Selection
    echo -e "\n${BLUE}Please select your E-Paper Display version:${NC}"
    echo "1. epd2in13"
    echo "2. epd2in13_V2"
    echo "3. epd2in13_V3"
    echo "4. epd2in13_V4 (default)"
    echo "5. epd2in7"
    echo -e "${YELLOW}Auto-selecting epd2in13_V4 in 15 seconds if no response is given.${NC}"
    
    while true; do
        read -t 15 -p "Enter your choice (1-5) [auto-select 4 in 15s]: " epd_choice
        read_exit_code=$?
        
        # Check if read timed out (exit code > 128)
        if [ $read_exit_code -gt 128 ]; then
            epd_choice=4
            echo -e "\n${YELLOW}No response received. Auto-selecting epd2in13_V4 (option 4)...${NC}"
            log "INFO" "Auto-selected E-Paper Display version: epd2in13_V4 after 15 second timeout."
        fi
        
        case $epd_choice in
            1) EPD_VERSION="epd2in13"; break;;
            2) EPD_VERSION="epd2in13_V2"; break;;
            3) EPD_VERSION="epd2in13_V3"; break;;
            4) EPD_VERSION="epd2in13_V4"; break;;
            5) EPD_VERSION="epd2in7"; break;;
            *) echo -e "${RED}Invalid choice. Please select 1-5.${NC}";;
        esac
    done

    log "INFO" "Selected E-Paper Display version: $EPD_VERSION"

    # Execute full installation steps
    CURRENT_STEP=1; show_progress "Checking system compatibility"
    check_system_compatibility

    CURRENT_STEP=2; show_progress "Installing system dependencies"
    install_dependencies

    CURRENT_STEP=3; show_progress "Configuring system limits"
    configure_system_limits

    CURRENT_STEP=4; show_progress "Configuring interfaces"
    configure_interfaces

    CURRENT_STEP=5; show_progress "Setting up BJORN"
    setup_bjorn

    CURRENT_STEP=6; show_progress "Configuring USB Gadget"
    configure_usb_gadget

    CURRENT_STEP=7; show_progress "Setting up services"
    setup_services

    CURRENT_STEP=8; show_progress "Verifying installation"
    verify_installation

    #removed git files
    find "$BJORN_PATH" -name ".git*" -exec rm -rf {} +

    log "SUCCESS" "BJORN installation completed!"
    log "INFO" "Please reboot your system to apply all changes."
    echo -e "\n${GREEN}Installation completed successfully!${NC}"
    echo -e "${YELLOW}Important notes:${NC}"
    echo "1. If configuring Windows PC for USB gadget connection:"
    echo "   - Set static IP: 172.20.2.2"
    echo "   - Subnet Mask: 255.255.255.0"
    echo "   - Default Gateway: 172.20.2.1"
    echo "   - DNS Servers: 8.8.8.8, 8.8.4.4"
    echo "2. Web interface will be available at: http://[device-ip]:8000"
    echo "3. Make sure your e-Paper HAT (2.13-inch) is properly connected"

    echo -e "${YELLOW}System will automatically reboot in 15 seconds if no response is given.${NC}"
    read -t 15 -p "Would you like to reboot now? (y/n) [auto-reboot in 15s]: " reboot_now
    read_exit_code=$?
    
    # Check if read timed out (exit code > 128) or user answered 'y'
    if [ $read_exit_code -gt 128 ] || [ "$reboot_now" = "y" ]; then
        if [ $read_exit_code -gt 128 ]; then
            echo -e "\n${YELLOW}No response received. Automatically rebooting system...${NC}"
            log "INFO" "Auto-reboot initiated after 15 second timeout."
        else
            log "INFO" "User requested system reboot."
        fi
        
        if reboot; then
            log "INFO" "System reboot initiated."
        else
            log "ERROR" "Failed to initiate reboot."
            exit 1
        fi
    else
        echo -e "${YELLOW}Reboot your system to apply all changes & run Bjorn service.${NC}"
    fi
}

main




