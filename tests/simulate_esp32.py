#!/usr/bin/env python3
"""
ESP32 Data Simulator - Send realistic data to GUI via virtual serial connection
This simulates what a properly working ESP32 would send
"""

import tkinter as tk
import threading
import time
import random
import sys
import os

# Add the python_gui directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python_gui'))

from python_gui.noise_logger_gui import ESP32NoiseLoggerGUI

def simulate_esp32_data(gui_instance):
    """Simulate ESP32 sending realistic elephant detection data"""
    print("[SIMULATOR] Starting ESP32 data simulation...")
    time.sleep(3)  # Wait for GUI to fully load
    
    # Send initial status
    gui_instance.data_queue.put("ESP32_NOISE_LOGGER_READY")
    gui_instance.data_queue.put("STATUS:1000,512,45000")  # uptime, samples, memory
    
    counter = 0
    elephant_detected = False
    
    while True:
        # Simulate realistic audio features for elephant sounds
        # Based on research: elephants produce infrasound 1-20Hz, some up to 40Hz
        # Our system monitors 10-200Hz range
        
        if counter % 30 == 0:  # Every 3 seconds, chance of elephant
            elephant_detected = random.random() < 0.3  # 30% chance
            
        if elephant_detected and counter % 30 < 10:  # Elephant for 1 second
            # Elephant features - higher infrasound, specific frequency patterns
            rms = random.uniform(0.4, 0.9)  # High energy
            spectral_centroid = random.uniform(25, 60)  # Low frequency focus
            infrasound_energy = random.uniform(0.6, 0.95)  # Strong infrasound
            low_band_energy = random.uniform(0.4, 0.8)  # Good low frequency
            mid_band_energy = random.uniform(0.1, 0.3)  # Less mid frequency
            dominant_freq = random.uniform(12, 45)  # Elephant frequency range
            temporal_envelope = random.uniform(0.3, 0.7)  # Sustained sounds
            spectral_flux = random.uniform(0.1, 0.4)  # Moderate changes
            
            classification = "elephant"
            confidence = random.uniform(0.75, 0.95)
            
            if counter % 10 == 0:  # Print every second during detection
                print(f"[SIMULATOR] Simulating ELEPHANT detection (confidence: {confidence:.2f})")
                
        else:
            # Background noise/not elephant - more random patterns
            rms = random.uniform(0.05, 0.4)
            spectral_centroid = random.uniform(45, 150)  # Higher frequencies
            infrasound_energy = random.uniform(0.1, 0.5)  # Lower infrasound
            low_band_energy = random.uniform(0.1, 0.5)
            mid_band_energy = random.uniform(0.1, 0.6)
            dominant_freq = random.uniform(30, 180)  # Wider frequency range
            temporal_envelope = random.uniform(0.1, 0.5)
            spectral_flux = random.uniform(0.05, 0.3)
            
            classification = "not_elephant"
            confidence = random.uniform(0.5, 0.85)
        
        # Create FEATURES data string (same format as ESP32)
        features_data = f"FEATURES:{rms:.4f},{spectral_centroid:.1f},{infrasound_energy:.4f},{low_band_energy:.4f},{mid_band_energy:.4f},{dominant_freq:.1f},{temporal_envelope:.4f},{spectral_flux:.4f},{classification},{confidence:.3f}"
        
        # Add to queue
        gui_instance.data_queue.put(features_data)
        
        # Send periodic status updates
        if counter % 50 == 0:  # Every 5 seconds
            uptime = counter * 100  # ms
            samples = counter * 10
            memory = random.randint(40000, 50000)
            gui_instance.data_queue.put(f"STATUS:{uptime},{samples},{memory}")
        
        counter += 1
        time.sleep(0.1)  # 10 Hz rate

def main():
    print("[SIMULATOR] Starting ESP32 Data Simulator...")
    print("[INFO] This simulates a working ESP32 with microphone")
    print("[INFO] You should see real-time data updates in the GUI")
    
    root = tk.Tk()
    gui = ESP32NoiseLoggerGUI(root)
    
    # Simulate connection
    gui.connected = True
    gui.connection_status.config(text="✓ Connected: COM8 (Simulated)", fg="#4caf50")
    if hasattr(gui, 'connection_status_bar'):
        gui.connection_status_bar.config(text="⚡ Connected (Simulated)", fg="#3fb950")
    gui.log_message("🔗 ESP32 Data Simulator connected")
    gui.log_message("📡 Simulating elephant detection system...")
    
    # Start simulation thread
    sim_thread = threading.Thread(target=simulate_esp32_data, args=(gui,), daemon=True)
    sim_thread.start()
    
    root.protocol("WM_DELETE_WINDOW", gui.on_closing)
    
    try:
        print("[GUI] Starting GUI with simulated ESP32 data...")
        root.mainloop()
    except KeyboardInterrupt:
        gui.on_closing()

if __name__ == "__main__":
    main()
