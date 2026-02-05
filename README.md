# Polyp Detection

A tool for assessing train and validation datasets for polyp detection tasks.

## Overview

This repository provides tools to analyze and assess medical imaging datasets for polyp detection, particularly focusing on train and validation set quality, distribution, and characteristics.

## Features

- **Dataset Structure Validation**: Verifies the presence and organization of train/validation splits
- **Image Counting**: Counts images across different formats (JPG, PNG, BMP, etc.)
- **Image Analysis**: Analyzes image properties including:
  - Dimensions (width, height)
  - File sizes
  - Aspect ratios
  - Color modes
- **Statistical Reporting**: Provides comprehensive statistics:
  - Average, min, max dimensions
  - File size distribution
  - Split ratio analysis
- **Quality Checks**: Identifies potential issues:
  - Missing datasets
  - Insufficient data
  - Improper train/validation splits
- **JSON Report Generation**: Saves detailed assessment results for further analysis

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tkorzhan1995/Polyp-detection.git
cd Polyp-detection
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Dataset Structure

Organize your polyp detection dataset in the following structure:

```
data/
├── train/              # Training images
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── validation/         # Validation images
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
```

## Usage

### Basic Assessment

Run the assessment tool on your dataset:

```bash
python assess_dataset.py --data_dir ./data
```

### Custom Output Location

Specify a custom output file for the assessment report:

```bash
python assess_dataset.py --data_dir ./data --output my_report.json
```

### Example Output

```
============================================================
DATASET ASSESSMENT FOR POLYP DETECTION
============================================================

============================================================
Assessing TRAIN dataset
============================================================

Total images found: 150

Image Statistics:
  Average dimensions: 512.0 x 512.0 pixels
  Width range: [480, 640]
  Height range: [480, 640]
  Average size: 125.3 KB
  Size range: [50.2, 250.8] KB
  Average aspect ratio: 1.00
  Color modes: {'RGB': 150}

============================================================
Assessing VALIDATION dataset
============================================================

Total images found: 50

Image Statistics:
  Average dimensions: 512.0 x 512.0 pixels
  ...

============================================================
SUMMARY
============================================================

Dataset Sizes:
  Train: 150 images
  Validation: 50 images
  Total: 200 images

Split Ratio:
  Train: 75.0%
  Validation: 25.0%
  ✓ Split ratio is within recommended range (70-90% train)

Data Quality Checks:
  ✓ Training set has sufficient images
  ✓ Validation set has sufficient images
```

## Output Files

The assessment tool generates a JSON report (`dataset_assessment_report.json` by default) containing:

- Image counts for train and validation sets
- Detailed statistics (dimensions, file sizes, aspect ratios)
- File format distribution
- Color mode information

## Requirements

- Python 3.7+
- numpy
- pandas
- Pillow
- matplotlib
- seaborn

See `requirements.txt` for specific versions.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.
