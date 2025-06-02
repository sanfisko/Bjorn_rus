#!/usr/bin/env python3

import requests
import json
import time
import subprocess

def test_wifi_toggle():
    """Test the WiFi script toggle functionality"""
    base_url = "http://localhost:8000"
    
    print("=== Testing WiFi Script Toggle ===")
    
    # 1. Get current status
    print("\n1. Getting current WiFi script status...")
    try:
        response = requests.get(f"{base_url}/get_wifi_script_status")
        if response.status_code == 200:
            status = response.json()
            print(f"Current status: {status}")
        else:
            print(f"Failed to get status: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error getting status: {e}")
        return False
    
    # 2. Test turning ON the WiFi script
    print("\n2. Turning ON WiFi script...")
    try:
        data = {"wifi_script_running": True}
        response = requests.post(f"{base_url}/save_config", 
                               json=data,
                               headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {result}")
        else:
            print(f"Failed to turn on: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error turning on: {e}")
        return False
    
    # 3. Wait and check if process is running
    print("\n3. Waiting 3 seconds and checking if process is running...")
    time.sleep(3)
    
    try:
        result = subprocess.run("ps aux | grep wifi_auto_connect.sh | grep -v grep", 
                              shell=True, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            print("✓ WiFi script process is running!")
            print(f"Process info: {result.stdout.strip()}")
        else:
            print("✗ WiFi script process is NOT running")
            print(f"ps command output: '{result.stdout.strip()}'")
    except Exception as e:
        print(f"Error checking process: {e}")
    
    # 4. Check status file
    print("\n4. Checking status file...")
    try:
        with open('/tmp/wifi_auto_connect_status', 'r') as f:
            status_data = json.load(f)
            print(f"Status file content: {status_data}")
    except FileNotFoundError:
        print("✗ Status file not found")
    except Exception as e:
        print(f"Error reading status file: {e}")
    
    # 5. Get updated status from web interface
    print("\n5. Getting updated status from web interface...")
    try:
        response = requests.get(f"{base_url}/get_wifi_script_status")
        if response.status_code == 200:
            status = response.json()
            print(f"Updated status: {status}")
        else:
            print(f"Failed to get updated status: {response.status_code}")
    except Exception as e:
        print(f"Error getting updated status: {e}")
    
    # 6. Test turning OFF the WiFi script
    print("\n6. Turning OFF WiFi script...")
    try:
        data = {"wifi_script_running": False}
        response = requests.post(f"{base_url}/save_config", 
                               json=data,
                               headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {result}")
        else:
            print(f"Failed to turn off: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error turning off: {e}")
        return False
    
    # 7. Wait and check if process is stopped
    print("\n7. Waiting 3 seconds and checking if process is stopped...")
    time.sleep(3)
    
    try:
        result = subprocess.run("ps aux | grep wifi_auto_connect.sh | grep -v grep", 
                              shell=True, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            print("✗ WiFi script process is still running!")
            print(f"Process info: {result.stdout.strip()}")
        else:
            print("✓ WiFi script process is stopped")
    except Exception as e:
        print(f"Error checking process: {e}")
    
    # 8. Final status check
    print("\n8. Final status check...")
    try:
        response = requests.get(f"{base_url}/get_wifi_script_status")
        if response.status_code == 200:
            status = response.json()
            print(f"Final status: {status}")
        else:
            print(f"Failed to get final status: {response.status_code}")
    except Exception as e:
        print(f"Error getting final status: {e}")
    
    print("\n=== Test completed ===")
    return True

if __name__ == "__main__":
    test_wifi_toggle()