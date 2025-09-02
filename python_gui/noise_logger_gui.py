import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import serial
import serial.tools.list_ports
import threading
import time
import queue
from datetime import datetime
from typing import Dict, List, Optional

class ESP32NoiseLoggerGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("🐘 ESP32 Elephant Detection System - Real-time AI Audio Analysis")
        self.root.geometry("1600x1000")  # Larger for better space utilization
        self.root.minsize(1400, 900)     # Increased minimum size
        self.root.state('zoomed')        # Start maximized on Windows
        
        # Modern enhanced dark theme with better contrast
        self.theme_bg = "#0d1117"        # Darker GitHub-style background
        self.theme_fg = "#f0f6fc"        # Softer white
        self.card_bg = "#161b22"         # Darker cards
        self.card_hover = "#21262d"      # Hover state
        self.accent = "#238636"          # GitHub green
        self.warn = "#da3633"            # GitHub red  
        self.info = "#1f6feb"            # GitHub blue
        self.elephant_color = "#fd7e14"  # Modern orange
        self.success_color = "#00c853"   # Success green
        
        self.root.configure(bg=self.theme_bg)
        
        # Set modern window icon style
        try:
            self.root.iconbitmap(default="")
        except:
            pass

        # Serial connection
        self.serial_connection = None
        self.connected = False

        # Data storage
        self.feature_history = []
        self.classification_history = []
        self.max_history = 100

        # Threading
        self.data_queue = queue.Queue()
        self.running = True
        self.connection_attempts = 0
        self.max_connection_attempts = 3

        # Current features
        self.current_features = None
        self.current_classification = "not_elephant"
        self.current_confidence = 0.0

        # GUI elements
        self.port_var = tk.StringVar()
        self.custom_label_var = tk.StringVar()
        self.feature_labels = {}

        # GUI widgets (initialized in setup_ui)
        self.connection_status = None
        self.uptime_label = None
        self.samples_label = None
        self.memory_label = None
        self.classification_label = None
        self.confidence_label = None
        self.dataset_info_label = None
        self.log_text = None
        self.detection_indicator = None
        self.detection_log = None

        # Initialize GUI and start threads
        self.setup_ui()
        self.start_data_thread()
        
        # Start auto-connection after GUI is ready
        self.root.after(1000, self.auto_connect_serial)  # Wait 1 second for GUI to be ready

    def setup_ui(self) -> None:
        """Create the enhanced user interface with scrollable content"""
        # Create main canvas with both vertical and horizontal scrollbars
        self.canvas = tk.Canvas(self.root, bg=self.theme_bg, highlightthickness=0)
        v_scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        h_scrollbar = tk.Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
        scrollable_frame = tk.Frame(self.canvas, bg=self.theme_bg)

        # Configure scrollable area
        scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Pack canvas and scrollbars
        self.canvas.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure root grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Add mouse wheel scrolling support
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
        def _unbind_from_mousewheel(event):
            self.canvas.unbind_all("<MouseWheel>")
            
        self.canvas.bind('<Enter>', _bind_to_mousewheel)
        self.canvas.bind('<Leave>', _unbind_from_mousewheel)

        # Create main container with reduced padding for better fit
        main_container = tk.Frame(scrollable_frame, bg=self.theme_bg)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Modern header with enhanced styling
        header_frame = tk.Frame(main_container, bg=self.theme_bg, height=70)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)

        # Main title with modern typography
        title_label = tk.Label(header_frame, text="🐘 ELEPHANT DETECTION SYSTEM", 
                              bg=self.theme_bg, fg=self.theme_fg, 
                              font=("Segoe UI", 28, "bold"))  # Modern font and larger size
        title_label.pack(side=tk.TOP, pady=(10, 5))

        # Enhanced subtitle with modern styling
        subtitle_label = tk.Label(header_frame, text="Real-time AI Audio Analysis • 1kHz Sampling • 8D Feature Classification • Enhanced Performance Mode", 
                                 bg=self.theme_bg, fg=self.info, 
                                 font=("Segoe UI", 11, "normal"))  # Modern font
        subtitle_label.pack(side=tk.TOP)

        # Create enhanced 3-column layout for better space utilization
        content_frame = tk.Frame(main_container, bg=self.theme_bg)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure 3-column grid with proportional widths
        content_frame.grid_columnconfigure(0, weight=2, minsize=450)  # Left column (wider)
        content_frame.grid_columnconfigure(1, weight=2, minsize=450)  # Middle column 
        content_frame.grid_columnconfigure(2, weight=1, minsize=350)  # Right column (narrower)
        content_frame.grid_rowconfigure(2, weight=1)  # Make features row expandable

        # Enhanced Connection panel (top left) 
        conn_panel = self.create_card(content_frame, "🔗 CONNECTION STATUS", 0, 0, sticky="ew", padx=(0, 8), pady=8)
        self.setup_connection_panel(conn_panel)

        # Enhanced Controls panel (below connection, left column)
        controls_panel = self.create_card(content_frame, "�️ CONTROLS", 1, 0, sticky="ew", padx=(0, 8), pady=8)
        self.setup_controls_panel(controls_panel)

        # Enhanced Detection panel (top middle, spans 2 rows)
        detect_panel = self.create_card(content_frame, "� LIVE DETECTION", 0, 1, rowspan=2, sticky="nsew", padx=(4, 4), pady=8)
        self.setup_detection_panel(detect_panel)

        # Enhanced Log panel (top right, spans 2 rows)
        log_panel = self.create_card(content_frame, "� DETECTION LOG", 0, 2, rowspan=2, sticky="nsew", padx=(8, 0), pady=8)
        self.setup_log_panel(log_panel)

        # Wide Features panel (bottom, spans all 3 columns)
        features_panel = self.create_card(content_frame, "� AUDIO FEATURES", 2, 0, columnspan=3, sticky="nsew", padx=0, pady=8)
        self.setup_features_panel(features_panel)
        
        # Modern status bar at the bottom
        self.create_status_bar(main_container)

    def create_card(self, parent, title, row, col, columnspan=1, rowspan=1, sticky="nsew", padx=0, pady=10):
        """Create a modern card-style panel with enhanced visual design"""
        # Modern card container with subtle shadow effect
        card_container = tk.Frame(parent, bg=self.theme_bg)
        
        # Handle tuple or integer padding values for grid
        padx_grid = padx
        pady_grid = pady
        
        card_container.grid(row=row, column=col, columnspan=columnspan, rowspan=rowspan, sticky=sticky, padx=padx_grid, pady=pady_grid)
        
        # Main card with modern styling
        card = tk.Frame(card_container, bg=self.card_bg, relief=tk.SOLID, bd=1, highlightbackground="#30363d", highlightthickness=1)
        card.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)  # Shadow effect
        
        # Modern card header with gradient effect
        header_frame = tk.Frame(card, bg=self.card_bg, height=45)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title with modern typography and icon spacing
        title_label = tk.Label(header_frame, text=title, bg=self.card_bg, fg=self.theme_fg,
                              font=("Segoe UI", 13, "bold"), anchor="w")
        title_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=20, pady=12)
        
        # Separator line
        separator = tk.Frame(card, bg="#30363d", height=1)
        separator.pack(fill=tk.X)
        
        # Modern card content area with better padding
        content = tk.Frame(card, bg=self.card_bg)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=16)
        
        return content

    def setup_connection_panel(self, parent):
        """Setup the connection status panel"""
        # Status indicator
        status_frame = tk.Frame(parent, bg=self.card_bg)
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.connection_status = tk.Label(status_frame, text="🔍 Searching for ESP32...", 
                                         bg=self.card_bg, fg=self.info, 
                                         font=("Arial", 14, "bold"))
        self.connection_status.pack(anchor="w")

        # Connection buttons
        btn_frame = tk.Frame(parent, bg=self.card_bg)
        btn_frame.pack(fill=tk.X)

        self.create_modern_button(btn_frame, "🔄 Auto Connect", self.reconnect_esp32, self.success_color, row=0, col=0)
        self.create_modern_button(btn_frame, "📋 Manual", self.manual_connect_dialog, self.info, row=0, col=1)
        self.create_modern_button(btn_frame, "❌ Disconnect", self.disconnect_esp32, self.warn, row=1, col=0)
        self.create_modern_button(btn_frame, "🔍 Scan", self.scan_and_display_ports, "#666", row=1, col=1)

    def setup_detection_panel(self, parent):
        """Setup enhanced live detection panel with modern styling"""
        # Modern large detection indicator with gradient effect
        indicator_frame = tk.Frame(parent, bg="#1c2128", relief=tk.SOLID, bd=1)
        indicator_frame.pack(fill=tk.X, pady=(0, 16))
        
        self.detection_indicator = tk.Label(indicator_frame, text="⏳ INITIALIZING...", 
                                           font=("Segoe UI", 18, "bold"), 
                                           bg="#1c2128", fg="#7c3aed", 
                                           height=4, anchor="center")
        self.detection_indicator.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Modern classification details with cards
        details_container = tk.Frame(parent, bg=self.card_bg)
        details_container.pack(fill=tk.X, pady=(0, 16))
        
        # Classification card
        class_card = tk.Frame(details_container, bg="#1c2128", relief=tk.SOLID, bd=1)
        class_card.pack(fill=tk.X, pady=(0, 8))
        
        class_header = tk.Label(class_card, text="🎯 Classification", 
                               bg="#1c2128", fg="#60a5fa", 
                               font=("Segoe UI", 10, "bold"))
        class_header.pack(anchor="w", padx=16, pady=(12, 4))
        
        self.classification_label = tk.Label(class_card, text="Initializing...", 
                                           font=("Segoe UI", 14, "bold"), 
                                           bg="#1c2128", fg=self.theme_fg)
        self.classification_label.pack(anchor="w", padx=16, pady=(0, 12))

        # Confidence card
        conf_card = tk.Frame(details_container, bg="#1c2128", relief=tk.SOLID, bd=1)
        conf_card.pack(fill=tk.X)
        
        conf_header = tk.Label(conf_card, text="📊 Confidence", 
                              bg="#1c2128", fg="#34d399", 
                              font=("Segoe UI", 10, "bold"))
        conf_header.pack(anchor="w", padx=16, pady=(12, 4))
        
        self.confidence_label = tk.Label(conf_card, text="0%", 
                                        font=("Segoe UI", 14, "bold"), 
                                        bg="#1c2128", fg="#34d399")
        self.confidence_label.pack(anchor="w", padx=16, pady=(0, 12))

        # Modern labeling buttons with enhanced styling
        label_frame = tk.Frame(parent, bg=self.card_bg)
        label_frame.pack(fill=tk.X, pady=(16, 0))

        self.create_modern_button(label_frame, "🐘 Label: Elephant", lambda: self.send_label("elephant"), 
                                 self.elephant_color, row=0, col=0, columnspan=2)
        self.create_modern_button(label_frame, "🚫 Label: Not Elephant", lambda: self.send_label("not_elephant"), 
                                 self.warn, row=1, col=0, columnspan=2)

    def setup_features_panel(self, parent):
        """Setup enhanced audio features panel with modern grid layout"""
        self.feature_labels = {}
        feature_configs = [
            ("RMS Energy", "rms", "🔊", "#fd7e14"),
            ("Spectral Centroid", "spectral_centroid", "📈", "#20c997"), 
            ("Infrasound (10-40Hz)", "infrasound_energy", "🌊", "#6f42c1"),
            ("Low Band (40-100Hz)", "low_band_energy", "📊", "#0dcaf0"),
            ("Mid Band (100-200Hz)", "mid_band_energy", "📉", "#198754"),
            ("Dominant Frequency", "dominant_frequency", "🎵", "#ffc107"),
            ("Temporal Envelope", "temporal_envelope", "⏱️", "#dc3545"),
            ("Spectral Flux", "spectral_flux", "🌀", "#6610f2")
        ]

        # Create modern grid layout for features (4x2 grid)
        features_grid = tk.Frame(parent, bg=self.card_bg)
        features_grid.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights for even distribution
        for i in range(4):
            features_grid.grid_columnconfigure(i, weight=1, minsize=200)
        for i in range(2):
            features_grid.grid_rowconfigure(i, weight=1)

        for i, (display_name, key, icon, color) in enumerate(feature_configs):
            row = i // 4
            col = i % 4
            
            # Modern feature card
            feature_card = tk.Frame(features_grid, bg="#1c2128", relief=tk.SOLID, bd=1)
            feature_card.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)
            
            # Icon and title
            header = tk.Frame(feature_card, bg="#1c2128")
            header.pack(fill=tk.X, padx=12, pady=(8, 4))
            
            icon_label = tk.Label(header, text=icon, bg="#1c2128", fg=color, 
                                font=("Segoe UI", 16))
            icon_label.pack(side=tk.LEFT)
            
            title_label = tk.Label(header, text=display_name, bg="#1c2128", fg=self.theme_fg,
                                 font=("Segoe UI", 9, "bold"), anchor="w")
            title_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 0))
            
            # Value display
            value_label = tk.Label(feature_card, text="--", bg="#1c2128", fg=color,
                                 font=("Segoe UI", 14, "bold"), anchor="center")
            value_label.pack(fill=tk.X, padx=12, pady=(0, 8))
            
            self.feature_labels[key] = value_label

    def setup_controls_panel(self, parent):
        """Setup the controls panel"""
        # System status
        status_frame = tk.LabelFrame(parent, text="📊 System Status", bg=self.card_bg, fg=self.theme_fg, 
                                    font=("Arial", 11, "bold"))
        status_frame.pack(fill=tk.X, pady=(0, 15))

        self.uptime_label = tk.Label(status_frame, text="Uptime: --", bg=self.card_bg, fg=self.theme_fg, font=("Arial", 10))
        self.uptime_label.pack(anchor="w", padx=10, pady=2)
        
        self.samples_label = tk.Label(status_frame, text="Samples: --", bg=self.card_bg, fg=self.theme_fg, font=("Arial", 10))
        self.samples_label.pack(anchor="w", padx=10, pady=2)
        
        self.memory_label = tk.Label(status_frame, text="Memory: --", bg=self.card_bg, fg=self.theme_fg, font=("Arial", 10))
        self.memory_label.pack(anchor="w", padx=10, pady=2)

        self.dataset_info_label = tk.Label(status_frame, text="Dataset: --", bg=self.card_bg, fg=self.theme_fg, font=("Arial", 10))
        self.dataset_info_label.pack(anchor="w", padx=10, pady=2)

        # Control buttons
        control_frame = tk.Frame(parent, bg=self.card_bg)
        control_frame.pack(fill=tk.X)

        self.create_modern_button(control_frame, "📊 Get Status", self.request_status, self.info, row=0, col=0)
        self.create_modern_button(control_frame, "🎵 Get Features", self.request_features, "#17a2b8", row=0, col=1)
        self.create_modern_button(control_frame, "💾 Save Data", self.save_data, self.success_color, row=1, col=0)
        self.create_modern_button(control_frame, "🗑️ Clear Data", self.clear_data, self.warn, row=1, col=1)

    def setup_log_panel(self, parent):
        """Setup the detection log panel"""
        # Create text widget with scrollbar
        text_frame = tk.Frame(parent, bg=self.card_bg)
        text_frame.pack(fill=tk.BOTH, expand=True)

        self.detection_log = tk.Text(text_frame, height=8, wrap=tk.WORD, state="disabled", 
                                    bg="#1e1e1e", fg="#e0e0e0", font=("Consolas", 10),
                                    insertbackground="#fff", selectbackground="#404040")
        
        log_scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=self.detection_log.yview, bg=self.card_bg)
        self.detection_log.configure(yscrollcommand=log_scrollbar.set)

        self.detection_log.pack(side="left", fill="both", expand=True)
        log_scrollbar.pack(side="right", fill="y")

    def create_modern_button(self, parent, text, command, color, row=0, col=0, columnspan=1):
        """Create modern styled button with enhanced visual effects"""
        btn = tk.Button(parent, text=text, command=command, 
                       bg=color, fg="#ffffff", font=("Segoe UI", 11, "bold"),
                       relief=tk.FLAT, bd=0, padx=20, pady=12,
                       cursor="hand2", activebackground=self.lighten_color(color))
        btn.grid(row=row, column=col, columnspan=columnspan, padx=4, pady=4, sticky="ew")
        
        # Enhanced hover effects with smooth transitions
        def on_enter(e):
            btn.config(bg=self.lighten_color(color), relief=tk.SOLID, bd=1)
        def on_leave(e):
            btn.config(bg=color, relief=tk.FLAT, bd=0)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        # Configure grid weights for even distribution
        parent.grid_columnconfigure(col, weight=1)
        if columnspan > 1:
            for i in range(col, col + columnspan):
                parent.grid_columnconfigure(i, weight=1)
        
        # Hover effects
        def on_enter(e):
            btn.config(bg=self.lighten_color(color))
        def on_leave(e):
            btn.config(bg=color)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn

    def lighten_color(self, color):
        """Lighten a hex color by 20%"""
        # Ensure color starts with #
        if not color.startswith('#'):
            color = '#' + color
            
        # Handle 3-character hex colors like #666
        if len(color) == 4:
            color = '#' + color[1] + color[1] + color[2] + color[2] + color[3] + color[3]
            
        try:
            r, g, b = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            r = min(255, int(r * 1.2))
            g = min(255, int(g * 1.2))
            b = min(255, int(b * 1.2))
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return "#777777"  # Default lighter gray

    def create_status_bar(self, parent) -> None:
        """Create enhanced modern status bar with real-time metrics"""
        status_bar = tk.Frame(parent, bg="#0d1117", height=35, relief=tk.SOLID, bd=1)
        status_bar.pack(side="bottom", fill="x", pady=(16, 0))
        status_bar.pack_propagate(False)
        
        # Left side - System status
        left_frame = tk.Frame(status_bar, bg="#0d1117")
        left_frame.pack(side="left", fill="x", expand=True, padx=20, pady=8)
        
        self.status_text = tk.Label(left_frame, text="🚀 System Ready - Enhanced Performance Mode Active", 
                                   bg="#0d1117", fg="#7c3aed", font=("Segoe UI", 10, "bold"))
        self.status_text.pack(side="left")
        
        # Center - Connection status
        center_frame = tk.Frame(status_bar, bg="#0d1117")
        center_frame.pack(side="left", padx=20, pady=8)
        
        self.connection_status_bar = tk.Label(center_frame, text="⚡ Disconnected", 
                                            bg="#0d1117", fg="#f85149", font=("Segoe UI", 10))
        self.connection_status_bar.pack()
        
        # Right side - Performance metrics
        right_frame = tk.Frame(status_bar, bg="#0d1117")
        right_frame.pack(side="right", padx=20, pady=8)
        
        self.perf_metrics = tk.Label(right_frame, text="📊 66 FPS | 🎯 Real-time | 🚀 Enhanced", 
                                   bg="#0d1117", fg="#3fb950", font=("Segoe UI", 10, "bold"))
        self.perf_metrics.pack(side="right")

    def find_esp32_port(self) -> Optional[str]:
        """Find ESP32 board port by checking device descriptions and VID/PID"""
        esp32_keywords = [
            'CP210x',  # Silicon Labs CP2102 (common on ESP32 boards)
            'CH340',   # WCH CH340 USB-to-Serial
            'CH341',   # WCH CH341 USB-to-Serial
            'FTDI',    # FTDI USB-to-Serial
            'ESP32',   # Direct ESP32 reference
            'Silicon Labs',  # Silicon Labs devices
            'USB-SERIAL CH340',  # CH340 description
            'USB2.0-Serial',     # Generic USB serial
            'USB Serial Port',   # Windows generic description
            'Prolific',          # Prolific USB-to-Serial
            'Arduino',           # Arduino boards
            'NodeMCU',           # NodeMCU boards
            'DevKit',            # ESP32 DevKit boards
        ]
        
        # Known ESP32 VID:PID combinations (expanded list)
        esp32_vid_pids = [
            (0x10C4, 0xEA60),  # Silicon Labs CP2102/CP2104
            (0x1A86, 0x7523),  # WCH CH340
            (0x1A86, 0x55D4),  # WCH CH341
            (0x0403, 0x6001),  # FTDI FT232R
            (0x0403, 0x6010),  # FTDI FT2232H
            (0x0403, 0x6014),  # FTDI FT232H
            (0x303A, 0x1001),  # Espressif ESP32-S2
            (0x303A, 0x1002),  # Espressif ESP32-S3
            (0x303A, 0x8001),  # Espressif ESP32-C3
            (0x2341, 0x0043),  # Arduino Uno R3
            (0x2341, 0x0001),  # Arduino Uno R1
            (0x067B, 0x2303),  # Prolific PL2303
            (0x16C0, 0x0483),  # Generic USB serial
        ]
        
        try:
            ports = list(serial.tools.list_ports.comports())
            self.log_message(f"Hardware detection: scanning {len(ports)} available ports...")
            
            # First priority: Check by VID/PID (most reliable)
            for port in ports:
                # Log port details for debugging
                vid_pid_str = "Unknown"
                if hasattr(port, 'vid') and hasattr(port, 'pid') and port.vid and port.pid:
                    vid_pid_str = f"VID:{port.vid:04X}, PID:{port.pid:04X}"
                    
                self.log_message(f"  {port.device}: {port.description} ({vid_pid_str})")
                
                # Check by VID/PID first (most reliable)
                if hasattr(port, 'vid') and hasattr(port, 'pid') and port.vid and port.pid:
                    if (port.vid, port.pid) in esp32_vid_pids:
                        self.log_message(f"✓ Found ESP32 by VID/PID: {port.device}")
                        return port.device
            
            # Second priority: Check by description keywords
            for port in ports:
                description = (port.description or "").upper()
                manufacturer = (port.manufacturer or "").upper()
                
                for keyword in esp32_keywords:
                    if keyword.upper() in description or keyword.upper() in manufacturer:
                        self.log_message(f"✓ Found potential ESP32 by description: {port.device} ({keyword})")
                        return port.device
            
            # Third priority: Any COM port (as fallback)
            for port in ports:
                if port.device.upper().startswith('COM'):
                    self.log_message(f"? Found generic COM port: {port.device} (will test)")
                    return port.device
                        
            self.log_message("✗ No potential ESP32 ports found by hardware detection")
            return None
            
        except Exception as e:
            self.log_message(f"Error in hardware detection: {e}")
            return None

    def test_esp32_connection(self, port: str) -> bool:
        """Test if the given port has an ESP32 with our firmware"""
        try:
            self.log_message(f"Testing connection to {port}...")
            test_connection = serial.Serial(port, 115200, timeout=2)
            time.sleep(2)  # Wait for ESP32 to reset and initialize
            
            # Send multiple test commands to verify it's our firmware
            test_commands = ["GET_STATUS", "GET_FEATURES", "PING"]
            
            for cmd in test_commands:
                test_connection.write((cmd + "\n").encode())
                time.sleep(0.5)
                
                # Read any available responses
                responses: List[str] = []
                while test_connection.in_waiting > 0:
                    response = test_connection.readline().decode().strip()
                    if response:
                        responses.append(response)
                        
                # Check for expected response patterns
                for response in responses:
                    if any(pattern in response for pattern in ["STATUS:", "FEATURES:", "ERROR:", "OK:"]):
                        test_connection.close()
                        self.log_message(f"✓ ESP32 Noise Logger confirmed on {port}")
                        return True
                        
            test_connection.close()
            self.log_message(f"✗ No valid response from {port}")
            return False
            
        except Exception as e:
            self.log_message(f"✗ Connection test failed on {port}: {e}")
            return False

    def test_esp32_connection_extended(self, port: str) -> bool:
        """Extended test with longer timeouts and more thorough checking"""
        try:
            self.log_message(f"Extended testing on {port} (longer timeout)...")
            test_connection = serial.Serial(port, 115200, timeout=5)  # Longer timeout
            time.sleep(3)  # Longer wait for ESP32 to reset and initialize
            
            # Clear any existing data in buffer
            test_connection.reset_input_buffer()
            test_connection.reset_output_buffer()
            
            # Try a simple ping first
            test_connection.write(b"PING\n")
            time.sleep(1)
            
            # Try to get status
            test_connection.write(b"GET_STATUS\n")
            time.sleep(1)
            
            # Try to get features
            test_connection.write(b"GET_FEATURES\n")
            time.sleep(1)
            
            # Read all available responses
            responses: List[str] = []
            attempts = 0
            while attempts < 10:  # Try multiple times
                if test_connection.in_waiting > 0:
                    try:
                        response = test_connection.readline().decode('utf-8', errors='ignore').strip()
                        if response:
                            responses.append(response)
                            self.log_message(f"Received from {port}: {response}")
                    except:
                        pass
                time.sleep(0.2)
                attempts += 1
                
            test_connection.close()
            
            # Check if we got any ESP32-like responses
            esp32_indicators = ["STATUS:", "FEATURES:", "ERROR:", "OK:", "PING:", "DATASET:", "LABELED:"]
            
            for response in responses:
                for indicator in esp32_indicators:
                    if indicator in response:
                        self.log_message(f"✓ ESP32 confirmed on {port} (found: {indicator})")
                        return True
                        
            self.log_message(f"✗ No ESP32 signature found on {port}")
            return False
            
        except Exception as e:
            self.log_message(f"✗ Extended test failed on {port}: {e}")
            return False

    def auto_connect_serial(self) -> None:
        """Automatically connect to ESP32 with enhanced detection"""
        if self.connected:
            return  # Already connected
            
        self.connection_attempts += 1
        self.connection_status.config(text=f"Searching for ESP32... (attempt {self.connection_attempts})", foreground="orange")
        self.log_message(f"=== ESP32 Auto-Detection Attempt {self.connection_attempts}/{self.max_connection_attempts} ===")
        
        try:
            # Get all available ports first
            ports = list(serial.tools.list_ports.comports())
            self.log_message(f"Found {len(ports)} available COM ports")
            
            if len(ports) == 0:
                self.log_message("❌ No COM ports found! Check USB connection.")
                self.schedule_retry()
                return
            
            # Log all available ports for debugging
            for port in ports:
                self.log_message(f"Available: {port.device} - {port.description} ({port.manufacturer})")
            
            # Strategy 1: Try hardware detection by VID/PID and description
            self.log_message("Strategy 1: Hardware detection by VID/PID...")
            esp32_port = self.find_esp32_port()
            
            if esp32_port:
                self.log_message(f"Hardware detection found ESP32 on {esp32_port}")
                if self.test_esp32_connection(esp32_port):
                    self.connect_to_port(esp32_port)
                    return
                else:
                    self.log_message(f"Hardware detected port {esp32_port} failed communication test")
                    
            # Strategy 2: Test all ports for ESP32 firmware response
            self.log_message("Strategy 2: Testing all ports for ESP32 firmware...")
            
            for port in ports:
                self.log_message(f"Testing port {port.device}...")
                if self.test_esp32_connection(port.device):
                    self.log_message(f"Found working ESP32 on {port.device}")
                    self.connect_to_port(port.device)
                    return
                    
            # Strategy 3: More aggressive testing with different timeouts
            self.log_message("Strategy 3: Extended timeout testing...")
            
            for port in ports:
                self.log_message(f"Extended test on {port.device}...")
                if self.test_esp32_connection_extended(port.device):
                    self.log_message(f"Extended test found ESP32 on {port.device}")
                    self.connect_to_port(port.device)
                    return
                    
            # No ESP32 found after all strategies
            self.log_message("❌ ESP32 Elephant Detection System not found on any port")
            self.schedule_retry()
            
        except Exception as e:
            self.connection_status.config(text=f"Auto-connect error: {str(e)}", foreground="red")
            self.log_message(f"Auto-connect error: {str(e)}")
            self.schedule_retry()

    def schedule_retry(self) -> None:
        """Schedule a retry connection attempt"""
        if self.connection_attempts < self.max_connection_attempts:
            self.connection_status.config(text=f"Retrying in 5 seconds... ({self.connection_attempts}/{self.max_connection_attempts})", foreground="orange")
            self.log_message(f"Will retry connection in 5 seconds...")
            self.root.after(5000, self.auto_connect_serial)  # Retry after 5 seconds
        else:
            self.connection_status.config(text="ESP32 not found - Use Manual connection", foreground="red")
            self.connected = False
            self.log_message("🔴 All automatic connection attempts failed")
            self.log_message("📝 Troubleshooting checklist:")
            self.log_message("  1. Ensure ESP32 is connected via USB cable")
            self.log_message("  2. Run auto_run.bat to upload firmware") 
            self.log_message("  3. Check Windows Device Manager for COM ports")
            self.log_message("  4. Install ESP32 USB drivers if needed")
            self.log_message("  5. Try different USB cable or port")
            self.log_message("  6. Click 'Manual' button to select port manually")
            self.log_message("  7. Check if ESP32 is recognized in Device Manager")

    def connect_to_port(self, port: str) -> None:
        """Connect to a specific port"""
        try:
            self.serial_connection = serial.Serial(port, 115200, timeout=1)
            time.sleep(2)  # Wait for ESP32 to reset
            
            self.connected = True
            self.connection_attempts = 0  # Reset attempts on successful connection
            self.connection_status.config(text=f"✓ Connected: {port}", foreground="green")
            # Update footer status bar
            if hasattr(self, 'connection_status_bar'):
                self.connection_status_bar.config(text=f"⚡ Connected ({port})", fg="#3fb950")
            self.log_message(f"🔗 Successfully connected to ESP32 on {port}")
            
            # Send initial commands to sync and start data flow
            self.serial_connection.write(b"GET_STATUS\n")
            time.sleep(0.1)
            self.serial_connection.write(b"GET_FEATURES\n")
            
        except Exception as e:
            self.connected = False
            self.connection_status.config(text=f"Connection failed: {str(e)}", foreground="red")
            # Update footer status bar
            if hasattr(self, 'connection_status_bar'):
                self.connection_status_bar.config(text="⚡ Connection Failed", fg="#f85149")
            self.log_message(f"Connection failed to {port}: {str(e)}")
            
            if self.serial_connection and self.serial_connection.is_open:
                self.serial_connection.close()
                self.serial_connection = None

    def manual_connect_dialog(self) -> None:
        """Show manual port selection dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Manual Port Selection")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        # Center the dialog
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Select ESP32 Port:", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Port listbox
        frame = ttk.Frame(dialog)
        frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        listbox = tk.Listbox(frame, height=8)
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)  # type: ignore
        listbox.configure(yscrollcommand=scrollbar.set)
        
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate ports
        ports = list(serial.tools.list_ports.comports())
        for i, port in enumerate(ports):
            display_text = f"{port.device} - {port.description}"
            listbox.insert(i, display_text)
            
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        def connect_selected():
            selection = listbox.curselection()  # type: ignore
            if selection:
                port_index = int(selection[0])  # type: ignore
                selected_port = str(ports[port_index].device)
                dialog.destroy()
                self.connect_to_port(selected_port)
            else:
                messagebox.showwarning("Warning", "Please select a port")
                
        def refresh_ports():
            listbox.delete(0, tk.END)
            ports.clear()
            ports.extend(serial.tools.list_ports.comports())
            for i, port in enumerate(ports):
                display_text = f"{port.device} - {port.description}"
                listbox.insert(i, display_text)
        
        ttk.Button(button_frame, text="Connect", command=connect_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", command=refresh_ports).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def reconnect_esp32(self) -> None:
        """Reconnect to ESP32 - disconnect first if connected, then auto-connect"""
        self.connection_attempts = 0  # Reset attempts for manual reconnection
        if self.connected:
            self.disconnect_esp32()
            time.sleep(1)  # Wait a moment before reconnecting
        self.log_message("🔄 Manual reconnection initiated...")
        self.auto_connect_serial()

    def disconnect_esp32(self) -> None:
        """Disconnect from ESP32"""
        try:
            if self.serial_connection and self.serial_connection.is_open:
                self.serial_connection.close()
                self.serial_connection = None
            
            self.connected = False
            if self.connection_status:
                self.connection_status.config(text="Disconnected", foreground="red")
            # Update footer status bar
            if hasattr(self, 'connection_status_bar'):
                self.connection_status_bar.config(text="⚡ Disconnected", fg="#f85149")
            self.log_message("🔌 Disconnected from ESP32")
            
        except Exception as e:
            self.log_message(f"Error during disconnect: {e}")

    def scan_and_display_ports(self) -> None:
        """Scan and display all available ports with details"""
        self.log_message("=== Port Scan Results ===")
        try:
            ports = list(serial.tools.list_ports.comports())
            if not ports:
                self.log_message("No serial ports found")
                return
                
            for i, port in enumerate(ports, 1):
                self.log_message(f"{i}. Port: {port.device}")
                self.log_message(f"   Description: {port.description}")
                self.log_message(f"   Manufacturer: {port.manufacturer or 'Unknown'}")
                
                if hasattr(port, 'vid') and hasattr(port, 'pid'):
                    vid_pid = f"VID:{port.vid:04X}, PID:{port.pid:04X}" if port.vid and port.pid else "Unknown"
                    self.log_message(f"   VID/PID: {vid_pid}")
                
                # Test if it's likely an ESP32
                esp32_indicators: List[str] = []
                if port.description and any(keyword.upper() in port.description.upper() 
                                         for keyword in ['CP210x', 'CH340', 'CH341', 'ESP32', 'Silicon Labs']):
                    esp32_indicators.append("Description match")
                    
                if hasattr(port, 'vid') and hasattr(port, 'pid') and port.vid and port.pid:
                    esp32_vid_pids = [(0x10C4, 0xEA60), (0x1A86, 0x7523), (0x1A86, 0x55D4), 
                                     (0x0403, 0x6001), (0x0403, 0x6010), (0x303A, 0x1001), (0x303A, 0x1002)]
                    if (port.vid, port.pid) in esp32_vid_pids:
                        esp32_indicators.append("VID/PID match")
                
                if esp32_indicators:
                    self.log_message(f"   🎯 Likely ESP32: {', '.join(esp32_indicators)}")
                else:
                    self.log_message(f"   ❓ Unknown device type")
                    
                self.log_message("")  # Empty line between ports
                
        except Exception as e:
            self.log_message(f"Error scanning ports: {e}")

    def start_data_thread(self) -> None:
        """Start background thread for data reception"""
        def data_receiver():
            while self.running:
                try:
                    if self.connected and self.serial_connection and self.serial_connection.is_open:
                        if self.serial_connection.in_waiting > 0:
                            raw_data = self.serial_connection.readline()
                            
                            # Try to decode with error handling
                            try:
                                line = raw_data.decode('utf-8').strip()
                            except UnicodeDecodeError:
                                # If UTF-8 fails, try with error handling
                                try:
                                    line = raw_data.decode('utf-8', errors='ignore').strip()
                                    if line:
                                        self.log_message(f"⚠️ Received corrupted data, recovered: {line}")
                                except:
                                    # If all else fails, show as hex
                                    hex_data = ' '.join([f'{b:02x}' for b in raw_data])
                                    self.log_message(f"❌ Binary data received: {hex_data}")
                                    continue
                            
                            if line:
                                self.data_queue.put(line)
                except Exception as e:
                    self.log_message(f"Data reception error: {str(e)}")
                    self.connected = False
                time.sleep(0.01)
        
        self.data_thread = threading.Thread(target=data_receiver, daemon=True)
        self.data_thread.start()
        
        # Start data processing
        self.process_queue()

    def process_queue(self) -> None:
        """Process queued data from ESP32 - enhanced for ultra-responsive real-time performance"""
        processed_count = 0
        max_batch_size = 20  # Increased batch size for better throughput
        
        try:
            while not self.data_queue.empty() and processed_count < max_batch_size:
                line = self.data_queue.get_nowait()
                self.process_serial_data(line)
                processed_count += 1
        except queue.Empty:
            pass
        except Exception as e:
            print(f"Queue processing error: {e}")
        
        # Ultra-responsive 15ms intervals for 66 FPS update rate
        self.root.after(15, self.process_queue)

    def process_serial_data(self, data: str) -> None:
        """Process data received from ESP32"""
        try:
            if data.startswith("FEATURES:"):
                self.log_message(f"📊 Received features data")
                self.parse_features(data)
            elif data.startswith("STATUS:"):
                self.parse_status(data)
            elif data.startswith("DATASET:"):
                self.parse_dataset(data)
            elif data.startswith("LABELED:"):
                self.log_message(f"Label confirmed: {data[8:]}")
            elif data.startswith("ERROR:"):
                self.log_message(f"ESP32 Error: {data[6:]}")
            elif data.startswith("OK:"):
                self.log_message(f"ESP32 OK: {data[3:]}")
            elif data.startswith("DEBUG:"):
                self.log_message(f"ESP32 DEBUG: {data[6:]}")
            else:
                self.log_message(f"ESP32: {data}")
        except Exception as e:
            self.log_message(f"Data processing error: {str(e)}")

    def parse_features(self, data: str) -> None:
        """Parse FEATURES: line from ESP32 and update current features and GUI."""
        try:
            # Remove "FEATURES:" prefix and split
            parts = data[9:].split(",")
            # Order: rms, centroid, infrasound_energy, low_band_energy, mid_band_energy, dominant_freq, temporal_envelope, spectral_flux, label, confidence
            if len(parts) >= 10:
                self.current_features = {
                    'rms': float(parts[0]),
                    'spectral_centroid': float(parts[1]),
                    'infrasound_energy': float(parts[2]),
                    'low_band_energy': float(parts[3]),
                    'mid_band_energy': float(parts[4]),
                    'dominant_freq': float(parts[5]),
                    'temporal_envelope': float(parts[6]),
                    'spectral_flux': float(parts[7]),
                }
                self.current_classification = parts[8].strip()
                self.current_confidence = float(parts[9])
                self.update_display()
                self.update_detection_indicator(self.current_classification, self.current_confidence)
                self.log_detection_event(self.current_classification, self.current_confidence)
        except Exception as e:
            self.log_message(f"Feature parsing error: {str(e)}")

    def update_detection_indicator(self, classification: str, confidence: float) -> None:
        """Update the detection indicator with enhanced visual feedback"""
        if not self.detection_indicator:
            return
            
        # High confidence elephant detection
        if classification == "elephant" and confidence > 0.8:
            self.detection_indicator.config(
                text="🐘 ELEPHANT DETECTED! 🚨", 
                bg="#ff4444", fg="#ffffff",
                font=("Arial", 22, "bold")
            )
            self.root.bell()  # Audio alert
            # Flash effect
            self.root.after(100, lambda: self.detection_indicator.config(bg="#ff6666"))
            self.root.after(200, lambda: self.detection_indicator.config(bg="#ff4444"))
            
        # Medium confidence elephant detection  
        elif classification == "elephant" and confidence > 0.6:
            self.detection_indicator.config(
                text="🐘 Possible Elephant", 
                bg=self.elephant_color, fg="#ffffff",
                font=("Arial", 20, "bold")
            )
            
        # Low confidence elephant
        elif classification == "elephant":
            self.detection_indicator.config(
                text="🤔 Elephant (Low Confidence)", 
                bg="#666666", fg="#ffffff",
                font=("Arial", 18, "bold")
            )
            
        # No elephant detected
        else:
            self.detection_indicator.config(
                text="✅ No Elephant", 
                bg="#2d5a2d", fg="#ffffff",
                font=("Arial", 18, "bold")
            )

    def log_detection_event(self, classification: str, confidence: float) -> None:
        """Log detection events with timestamp"""
        if classification == "elephant" and confidence > 0.5:
            timestamp = datetime.now().strftime("%H:%M:%S")
            event_text = f"[{timestamp}] Elephant detected (confidence: {confidence*100:.1f}%)\n"
            
            if self.detection_log:
                self.detection_log.config(state="normal")
                self.detection_log.insert(tk.END, event_text)
                self.detection_log.see(tk.END)
                self.detection_log.config(state="disabled")

    def update_display(self) -> None:
        """Update the GUI display with current data - enhanced with visual indicators"""
        if not self.current_features:
            return
            
        # Update classification with color coding
        if self.classification_label:
            color = self.accent if self.current_classification == "elephant" else "#666"
            self.classification_label.config(
                text=f"Classification: {self.current_classification.upper()}", 
                fg=color
            )
            
        if self.confidence_label:
            # Color-code confidence based on level
            if self.current_confidence > 0.8:
                conf_color = "#4caf50"  # Green for high confidence
            elif self.current_confidence > 0.6:
                conf_color = "#ff9800"  # Orange for medium confidence
            else:
                conf_color = "#666"     # Gray for low confidence
                
            self.confidence_label.config(
                text=f"Confidence: {self.current_confidence*100:.1f}%",
                fg=conf_color
            )
        
        # Update features with enhanced formatting and activity indicators
        feature_updates = [
            ('rms', f"🔊 RMS Energy: {self.current_features.get('rms', 0):.4f}"),
            ('spectral_centroid', f"📈 Spectral Centroid: {self.current_features.get('spectral_centroid', 0):.1f} Hz"),
            ('infrasound_energy', f"🌊 Infrasound (10-40Hz): {self.current_features.get('infrasound_energy', 0):.4f}"),
            ('low_band_energy', f"📊 Low Band (40-100Hz): {self.current_features.get('low_band_energy', 0):.4f}"),
            ('mid_band_energy', f"📉 Mid Band (100-200Hz): {self.current_features.get('mid_band_energy', 0):.4f}"),
            ('dominant_frequency', f"🎵 Dominant Freq: {self.current_features.get('dominant_freq', 0):.1f} Hz"),
            ('temporal_envelope', f"⏱️ Temporal Envelope: {self.current_features.get('temporal_envelope', 0):.4f}"),
            ('spectral_flux', f"🌀 Spectral Flux: {self.current_features.get('spectral_flux', 0):.4f}")
        ]
        
        for key, text in feature_updates:
            if key in self.feature_labels:
                label = self.feature_labels[key]
                label.config(text=text)
                
                # Add visual activity indicator for significant values
                value = self.current_features.get(key.replace('_', '_'), 0)
                if isinstance(value, (int, float)) and value > 0.1:
                    # Briefly highlight active features
                    label.config(fg="#4caf50")
                    self.root.after(500, lambda l=label: l.config(fg=self.theme_fg))
                else:
                    label.config(fg=self.theme_fg)

    def parse_dataset(self, data: str) -> None:
        """Parse dataset info from ESP32"""
        try:
            parts = data[8:].split(',')  # Remove "DATASET:" prefix
            if len(parts) >= 3:
                total = parts[0]
                elephant = parts[1]
                not_elephant = parts[2]
                text = f"Total: {total} (Elephant: {elephant}, Not Elephant: {not_elephant})"
                self.dataset_info_label.config(text=text)
            else:
                self.dataset_info_label.config(text="Dataset: No data")
        except Exception as e:
            self.dataset_info_label.config(text=f"Dataset error: {str(e)}")

    def parse_status(self, data: str) -> None:
        """Parse status data from ESP32"""
        try:
            parts = data[7:].split(',')  # Remove "STATUS:" prefix
            if len(parts) >= 3:
                sample_count = parts[0]
                uptime_ms = int(parts[1])
                free_memory = parts[2]
                
                uptime_sec = uptime_ms // 1000
                uptime_str = f"{uptime_sec // 60}:{uptime_sec % 60:02d}"
                
                self.samples_label.config(text=f"Samples: {sample_count}")
                self.uptime_label.config(text=f"Uptime: {uptime_str}")
                self.memory_label.config(text=f"Free Memory: {free_memory} bytes")
                
        except Exception as e:
            self.log_message(f"Status parsing error: {str(e)}")

    def parse_labeled(self, data: str) -> None:
        """Parse labeling confirmation"""
        try:
            parts = data[8:].split(',')  # Remove "LABELED:" prefix
            if len(parts) >= 2:
                label = parts[0]
                count = parts[1]
                self.log_message(f"Labeled as '{label}' - Total samples: {count}")
                
        except Exception as e:
            self.log_message(f"Label parsing error: {str(e)}")



    def send_command(self, command: str) -> None:
        """Send command to ESP32"""
        try:
            if self.connected and self.serial_connection:
                self.serial_connection.write(f"{command}\n".encode())
                self.log_message(f"Sent: {command}")
            else:
                self.log_message("Not connected to ESP32")
        except Exception as e:
            self.log_message(f"Send error: {str(e)}")

    def send_label(self, label: str) -> None:
        """Send label for current sound"""
        self.send_command(f"LABEL:{label}")

    def send_custom_label(self) -> None:
        """Send custom label"""
        label = self.custom_label_var.get().strip()
        if label:
            self.send_label(label)
            self.custom_label_var.set("")

    def request_status(self) -> None:
        """Request status from ESP32"""
        self.send_command("GET_STATUS")
        self.send_command("GET_DATASET")

    def request_features(self) -> None:
        """Request current features from ESP32"""
        self.send_command("GET_FEATURES")
        self.log_message("📊 Requesting current audio features...")

    def save_data(self) -> None:
        """Save data on ESP32"""
        self.send_command("SAVE_DATA")

    def clear_data(self) -> None:
        """Clear data on ESP32"""
        if messagebox.askyesno("Confirm", "Clear all training data?"):
            self.send_command("CLEAR_DATA")

    def reconnect(self) -> None:
        """Reconnect to ESP32"""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
        self.connected = False
        if self.connection_status:
            self.connection_status.config(text="Reconnecting...", foreground="orange")
        self.root.after(1000, self.auto_connect_serial)

    def log_message(self, message: str) -> None:
        """Add message to detection log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        if self.detection_log:
            self.detection_log.config(state="normal")
            self.detection_log.insert(tk.END, log_entry)
            self.detection_log.see(tk.END)
            self.detection_log.config(state="disabled")
        else:
            # Fallback to console if GUI not ready
            print(log_entry.strip())

    def on_closing(self) -> None:
        """Handle window closing"""
        self.running = False
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    app = ESP32NoiseLoggerGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        app.on_closing()


if __name__ == "__main__":
    main()
