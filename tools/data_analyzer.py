"""
Elephant Detection System - Data Analysis Tool
============================================

This script analyzes logged data from the ESP32 elephant detection system.
It provides comprehensive visualization of audio features, PCA analysis,
correlation matrices, and detection patterns.

Features:
- Time-series analysis of all 8 audio features
- Principal Component Analysis (PCA) for dimensionality reduction
- Correlation analysis between features
- Detection timeline and confidence analysis
- Statistical distributions and outlier detection
- Interactive plots with zoom and pan capabilities

Author: Elephant Detection System
Date: September 2025
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from datetime import datetime, timedelta
import json
import argparse
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

class DataAnalyzer:
    """
    Main class for analyzing elephant detection system data
    """
    
    def __init__(self):
        """Initialize the data analyzer"""
        self.data = None
        self.features = ['rms', 'zcr', 'energy', 'spectral_centroid', 
                        'spectral_rolloff', 'mfcc1', 'mfcc2', 'mfcc3']
        self.scaler = StandardScaler()
        self.pca = PCA()
        self.output_dir = "analysis_results"
        self.setup_output_directory()
        
    def setup_output_directory(self):
        """Create output directory for analysis results"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"Created output directory: {self.output_dir}")
    
    def load_data(self, file_path=None):
        """
        Load data from various sources (CSV, JSON, or serial logs)
        
        Args:
            file_path (str): Path to data file. If None, opens file dialog.
        """
        if file_path is None:
            file_path = self.select_file()
            
        if not file_path:
            print("No file selected. Exiting...")
            return False
            
        try:
            print(f"Loading data from: {file_path}")
            
            # Determine file type and load accordingly
            if file_path.endswith('.csv'):
                self.data = pd.read_csv(file_path)
            elif file_path.endswith('.json'):
                self.data = pd.read_json(file_path)
            elif file_path.endswith('.txt') or file_path.endswith('.log'):
                # Parse serial log format
                self.data = self.parse_serial_log(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
            
            print(f"Loaded {len(self.data)} records")
            self.validate_data()
            return True
            
        except Exception as e:
            print(f"Error loading data: {e}")
            messagebox.showerror("Error", f"Failed to load data: {e}")
            return False
    
    def select_file(self):
        """Open file dialog to select data file"""
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        file_types = [
            ("All Supported", "*.csv;*.json;*.txt;*.log"),
            ("CSV files", "*.csv"),
            ("JSON files", "*.json"),
            ("Log files", "*.txt;*.log"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Select Data File",
            filetypes=file_types
        )
        
        root.destroy()
        return file_path
    
    def parse_serial_log(self, file_path):
        """
        Parse ESP32 serial log format
        Expected format: timestamp,feature1,feature2,...,detection,confidence
        """
        data_records = []
        
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                try:
                    # Parse different possible formats
                    if ',' in line:
                        parts = line.split(',')
                        if len(parts) >= 10:  # timestamp + 8 features + detection
                            record = {
                                'timestamp': parts[0],
                                'rms': float(parts[1]),
                                'zcr': float(parts[2]),
                                'energy': float(parts[3]),
                                'spectral_centroid': float(parts[4]),
                                'spectral_rolloff': float(parts[5]),
                                'mfcc1': float(parts[6]),
                                'mfcc2': float(parts[7]),
                                'mfcc3': float(parts[8]),
                                'detection': int(parts[9]) if len(parts) > 9 else 0,
                                'confidence': float(parts[10]) if len(parts) > 10 else 0.0
                            }
                            data_records.append(record)
                except (ValueError, IndexError) as e:
                    print(f"Skipping invalid line: {line}")
                    continue
        
        if not data_records:
            raise ValueError("No valid data records found in log file")
        
        df = pd.DataFrame(data_records)
        
        # Convert timestamp to datetime if possible
        try:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        except:
            # If timestamp parsing fails, create artificial timestamps
            print("Using artificial timestamps (1 second intervals)")
            df['timestamp'] = pd.date_range(
                start='2025-01-01 00:00:00', 
                periods=len(df), 
                freq='1S'
            )
        
        return df
    
    def validate_data(self):
        """Validate loaded data structure"""
        if self.data is None:
            raise ValueError("No data loaded")
        
        # Check for required columns
        missing_features = [f for f in self.features if f not in self.data.columns]
        if missing_features:
            print(f"Warning: Missing features: {missing_features}")
        
        # Add missing columns with default values
        for feature in missing_features:
            self.data[feature] = 0.0
        
        # Ensure timestamp column exists
        if 'timestamp' not in self.data.columns:
            self.data['timestamp'] = pd.date_range(
                start='2025-01-01 00:00:00', 
                periods=len(self.data), 
                freq='1S'
            )
        
        # Add detection columns if missing
        if 'detection' not in self.data.columns:
            self.data['detection'] = 0
        if 'confidence' not in self.data.columns:
            self.data['confidence'] = 0.0
        
        print(f"Data validation complete. Shape: {self.data.shape}")
        print(f"Available columns: {list(self.data.columns)}")
    
    def generate_sample_data(self, num_samples=1000):
        """Generate sample data for demonstration"""
        print(f"Generating {num_samples} sample data points...")
        
        # Create timestamp range
        timestamps = pd.date_range(
            start='2025-01-01 00:00:00', 
            periods=num_samples, 
            freq='1S'
        )
        
        # Generate realistic audio features with some elephant detection patterns
        np.random.seed(42)  # For reproducible results
        
        # Base feature values (normal background)
        rms = np.random.normal(0.02, 0.005, num_samples)
        zcr = np.random.normal(0.15, 0.03, num_samples)
        energy = np.random.normal(0.001, 0.0002, num_samples)
        spectral_centroid = np.random.normal(250, 50, num_samples)
        spectral_rolloff = np.random.normal(500, 100, num_samples)
        mfcc1 = np.random.normal(-2.5, 0.5, num_samples)
        mfcc2 = np.random.normal(1.2, 0.3, num_samples)
        mfcc3 = np.random.normal(-0.8, 0.2, num_samples)
        
        # Add elephant detection events (higher energy, different spectral characteristics)
        detection_events = np.random.choice(num_samples, size=int(num_samples * 0.05), replace=False)
        
        detections = np.zeros(num_samples)
        confidences = np.zeros(num_samples)
        
        for event_idx in detection_events:
            # Modify features for detection event
            rms[event_idx] *= 3.0  # Higher amplitude
            energy[event_idx] *= 5.0  # Much higher energy
            spectral_centroid[event_idx] *= 0.3  # Lower frequency content
            spectral_rolloff[event_idx] *= 0.4  # More low-frequency energy
            mfcc1[event_idx] += 1.0  # Different spectral shape
            
            detections[event_idx] = 1
            confidences[event_idx] = np.random.uniform(0.7, 0.95)
        
        # Create DataFrame
        self.data = pd.DataFrame({
            'timestamp': timestamps,
            'rms': rms,
            'zcr': zcr,
            'energy': energy,
            'spectral_centroid': spectral_centroid,
            'spectral_rolloff': spectral_rolloff,
            'mfcc1': mfcc1,
            'mfcc2': mfcc2,
            'mfcc3': mfcc3,
            'detection': detections,
            'confidence': confidences
        })
        
        print("Sample data generated successfully!")
        return True

    def plot_feature_timeseries(self):
        """Create time-series plots for all features"""
        print("Creating feature time-series plots...")
        
        fig, axes = plt.subplots(4, 2, figsize=(15, 12))
        fig.suptitle('Audio Feature Analysis Over Time', fontsize=16, fontweight='bold')
        
        axes = axes.flatten()
        
        for i, feature in enumerate(self.features):
            ax = axes[i]
            
            # Plot feature values
            ax.plot(self.data['timestamp'], self.data[feature], 
                   alpha=0.7, linewidth=1, label=f'{feature}')
            
            # Highlight detection events
            detection_mask = self.data['detection'] == 1
            if detection_mask.any():
                detection_data = self.data[detection_mask]
                ax.scatter(detection_data['timestamp'], detection_data[feature],
                          color='red', s=20, alpha=0.8, label='Elephant Detection')
            
            ax.set_title(f'{feature.replace("_", " ").title()}')
            ax.set_xlabel('Time')
            ax.set_ylabel('Value')
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            # Rotate x-axis labels
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        # Save plot
        output_path = os.path.join(self.output_dir, 'feature_timeseries.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Feature time-series plot saved: {output_path}")
        
        plt.show()
    
    def perform_pca_analysis(self):
        """Perform Principal Component Analysis on the features"""
        print("Performing PCA analysis...")
        
        # Prepare feature matrix
        feature_matrix = self.data[self.features].values
        
        # Handle any NaN or infinite values
        feature_matrix = np.nan_to_num(feature_matrix, nan=0.0, posinf=1e6, neginf=-1e6)
        
        # Standardize features
        feature_matrix_scaled = self.scaler.fit_transform(feature_matrix)
        
        # Perform PCA
        self.pca.fit(feature_matrix_scaled)
        pca_components = self.pca.transform(feature_matrix_scaled)
        
        # Create PCA visualization
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Principal Component Analysis Results', fontsize=16, fontweight='bold')
        
        # 1. Explained variance ratio
        ax1.bar(range(1, len(self.pca.explained_variance_ratio_) + 1), 
                self.pca.explained_variance_ratio_, alpha=0.7, color='skyblue')
        ax1.set_xlabel('Principal Component')
        ax1.set_ylabel('Explained Variance Ratio')
        ax1.set_title('Explained Variance by Component')
        ax1.grid(True, alpha=0.3)
        
        # Add cumulative explained variance line
        cumsum = np.cumsum(self.pca.explained_variance_ratio_)
        ax1_twin = ax1.twinx()
        ax1_twin.plot(range(1, len(cumsum) + 1), cumsum, 
                     color='red', marker='o', linewidth=2, label='Cumulative')
        ax1_twin.set_ylabel('Cumulative Explained Variance')
        ax1_twin.legend()
        
        # 2. PCA scatter plot (first two components)
        detection_mask = self.data['detection'] == 1
        
        # Plot normal points
        normal_points = ~detection_mask
        ax2.scatter(pca_components[normal_points, 0], pca_components[normal_points, 1], 
                   alpha=0.6, c='blue', s=10, label='Normal Audio')
        
        # Plot detection points
        if detection_mask.any():
            ax2.scatter(pca_components[detection_mask, 0], pca_components[detection_mask, 1], 
                       alpha=0.8, c='red', s=30, label='Elephant Detection')
        
        ax2.set_xlabel(f'PC1 ({self.pca.explained_variance_ratio_[0]:.1%} variance)')
        ax2.set_ylabel(f'PC2 ({self.pca.explained_variance_ratio_[1]:.1%} variance)')
        ax2.set_title('PCA: First Two Components')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # 3. Feature loadings (biplot)
        loadings = self.pca.components_[:2].T
        ax3.scatter(pca_components[:, 0], pca_components[:, 1], 
                   alpha=0.3, c='lightblue', s=5)
        
        for i, feature in enumerate(self.features):
            ax3.arrow(0, 0, loadings[i, 0]*3, loadings[i, 1]*3, 
                     head_width=0.1, head_length=0.1, fc='red', ec='red')
            ax3.text(loadings[i, 0]*3.2, loadings[i, 1]*3.2, feature, 
                    fontsize=9, ha='center', va='center')
        
        ax3.set_xlabel(f'PC1 ({self.pca.explained_variance_ratio_[0]:.1%} variance)')
        ax3.set_ylabel(f'PC2 ({self.pca.explained_variance_ratio_[1]:.1%} variance)')
        ax3.set_title('PCA Biplot: Features Loading')
        ax3.grid(True, alpha=0.3)
        
        # 4. 3D PCA plot (if we have at least 3 components)
        if len(self.pca.components_) >= 3:
            ax4.remove()
            ax4 = fig.add_subplot(2, 2, 4, projection='3d')
            
            ax4.scatter(pca_components[normal_points, 0], 
                       pca_components[normal_points, 1],
                       pca_components[normal_points, 2],
                       alpha=0.6, c='blue', s=5, label='Normal Audio')
            
            if detection_mask.any():
                ax4.scatter(pca_components[detection_mask, 0], 
                           pca_components[detection_mask, 1],
                           pca_components[detection_mask, 2],
                           alpha=0.8, c='red', s=20, label='Elephant Detection')
            
            ax4.set_xlabel(f'PC1 ({self.pca.explained_variance_ratio_[0]:.1%})')
            ax4.set_ylabel(f'PC2 ({self.pca.explained_variance_ratio_[1]:.1%})')
            ax4.set_zlabel(f'PC3 ({self.pca.explained_variance_ratio_[2]:.1%})')
            ax4.set_title('3D PCA Visualization')
            ax4.legend()
        
        plt.tight_layout()
        
        # Save plot
        output_path = os.path.join(self.output_dir, 'pca_analysis.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"PCA analysis plot saved: {output_path}")
        
        # Print PCA summary
        print("\nPCA Analysis Summary:")
        print(f"Total variance explained by first 2 components: {cumsum[1]:.1%}")
        print(f"Total variance explained by first 3 components: {cumsum[2]:.1%}")
        
        plt.show()
        
        return pca_components
    
    def plot_correlation_matrix(self):
        """Create correlation matrix visualization"""
        print("Creating correlation matrix...")
        
        # Calculate correlation matrix
        correlation_matrix = self.data[self.features].corr()
        
        # Create the plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        fig.suptitle('Feature Correlation Analysis', fontsize=16, fontweight='bold')
        
        # 1. Correlation heatmap
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                   square=True, fmt='.2f', cbar_kws={'shrink': 0.8}, ax=ax1)
        ax1.set_title('Feature Correlation Matrix')
        
        # 2. Correlation network (only strong correlations)
        threshold = 0.5
        strong_corr = correlation_matrix.copy()
        strong_corr = strong_corr.where(np.abs(strong_corr) >= threshold, 0)
        
        # Create network-style visualization
        positions = {}
        n_features = len(self.features)
        angle_step = 2 * np.pi / n_features
        
        for i, feature in enumerate(self.features):
            angle = i * angle_step
            positions[feature] = (np.cos(angle), np.sin(angle))
        
        ax2.set_xlim(-1.5, 1.5)
        ax2.set_ylim(-1.5, 1.5)
        
        # Draw nodes
        for feature, (x, y) in positions.items():
            ax2.scatter(x, y, s=200, c='lightblue', edgecolors='black', zorder=3)
            ax2.text(x*1.2, y*1.2, feature, ha='center', va='center', fontsize=9)
        
        # Draw edges for strong correlations
        for i, feature1 in enumerate(self.features):
            for j, feature2 in enumerate(self.features):
                if i < j and abs(strong_corr.iloc[i, j]) >= threshold:
                    x1, y1 = positions[feature1]
                    x2, y2 = positions[feature2]
                    
                    correlation_val = strong_corr.iloc[i, j]
                    color = 'red' if correlation_val > 0 else 'blue'
                    alpha = min(abs(correlation_val), 0.8)
                    width = abs(correlation_val) * 3
                    
                    ax2.plot([x1, x2], [y1, y2], color=color, alpha=alpha, 
                            linewidth=width, zorder=1)
        
        ax2.set_aspect('equal')
        ax2.set_title(f'Strong Correlations (|r| ≥ {threshold})')
        ax2.axis('off')
        
        plt.tight_layout()
        
        # Save plot
        output_path = os.path.join(self.output_dir, 'correlation_analysis.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Correlation analysis plot saved: {output_path}")
        
        plt.show()
    
    def plot_detection_analysis(self):
        """Analyze detection patterns and confidence scores"""
        print("Creating detection analysis...")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Elephant Detection Analysis', fontsize=16, fontweight='bold')
        
        # 1. Detection timeline
        detection_times = self.data[self.data['detection'] == 1]['timestamp']
        if len(detection_times) > 0:
            ax1.scatter(detection_times, [1] * len(detection_times), 
                       c='red', s=50, alpha=0.7)
            ax1.set_ylim(0, 2)
            ax1.set_ylabel('Detection Event')
            ax1.set_xlabel('Time')
            ax1.set_title(f'Detection Timeline ({len(detection_times)} events)')
            ax1.grid(True, alpha=0.3)
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        else:
            ax1.text(0.5, 0.5, 'No detections found', ha='center', va='center', 
                    transform=ax1.transAxes, fontsize=12)
            ax1.set_title('Detection Timeline (No events)')
        
        # 2. Confidence score distribution
        confidence_scores = self.data[self.data['detection'] == 1]['confidence']
        if len(confidence_scores) > 0:
            ax2.hist(confidence_scores, bins=20, alpha=0.7, color='orange', edgecolor='black')
            ax2.set_xlabel('Confidence Score')
            ax2.set_ylabel('Frequency')
            ax2.set_title('Confidence Score Distribution')
            ax2.axvline(confidence_scores.mean(), color='red', linestyle='--', 
                       label=f'Mean: {confidence_scores.mean():.2f}')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
        else:
            ax2.text(0.5, 0.5, 'No confidence scores available', ha='center', va='center', 
                    transform=ax2.transAxes, fontsize=12)
            ax2.set_title('Confidence Score Distribution')
        
        # 3. Detection rate over time (hourly bins)
        self.data['hour'] = self.data['timestamp'].dt.hour
        detection_by_hour = self.data.groupby('hour')['detection'].sum()
        total_by_hour = self.data.groupby('hour').size()
        detection_rate = (detection_by_hour / total_by_hour).fillna(0)
        
        ax3.bar(detection_rate.index, detection_rate.values, alpha=0.7, color='green')
        ax3.set_xlabel('Hour of Day')
        ax3.set_ylabel('Detection Rate')
        ax3.set_title('Detection Rate by Hour')
        ax3.set_xticks(range(0, 24, 2))
        ax3.grid(True, alpha=0.3)
        
        # 4. Feature comparison: detected vs normal
        detection_data = self.data[self.data['detection'] == 1]
        normal_data = self.data[self.data['detection'] == 0]
        
        if len(detection_data) > 0 and len(normal_data) > 0:
            # Calculate mean feature values for each group
            detection_means = detection_data[self.features].mean()
            normal_means = normal_data[self.features].mean()
            
            x_pos = np.arange(len(self.features))
            width = 0.35
            
            ax4.bar(x_pos - width/2, normal_means, width, label='Normal Audio', 
                   alpha=0.7, color='blue')
            ax4.bar(x_pos + width/2, detection_means, width, label='Elephant Detection', 
                   alpha=0.7, color='red')
            
            ax4.set_xlabel('Features')
            ax4.set_ylabel('Mean Value')
            ax4.set_title('Feature Comparison: Normal vs Detection')
            ax4.set_xticks(x_pos)
            ax4.set_xticklabels([f.replace('_', '\n') for f in self.features], rotation=45)
            ax4.legend()
            ax4.grid(True, alpha=0.3)
        else:
            ax4.text(0.5, 0.5, 'Insufficient data for comparison', ha='center', va='center', 
                    transform=ax4.transAxes, fontsize=12)
            ax4.set_title('Feature Comparison')
        
        plt.tight_layout()
        
        # Save plot
        output_path = os.path.join(self.output_dir, 'detection_analysis.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Detection analysis plot saved: {output_path}")
        
        plt.show()
    
    def plot_statistical_summary(self):
        """Create comprehensive statistical summary"""
        print("Creating statistical summary...")
        
        fig = plt.figure(figsize=(20, 15))
        gs = fig.add_gridspec(4, 4, hspace=0.3, wspace=0.3)
        fig.suptitle('Comprehensive Statistical Analysis', fontsize=20, fontweight='bold')
        
        # Feature distributions (2x4 grid)
        for i, feature in enumerate(self.features):
            row = i // 4
            col = i % 4
            ax = fig.add_subplot(gs[row, col])
            
            # Histogram with KDE
            ax.hist(self.data[feature], bins=30, alpha=0.7, density=True, color='skyblue')
            
            # Add KDE curve
            from scipy import stats
            x_range = np.linspace(self.data[feature].min(), self.data[feature].max(), 100)
            kde = stats.gaussian_kde(self.data[feature].dropna())
            ax.plot(x_range, kde(x_range), 'r-', linewidth=2, label='KDE')
            
            ax.set_title(f'{feature.replace("_", " ").title()}')
            ax.set_xlabel('Value')
            ax.set_ylabel('Density')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        # Summary statistics table
        ax_table = fig.add_subplot(gs[2:, :])
        ax_table.axis('off')
        
        # Calculate statistics
        stats_df = self.data[self.features].describe().round(4)
        
        # Add additional statistics
        stats_df.loc['skewness'] = self.data[self.features].skew().round(4)
        stats_df.loc['kurtosis'] = self.data[self.features].kurtosis().round(4)
        
        # Create table
        table_data = []
        for stat in stats_df.index:
            row = [stat] + [f"{val:.4f}" for val in stats_df.loc[stat]]
            table_data.append(row)
        
        headers = ['Statistic'] + [f.replace('_', ' ').title() for f in self.features]
        
        table = ax_table.table(cellText=table_data, colLabels=headers,
                              cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1.2, 1.5)
        
        # Color code the table
        for i in range(len(headers)):
            table[(0, i)].set_facecolor('#40466e')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        ax_table.set_title('Detailed Feature Statistics', fontsize=14, fontweight='bold', pad=20)
        
        # Save plot
        output_path = os.path.join(self.output_dir, 'statistical_summary.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Statistical summary plot saved: {output_path}")
        
        plt.show()
    
    def run_complete_analysis(self):
        """Run all analysis functions"""
        print("Running complete analysis...")
        
        # Run all analysis functions
        self.plot_feature_timeseries()
        pca_components = self.perform_pca_analysis()
        self.plot_correlation_matrix()
        self.plot_detection_analysis()
        self.plot_statistical_summary()
        
        # Generate summary report
        self.generate_summary_report()
        
        print("\n" + "="*60)
        print("COMPLETE ANALYSIS FINISHED!")
        print("="*60)
        print(f"All results saved in: {self.output_dir}")
    
    def generate_summary_report(self):
        """Generate a text summary report"""
        print("Generating summary report...")
        
        report_path = os.path.join(self.output_dir, 'analysis_report.txt')
        
        with open(report_path, 'w') as f:
            f.write("ELEPHANT DETECTION SYSTEM - DATA ANALYSIS REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Data Points: {len(self.data):,}\n")
            f.write(f"Time Range: {self.data['timestamp'].min()} to {self.data['timestamp'].max()}\n\n")
            
            # Detection summary
            total_detections = self.data['detection'].sum()
            detection_rate = total_detections / len(self.data) * 100
            f.write("DETECTION SUMMARY:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Total Detections: {total_detections}\n")
            f.write(f"Detection Rate: {detection_rate:.2f}%\n")
            
            if total_detections > 0:
                avg_confidence = self.data[self.data['detection'] == 1]['confidence'].mean()
                f.write(f"Average Confidence: {avg_confidence:.3f}\n")
            
            f.write("\n")
            
            # Feature statistics
            f.write("FEATURE STATISTICS:\n")
            f.write("-" * 20 + "\n")
            stats_summary = self.data[self.features].describe()
            f.write(stats_summary.to_string())
            f.write("\n\n")
            
            # PCA summary
            if hasattr(self.pca, 'explained_variance_ratio_'):
                f.write("PCA ANALYSIS:\n")
                f.write("-" * 15 + "\n")
                for i, ratio in enumerate(self.pca.explained_variance_ratio_):
                    f.write(f"PC{i+1}: {ratio:.1%} variance explained\n")
                
                cumulative = np.cumsum(self.pca.explained_variance_ratio_)
                f.write(f"\nFirst 2 components explain: {cumulative[1]:.1%} of variance\n")
                f.write(f"First 3 components explain: {cumulative[2]:.1%} of variance\n")
            
            f.write("\n" + "=" * 50 + "\n")
        
        print(f"Summary report saved: {report_path}")

def main():
    """Main function to run the data analyzer"""
    print("=" * 60)
    print("Elephant Detection System - Data Analysis Tool")
    print("=" * 60)
    
    analyzer = DataAnalyzer()
    
    # Command line argument parsing
    parser = argparse.ArgumentParser(description='Analyze elephant detection data')
    parser.add_argument('--file', '-f', type=str, help='Path to data file')
    parser.add_argument('--sample', '-s', action='store_true', 
                       help='Generate sample data for demonstration')
    parser.add_argument('--output', '-o', type=str, default='analysis_results',
                       help='Output directory for results')
    
    args = parser.parse_args()
    
    # Set output directory
    if args.output:
        analyzer.output_dir = args.output
        analyzer.setup_output_directory()
    
    # Load or generate data
    if args.sample:
        success = analyzer.generate_sample_data()
    else:
        success = analyzer.load_data(args.file)
    
    if not success:
        return
    
    try:
        # Interactive menu for analysis options
        print("\nAvailable Analysis Options:")
        print("1. Complete Analysis (All visualizations)")
        print("2. Feature Time-series Only")
        print("3. PCA Analysis Only")
        print("4. Correlation Analysis Only") 
        print("5. Detection Analysis Only")
        print("6. Statistical Summary Only")
        
        if len(sys.argv) == 1:  # No command line arguments
            choice = input("\nEnter your choice (1-6) or press Enter for complete analysis: ").strip()
            if not choice:
                choice = "1"
        else:
            choice = "1"  # Default to complete analysis when run with arguments
        
        print(f"\nRunning analysis option {choice}...")
        
        if choice == "1":
            analyzer.run_complete_analysis()
        elif choice == "2":
            analyzer.plot_feature_timeseries()
        elif choice == "3":
            analyzer.perform_pca_analysis()
        elif choice == "4":
            analyzer.plot_correlation_matrix()
        elif choice == "5":
            analyzer.plot_detection_analysis()
        elif choice == "6":
            analyzer.plot_statistical_summary()
        else:
            print("Invalid choice. Running complete analysis...")
            analyzer.run_complete_analysis()
        
        print("\nAnalysis complete! Check the output directory for results.")
        print(f"Results saved in: {analyzer.output_dir}")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()