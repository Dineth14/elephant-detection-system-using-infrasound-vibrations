#!/usr/bin/env python3
"""
Simple Elephant Detection GUI
A clean, easy-to-use interface for the ESP32 Elephant Detection System
"""

import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import threading
import time
import queue
from datetime import datetime
import json
import os

class SimpleElephantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🐘 Simple Elephant Detection System")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg='#2b2b2b')
        
        # Connection variables
        self.serial_connection = None
        self.connected = False
        self.data_queue = queue.Queue()
        self.running = True
        
        # Data storage
        self.current_features = {}
        self.current_classification = "not_elephant"
        self.current_confidence = 0.0
        self.feature_history = []
        
        # Detection display timer (5-second intervals)
        self.detection_timer_start = 0
        self.detection_timer_duration = 5.0  # 5 seconds
        self.last_detection_state = "no_elephant"
        self.detection_locked = False
        
        # GUI setup
        self.setup_ui()
        self.start_data_thread()
        
        # Auto-connect after GUI is ready
        self.root.after(2000, self.auto_connect)
    
    def setup_ui(self):
        """Create the user interface"""
        # Create main canvas with scrollbar
        canvas = tk.Canvas(self.root, bg='#2b2b2b', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#2b2b2b')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Main title
        title_frame = tk.Frame(scrollable_frame, bg='#2b2b2b')
        title_frame.pack(fill='x', padx=20, pady=10)
        
        title_label = tk.Label(title_frame, text="🐘 Elephant Detection System", 
                              font=('Arial', 24, 'bold'), fg='white', bg='#2b2b2b')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Real-time Audio Analysis & Classification", 
                                 font=('Arial', 12), fg='#cccccc', bg='#2b2b2b')
        subtitle_label.pack()
        
        # Connection panel
        self.setup_connection_panel(scrollable_frame)
        
        # Detection panel
        self.setup_detection_panel(scrollable_frame)
        
        # Features panel
        self.setup_features_panel(scrollable_frame)
        
        # Control panel
        self.setup_control_panel(scrollable_frame)
        
        # Status panel
        self.setup_status_panel(scrollable_frame)
    
    def setup_connection_panel(self, parent):
        """Setup connection controls"""
        conn_frame = tk.LabelFrame(parent, text="🔗 Connection", 
                                  font=('Arial', 12, 'bold'), fg='white', bg='#2b2b2b')
        conn_frame.pack(fill='x', padx=20, pady=10)
        
        # Connection status
        self.status_label = tk.Label(conn_frame, text="🔍 Searching for ESP32...", 
                                    font=('Arial', 14, 'bold'), fg='orange', bg='#2b2b2b')
        self.status_label.pack(pady=10)
        
        # Connection buttons
        btn_frame = tk.Frame(conn_frame, bg='#2b2b2b')
        btn_frame.pack(pady=10)
        
        self.connect_btn = tk.Button(btn_frame, text="🔄 Connect", command=self.connect_esp32,
                                    font=('Arial', 10, 'bold'), bg='#4CAF50', fg='white',
                                    padx=20, pady=5)
        self.connect_btn.pack(side='left', padx=5)
        
        self.disconnect_btn = tk.Button(btn_frame, text="❌ Disconnect", command=self.disconnect_esp32,
                                       font=('Arial', 10, 'bold'), bg='#f44336', fg='white',
                                       padx=20, pady=5, state='disabled')
        self.disconnect_btn.pack(side='left', padx=5)
    
    def setup_detection_panel(self, parent):
        """Setup detection display"""
        detect_frame = tk.LabelFrame(parent, text="🎯 Live Detection", 
                                    font=('Arial', 12, 'bold'), fg='white', bg='#2b2b2b')
        detect_frame.pack(fill='x', padx=20, pady=10)
        
        # Detection indicator
        self.detection_label = tk.Label(detect_frame, text="⏳ Initializing...", 
                                       font=('Arial', 20, 'bold'), fg='white', bg='#333333',
                                       height=3, relief='raised', bd=2)
        self.detection_label.pack(fill='x', padx=20, pady=20)
        
        # Classification details
        details_frame = tk.Frame(detect_frame, bg='#2b2b2b')
        details_frame.pack(fill='x', padx=20, pady=10)
        
        self.classification_label = tk.Label(details_frame, text="Classification: --", 
                                           font=('Arial', 12), fg='white', bg='#2b2b2b')
        self.classification_label.pack(side='left')
        
        self.confidence_label = tk.Label(details_frame, text="Confidence: --%", 
                                        font=('Arial', 12), fg='white', bg='#2b2b2b')
        self.confidence_label.pack(side='right')
        
        # Detection timer display
        timer_frame = tk.Frame(detect_frame, bg='#2b2b2b')
        timer_frame.pack(fill='x', padx=20, pady=5)
        
        self.timer_label = tk.Label(timer_frame, text="", 
                                   font=('Arial', 10), fg='#FFD700', bg='#2b2b2b')
        self.timer_label.pack()
    
    def setup_features_panel(self, parent):
        """Setup audio features display"""
        features_frame = tk.LabelFrame(parent, text="📊 Audio Features", 
                                      font=('Arial', 12, 'bold'), fg='white', bg='#2b2b2b')
        features_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create features grid
        self.feature_labels = {}
        feature_names = [
            ('rms', 'RMS Energy', '🔊'),
            ('infrasound_energy', 'Infrasound (5-35Hz)', '🌊'),
            ('low_band_energy', 'Low Band (35-80Hz)', '📊'),
            ('mid_band_energy', 'Mid Band (80-250Hz)', '📉'),
            ('spectral_centroid', 'Spectral Centroid', '📈'),
            ('dominant_freq', 'Dominant Frequency', '🎵'),
            ('temporal_envelope', 'Temporal Envelope', '⏱️'),
            ('spectral_flux', 'Spectral Flux', '🌀')
        ]
        
        for i, (key, name, icon) in enumerate(feature_names):
            row = i // 2
            col = i % 2
            
            feature_frame = tk.Frame(features_frame, bg='#333333', relief='raised', bd=1)
            feature_frame.grid(row=row, column=col, sticky='ew', padx=5, pady=5)
            
            # Feature name
            name_label = tk.Label(feature_frame, text=f"{icon} {name}", 
                                 font=('Arial', 10, 'bold'), fg='white', bg='#333333')
            name_label.pack(anchor='w', padx=10, pady=(5, 0))
            
            # Feature value
            value_label = tk.Label(feature_frame, text="--", 
                                  font=('Arial', 14, 'bold'), fg='#4CAF50', bg='#333333')
            value_label.pack(anchor='w', padx=10, pady=(0, 5))
            
            self.feature_labels[key] = value_label
        
        # Configure grid weights
        features_frame.grid_columnconfigure(0, weight=1)
        features_frame.grid_columnconfigure(1, weight=1)
    
    def setup_control_panel(self, parent):
        """Setup control buttons"""
        control_frame = tk.LabelFrame(parent, text="🎮 Controls", 
                                     font=('Arial', 12, 'bold'), fg='white', bg='#2b2b2b')
        control_frame.pack(fill='x', padx=20, pady=10)
        
        btn_frame = tk.Frame(control_frame, bg='#2b2b2b')
        btn_frame.pack(pady=10)
        
        # Labeling buttons
        self.elephant_btn = tk.Button(btn_frame, text="🐘 Label as Elephant", 
                                     command=lambda: self.send_label("elephant"),
                                     font=('Arial', 10, 'bold'), bg='#FF9800', fg='white',
                                     padx=15, pady=5, state='disabled')
        self.elephant_btn.pack(side='left', padx=5)
        
        self.not_elephant_btn = tk.Button(btn_frame, text="🚫 Label as Not Elephant", 
                                         command=lambda: self.send_label("not_elephant"),
                                         font=('Arial', 10, 'bold'), bg='#607D8B', fg='white',
                                         padx=15, pady=5, state='disabled')
        self.not_elephant_btn.pack(side='left', padx=5)
        
        # Data buttons
        self.save_btn = tk.Button(btn_frame, text="💾 Save Data", 
                                 command=self.save_data,
                                 font=('Arial', 10, 'bold'), bg='#4CAF50', fg='white',
                                 padx=15, pady=5, state='disabled')
        self.save_btn.pack(side='left', padx=5)
        
        self.clear_btn = tk.Button(btn_frame, text="🗑️ Clear Data", 
                                  command=self.clear_data,
                                  font=('Arial', 10, 'bold'), bg='#f44336', fg='white',
                                  padx=15, pady=5, state='disabled')
        self.clear_btn.pack(side='left', padx=5)
        
        # Test button for debugging
        self.test_btn = tk.Button(btn_frame, text="🧪 Test Detection", 
                                 command=self.test_elephant_detection,
                                 font=('Arial', 10, 'bold'), bg='#FF5722', fg='white',
                                 padx=15, pady=5)
        self.test_btn.pack(side='left', padx=5)
    
    def setup_status_panel(self, parent):
        """Setup status information"""
        status_frame = tk.Frame(parent, bg='#2b2b2b')
        status_frame.pack(fill='x', padx=20, pady=10)
        
        # Status text
        self.status_text = tk.Text(status_frame, height=6, font=('Consolas', 9), 
                                  bg='#1e1e1e', fg='#00ff00', wrap='word')
        status_scrollbar = tk.Scrollbar(status_frame, orient='vertical', command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=status_scrollbar.set)
        
        self.status_text.pack(side='left', fill='both', expand=True)
        status_scrollbar.pack(side='right', fill='y')
        
        # Add initial message
        self.log_message("🚀 Simple Elephant Detection System Ready")
        self.log_message("🔍 Searching for ESP32 device...")
    
    def log_message(self, message):
        """Add message to status log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.status_text.insert(tk.END, log_entry)
        self.status_text.see(tk.END)
        
        # Limit log size
        lines = self.status_text.get("1.0", tk.END).split('\n')
        if len(lines) > 100:
            self.status_text.delete("1.0", "50.0")
    
    def find_esp32_port(self):
        """Find ESP32 port automatically"""
        ports = list(serial.tools.list_ports.comports())
        
        # Look for ESP32 by description
        for port in ports:
            desc = port.description.upper()
            if any(keyword in desc for keyword in ['CP210', 'CH340', 'CH341', 'FTDI', 'USB-SERIAL', 'SILICON LABS', 'ESP32']):
                return port.device
        
        return None
    
    def auto_connect(self):
        """Automatically connect to ESP32"""
        if self.connected:
            return
        
        self.log_message("🔍 Auto-detecting ESP32...")
        port = self.find_esp32_port()
        
        if port:
            self.log_message(f"✅ Found ESP32 on {port}")
            self.connect_to_port(port)
        else:
            self.log_message("❌ No ESP32 found. Click 'Connect' to try manually.")
            self.status_label.config(text="❌ ESP32 not found", fg='red')
    
    def connect_esp32(self):
        """Connect to ESP32 manually"""
        port = self.find_esp32_port()
        if port:
            self.connect_to_port(port)
        else:
            messagebox.showerror("Error", "No ESP32 device found!\n\nMake sure:\n- ESP32 is connected via USB\n- Drivers are installed\n- Device is powered on")
    
    def connect_to_port(self, port):
        """Connect to specific port"""
        try:
            self.log_message(f"🔌 Connecting to {port}...")
            self.serial_connection = serial.Serial(port, 115200, timeout=1)
            time.sleep(2)  # Wait for ESP32 to initialize
            
            self.connected = True
            self.status_label.config(text=f"✅ Connected: {port}", fg='green')
            
            # Enable/disable buttons
            self.connect_btn.config(state='disabled')
            self.disconnect_btn.config(state='normal')
            self.elephant_btn.config(state='normal')
            self.not_elephant_btn.config(state='normal')
            self.save_btn.config(state='normal')
            self.clear_btn.config(state='normal')
            
            self.log_message("🎉 Connected successfully!")
            
            # Start data reading thread
            self.data_thread = threading.Thread(target=self.read_serial_data, daemon=True)
            self.data_thread.start()
            
        except Exception as e:
            self.log_message(f"❌ Connection failed: {str(e)}")
            self.status_label.config(text="❌ Connection failed", fg='red')
    
    def disconnect_esp32(self):
        """Disconnect from ESP32"""
        try:
            if self.serial_connection and self.serial_connection.is_open:
                self.serial_connection.close()
            
            self.connected = False
            self.status_label.config(text="❌ Disconnected", fg='red')
            
            # Enable/disable buttons
            self.connect_btn.config(state='normal')
            self.disconnect_btn.config(state='disabled')
            self.elephant_btn.config(state='disabled')
            self.not_elephant_btn.config(state='disabled')
            self.save_btn.config(state='disabled')
            self.clear_btn.config(state='disabled')
            
            self.log_message("🔌 Disconnected from ESP32")
            
        except Exception as e:
            self.log_message(f"❌ Disconnect error: {str(e)}")
    
    def read_serial_data(self):
        """Read data from ESP32 in background thread"""
        while self.connected and self.serial_connection and self.serial_connection.is_open:
            try:
                if self.serial_connection.in_waiting > 0:
                    line = self.serial_connection.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        self.data_queue.put(line)
                time.sleep(0.01)
            except Exception as e:
                if self.connected:
                    self.log_message(f"❌ Serial read error: {str(e)}")
                break
    
    def process_data_queue(self):
        """Process queued data from ESP32"""
        try:
            while not self.data_queue.empty():
                line = self.data_queue.get_nowait()
                self.process_serial_line(line)
        except queue.Empty:
            pass
        
        # Schedule next processing
        if self.running:
            self.root.after(50, self.process_data_queue)
            # Also update detection display for timer countdown
            if self.detection_locked:
                self.update_detection_display()
    
    def process_serial_line(self, line):
        """Process a line of data from ESP32"""
        try:
            if line.startswith("FEATURES:"):
                self.parse_features(line)
            elif line.startswith("CLASSIFICATION:"):
                self.parse_classification(line)
            elif line.startswith("STATUS:"):
                self.parse_status(line)
            elif line.startswith("ERROR:"):
                self.log_message(f"❌ ESP32 Error: {line[6:]}")
            elif line.startswith("OK:"):
                self.log_message(f"✅ ESP32: {line[3:]}")
            else:
                # Log other messages
                if len(line) > 0 and not line.startswith("ESP32"):
                    self.log_message(f"📡 ESP32: {line}")
        except Exception as e:
            self.log_message(f"❌ Data processing error: {str(e)}")
    
    def parse_features(self, line):
        """Parse features data"""
        try:
            parts = line[9:].split(",")  # Remove "FEATURES:" prefix
            if len(parts) >= 8:
                self.current_features = {
                    'rms': float(parts[0]),
                    'infrasound_energy': float(parts[1]),
                    'low_band_energy': float(parts[2]),
                    'mid_band_energy': float(parts[3]),
                    'spectral_centroid': float(parts[4]),
                    'dominant_freq': float(parts[5]),
                    'spectral_flux': float(parts[6]),
                    'temporal_envelope': float(parts[7])
                }
                self.update_features_display()
        except Exception as e:
            self.log_message(f"❌ Feature parsing error: {str(e)}")
    
    def parse_classification(self, line):
        """Parse classification data"""
        try:
            parts = line[15:].split(",")  # Remove "CLASSIFICATION:" prefix (15 chars)
            self.log_message(f"🔍 DEBUG: Classification line: '{line}', Parts: {parts}")
            
            if len(parts) >= 2:  # Changed from >= 3 to >= 2
                self.current_classification = parts[0].strip()
                self.current_confidence = float(parts[1].strip())
                self.log_message(f"📊 Classification: {self.current_classification}, Confidence: {self.current_confidence}")
                self.update_detection_display()
            else:
                self.log_message(f"⚠️ Invalid classification format: {line}")
        except Exception as e:
            self.log_message(f"❌ Classification parsing error: {str(e)} for line: {line}")
    
    def parse_status(self, line):
        """Parse status data"""
        try:
            parts = line[7:].split(",")  # Remove "STATUS:" prefix
            if len(parts) >= 3:
                sample_count = parts[0]
                uptime_ms = int(parts[1])
                free_memory = parts[2]
                
                uptime_sec = uptime_ms // 1000
                uptime_str = f"{uptime_sec // 60}:{uptime_sec % 60:02d}"
                
                self.log_message(f"📊 Status: {sample_count} samples, {uptime_str} uptime, {free_memory} bytes free")
        except Exception as e:
            self.log_message(f"❌ Status parsing error: {str(e)}")
    
    def update_features_display(self):
        """Update the features display"""
        for key, label in self.feature_labels.items():
            if key in self.current_features:
                value = self.current_features[key]
                if key in ['spectral_centroid', 'dominant_freq']:
                    label.config(text=f"{value:.1f} Hz")
                else:
                    label.config(text=f"{value:.4f}")
    
    def update_detection_display(self):
        """Update the detection display with 5-second persistence"""
        current_time = time.time()
        
        # Determine current detection state
        if self.current_classification == "elephant":
            if self.current_confidence > 0.5:  # Lowered threshold for better detection
                new_detection_state = "elephant_high"
            elif self.current_confidence > 0.3:
                new_detection_state = "elephant_medium"
            else:
                new_detection_state = "elephant_low"
        else:
            new_detection_state = "no_elephant"
        
        # Check if we need to start a new 5-second detection period
        if new_detection_state != "no_elephant" and (not self.detection_locked or 
            new_detection_state != self.last_detection_state):
            # Start new 5-second detection period
            self.detection_timer_start = current_time
            self.detection_locked = True
            self.last_detection_state = new_detection_state
            
            if new_detection_state == "elephant_high":
                self.detection_label.config(text="🐘 ELEPHANT DETECTED! 🚨", 
                                          bg='#f44336', fg='white')
                self.root.bell()  # Sound alert
            elif new_detection_state == "elephant_medium":
                self.detection_label.config(text="🐘 Possible Elephant", 
                                          bg='#FF9800', fg='white')
            else:
                self.detection_label.config(text="🤔 Elephant (Low Confidence)", 
                                          bg='#607D8B', fg='white')
        
        # Check if 5-second period has elapsed
        elif self.detection_locked:
            elapsed = current_time - self.detection_timer_start
            if elapsed >= self.detection_timer_duration:
                # 5-second period finished, check current state
                self.detection_locked = False
                if new_detection_state == "no_elephant":
                    self.detection_label.config(text="✅ No Elephant", 
                                              bg='#4CAF50', fg='white')
                    self.last_detection_state = "no_elephant"
                else:
                    # Continue with current detection if still active
                    self.detection_timer_start = current_time
                    self.detection_locked = True
                    self.last_detection_state = new_detection_state
        
        # If no detection lock, show current state immediately
        elif not self.detection_locked and new_detection_state == "no_elephant":
            self.detection_label.config(text="✅ No Elephant", 
                                      bg='#4CAF50', fg='white')
            self.last_detection_state = "no_elephant"
        
        # Update classification labels
        self.classification_label.config(text=f"Classification: {self.current_classification}")
        self.confidence_label.config(text=f"Confidence: {self.current_confidence*100:.1f}%")
        
        # Update timer display
        if self.detection_locked and self.last_detection_state != "no_elephant":
            remaining = max(0, self.detection_timer_duration - (current_time - self.detection_timer_start))
            self.timer_label.config(text=f"Detection active: {remaining:.1f}s remaining")
        else:
            self.timer_label.config(text="")
    
    def send_label(self, label):
        """Send label to ESP32"""
        if self.connected:
            try:
                self.serial_connection.write(f"LABEL:{label}\n".encode())
                self.log_message(f"📝 Labeled as: {label}")
            except Exception as e:
                self.log_message(f"❌ Label send error: {str(e)}")
    
    def save_data(self):
        """Save data on ESP32"""
        if self.connected:
            try:
                self.serial_connection.write(b"SAVE_DATA\n")
                self.log_message("💾 Saving data...")
            except Exception as e:
                self.log_message(f"❌ Save error: {str(e)}")
    
    def clear_data(self):
        """Clear data on ESP32"""
        if messagebox.askyesno("Confirm", "Clear all training data?"):
            if self.connected:
                try:
                    self.serial_connection.write(b"CLEAR_DATA\n")
                    self.log_message("🗑️ Clearing data...")
                except Exception as e:
                    self.log_message(f"❌ Clear error: {str(e)}")
    
    def start_data_thread(self):
        """Start data processing thread"""
        self.process_data_queue()
    
    def test_elephant_detection(self):
        """Test elephant detection visual by simulating ESP32 data"""
        self.log_message("🧪 Testing elephant detection visual...")
        
        # Simulate receiving classification data from ESP32
        test_line = "CLASSIFICATION:elephant,0.85,high_confidence"
        self.log_message(f"📡 Simulating ESP32 data: {test_line}")
        self.parse_classification(test_line)
        
        # Also test some features
        feature_line = "FEATURES:0.05,0.8,0.12,0.08,85.2,95.1,0.15,0.22"
        self.log_message(f"📡 Simulating features: {feature_line}")
        self.parse_features(feature_line)
    
    def on_closing(self):
        """Handle window closing"""
        self.running = False
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = SimpleElephantGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
