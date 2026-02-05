# Dataset Assessment Usage Example

This document demonstrates the usage and output of the dataset assessment tool.

## Basic Usage

```bash
python assess_dataset.py --data_dir ./data
```

## Example Output

When running on a sample dataset with 5 training images and 2 validation images:

```
============================================================
DATASET ASSESSMENT FOR POLYP DETECTION
============================================================

============================================================
Assessing TRAIN dataset
============================================================

Total images found: 5
File extensions: {'.jpg': 5, '.png': 0, '.jpeg': 0, ...}

Analyzing image properties (sampling first 100 images)...

Image Statistics:
  Average dimensions: 462.0 x 492.8 pixels
  Width range: [402, 578]
  Height range: [427, 559]
  Average size: 5.2 KB
  Size range: [4.5, 6.4] KB
  Average aspect ratio: 0.95
  Color modes: {'RGB': 5}

============================================================
Assessing VALIDATION dataset
============================================================

Total images found: 2
File extensions: {'.jpg': 2, '.png': 0, '.jpeg': 0, ...}

Analyzing image properties (sampling first 100 images)...

Image Statistics:
  Average dimensions: 500.0 x 508.0 pixels
  Width range: [443, 557]
  Height range: [436, 580]
  Average size: 5.5 KB
  Size range: [5.4, 5.5] KB
  Average aspect ratio: 1.02
  Color modes: {'RGB': 2}

============================================================
SUMMARY
============================================================

Dataset Sizes:
  Train: 5 images
  Validation: 2 images
  Total: 7 images

Split Ratio:
  Train: 71.4%
  Validation: 28.6%
  ✓ Split ratio is within recommended range (70-90% train)

Data Quality Checks:
  ⚠ WARNING: Very small training set (5 images)
  ⚠ WARNING: Very small validation set (2 images)

============================================================

Report saved to: data/dataset_assessment_report.json

✓ Assessment completed successfully!
```

## JSON Report Structure

The tool generates a detailed JSON report with the following structure:

```json
{
  "train": {
    "exists": true,
    "directory": "data/train",
    "count": 5,
    "extensions": {
      ".jpg": 5,
      ".png": 0,
      ...
    },
    "statistics": {
      "count": 5,
      "avg_width": 462.0,
      "std_width": 62.76,
      "min_width": 402,
      "max_width": 578,
      "avg_height": 492.8,
      "std_height": 51.07,
      "min_height": 427,
      "max_height": 559,
      "avg_size_kb": 5.25,
      "std_size_kb": 0.68,
      "min_size_kb": 4.50,
      "max_size_kb": 6.41,
      "avg_aspect_ratio": 0.95,
      "std_aspect_ratio": 0.20,
      "color_modes": {
        "RGB": 5
      }
    }
  },
  "validation": {
    ...
  }
}
```

## Key Metrics Provided

1. **Dataset Counts**: Number of images in train/validation sets
2. **File Format Distribution**: Count by file extension
3. **Dimension Statistics**: Average, min, max, and standard deviation for width and height
4. **File Size Statistics**: Average, min, max, and standard deviation for file sizes
5. **Aspect Ratio Analysis**: Average and standard deviation
6. **Color Mode Distribution**: Count of images by color mode (RGB, grayscale, etc.)
7. **Split Ratio Analysis**: Percentage split between train and validation with recommendations
8. **Quality Checks**: Warnings for insufficient data or improper splits

## Recommendations

- Training set should be 70-90% of total data
- Minimum 100+ training images recommended for deep learning
- Minimum 20+ validation images recommended
- Images should have consistent dimensions and color modes
