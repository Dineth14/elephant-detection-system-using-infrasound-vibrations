#!/usr/bin/env python3
"""
Direct ESP32 communication test
This will connect to COM8 and show raw data from ESP32
"""

import serial
import time

def test_esp32_communication():
    print("[TEST] Testing direct ESP32 communication on COM8...")
    
    try:
        # Connect to ESP32
        ser = serial.Serial('COM8', 115200, timeout=1)
        time.sleep(2)  # Wait for ESP32 to reset
        
        print("[CONNECTED] ESP32 connected on COM8")
        print("[LISTENING] Waiting for ESP32 data (60 seconds)...")
        print("-" * 50)
        
        # Send some commands to wake up ESP32
        ser.write(b"GET_STATUS\n")
        time.sleep(0.1)
        ser.write(b"GET_FEATURES\n")
        time.sleep(0.1)
        
        start_time = time.time()
        line_count = 0
        
        while time.time() - start_time < 60:  # Listen for 60 seconds
            if ser.in_waiting > 0:
                try:
                    line = ser.readline().decode('utf-8').strip()
                    if line:
                        line_count += 1
                        timestamp = time.strftime("%H:%M:%S")
                        print(f"[{timestamp}] {line}")
                        
                        # If we see features data, that means audio processing is working
                        if line.startswith("FEATURES:"):
                            print("✅ FEATURES data detected - ESP32 audio processing is working!")
                        elif line.startswith("DEBUG:"):
                            print("🔧 Debug info from ESP32")
                        elif line.startswith("STATUS:"):
                            print("📊 Status info from ESP32")
                            
                except UnicodeDecodeError as e:
                    print(f"[{time.strftime('%H:%M:%S')}] Unicode error: {e}")
            else:
                time.sleep(0.1)
        
        print("-" * 50)
        print(f"[SUMMARY] Received {line_count} lines in 60 seconds")
        
        if line_count == 0:
            print("❌ No data received from ESP32")
            print("Possible issues:")
            print("  - No microphone connected to GPIO34")
            print("  - ESP32 firmware not running properly") 
            print("  - Audio processing not working")
        else:
            print("✅ ESP32 is sending data")
            
        ser.close()
        
    except Exception as e:
        print(f"[ERROR] Communication test failed: {e}")

if __name__ == "__main__":
    test_esp32_communication()
