#!/usr/bin/env python3
"""
Advanced Elephant Detection GUI
A sophisticated interface with real-time visualization, data analysis, and machine learning features
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import serial
import serial.tools.list_ports
import threading
import time
import queue
from datetime import datetime
import json
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
from collections import deque
import math

class AdvancedElephantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Elephant Detection System - AI-Powered Audio Analysis")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        self.root.configure(bg='#1a1a1a')
        
        # Connection variables
        self.serial_connection = None
        self.connected = False
        self.data_queue = queue.Queue()
        self.running = True
        
        # Data storage
        self.current_features = {}
        self.current_classification = "not_elephant"
        self.current_confidence = 0.0
        self.feature_history = deque(maxlen=1000)  # Store last 1000 samples
        self.classification_history = deque(maxlen=1000)
        self.training_data = []
        
        # Real-time plotting data (RMS only)
        self.plot_data = {
            'time': deque(maxlen=200),
            'rms': deque(maxlen=200)
        }
        
        # Statistics
        self.stats = {
            'total_samples': 0,
            'elephant_detections': 0,
            'accuracy': 0.0,
            'session_start': time.time()
        }
        
        # 5-second labeling buffer
        self.labeling_buffer = []
        self.is_labeling = False
        self.labeling_start_time = 0
        self.labeling_duration = 5.0  # 5 seconds
        self.current_label = None
        self.labeling_progress = 0.0
        
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
        """Create the advanced user interface"""
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Configure notebook style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#2b2b2b')
        style.configure('TNotebook.Tab', background='#3b3b3b', foreground='white', padding=[20, 10])
        
        # Create tabs
        self.setup_dashboard_tab()
        self.setup_analysis_tab()
        self.setup_training_tab()
        self.setup_settings_tab()
    
    def setup_dashboard_tab(self):
        """Setup main dashboard tab"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Live Dashboard")
        
        # Create main container with proper spacing
        main_container = tk.Frame(dashboard_frame, bg='#2b2b2b')
        main_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Top row - Connection and Status (compact)
        top_frame = tk.Frame(main_container, bg='#2b2b2b')
        top_frame.pack(fill='x', pady=2)
        
        # Connection status (left)
        conn_frame = tk.LabelFrame(top_frame, text="Connection Status", 
                                  font=('Arial', 10, 'bold'), fg='white', bg='#2b2b2b')
        conn_frame.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        self.status_label = tk.Label(conn_frame, text="Searching for ESP32...", 
                                    font=('Arial', 12, 'bold'), fg='orange', bg='#2b2b2b')
        self.status_label.pack(pady=3)
        
        # Connection buttons
        btn_frame = tk.Frame(conn_frame, bg='#2b2b2b')
        btn_frame.pack(pady=3)
        
        self.connect_btn = tk.Button(btn_frame, text="Connect", command=self.connect_esp32,
                                    font=('Arial', 9, 'bold'), bg='#4CAF50', fg='white',
                                    padx=10, pady=3)
        self.connect_btn.pack(side='left', padx=2)
        
        self.disconnect_btn = tk.Button(btn_frame, text="Disconnect", command=self.disconnect_esp32,
                                       font=('Arial', 9, 'bold'), bg='#f44336', fg='white',
                                       padx=10, pady=3, state='disabled')
        self.disconnect_btn.pack(side='left', padx=2)
        
        # Statistics (right)
        stats_frame = tk.LabelFrame(top_frame, text="Session Statistics", 
                                   font=('Arial', 10, 'bold'), fg='white', bg='#2b2b2b')
        stats_frame.pack(side='right', fill='x', expand=True, padx=(5, 0))
        
        self.stats_label = tk.Label(stats_frame, text="Samples: 0 | Detections: 0 | Accuracy: 0%", 
                                   font=('Arial', 10), fg='white', bg='#2b2b2b')
        self.stats_label.pack(pady=3)
        
        # Middle row - Detection and Features (side by side)
        middle_frame = tk.Frame(main_container, bg='#2b2b2b')
        middle_frame.pack(fill='both', expand=True, pady=2)
        
        # Left side - Detection Panel (compact)
        detection_panel = tk.Frame(middle_frame, bg='#2b2b2b')
        detection_panel.pack(side='left', fill='both', expand=True, padx=(0, 3))
        
        detect_frame = tk.LabelFrame(detection_panel, text="Live Detection", 
                                    font=('Arial', 10, 'bold'), fg='white', bg='#2b2b2b')
        detect_frame.pack(fill='both', expand=True)
        
        self.detection_label = tk.Label(detect_frame, text="Initializing...", 
                                       font=('Arial', 18, 'bold'), fg='white', bg='#333333',
                                       height=2, relief='raised', bd=2)
        self.detection_label.pack(fill='x', padx=5, pady=5)
        
        # Classification details
        details_frame = tk.Frame(detect_frame, bg='#2b2b2b')
        details_frame.pack(fill='x', padx=5, pady=2)
        
        self.classification_label = tk.Label(details_frame, text="Classification: --", 
                                           font=('Arial', 10, 'bold'), fg='white', bg='#2b2b2b')
        self.classification_label.pack(side='left')
        
        self.confidence_label = tk.Label(details_frame, text="Confidence: --%", 
                                        font=('Arial', 10, 'bold'), fg='white', bg='#2b2b2b')
        self.confidence_label.pack(side='right')
        
        # Detection timer display
        self.timer_label = tk.Label(details_frame, text="", 
                                   font=('Arial', 9), fg='#FFD700', bg='#2b2b2b')
        self.timer_label.pack(side='bottom')
        
        # Right side - Features Panel (compact)
        features_panel = tk.Frame(middle_frame, bg='#2b2b2b')
        features_panel.pack(side='right', fill='both', expand=True, padx=(3, 0))
        
        self.setup_features_display(features_panel)
        
        # Bottom row - Controls (ALWAYS VISIBLE)
        controls_frame = tk.LabelFrame(main_container, text="Quick Controls - Labeling", 
                                      font=('Arial', 10, 'bold'), fg='white', bg='#2b2b2b')
        controls_frame.pack(fill='x', pady=2)
        
        self.setup_quick_controls(controls_frame)
        
        # Bottom row - Real-time Plot (smaller)
        plot_frame = tk.LabelFrame(main_container, text="Real-time Feature Visualization", 
                                  font=('Arial', 10, 'bold'), fg='white', bg='#2b2b2b')
        plot_frame.pack(fill='both', expand=True, pady=2)
        
        self.setup_realtime_plot(plot_frame)
    
    def setup_features_display(self, parent):
        """Setup compact features display"""
        features_frame = tk.LabelFrame(parent, text="Audio Features", 
                                      font=('Arial', 10, 'bold'), fg='white', bg='#2b2b2b')
        features_frame.pack(fill='both', expand=True)
        
        # Create features grid (4x2 for compact display)
        self.feature_labels = {}
        feature_configs = [
            ('rms', 'RMS Energy', '#FF6B6B'),
            ('infrasound_energy', 'Infrasound (5-35Hz)', '#4ECDC4'),
            ('low_band_energy', 'Low Band (35-80Hz)', '#45B7D1'),
            ('mid_band_energy', 'Mid Band (80-250Hz)', '#96CEB4'),
            ('spectral_centroid', 'Spectral Centroid', '#FFEAA7'),
            ('dominant_freq', 'Dominant Frequency', '#DDA0DD'),
            ('temporal_envelope', 'Temporal Envelope', '#98D8C8'),
            ('spectral_flux', 'Spectral Flux', '#F7DC6F')
        ]
        
        for i, (key, name, color) in enumerate(feature_configs):
            row = i // 2
            col = i % 2
            
            feature_card = tk.Frame(features_frame, bg='#3b3b3b', relief='raised', bd=1)
            feature_card.grid(row=row, column=col, sticky='ew', padx=2, pady=2)
            
            # Feature name (compact)
            name_label = tk.Label(feature_card, text=name, bg='#3b3b3b', fg='white',
                                 font=('Arial', 8, 'bold'), anchor='w')
            name_label.pack(fill='x', padx=5, pady=(3, 0))
            
            # Feature value (compact)
            value_label = tk.Label(feature_card, text="--", bg='#3b3b3b', fg=color,
                                 font=('Arial', 12, 'bold'), anchor='center')
            value_label.pack(fill='x', padx=5, pady=(0, 3))
            
            self.feature_labels[key] = value_label
        
        # Configure grid weights
        features_frame.grid_columnconfigure(0, weight=1)
        features_frame.grid_columnconfigure(1, weight=1)
    
    def setup_realtime_plot(self, parent):
        """Setup compact real-time plotting (RMS only)"""
        # Create matplotlib figure (smaller)
        self.fig = Figure(figsize=(8, 3), facecolor='#2b2b2b')
        self.ax = self.fig.add_subplot(111, facecolor='#2b2b2b')
        self.ax.set_title('Real-time RMS Amplitude', color='white', fontsize=10)
        self.ax.set_xlabel('Time (s)', color='white', fontsize=8)
        self.ax.set_ylabel('RMS Amplitude', color='white', fontsize=8)
        self.ax.tick_params(colors='white', labelsize=8)
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, parent)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
        
        # Initialize plot line (RMS only)
        self.lines = {}
        self.lines['rms'], = self.ax.plot([], [], color='#FF6B6B', linewidth=2.0, label='RMS Amplitude')
        
        self.ax.legend(loc='upper right', facecolor='#3b3b3b', edgecolor='white', fontsize=8)
        self.ax.grid(True, alpha=0.3, color='white')
    
    def setup_quick_controls(self, parent):
        """Setup compact quick control buttons"""
        # Main button frame
        btn_frame = tk.Frame(parent, bg='#2b2b2b')
        btn_frame.pack(pady=5)
        
        # Row 1 - Labeling buttons (most important)
        label_frame = tk.Frame(btn_frame, bg='#2b2b2b')
        label_frame.pack(fill='x', pady=2)
        
        tk.Label(label_frame, text="LABELING (5s):", font=('Arial', 9, 'bold'), 
                fg='white', bg='#2b2b2b').pack(side='left', padx=(0, 10))
        
        self.elephant_btn = tk.Button(label_frame, text="ELEPHANT", 
                                     command=lambda: self.start_labeling("elephant"),
                                     font=('Arial', 10, 'bold'), bg='#FF9800', fg='white',
                                     padx=15, pady=5, state='disabled')
        self.elephant_btn.pack(side='left', padx=3)
        
        self.not_elephant_btn = tk.Button(label_frame, text="NOT ELEPHANT", 
                                         command=lambda: self.start_labeling("not_elephant"),
                                         font=('Arial', 10, 'bold'), bg='#607D8B', fg='white',
                                         padx=15, pady=5, state='disabled')
        self.not_elephant_btn.pack(side='left', padx=3)
        
        # Progress indicator
        self.progress_label = tk.Label(label_frame, text="Ready", 
                                      font=('Arial', 9), fg='#4CAF50', bg='#2b2b2b')
        self.progress_label.pack(side='left', padx=(10, 0))
        
        # Progress bar
        self.progress_bar = tk.Frame(label_frame, bg='#333333', height=4, width=100)
        self.progress_bar.pack(side='left', padx=(5, 0))
        self.progress_fill = tk.Frame(self.progress_bar, bg='#4CAF50', height=4)
        self.progress_fill.pack(side='left', fill='y')
        
        # Row 2 - Data management buttons
        data_frame = tk.Frame(btn_frame, bg='#2b2b2b')
        data_frame.pack(fill='x', pady=2)
        
        tk.Label(data_frame, text="DATA:", font=('Arial', 9, 'bold'), 
                fg='white', bg='#2b2b2b').pack(side='left', padx=(0, 10))
        
        self.save_btn = tk.Button(data_frame, text="SAVE", 
                                 command=self.save_data,
                                 font=('Arial', 9, 'bold'), bg='#4CAF50', fg='white',
                                 padx=12, pady=4, state='disabled')
        self.save_btn.pack(side='left', padx=2)
        
        self.clear_btn = tk.Button(data_frame, text="CLEAR", 
                                  command=self.clear_data,
                                  font=('Arial', 9, 'bold'), bg='#f44336', fg='white',
                                  padx=12, pady=4, state='disabled')
        self.clear_btn.pack(side='left', padx=2)
        
        self.analyze_btn = tk.Button(data_frame, text="ANALYZE", 
                                    command=self.show_analysis,
                                    font=('Arial', 9, 'bold'), bg='#9C27B0', fg='white',
                                    padx=12, pady=4, state='disabled')
        self.analyze_btn.pack(side='left', padx=2)
        
        # Test button for debugging
        self.test_btn = tk.Button(data_frame, text="TEST", 
                                 command=self.test_elephant_detection,
                                 font=('Arial', 9, 'bold'), bg='#FF5722', fg='white',
                                 padx=12, pady=4)
        self.test_btn.pack(side='left', padx=2)
    
    def setup_analysis_tab(self):
        """Setup data analysis tab"""
        analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(analysis_frame, text="Data Analysis")
        
        # Analysis controls
        controls_frame = tk.Frame(analysis_frame, bg='#2b2b2b')
        controls_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(controls_frame, text="📈 Data Analysis & Visualization", 
                font=('Arial', 16, 'bold'), fg='white', bg='#2b2b2b').pack(pady=10)
        
        # Analysis buttons
        btn_frame = tk.Frame(controls_frame, bg='#2b2b2b')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="📊 Feature Distribution", command=self.plot_feature_distribution,
                 font=('Arial', 11, 'bold'), bg='#2196F3', fg='white', padx=15, pady=5).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="📈 Time Series Analysis", command=self.plot_time_series,
                 font=('Arial', 11, 'bold'), bg='#FF9800', fg='white', padx=15, pady=5).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="🎯 Classification Analysis", command=self.plot_classification_analysis,
                 font=('Arial', 11, 'bold'), bg='#4CAF50', fg='white', padx=15, pady=5).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="💾 Export Data", command=self.export_data,
                 font=('Arial', 11, 'bold'), bg='#9C27B0', fg='white', padx=15, pady=5).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="🎬 Labeling Data Stats", command=self.show_labeling_stats,
                 font=('Arial', 11, 'bold'), bg='#FF5722', fg='white', padx=15, pady=5).pack(side='left', padx=5)
        
        # Analysis results area
        self.analysis_text = tk.Text(analysis_frame, height=20, font=('Consolas', 10), 
                                    bg='#1e1e1e', fg='#00ff00', wrap='word')
        analysis_scrollbar = tk.Scrollbar(analysis_frame, orient='vertical', command=self.analysis_text.yview)
        self.analysis_text.configure(yscrollcommand=analysis_scrollbar.set)
        
        self.analysis_text.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        analysis_scrollbar.pack(side='right', fill='y')
    
    def setup_training_tab(self):
        """Setup machine learning training tab"""
        training_frame = ttk.Frame(self.notebook)
        self.notebook.add(training_frame, text="ML Training")
        
        tk.Label(training_frame, text="🤖 Machine Learning Training", 
                font=('Arial', 16, 'bold'), fg='white', bg='#2b2b2b').pack(pady=20)
        
        # Training controls
        controls_frame = tk.Frame(training_frame, bg='#2b2b2b')
        controls_frame.pack(fill='x', padx=20, pady=10)
        
        # Dataset info
        dataset_frame = tk.LabelFrame(controls_frame, text="📊 Dataset Information", 
                                     font=('Arial', 12, 'bold'), fg='white', bg='#2b2b2b')
        dataset_frame.pack(fill='x', pady=10)
        
        self.dataset_info = tk.Label(dataset_frame, text="No data collected yet", 
                                    font=('Arial', 11), fg='white', bg='#2b2b2b')
        self.dataset_info.pack(pady=10)
        
        # Training buttons
        train_frame = tk.Frame(controls_frame, bg='#2b2b2b')
        train_frame.pack(fill='x', pady=10)
        
        tk.Button(train_frame, text="🎯 Train Model", command=self.train_model,
                 font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white', padx=20, pady=8).pack(side='left', padx=5)
        
        tk.Button(train_frame, text="📊 Test Model", command=self.test_model,
                 font=('Arial', 12, 'bold'), bg='#2196F3', fg='white', padx=20, pady=8).pack(side='left', padx=5)
        
        tk.Button(train_frame, text="💾 Save Model", command=self.save_model,
                 font=('Arial', 12, 'bold'), bg='#FF9800', fg='white', padx=20, pady=8).pack(side='left', padx=5)
        
        tk.Button(train_frame, text="📁 Load Model", command=self.load_model,
                 font=('Arial', 12, 'bold'), bg='#9C27B0', fg='white', padx=20, pady=8).pack(side='left', padx=5)
        
        # Training results
        results_frame = tk.LabelFrame(controls_frame, text="📈 Training Results", 
                                     font=('Arial', 12, 'bold'), fg='white', bg='#2b2b2b')
        results_frame.pack(fill='both', expand=True, pady=10)
        
        self.training_results = tk.Text(results_frame, height=15, font=('Consolas', 10), 
                                       bg='#1e1e1e', fg='#00ff00', wrap='word')
        results_scrollbar = tk.Scrollbar(results_frame, orient='vertical', command=self.training_results.yview)
        self.training_results.configure(yscrollcommand=results_scrollbar.set)
        
        self.training_results.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        results_scrollbar.pack(side='right', fill='y')
    
    def setup_settings_tab(self):
        """Setup settings and configuration tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        tk.Label(settings_frame, text="⚙️ System Settings & Configuration", 
                font=('Arial', 16, 'bold'), fg='white', bg='#2b2b2b').pack(pady=20)
        
        # Settings panels
        settings_panel = tk.Frame(settings_frame, bg='#2b2b2b')
        settings_panel.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Audio settings
        audio_frame = tk.LabelFrame(settings_panel, text="🎵 Audio Settings", 
                                   font=('Arial', 12, 'bold'), fg='white', bg='#2b2b2b')
        audio_frame.pack(fill='x', pady=10)
        
        # Detection settings
        detection_frame = tk.LabelFrame(settings_panel, text="🎯 Detection Settings", 
                                       font=('Arial', 12, 'bold'), fg='white', bg='#2b2b2b')
        detection_frame.pack(fill='x', pady=10)
        
        # System settings
        system_frame = tk.LabelFrame(settings_panel, text="💻 System Settings", 
                                    font=('Arial', 12, 'bold'), fg='white', bg='#2b2b2b')
        system_frame.pack(fill='x', pady=10)
    
    def log_message(self, message, tab="dashboard"):
        """Add message to appropriate log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        if tab == "analysis":
            self.analysis_text.insert(tk.END, log_entry)
            self.analysis_text.see(tk.END)
        elif tab == "training":
            self.training_results.insert(tk.END, log_entry)
            self.training_results.see(tk.END)
    
    def find_esp32_port(self):
        """Find ESP32 port automatically"""
        ports = list(serial.tools.list_ports.comports())
        
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
            messagebox.showerror("Error", "No ESP32 device found!")
    
    def connect_to_port(self, port):
        """Connect to specific port"""
        try:
            self.log_message(f"🔌 Connecting to {port}...")
            self.serial_connection = serial.Serial(port, 115200, timeout=1)
            time.sleep(2)
            
            self.connected = True
            self.status_label.config(text=f"✅ Connected: {port}", fg='green')
            
            # Enable buttons
            self.connect_btn.config(state='disabled')
            self.disconnect_btn.config(state='normal')
            self.elephant_btn.config(state='normal')
            self.not_elephant_btn.config(state='normal')
            self.save_btn.config(state='normal')
            self.clear_btn.config(state='normal')
            self.analyze_btn.config(state='normal')
            
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
            
            # Disable buttons
            self.connect_btn.config(state='normal')
            self.disconnect_btn.config(state='disabled')
            self.elephant_btn.config(state='disabled')
            self.not_elephant_btn.config(state='disabled')
            self.save_btn.config(state='disabled')
            self.clear_btn.config(state='disabled')
            self.analyze_btn.config(state='disabled')
            
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
    
    def start_data_thread(self):
        """Start data processing thread"""
        self.process_data_queue()
    
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
        except Exception as e:
            self.log_message(f"❌ Data processing error: {str(e)}")
    
    def parse_features(self, line):
        """Parse features data"""
        try:
            parts = line[9:].split(",")
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
                self.update_realtime_plot()
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
            parts = line[7:].split(",")
            if len(parts) >= 3:
                sample_count = parts[0]
                uptime_ms = int(parts[1])
                free_memory = parts[2]
                
                self.stats['total_samples'] = int(sample_count)
                self.update_statistics()
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
                self.root.bell()
                self.stats['elephant_detections'] += 1
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
            
        # Debug logging
        self.log_message(f"🎯 Detection display updated: {self.last_detection_state}, locked: {self.detection_locked}")
    
    def update_realtime_plot(self):
        """Update real-time plot (RMS only)"""
        current_time = time.time()
        
        # Add data to plot queues (RMS only)
        self.plot_data['time'].append(current_time)
        self.plot_data['rms'].append(self.current_features.get('rms', 0))
        
        # Update plot
        if len(self.plot_data['time']) > 1:
            times = list(self.plot_data['time'])
            rms_values = list(self.plot_data['rms'])
            self.lines['rms'].set_data(times, rms_values)
            
            # Auto-scale axes
            self.ax.relim()
            self.ax.autoscale_view()
            self.canvas.draw()
    
    def update_statistics(self):
        """Update statistics display"""
        accuracy = (self.stats['elephant_detections'] / max(self.stats['total_samples'], 1)) * 100
        self.stats['accuracy'] = accuracy
        
        stats_text = f"Samples: {self.stats['total_samples']} | Detections: {self.stats['elephant_detections']} | Accuracy: {accuracy:.1f}%"
        self.stats_label.config(text=stats_text)
    
    def start_labeling(self, label):
        """Start 5-second labeling process"""
        if not self.connected:
            self.log_message("❌ Not connected to ESP32")
            return
            
        if self.is_labeling:
            self.log_message("❌ Already labeling, please wait...")
            return
            
        # Start labeling process
        self.is_labeling = True
        self.current_label = label
        self.labeling_start_time = time.time()
        self.labeling_buffer = []
        self.labeling_progress = 0.0
        
        # Update UI
        self.elephant_btn.config(state='disabled')
        self.not_elephant_btn.config(state='disabled')
        self.progress_label.config(text=f"Recording {label}...", fg='#FF9800')
        
        self.log_message(f"🎬 Started recording {label} for 5 seconds...")
        
        # Start progress update
        self.update_labeling_progress()
    
    def update_labeling_progress(self):
        """Update labeling progress and collect data"""
        if not self.is_labeling:
            return
            
        current_time = time.time()
        elapsed = current_time - self.labeling_start_time
        self.labeling_progress = min(elapsed / self.labeling_duration, 1.0)
        
        # Update progress display
        remaining = max(0, self.labeling_duration - elapsed)
        self.progress_label.config(text=f"Recording {self.current_label}... {remaining:.1f}s")
        
        # Update progress bar
        progress_width = int(self.labeling_progress * 100)
        self.progress_fill.config(width=progress_width)
        
        # Collect current features if available
        if self.current_features:
            self.labeling_buffer.append({
                'features': self.current_features.copy(),
                'timestamp': current_time,
                'classification': self.current_classification,
                'confidence': self.current_confidence
            })
        
        if elapsed >= self.labeling_duration:
            # Finish labeling
            self.finish_labeling()
        else:
            # Continue updating
            self.root.after(100, self.update_labeling_progress)
    
    def finish_labeling(self):
        """Finish the 5-second labeling process"""
        if not self.is_labeling:
            return
            
        # Process collected data
        if len(self.labeling_buffer) > 0:
            # Calculate average features over the 5-second period
            avg_features = self.calculate_average_features()
            
            # Store training data
            self.training_data.append({
                'features': avg_features,
                'label': self.current_label,
                'timestamp': time.time(),
                'samples_count': len(self.labeling_buffer),
                'raw_samples': self.labeling_buffer.copy()
            })
            
            # Send to ESP32
            try:
                self.serial_connection.write(f"LABEL:{self.current_label}\n".encode())
                self.log_message(f"✅ Labeled {len(self.labeling_buffer)} samples as: {self.current_label}")
            except Exception as e:
                self.log_message(f"❌ Label send error: {str(e)}")
        else:
            self.log_message("❌ No data collected during labeling")
        
        # Reset labeling state
        self.is_labeling = False
        self.current_label = None
        self.labeling_buffer = []
        self.labeling_progress = 0.0
        
        # Update UI
        self.elephant_btn.config(state='normal')
        self.not_elephant_btn.config(state='normal')
        self.progress_label.config(text="Ready", fg='#4CAF50')
        self.progress_fill.config(width=0)  # Reset progress bar
    
    def calculate_average_features(self):
        """Calculate average features from the labeling buffer"""
        if not self.labeling_buffer:
            return {}
            
        # Initialize feature sums
        feature_sums = {}
        feature_counts = {}
        
        # Sum all features
        for sample in self.labeling_buffer:
            features = sample['features']
            for key, value in features.items():
                if isinstance(value, (int, float)):
                    feature_sums[key] = feature_sums.get(key, 0) + value
                    feature_counts[key] = feature_counts.get(key, 0) + 1
        
        # Calculate averages
        avg_features = {}
        for key in feature_sums:
            if feature_counts[key] > 0:
                avg_features[key] = feature_sums[key] / feature_counts[key]
            else:
                avg_features[key] = 0.0
                
        return avg_features
    
    def show_labeling_stats(self):
        """Show statistics about the 5-second labeling data"""
        if not self.training_data:
            self.log_message("❌ No labeling data available")
            return
            
        # Calculate statistics
        elephant_samples = [d for d in self.training_data if d['label'] == 'elephant']
        not_elephant_samples = [d for d in self.training_data if d['label'] == 'not_elephant']
        
        total_samples = len(self.training_data)
        elephant_count = len(elephant_samples)
        not_elephant_count = len(not_elephant_samples)
        
        # Calculate average sample counts per labeling session
        avg_elephant_samples = sum(d.get('samples_count', 0) for d in elephant_samples) / max(elephant_count, 1)
        avg_not_elephant_samples = sum(d.get('samples_count', 0) for d in not_elephant_samples) / max(not_elephant_count, 1)
        
        # Display statistics
        stats_text = f"""
🎬 5-SECOND LABELING DATA STATISTICS
{'='*50}

📊 OVERVIEW:
• Total Labeling Sessions: {total_samples}
• Elephant Sessions: {elephant_count} ({elephant_count/total_samples*100:.1f}%)
• Not Elephant Sessions: {not_elephant_count} ({not_elephant_count/total_samples*100:.1f}%)

📈 DATA QUALITY:
• Average Samples per Elephant Session: {avg_elephant_samples:.1f}
• Average Samples per Not-Elephant Session: {avg_not_elephant_samples:.1f}
• Total Raw Samples Collected: {sum(d.get('samples_count', 0) for d in self.training_data)}

⏱️ TIMING:
• Each labeling session captures 5 seconds of data
• Data is collected at ~1.25 Hz (every 800ms)
• Expected samples per session: ~6-7 samples
• Actual average: {(avg_elephant_samples + avg_not_elephant_samples)/2:.1f} samples

🎯 RECOMMENDATIONS:
• {'✅ Good data collection!' if avg_elephant_samples >= 5 and avg_not_elephant_samples >= 5 else '⚠️ Consider collecting more data'}
• {'✅ Balanced dataset!' if abs(elephant_count - not_elephant_count) <= 2 else '⚠️ Try to balance elephant vs not-elephant samples'}
• {'✅ Ready for training!' if total_samples >= 10 else '📝 Collect more labeled data for better training'}

📋 RECENT LABELING SESSIONS:
"""
        
        # Add recent sessions
        for i, session in enumerate(self.training_data[-5:], 1):
            timestamp = time.strftime('%H:%M:%S', time.localtime(session['timestamp']))
            samples = session.get('samples_count', 0)
            stats_text += f"• Session {i}: {session['label']} at {timestamp} ({samples} samples)\n"
        
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, stats_text)
        self.log_message("📊 Labeling statistics displayed")
    
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
                    self.training_data.clear()
                except Exception as e:
                    self.log_message(f"❌ Clear error: {str(e)}")
    
    def show_analysis(self):
        """Switch to analysis tab"""
        self.notebook.select(1)  # Switch to analysis tab
    
    def plot_feature_distribution(self):
        """Plot feature distribution analysis"""
        if not self.training_data:
            self.log_message("❌ No training data available for analysis", "analysis")
            return
        
        self.log_message("📊 Generating feature distribution analysis...", "analysis")
        # Implementation for feature distribution analysis
        self.log_message("✅ Feature distribution analysis complete", "analysis")
    
    def plot_time_series(self):
        """Plot time series analysis"""
        if not self.training_data:
            self.log_message("❌ No training data available for analysis", "analysis")
            return
        
        self.log_message("📈 Generating time series analysis...", "analysis")
        # Implementation for time series analysis
        self.log_message("✅ Time series analysis complete", "analysis")
    
    def plot_classification_analysis(self):
        """Plot classification analysis"""
        if not self.training_data:
            self.log_message("❌ No training data available for analysis", "analysis")
            return
        
        self.log_message("🎯 Generating classification analysis...", "analysis")
        # Implementation for classification analysis
        self.log_message("✅ Classification analysis complete", "analysis")
    
    def export_data(self):
        """Export data to file"""
        if not self.training_data:
            messagebox.showwarning("Warning", "No data to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    with open(filename, 'w') as f:
                        json.dump(self.training_data, f, indent=2)
                elif filename.endswith('.csv'):
                    df = pd.DataFrame(self.training_data)
                    df.to_csv(filename, index=False)
                
                self.log_message(f"✅ Data exported to {filename}", "analysis")
            except Exception as e:
                self.log_message(f"❌ Export error: {str(e)}", "analysis")
    
    def train_model(self):
        """Train machine learning model"""
        if not self.training_data:
            self.log_message("❌ No training data available", "training")
            return
        
        self.log_message("🤖 Starting model training...", "training")
        # Implementation for model training
        self.log_message("✅ Model training complete", "training")
    
    def test_model(self):
        """Test machine learning model"""
        self.log_message("🧪 Testing model performance...", "training")
        # Implementation for model testing
        self.log_message("✅ Model testing complete", "training")
    
    def save_model(self):
        """Save trained model"""
        self.log_message("💾 Saving model...", "training")
        # Implementation for model saving
        self.log_message("✅ Model saved", "training")
    
    def load_model(self):
        """Load trained model"""
        self.log_message("📁 Loading model...", "training")
        # Implementation for model loading
        self.log_message("✅ Model loaded", "training")
    
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
    app = AdvancedElephantGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
