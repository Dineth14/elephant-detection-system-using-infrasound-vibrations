#!/usr/bin/env python3
"""
Direct GUI Launcher - Simple Elephant Detection System
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Import and run the simple GUI
    from python_gui.simple_elephant_gui import main
    print("🐘 Starting Simple Elephant Detection GUI...")
    main()
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")
