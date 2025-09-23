"""
Sample Data Generator for Elephant Detection System
==================================================

This script generates realistic sample data that mimics the output
from the ESP32 elephant detection system for testing the data analyzer.

Usage:
    python generate_sample_data.py [options]

Options:
    --samples N     Number of samples to generate (default: 2000)
    --detections N  Number of detection events (default: 5% of samples)  
    --output FILE   Output file path (default: sample_data.csv)
    --format FORMAT Output format: csv, json, or log (default: csv)
"""

import pandas as pd
import numpy as np
import argparse
import json
from datetime import datetime, timedelta

def generate_elephant_data(num_samples=2000, detection_rate=0.05, start_time=None):
    """
    Generate realistic elephant detection data
    
    Args:
        num_samples (int): Number of data points to generate
        detection_rate (float): Fraction of samples that should be detections
        start_time (datetime): Start timestamp (default: now - num_samples seconds)
    
    Returns:
        pandas.DataFrame: Generated data
    """
    
    if start_time is None:
        start_time = datetime.now() - timedelta(seconds=num_samples)
    
    # Generate timestamps (1 second intervals)
    timestamps = pd.date_range(start=start_time, periods=num_samples, freq='1S')
    
    # Set random seed for reproducible results
    np.random.seed(42)
    
    print(f"Generating {num_samples} samples with {detection_rate:.1%} detection rate...")
    
    # Generate base audio features (normal forest/environment sounds)
    data = {
        'timestamp': timestamps,
        # RMS amplitude (typical range for environmental audio)
        'rms': np.random.lognormal(mean=np.log(0.02), sigma=0.5, size=num_samples),
        
        # Zero crossing rate (speech-like values but lower for environmental sounds)
        'zcr': np.random.beta(a=2, b=10, size=num_samples) * 0.3,
        
        # Energy (related to RMS but with different dynamics)
        'energy': np.random.lognormal(mean=np.log(0.0005), sigma=0.8, size=num_samples),
        
        # Spectral centroid (center frequency, environmental sounds are typically lower)
        'spectral_centroid': np.random.gamma(shape=2, scale=150, size=num_samples),
        
        # Spectral rolloff (85% energy frequency)
        'spectral_rolloff': np.random.gamma(shape=3, scale=200, size=num_samples),
        
        # MFCC coefficients (mel-frequency cepstral coefficients)
        'mfcc1': np.random.normal(loc=-2.0, scale=0.8, size=num_samples),
        'mfcc2': np.random.normal(loc=0.5, scale=0.6, size=num_samples),
        'mfcc3': np.random.normal(loc=-0.2, scale=0.4, size=num_samples),
    }
    
    # Initialize detection and confidence arrays
    detections = np.zeros(num_samples, dtype=int)
    confidences = np.zeros(num_samples, dtype=float)
    
    # Add elephant detection events
    num_detections = int(num_samples * detection_rate)
    detection_indices = np.random.choice(num_samples, size=num_detections, replace=False)
    
    print(f"Adding {num_detections} elephant detection events...")
    
    for idx in detection_indices:
        # Modify audio features to simulate elephant infrasound characteristics
        
        # Elephants produce high-energy, low-frequency sounds
        data['rms'][idx] *= np.random.uniform(2.5, 5.0)  # Much higher amplitude
        data['energy'][idx] *= np.random.uniform(8.0, 15.0)  # Very high energy
        
        # Lower frequency characteristics
        data['spectral_centroid'][idx] *= np.random.uniform(0.2, 0.5)  # Much lower frequencies
        data['spectral_rolloff'][idx] *= np.random.uniform(0.3, 0.6)   # More low-freq energy
        
        # Different spectral shape (MFCC modifications)
        data['mfcc1'][idx] += np.random.uniform(0.5, 1.5)  # Different spectral envelope
        data['mfcc2'][idx] += np.random.uniform(-0.5, 0.5)
        data['mfcc3'][idx] += np.random.uniform(-0.3, 0.3)
        
        # Zero crossing rate might be lower for pure tones
        data['zcr'][idx] *= np.random.uniform(0.3, 0.8)
        
        # Set detection flag and confidence
        detections[idx] = 1
        confidences[idx] = np.random.uniform(0.6, 0.95)  # High confidence for detections
        
        # Add some temporal spreading (elephant calls can last several seconds)
        spread_range = min(5, num_samples - idx - 1)  # Spread up to 5 seconds
        for offset in range(1, spread_range):
            if idx + offset < num_samples and np.random.random() < 0.6:  # 60% chance of continuation
                # Gradually reduce the effect
                fade_factor = 1.0 - (offset / spread_range)
                
                data['rms'][idx + offset] *= (1 + fade_factor * 1.5)
                data['energy'][idx + offset] *= (1 + fade_factor * 3.0)
                data['spectral_centroid'][idx + offset] *= (1 - fade_factor * 0.3)
                
                # Sometimes mark continuation as detection too
                if np.random.random() < 0.4 and detections[idx + offset] == 0:
                    detections[idx + offset] = 1
                    confidences[idx + offset] = confidences[idx] * fade_factor
    
    # Add detection and confidence to data
    data['detection'] = detections
    data['confidence'] = confidences
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Add some realistic noise and ensure no negative values for physical quantities
    for feature in ['rms', 'energy', 'spectral_centroid', 'spectral_rolloff']:
        df[feature] = np.maximum(df[feature], 0.0001)  # Ensure positive values
    
    # Clip unrealistic values
    df['zcr'] = np.clip(df['zcr'], 0, 1)  # ZCR should be between 0 and 1
    df['spectral_centroid'] = np.clip(df['spectral_centroid'], 10, 8000)  # Reasonable frequency range
    df['spectral_rolloff'] = np.clip(df['spectral_rolloff'], 20, 8000)
    
    print(f"Generated data with {len(df)} samples")
    print(f"Actual detection rate: {df['detection'].sum() / len(df):.1%}")
    
    return df

