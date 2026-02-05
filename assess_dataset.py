#!/usr/bin/env python3
"""
Dataset Assessment Tool for Polyp Detection

This script analyzes train and validation datasets for polyp detection,
providing comprehensive metrics and visualizations.

Usage:
    python assess_dataset.py --data_dir <path_to_data>
    
Example:
    python assess_dataset.py --data_dir ./data
"""

import argparse
import os
import json
from pathlib import Path
from collections import defaultdict
import sys

try:
    import numpy as np
    import pandas as pd
    from PIL import Image
    import matplotlib.pyplot as plt
    import seaborn as sns
except ImportError as e:
    print(f"Error: Required package not found. Please install requirements: pip install -r requirements.txt")
    print(f"Missing: {e}")
    sys.exit(1)


class DatasetAssessor:
    """Assess train and validation datasets for polyp detection."""
    
    def __init__(self, data_dir):
        """
        Initialize the dataset assessor.
        
        Args:
            data_dir (str): Root directory containing train and validation folders
        """
        self.data_dir = Path(data_dir)
        self.train_dir = self.data_dir / 'train'
        self.val_dir = self.data_dir / 'validation'
        self.results = {
            'train': {},
            'validation': {}
        }
        
    def check_structure(self):
        """Check if the dataset directory structure exists."""
        if not self.data_dir.exists():
            print(f"Error: Data directory '{self.data_dir}' does not exist.")
            return False
            
        if not self.train_dir.exists():
            print(f"Warning: Train directory '{self.train_dir}' does not exist.")
            
        if not self.val_dir.exists():
            print(f"Warning: Validation directory '{self.val_dir}' does not exist.")
            
        return True
    
    def count_images(self, directory):
        """
        Count images in a directory.
        
        Args:
            directory (Path): Directory to count images in
            
        Returns:
            dict: Dictionary with image counts and file list
        """
        if not directory.exists():
            return {'count': 0, 'files': [], 'extensions': {}}
        
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif'}
        files = []
        extensions = defaultdict(int)
        
        for ext in image_extensions:
            pattern_files = list(directory.glob(f'*{ext}')) + list(directory.glob(f'*{ext.upper()}'))
            files.extend(pattern_files)
            extensions[ext] += len(pattern_files)
        
        # Also search in subdirectories
        for subdir in directory.iterdir():
            if subdir.is_dir():
                for ext in image_extensions:
                    pattern_files = list(subdir.glob(f'*{ext}')) + list(subdir.glob(f'*{ext.upper()}'))
                    files.extend(pattern_files)
                    extensions[ext] += len(pattern_files)
        
        return {
            'count': len(files),
            'files': [str(f) for f in files],
            'extensions': dict(extensions)
        }
    
    def analyze_images(self, files):
        """
        Analyze image properties.
        
        Args:
            files (list): List of image file paths
            
        Returns:
            dict: Dictionary with image statistics
        """
        if not files:
            return {
                'dimensions': [],
                'sizes_kb': [],
                'aspect_ratios': [],
                'color_modes': {}
            }
        
        dimensions = []
        sizes_kb = []
        aspect_ratios = []
        color_modes = defaultdict(int)
        
        for file_path in files[:100]:  # Analyze first 100 images for performance
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    dimensions.append((width, height))
                    aspect_ratios.append(width / height if height > 0 else 0)
                    color_modes[img.mode] += 1
                    
                file_size = os.path.getsize(file_path) / 1024  # KB
                sizes_kb.append(file_size)
            except Exception as e:
                print(f"Warning: Could not analyze {file_path}: {e}")
        
        return {
            'dimensions': dimensions,
            'sizes_kb': sizes_kb,
            'aspect_ratios': aspect_ratios,
            'color_modes': dict(color_modes)
        }
    
    def compute_statistics(self, analysis):
        """
        Compute statistics from image analysis.
        
        Args:
            analysis (dict): Analysis results from analyze_images
            
        Returns:
            dict: Statistical summary
        """
        if not analysis['dimensions']:
            return {
                'count': 0,
                'avg_width': 0,
                'avg_height': 0,
                'avg_size_kb': 0,
                'avg_aspect_ratio': 0
            }
        
        widths = [d[0] for d in analysis['dimensions']]
        heights = [d[1] for d in analysis['dimensions']]
        
        return {
            'count': len(analysis['dimensions']),
            'avg_width': np.mean(widths),
            'std_width': np.std(widths),
            'min_width': np.min(widths),
            'max_width': np.max(widths),
            'avg_height': np.mean(heights),
            'std_height': np.std(heights),
            'min_height': np.min(heights),
            'max_height': np.max(heights),
            'avg_size_kb': np.mean(analysis['sizes_kb']),
            'std_size_kb': np.std(analysis['sizes_kb']),
            'min_size_kb': np.min(analysis['sizes_kb']),
            'max_size_kb': np.max(analysis['sizes_kb']),
            'avg_aspect_ratio': np.mean(analysis['aspect_ratios']),
            'std_aspect_ratio': np.std(analysis['aspect_ratios']),
            'color_modes': analysis['color_modes']
        }
    
    def assess_split(self, split_name, directory):
        """
        Assess a dataset split (train or validation).
        
        Args:
            split_name (str): Name of the split ('train' or 'validation')
            directory (Path): Directory containing the split data
            
        Returns:
            dict: Assessment results
        """
        print(f"\n{'='*60}")
        print(f"Assessing {split_name.upper()} dataset")
        print(f"{'='*60}")
        
        if not directory.exists():
            print(f"Directory does not exist: {directory}")
            return {
                'exists': False,
                'count': 0
            }
        
        # Count images
        count_info = self.count_images(directory)
        print(f"\nTotal images found: {count_info['count']}")
        
        if count_info['count'] == 0:
            return {
                'exists': True,
                'count': 0,
                'message': 'No images found in directory'
            }
        
        print(f"File extensions: {count_info['extensions']}")
        
        # Analyze images
        print(f"\nAnalyzing image properties (sampling first 100 images)...")
        analysis = self.analyze_images(count_info['files'])
        
        # Compute statistics
        stats = self.compute_statistics(analysis)
        
        print(f"\nImage Statistics:")
        print(f"  Average dimensions: {stats['avg_width']:.1f} x {stats['avg_height']:.1f} pixels")
        print(f"  Width range: [{stats['min_width']:.0f}, {stats['max_width']:.0f}]")
        print(f"  Height range: [{stats['min_height']:.0f}, {stats['max_height']:.0f}]")
        print(f"  Average size: {stats['avg_size_kb']:.1f} KB")
        print(f"  Size range: [{stats['min_size_kb']:.1f}, {stats['max_size_kb']:.1f}] KB")
        print(f"  Average aspect ratio: {stats['avg_aspect_ratio']:.2f}")
        print(f"  Color modes: {stats['color_modes']}")
        
        return {
            'exists': True,
            'directory': str(directory),
            'count': count_info['count'],
            'extensions': count_info['extensions'],
            'statistics': stats
        }
    
    def assess_all(self):
        """Assess both train and validation datasets."""
        print("\n" + "="*60)
        print("DATASET ASSESSMENT FOR POLYP DETECTION")
        print("="*60)
        
        if not self.check_structure():
            print("\nError: Invalid dataset structure.")
            return False
        
        # Assess train set
        self.results['train'] = self.assess_split('train', self.train_dir)
        
        # Assess validation set
        self.results['validation'] = self.assess_split('validation', self.val_dir)
        
        # Summary
        self.print_summary()
        
        return True
    
    def print_summary(self):
        """Print a summary comparison of train and validation sets."""
        print(f"\n{'='*60}")
        print("SUMMARY")
        print(f"{'='*60}")
        
        train_count = self.results['train'].get('count', 0)
        val_count = self.results['validation'].get('count', 0)
        total_count = train_count + val_count
        
        print(f"\nDataset Sizes:")
        print(f"  Train: {train_count} images")
        print(f"  Validation: {val_count} images")
        print(f"  Total: {total_count} images")
        
        if total_count > 0:
            train_ratio = (train_count / total_count) * 100
            val_ratio = (val_count / total_count) * 100
            print(f"\nSplit Ratio:")
            print(f"  Train: {train_ratio:.1f}%")
            print(f"  Validation: {val_ratio:.1f}%")
            
            # Check if split is reasonable
            if 70 <= train_ratio <= 90:
                print(f"  ✓ Split ratio is within recommended range (70-90% train)")
            else:
                print(f"  ⚠ Split ratio is outside recommended range (70-90% train)")
        
        # Check for common issues
        print(f"\nData Quality Checks:")
        if train_count == 0:
            print(f"  ⚠ WARNING: No training images found")
        elif train_count < 100:
            print(f"  ⚠ WARNING: Very small training set ({train_count} images)")
        else:
            print(f"  ✓ Training set has sufficient images")
            
        if val_count == 0:
            print(f"  ⚠ WARNING: No validation images found")
        elif val_count < 20:
            print(f"  ⚠ WARNING: Very small validation set ({val_count} images)")
        else:
            print(f"  ✓ Validation set has sufficient images")
        
        print(f"\n{'='*60}")
    
    def save_report(self, output_file='dataset_assessment_report.json'):
        """
        Save assessment results to a JSON file.
        
        Args:
            output_file (str): Path to output JSON file
        """
        output_path = self.data_dir / output_file
        
        # Convert numpy types to native Python types for JSON serialization
        def convert_types(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {key: convert_types(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_types(item) for item in obj]
            return obj
        
        results_serializable = convert_types(self.results)
        
        with open(output_path, 'w') as f:
            json.dump(results_serializable, f, indent=2)
        
        print(f"\nReport saved to: {output_path}")


def main():
    """Main function to run dataset assessment."""
    parser = argparse.ArgumentParser(
        description='Assess train and validation datasets for polyp detection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python assess_dataset.py --data_dir ./data
  python assess_dataset.py --data_dir /path/to/polyp/data --output report.json
        """
    )
    
    parser.add_argument(
        '--data_dir',
        type=str,
        default='./data',
        help='Root directory containing train and validation folders (default: ./data)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='dataset_assessment_report.json',
        help='Output JSON file for assessment report (default: dataset_assessment_report.json)'
    )
    
    args = parser.parse_args()
    
    # Run assessment
    assessor = DatasetAssessor(args.data_dir)
    success = assessor.assess_all()
    
    if success:
        assessor.save_report(args.output)
        print("\n✓ Assessment completed successfully!")
        return 0
    else:
        print("\n✗ Assessment failed.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
