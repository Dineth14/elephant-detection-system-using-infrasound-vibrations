#!/usr/bin/env python3
"""
Advanced GUI Launcher - Elephant Detection System
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['pyserial', 'tkinter', 'numpy', 'matplotlib', 'pandas']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'tkinter':
                import tkinter
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nInstalling missing packages...")
        
        import subprocess
        for package in missing_packages:
            if package != 'tkinter':  # tkinter comes with Python
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                    print(f"✅ Installed {package}")
                except subprocess.CalledProcessError:
                    print(f"❌ Failed to install {package}")
                    return False
    
    return True

def main():
    print("Advanced Elephant Detection System")
    print("=" * 50)
    
    # Check dependencies
    print("Checking dependencies...")
    if not check_dependencies():
        print("Failed to install required packages")
        input("Press Enter to exit...")
        return
    
    print("Dependencies OK")
    
    # Start the advanced GUI
    try:
        from python_gui.advanced_elephant_gui import main as gui_main
        print("Starting Advanced Elephant Detection GUI...")
        gui_main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