def save_data(df, filepath, format_type='csv'):
    """
    Save data in specified format
    
    Args:
        df (pandas.DataFrame): Data to save
        filepath (str): Output file path
        format_type (str): Format type ('csv', 'json', or 'log')
    """
    
    if format_type.lower() == 'csv':
        df.to_csv(filepath, index=False)
        print(f"Data saved as CSV: {filepath}")
        
    elif format_type.lower() == 'json':
        # Convert timestamps to string for JSON compatibility
        df_json = df.copy()
        df_json['timestamp'] = df_json['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df_json.to_json(filepath, orient='records', indent=2)
        print(f"Data saved as JSON: {filepath}")
        
    elif format_type.lower() == 'log':
        # Save in ESP32 serial log format
        with open(filepath, 'w') as f:
            f.write("# ESP32 Elephant Detection System Data Log\n")
            f.write("# Format: timestamp,rms,zcr,energy,spectral_centroid,spectral_rolloff,mfcc1,mfcc2,mfcc3,detection,confidence\n")
            
            for _, row in df.iterrows():
                timestamp_str = row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"{timestamp_str},{row['rms']:.6f},{row['zcr']:.6f},{row['energy']:.8f},")
                f.write(f"{row['spectral_centroid']:.2f},{row['spectral_rolloff']:.2f},")
                f.write(f"{row['mfcc1']:.4f},{row['mfcc2']:.4f},{row['mfcc3']:.4f},")
                f.write(f"{int(row['detection'])},{row['confidence']:.4f}\n")
        
        print(f"Data saved as log format: {filepath}")
    
    else:
        raise ValueError(f"Unsupported format: {format_type}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Generate sample elephant detection data')
    parser.add_argument('--samples', '-n', type=int, default=2000,
                       help='Number of samples to generate (default: 2000)')
    parser.add_argument('--detections', '-d', type=float, default=0.05,
                       help='Detection rate (0.0-1.0, default: 0.05)')
    parser.add_argument('--output', '-o', type=str, default='sample_data.csv',
                       help='Output file path (default: sample_data.csv)')
    parser.add_argument('--format', '-f', type=str, default='csv',
                       choices=['csv', 'json', 'log'],
                       help='Output format (default: csv)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Elephant Detection System - Sample Data Generator")
    print("=" * 60)
    
    # Generate data
    df = generate_elephant_data(
        num_samples=args.samples,
        detection_rate=args.detections
    )
    
    # Save data
    save_data(df, args.output, args.format)
    
    # Print summary
    print("\nData Summary:")
    print(f"Total samples: {len(df):,}")
    print(f"Detection events: {df['detection'].sum():,}")
    print(f"Detection rate: {df['detection'].sum() / len(df):.2%}")
    print(f"Time span: {df['timestamp'].iloc[0]} to {df['timestamp'].iloc[-1]}")
    
    if df['detection'].sum() > 0:
        avg_confidence = df[df['detection'] == 1]['confidence'].mean()
        print(f"Average confidence: {avg_confidence:.3f}")
    
    print(f"\nFile saved: {args.output}")
    print("\nYou can now use this file with the data analyzer:")
    print(f"python data_analyzer.py --file {args.output}")
    
if __name__ == "__main__":
    main()