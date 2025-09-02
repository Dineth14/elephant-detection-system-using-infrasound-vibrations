"""
Script to retrieve stored dataset from ESP32 via serial and save as CSV file.
Prompts for COM port and output filename.
"""
import serial
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
import sys

# Prompt user for serial port

root = tk.Tk()
root.withdraw()
port = simpledialog.askstring("Serial Port", "Enter ESP32 COM port (e.g., COM3):")
if not port:
    print("No port provided.")
    sys.exit(1)

BAUD = 115200
TIMEOUT = 10

print(f"Connecting to {port}...")
try:
    with serial.Serial(port, BAUD, timeout=TIMEOUT) as ser:
        ser.reset_input_buffer()
        print("Waiting for ESP32 to be ready...")
        import time
        start_time = time.time()
        TIMEOUT_SECONDS = 15
        # Wait for ESP32_NOISE_LOGGER_READY
        while True:
            line = ser.readline().decode(errors='ignore').strip()
            if line:
                print(f"[DEBUG] Received: {line.encode('ascii', errors='replace').decode('ascii')}")
            if 'ESP32_NOISE_LOGGER_READY' in line:
                print("[DEBUG] ESP32 is ready. Sending DUMP_DATASET command.")
                break
            if time.time() - start_time > TIMEOUT_SECONDS:
                print("[ERROR] Timeout waiting for ESP32 to be ready.")
                sys.exit(1)
        ser.reset_input_buffer()
        ser.write(b'DUMP_DATASET\n')
        lines = []
        print("Waiting for dataset...")
        start_time = time.time()
        TIMEOUT_SECONDS = 15
        while True:
            line = ser.readline().decode(errors='ignore').strip()
            if line:
                print(f"[DEBUG] Received: {line.encode('ascii', errors='replace').decode('ascii')}")
            if not line:
                if time.time() - start_time > TIMEOUT_SECONDS:
                    print("[ERROR] Timeout waiting for data from ESP32.")
                    break
                continue
            if line == 'END_DATASET':
                print("[DEBUG] END_DATASET received.")
                break
            # Only collect lines that look like CSV (should have 8 commas)
            if line.count(',') == 8:
                lines.append(line)
            start_time = time.time()  # Reset timeout after receiving a line
except Exception as e:
    print(f"Serial error: {e}")
    sys.exit(1)

if not lines:
    print("No data received from ESP32.")
    sys.exit(0)

header = ['RMS', 'Spectral_Centroid', 'Infrasound_Energy', 'Low_Band_Energy', 'Mid_Band_Energy', 'Dominant_Frequency', 'Temporal_Envelope', 'Spectral_Flux', 'Label']
data = [row for row in lines if ',' in row]

# Prompt for output file
output_path = filedialog.asksaveasfilename(
    title="Save Dataset As",
    defaultextension=".csv",
    filetypes=[("CSV Files", "*.csv")],
    initialfile="esp32_dataset.csv"
)
if not output_path:
    print("No output file selected.")
    sys.exit(0)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(','.join(header) + '\n')
    for row in data:
        f.write(row + '\n')

print(f"Dataset saved to {output_path}")
messagebox.showinfo("Done", f"Dataset saved to:\n{output_path}")
