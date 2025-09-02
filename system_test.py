#!/usr/bin/env python3
"""
System Test for ESP32 Elephant Detection System
Tests all major components without requiring hardware.
"""

import sys

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import tkinter  # type: ignore[unused-import]
        print("  [OK] tkinter")
    except ImportError as e:
        print(f"  [FAIL] tkinter: {e}")
        return False
    
    try:
        import matplotlib.pyplot  # type: ignore[unused-import]
        print("  [OK] matplotlib")
    except ImportError as e:
        print(f"  [FAIL] matplotlib: {e}")
        return False
    
    try:
        import serial  # type: ignore[unused-import]
        print("  [OK] pyserial")
    except ImportError as e:
        print(f"  [FAIL] pyserial: {e}")
        return False
    
    try:
        import python_gui.noise_logger_gui  # type: ignore[unused-import]
        print("  [OK] GUI module")
    except ImportError as e:
        print(f"  [FAIL] GUI module: {e}")
        return False
    
    return True

def test_gui_creation():
    """Test if the GUI can be created without errors."""
    print("\nTesting GUI creation...")
    
    try:
        import tkinter as tk
        from python_gui.noise_logger_gui import ESP32NoiseLoggerGUI
        root = tk.Tk()
        root.withdraw()  # Hide the window during testing
        gui = ESP32NoiseLoggerGUI(root)
        print("  [OK] GUI object created successfully")
        root.destroy()
        return True
    except Exception as e:
        print(f"  [FAIL] GUI creation failed: {e}")
        return False

def main():
    print("ESP32 Elephant Detection System - System Test")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n[RESULT] FAILED - Missing dependencies")
        print("Run: pip install -r requirements.txt")
        return 1
    
    # Test GUI creation
    if not test_gui_creation():
        print("\n[RESULT] FAILED - GUI creation error")
        return 1
    
    print("\n[RESULT] SUCCESS - All tests passed!")
    print("\nSystem is ready to use:")
    print("  Launch GUI: python python_gui/noise_logger_gui.py")
    print("  Or use launcher: run_gui.bat")
    print("  Test with simulated data: python simulate_esp32.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
